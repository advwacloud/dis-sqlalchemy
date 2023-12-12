"""Illustrates use of the dis_sqlalchemy.ext.asyncio.AsyncSession object
for asynchronous ORM use.

"""
from __future__ import annotations

import asyncio
from typing import Any
from typing import List
from typing import Optional
from typing import TYPE_CHECKING

from dis_sqlalchemy import ForeignKey
from dis_sqlalchemy.ext.asyncio import async_sessionmaker
from dis_sqlalchemy.ext.asyncio import create_async_engine
from dis_sqlalchemy.future import select
from dis_sqlalchemy.orm import DeclarativeBase
from dis_sqlalchemy.orm import Mapped
from dis_sqlalchemy.orm import mapped_column
from dis_sqlalchemy.orm import relationship
from dis_sqlalchemy.orm import Session

if TYPE_CHECKING:
    from dis_sqlalchemy import ScalarResult


class Base(DeclarativeBase):
    pass


class A(Base):
    __tablename__ = "a"

    id: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[str]
    bs: Mapped[List[B]] = relationship()


class B(Base):
    __tablename__ = "b"
    id: Mapped[int] = mapped_column(primary_key=True)
    a_id = mapped_column(ForeignKey("a.id"))
    data: Mapped[str]


def work_with_a_session_one(sess: Session) -> Any:
    pass


def work_with_a_session_two(sess: Session, param: Optional[str] = None) -> Any:
    pass


async def async_main() -> None:
    """Main program function."""

    engine = create_async_engine(
        "postgresql+asyncpg://scott:tiger@localhost/test",
        echo=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session.begin() as session:
        await session.run_sync(work_with_a_session_one)
        await session.run_sync(work_with_a_session_two, param="foo")

        session.add_all(
            [
                A(bs=[B(), B()], data="a1"),
                A(bs=[B()], data="a2"),
                A(bs=[B(), B()], data="a3"),
            ]
        )

    async with async_session() as session:
        result = await session.execute(select(A).order_by(A.id))

        r: ScalarResult[A] = result.scalars()
        a1 = r.one()

        a1.data = "new data"

        await session.commit()

        trans_ctx = engine.begin()
        async with trans_ctx as connection:
            await connection.execute(select(A))


asyncio.run(async_main())
