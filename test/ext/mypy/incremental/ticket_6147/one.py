from dis_sqlalchemy import Column
from dis_sqlalchemy import Integer
from .base import Base


class One(Base):
    __tablename__ = "one"
    id = Column(Integer, primary_key=True)


o1 = One(id=5)

One.id.in_([1, 2])
