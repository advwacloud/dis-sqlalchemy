from typing import Sequence
from typing import TYPE_CHECKING

from dis_sqlalchemy import create_engine
from dis_sqlalchemy import select
from dis_sqlalchemy.orm import DeclarativeBase
from dis_sqlalchemy.orm import Mapped
from dis_sqlalchemy.orm import mapped_column
from dis_sqlalchemy.orm import Session
from dis_sqlalchemy.orm import with_polymorphic


class Base(DeclarativeBase):
    ...


class Message(Base):
    __tablename__ = "message"
    __mapper_args__ = {
        "polymorphic_on": "message_type",
        "polymorphic_identity": __tablename__,
    }
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    message_type: Mapped[str]


class UserComment(Message):
    __mapper_args__ = {
        "polymorphic_identity": "user_comment",
    }
    username: Mapped[str] = mapped_column(nullable=True)


engine = create_engine("postgresql+psycopg2://scott:tiger@localhost/")


def get_messages() -> Sequence[Message]:
    with Session(engine) as session:
        message_query = select(Message)

        if TYPE_CHECKING:
            # EXPECTED_TYPE: Select[Tuple[Message]]
            reveal_type(message_query)

        return session.scalars(message_query).all()


def get_poly_messages() -> Sequence[Message]:
    with Session(engine) as session:
        PolymorphicMessage = with_polymorphic(Message, (UserComment,))

        if TYPE_CHECKING:
            # EXPECTED_TYPE: AliasedClass[Message]
            reveal_type(PolymorphicMessage)

        poly_query = select(PolymorphicMessage)

        if TYPE_CHECKING:
            # EXPECTED_TYPE: Select[Tuple[Message]]
            reveal_type(poly_query)

        return session.scalars(poly_query).all()
