'''
Custom data type definitions for SQLAlchemy
'''
from sqlalchemy import TypeDecorator, Integer
from sqlalchemy.engine import Dialect

# Custom data type for boolean stored as integer
class BooleanInteger(TypeDecorator[int]):
    impl = Integer

    # Convert Python bool to SQL integer
    def process_bind_param(self, value: int | None, dialect: Dialect) -> int | None:
        return None if value is None else value  # 0 or 1

    # Convert SQL integer to Python bool
    def process_result_value(self, value: int | None, dialect: Dialect) -> bool | None:
        return None if value is None else bool(value)  # False or True
