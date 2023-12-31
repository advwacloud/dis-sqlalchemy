from typing import Optional

from dis_sqlalchemy import Column
from dis_sqlalchemy import ForeignKey
from dis_sqlalchemy import Integer
from dis_sqlalchemy import String
from dis_sqlalchemy.orm import Mapped
from dis_sqlalchemy.orm import registry

reg: registry = registry()


@reg.mapped
class User:
    __tablename__ = "user"

    id = Column(Integer(), primary_key=True)
    name = Column(String)


@reg.mapped
class Address:
    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    user_id: Mapped[int] = Column(ForeignKey("user.id"))
    email_address = Column(String)


ad1 = Address()

p: Optional[int] = ad1.user_id

# it's not optional because we called it Mapped[int]
# and not Mapped[Optional[int]]
p2: int = ad1.user_id


# class-level descriptor access
User.name.in_(["x", "y"])


# class-level descriptor access
Address.user_id.in_([1, 2])
