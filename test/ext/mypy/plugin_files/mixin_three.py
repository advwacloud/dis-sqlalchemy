from typing import Callable

from dis_sqlalchemy import Column
from dis_sqlalchemy import Integer
from dis_sqlalchemy import String
from dis_sqlalchemy.orm import deferred
from dis_sqlalchemy.orm import Mapped
from dis_sqlalchemy.orm.decl_api import declarative_mixin
from dis_sqlalchemy.orm.decl_api import declared_attr
from dis_sqlalchemy.orm.interfaces import MapperProperty


def some_other_decorator(fn: Callable[..., None]) -> Callable[..., None]:
    return fn


@declarative_mixin
class HasAMixin:
    x: Mapped[int] = Column(Integer)

    y = Column(String)

    @declared_attr
    def data(cls) -> Column[String]:
        return Column(String)

    @declared_attr
    def data2(cls) -> MapperProperty[str]:
        return deferred(Column(String))

    @some_other_decorator
    def q(cls) -> None:
        return None
