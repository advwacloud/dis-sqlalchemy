import dataclasses

from dis_sqlalchemy import select
from dis_sqlalchemy.orm import composite
from dis_sqlalchemy.orm import DeclarativeBase
from dis_sqlalchemy.orm import Mapped
from dis_sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


@dataclasses.dataclass
class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Vertex(Base):
    __tablename__ = "vertices"

    id: Mapped[int] = mapped_column(primary_key=True)
    x1: Mapped[int]
    y1: Mapped[int]
    x2: Mapped[int]
    y2: Mapped[int]

    # inferred from right hand side
    start = composite(Point, "x1", "y1")

    # taken from left hand side
    end: Mapped[Point] = composite(Point, "x2", "y2")


v1 = Vertex(start=Point(3, 4), end=Point(5, 6))

stmt = select(Vertex).where(Vertex.start.in_([Point(3, 4)]))

# EXPECTED_TYPE: Select[Tuple[Vertex]]
reveal_type(stmt)

# EXPECTED_TYPE: composite.Point
reveal_type(v1.start)

# EXPECTED_TYPE: composite.Point
reveal_type(v1.end)

# EXPECTED_TYPE: int
reveal_type(v1.end.y)
