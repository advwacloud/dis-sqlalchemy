import uuid

from dis_sqlalchemy import Column
from dis_sqlalchemy import String
from dis_sqlalchemy.orm import declarative_base

Base = declarative_base()


class MyClass(Base):
    id = Column(String, default=lambda: uuid.uuid4(), primary_key=True)
