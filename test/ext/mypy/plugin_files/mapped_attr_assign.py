"""Test patterns that can be used for assignment of mapped attributes
after the mapping is complete


"""
from typing import Optional

from dis_sqlalchemy import Column
from dis_sqlalchemy import ForeignKey
from dis_sqlalchemy import inspect
from dis_sqlalchemy import Integer
from dis_sqlalchemy import select
from dis_sqlalchemy import String
from dis_sqlalchemy.ext.declarative import declarative_base
from dis_sqlalchemy.orm import column_property
from dis_sqlalchemy.orm import Mapped
from dis_sqlalchemy.orm import relationship

Base = declarative_base()


class B(Base):
    __tablename__ = "b"
    id = Column(Integer, primary_key=True)
    a_id: int = Column(ForeignKey("a.id"))

    # to attach attrs after the fact, declare them with Mapped
    # on the class...
    data: Mapped[str]

    a: Mapped[Optional["A"]]


class A(Base):
    __tablename__ = "a"

    id = Column(Integer, primary_key=True)
    data = Column(String)
    bs = relationship(B, uselist=True, back_populates="a")


# There's no way to intercept the __setattr__() from the metaclass
# here, and also when @reg.mapped() is used there is no metaclass.
# so have them do it the old way
inspect(B).add_property(
    "data",
    column_property(select(A.data).where(A.id == B.a_id).scalar_subquery()),
)
inspect(B).add_property("a", relationship(A))


# the constructor will pick them up
a1 = A()
b1 = B(data="b", a=a1)

# and it's mapped
B.data.in_(["x", "y"])
B.a.any()
