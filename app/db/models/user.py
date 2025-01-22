from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from db import CommonMixins, Base

class User(CommonMixins, Base):
    __tablename__ = 'users'

    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
