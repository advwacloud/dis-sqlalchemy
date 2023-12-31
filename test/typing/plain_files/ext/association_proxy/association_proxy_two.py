from __future__ import annotations

from typing import Final

from dis_sqlalchemy import Column
from dis_sqlalchemy import ForeignKey
from dis_sqlalchemy import Integer
from dis_sqlalchemy import String
from dis_sqlalchemy import Table
from dis_sqlalchemy.ext.associationproxy import association_proxy
from dis_sqlalchemy.ext.associationproxy import AssociationProxy
from dis_sqlalchemy.orm import DeclarativeBase
from dis_sqlalchemy.orm import Mapped
from dis_sqlalchemy.orm import mapped_column
from dis_sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    kw: Mapped[list[Keyword]] = relationship(
        secondary=lambda: user_keyword_table
    )

    def __init__(self, name: str):
        self.name = name

    # proxy the 'keyword' attribute from the 'kw' relationship
    keywords: AssociationProxy[list[str]] = association_proxy("kw", "keyword")


class Keyword(Base):
    __tablename__ = "keyword"
    id: Mapped[int] = mapped_column(primary_key=True)
    keyword: Mapped[str] = mapped_column(String(64))

    def __init__(self, keyword: str):
        self.keyword = keyword


user_keyword_table: Final[Table] = Table(
    "user_keyword",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("keyword_id", Integer, ForeignKey("keyword.id"), primary_key=True),
)

user = User("jek")

# EXPECTED_TYPE: list[Keyword]
reveal_type(user.kw)

user.kw.append(Keyword("cheese-inspector"))

user.keywords.append("cheese-inspector")

# EXPECTED_TYPE: list[str]
reveal_type(user.keywords)

user.keywords.append("snack ninja")
