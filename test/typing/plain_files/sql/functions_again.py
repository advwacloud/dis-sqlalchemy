from dis_sqlalchemy import func
from dis_sqlalchemy.orm import DeclarativeBase
from dis_sqlalchemy.orm import Mapped
from dis_sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class Foo(Base):
    __tablename__ = "foo"

    id: Mapped[int] = mapped_column(primary_key=True)
    a: Mapped[int]
    b: Mapped[int]


func.row_number().over(order_by=Foo.a, partition_by=Foo.b.desc())
func.row_number().over(order_by=[Foo.a.desc(), Foo.b.desc()])
func.row_number().over(partition_by=[Foo.a.desc(), Foo.b.desc()])
func.row_number().over(order_by="a", partition_by=("a", "b"))
func.row_number().over(partition_by="a", order_by=("a", "b"))
