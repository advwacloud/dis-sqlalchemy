from typing import List
from typing import TYPE_CHECKING

from dis_sqlalchemy import Column
from dis_sqlalchemy import ForeignKey
from dis_sqlalchemy import Integer
from dis_sqlalchemy import String
from dis_sqlalchemy.orm import Mapped
from dis_sqlalchemy.orm import relationship
from dis_sqlalchemy.orm.decl_api import declared_attr
from dis_sqlalchemy.orm.relationships import RelationshipProperty
from . import Base

if TYPE_CHECKING:
    from .address import Address


class User(Base):
    name = Column(String)

    othername = Column(String)

    addresses: Mapped[List["Address"]] = relationship(
        "Address", back_populates="user"
    )


class HasUser:
    @declared_attr
    def user_id(self) -> "Column[Integer]":
        return Column(
            Integer,
            ForeignKey(User.id, ondelete="CASCADE", onupdate="CASCADE"),
            nullable=False,
        )

    @declared_attr
    def user(self) -> RelationshipProperty[User]:
        return relationship(User)
