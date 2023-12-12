from dis_sqlalchemy import Integer
from dis_sqlalchemy import UniqueConstraint
from dis_sqlalchemy.dialects.sqlite import insert
from dis_sqlalchemy.orm import DeclarativeBase
from dis_sqlalchemy.orm import Mapped
from dis_sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class Test(Base):
    __tablename__ = "test_table_json"

    id = mapped_column(Integer, primary_key=True)
    data: Mapped[str] = mapped_column()


unique = UniqueConstraint(name="my_constraint")
insert(Test).on_conflict_do_nothing("foo", Test.id > 0).on_conflict_do_update(
    unique, Test.id > 0, {"id": 42, Test.data: 99}, Test.id == 22
).excluded.foo.desc()
