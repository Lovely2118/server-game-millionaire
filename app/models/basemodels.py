import re
from abc import abstractmethod

from sqlalchemy import MetaData, Column, Integer
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import Session


def camel_to_snake(str):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', str).lower()


naming_convention = {
    "all_column_names": lambda constraint, table: "_".join(
        [
            column.name
            for column in constraint.columns.values()
        ]
    ),
    "ix": "ix_%(table_name)s_%(all_column_names)s",
    "uq": "uq_%(table_name)s_%(all_column_names)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(all_column_names)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


@as_declarative(metadata=MetaData(naming_convention=naming_convention))
class BaseModel:
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    def is_unique(self, session: Session) -> bool:
        return self.get_unique_model(session) is None

    @declared_attr
    def __tablename__(cls) -> str:
        return camel_to_snake(cls.__name__)
