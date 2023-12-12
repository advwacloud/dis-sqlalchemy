"""Test that the right-hand expressions we normally "replace" are actually
type checked.

"""
from typing import List

from dis_sqlalchemy import Column
from dis_sqlalchemy import ForeignKey
from dis_sqlalchemy import Integer
from dis_sqlalchemy import String
from dis_sqlalchemy.orm import declarative_base
from dis_sqlalchemy.orm import Mapped
from dis_sqlalchemy.orm import relationship
from dis_sqlalchemy.orm.decl_api import declared_attr


Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)

    addresses: Mapped[List["Address"]] = relationship(
        "Address", wrong_arg="imwrong"
    )


class SubUser(User):
    __tablename__ = "subuser"

    id: int = Column(Integer, ForeignKey("user.id"), primary_key=True)


class Address(Base):
    __tablename__ = "address"

    id: int = Column(Integer, primary_key=True)

    user_id: int = Column(ForeignKey("user.id"))

    @declared_attr
    def email_address(cls) -> Column[String]:
        # EXPECTED_MYPY: Argument 1 to "Column" has incompatible type "bool";
        return Column(True)

    @declared_attr
    # EXPECTED_MYPY: Invalid type comment or annotation
    def thisisweird(cls) -> Column(String):
        # EXPECTED_MYPY: Argument 1 to "Column" has incompatible type "bool";
        return Column(False)
