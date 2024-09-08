from typing import Optional, List
from sqlalchemy.sql.expression import and_
from sqlalchemy.sql import exists
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from typing import Callable
from core import logger, security
from schemas import UserSchema
from db.models import User
from db import models, get_db

def email_exists(email: str) -> bool:
    db = get_db()
    return db.query(exists().where(User.email == email)).scalar()

def is_active(email: str) -> bool:
    db = get_db()
    return db.query(exists().where(and_(User.email == email, User.is_active == True))).scalar()

def get_by_id(id: int) -> Optional[User]:
    db = get_db()
    return db.query(User).filter(User.id == id).one_or_none()

def get_by_email(email: str) -> Optional[User]:
    db = get_db()
    return db.query(User).filter(User.email == email).one_or_none()

def get_all(skip: int = 0, limit: int = 10) -> List[User]:
    db = get_db()
    return db.query(User).offset(skip).limit(limit).all()

def create_and_commit(schema: UserSchema.Create) -> Optional[User]:
    db = get_db()
    try:
        db_obj = User(**schema.model_dump())
        setattr(db_obj, "password", security.get_password_hash(schema.password))
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating user: {e}")
        return None

def update_and_commit(schema: UserSchema.Update, id: int) -> Optional[User]:
    db = get_db()
    try:
        user = db.query(User).filter(User.id == id).one()
        for key, value in schema.model_dump().items():
            if key == "password":
                value = security.get_password_hash(value)
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user
    except NoResultFound:
        logger.error(f"No user found with id: {id}")
        return None
    except MultipleResultsFound:
        logger.error(f"Multiple users found with id: {id}")
        return None
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating user: {e}")
        return None
    
def validate_ownership(current_user: UserSchema.Read, model_name: str, resource_id: int) -> bool:
    db = get_db()
    try:
        db_obj = db.query(getattr(models, model_name)).filter_by(id=resource_id).one_or_none()
        if db_obj is None:
            logger.error(f"{model_name} with ID {resource_id} not found")
            return False
        
        owner_map: dict[str, Callable[[object], int]] = {
            "Property": lambda obj: obj.manager_id, # type: ignore
            "Building": lambda obj: obj.property.manager_id, # type: ignore
            "Unit": lambda obj: obj.building.property.manager_id, # type: ignore
            "Lease": lambda obj: obj.unit.building.property.manager_id, # type: ignore
            "Tenant": lambda obj: obj.lease.unit.building.property.manager_id, # type: ignore
            "Insurance": lambda obj: obj.tenant.lease.unit.building.property.manager_id, # type: ignore
        }
        
        owner_id = owner_map.get(model_name)
        if owner_id is None:
            logger.error(f"Ownership validation not supported for {model_name}")
            return False
        
        if owner_id(db_obj) != current_user.id:
            logger.warning(f"User {current_user.id} does not have permission to access {model_name} with ID {resource_id}")
            return False
        
        return True
    
    except AttributeError as e:
        logger.error(f"Attribute error during ownership validation: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        return False
