import datetime
from typing import Optional

from dis_sqlalchemy import Column
from dis_sqlalchemy import DateTime
from dis_sqlalchemy import Integer
from dis_sqlalchemy import String
from dis_sqlalchemy import Table
from dis_sqlalchemy.orm import declarative_base
from dis_sqlalchemy.orm import Mapped


Base = declarative_base()


class MyMappedClass(Base):
    __table_ = Table(
        "some_table",
        Base.metadata,
        Column("id", Integer, primary_key=True),
        Column("data", String(50)),
        Column("created_at", DateTime),
    )

    id: Mapped[int]
    data: Mapped[Optional[str]]
    created_at: Mapped[datetime.datetime]


m1 = MyMappedClass(id=5, data="string", created_at=datetime.datetime.now())

# EXPECTED_MYPY: Argument "created_at" to "MyMappedClass" has incompatible type "int"; expected "datetime" # noqa
m2 = MyMappedClass(id=5, data="string", created_at=12)


# EXPECTED_MYPY: Incompatible types in assignment (expression has type "Optional[str]", variable has type "str") # noqa
x: str = MyMappedClass().data
