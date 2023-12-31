# this should pass typing with no plugins

from typing import Any
from typing import List
from typing import Mapping
from typing import Optional

from dis_sqlalchemy import Column
from dis_sqlalchemy import create_engine
from dis_sqlalchemy import ForeignKey
from dis_sqlalchemy import Integer
from dis_sqlalchemy import select
from dis_sqlalchemy import String
from dis_sqlalchemy import Table
from dis_sqlalchemy.orm import registry
from dis_sqlalchemy.orm import relationship
from dis_sqlalchemy.orm import Session
from dis_sqlalchemy.orm.attributes import Mapped
from dis_sqlalchemy.orm.decl_api import DeclarativeMeta


class Base(metaclass=DeclarativeMeta):
    __abstract__ = True
    registry = registry()
    metadata = registry.metadata


class A(Base):
    __table__ = Table(
        "a",
        Base.metadata,
        Column("id", Integer, primary_key=True),
        Column("data", String),
    )

    __mapper_args__: Mapping[str, Any] = {
        "properties": {"bs": relationship("B")}
    }

    id: Mapped[int]
    data: Mapped[str]
    bs: "Mapped[List[B]]"

    def __init__(
        self,
        id: Optional[int] = None,  # noqa: A002
        data: Optional[str] = None,
        bs: "Optional[List[B]]" = None,
    ):
        self.registry.constructor(self, id=id, data=data, bs=bs)


class B(Base):
    __table__ = Table(
        "b",
        Base.metadata,
        Column("id", Integer, primary_key=True),
        Column("a_id", ForeignKey("a.id")),
        Column("data", String),
    )
    id: Mapped[int]
    a_id: Mapped[int]
    data: Mapped[str]

    def __init__(
        self,
        id: Optional[int] = None,  # noqa: A002
        a_id: Optional[int] = None,
        data: Optional[str] = None,
    ):
        self.registry.constructor(self, id=id, a_id=a_id, data=data)


e = create_engine("sqlite://", echo=True)
Base.metadata.create_all(e)

s = Session(e)


a1 = A(data="some data", bs=[B(data="some data")])

x: List[B] = a1.bs

s.add(a1)
s.commit()

# illustrate descriptor working at the class level, A.data.in_()
stmt = (
    select(A.data, B.data)
    .join(B)
    .where(A.data.in_(["some data", "some other data"]))
)

for row in s.execute(stmt):
    print(row)
