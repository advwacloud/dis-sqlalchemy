import typing

from dis_sqlalchemy import Integer
from dis_sqlalchemy import Text
from dis_sqlalchemy.orm import DeclarativeBase
from dis_sqlalchemy.orm import declared_attr
from dis_sqlalchemy.orm import Mapped
from dis_sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class HasRelatedDataMixin:
    @declared_attr
    def related_data(cls) -> Mapped[str]:
        return mapped_column(Text(), deferred=True)


class User(HasRelatedDataMixin, Base):
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return "user"

    @declared_attr.directive
    def __mapper_args__(cls) -> typing.Dict[str, typing.Any]:
        return {}

    id = mapped_column(Integer, primary_key=True)


class Foo(Base):
    __tablename__ = "foo"

    id = mapped_column(Integer, primary_key=True)


u1 = User()

if typing.TYPE_CHECKING:
    # EXPECTED_TYPE: str
    reveal_type(User.__tablename__)

    # EXPECTED_TYPE: str
    reveal_type(Foo.__tablename__)

    # EXPECTED_TYPE: str
    reveal_type(u1.related_data)

    # EXPECTED_TYPE: InstrumentedAttribute[str]
    reveal_type(User.related_data)
