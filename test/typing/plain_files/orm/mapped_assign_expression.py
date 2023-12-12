from datetime import datetime

from dis_sqlalchemy import create_engine
from dis_sqlalchemy.orm import Mapped
from dis_sqlalchemy.orm import registry
from dis_sqlalchemy.orm import Session
from dis_sqlalchemy.sql.functions import now
from dis_sqlalchemy.testing.schema import mapped_column

mapper_registry: registry = registry()
e = create_engine("sqlite:///database.db", echo=True)


@mapper_registry.mapped
class A:
    __tablename__ = "a"
    id: Mapped[int] = mapped_column(primary_key=True)
    date_time: Mapped[datetime]


mapper_registry.metadata.create_all(e)

with Session(e) as s:
    a = A()
    a.date_time = now()
    s.add(a)
    s.commit()
