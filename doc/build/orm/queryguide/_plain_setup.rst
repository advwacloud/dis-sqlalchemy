:orphan:

======================================
Setup for ORM Queryguide: SELECT
======================================

This page illustrates the mappings and fixture data used by the
:doc:`select` document of the :ref:`queryguide_toplevel`.

..  sourcecode:: python

    >>> from typing import List
    >>> from typing import Optional
    >>>
    >>> from dis_sqlalchemy import Column
    >>> from dis_sqlalchemy import create_engine
    >>> from dis_sqlalchemy import ForeignKey
    >>> from dis_sqlalchemy import Table
    >>> from dis_sqlalchemy.orm import DeclarativeBase
    >>> from dis_sqlalchemy.orm import Mapped
    >>> from dis_sqlalchemy.orm import mapped_column
    >>> from dis_sqlalchemy.orm import relationship
    >>> from dis_sqlalchemy.orm import Session
    >>>
    >>>
    >>> class Base(DeclarativeBase):
    ...     pass
    >>> class User(Base):
    ...     __tablename__ = "user_account"
    ...     id: Mapped[int] = mapped_column(primary_key=True)
    ...     name: Mapped[str]
    ...     fullname: Mapped[Optional[str]]
    ...     addresses: Mapped[List["Address"]] = relationship(back_populates="user")
    ...     orders: Mapped[List["Order"]] = relationship()
    ...
    ...     def __repr__(self) -> str:
    ...         return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"
    >>> class Address(Base):
    ...     __tablename__ = "address"
    ...     id: Mapped[int] = mapped_column(primary_key=True)
    ...     user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    ...     email_address: Mapped[str]
    ...     user: Mapped[User] = relationship(back_populates="addresses")
    ...
    ...     def __repr__(self) -> str:
    ...         return f"Address(id={self.id!r}, email_address={self.email_address!r})"
    >>> order_items_table = Table(
    ...     "order_items",
    ...     Base.metadata,
    ...     Column("order_id", ForeignKey("user_order.id"), primary_key=True),
    ...     Column("item_id", ForeignKey("item.id"), primary_key=True),
    ... )
    >>>
    >>> class Order(Base):
    ...     __tablename__ = "user_order"
    ...     id: Mapped[int] = mapped_column(primary_key=True)
    ...     user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    ...     items: Mapped[List["Item"]] = relationship(secondary=order_items_table)
    >>> class Item(Base):
    ...     __tablename__ = "item"
    ...     id: Mapped[int] = mapped_column(primary_key=True)
    ...     name: Mapped[str]
    ...     description: Mapped[str]
    >>> engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
    >>> Base.metadata.create_all(engine)
    BEGIN ...
    >>> conn = engine.connect()
    >>> session = Session(conn)
    >>> session.add_all(
    ...     [
    ...         User(
    ...             name="spongebob",
    ...             fullname="Spongebob Squarepants",
    ...             addresses=[Address(email_address="spongebob@dis_sqlalchemy.org")],
    ...         ),
    ...         User(
    ...             name="sandy",
    ...             fullname="Sandy Cheeks",
    ...             addresses=[
    ...                 Address(email_address="sandy@dis_sqlalchemy.org"),
    ...                 Address(email_address="squirrel@squirrelpower.org"),
    ...             ],
    ...         ),
    ...         User(
    ...             name="patrick",
    ...             fullname="Patrick Star",
    ...             addresses=[Address(email_address="pat999@aol.com")],
    ...         ),
    ...         User(
    ...             name="squidward",
    ...             fullname="Squidward Tentacles",
    ...             addresses=[Address(email_address="stentcl@dis_sqlalchemy.org")],
    ...         ),
    ...         User(name="ehkrabs", fullname="Eugene H. Krabs"),
    ...     ]
    ... )
    >>> session.commit()
    BEGIN ... COMMIT
    >>> conn.begin()
    BEGIN ...
