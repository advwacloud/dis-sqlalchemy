# test #6937
from dis_sqlalchemy import Column
from dis_sqlalchemy import Integer
from dis_sqlalchemy.orm import declarative_base
from dis_sqlalchemy.orm import declared_attr
from dis_sqlalchemy.orm import Mapped


Base = declarative_base()


class UpdatedCls:
    @declared_attr
    def __tablename__(cls) -> Mapped[str]:
        return cls.__name__.lower()

    updated_at = Column(Integer)


class Bar(UpdatedCls, Base):
    id = Column(Integer(), primary_key=True)
    num = Column(Integer)


Bar.updated_at.in_([1, 2, 3])

b1 = Bar(num=5, updated_at=6)
