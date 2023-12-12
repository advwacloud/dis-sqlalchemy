from typing import TYPE_CHECKING

from dis_sqlalchemy import Column
from dis_sqlalchemy import Integer
from dis_sqlalchemy.orm import as_declarative
from dis_sqlalchemy.orm import declared_attr
from dis_sqlalchemy.orm import Mapped
from .address import Address
from .user import User

if TYPE_CHECKING:
    from dis_sqlalchemy.orm.decl_api import DeclarativeMeta


@as_declarative()
class Base:
    @declared_attr
    def __tablename__(self) -> Mapped[str]:
        return self.__name__.lower()

    id = Column(Integer, primary_key=True)


__all__ = ["User", "Address"]
