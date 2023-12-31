"""This series of tests will illustrate different ways to UPDATE a large number
of rows in bulk (under construction! there's just one test at the moment)


"""
from dis_sqlalchemy import Column
from dis_sqlalchemy import create_engine
from dis_sqlalchemy import Integer
from dis_sqlalchemy import String
from dis_sqlalchemy.ext.declarative import declarative_base
from dis_sqlalchemy.orm import Session
from . import Profiler


Base = declarative_base()
engine = None


class Customer(Base):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(255))


Profiler.init("bulk_updates", num=100000)


@Profiler.setup
def setup_database(dburl, echo, num):
    global engine
    engine = create_engine(dburl, echo=echo)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    s = Session(engine)
    for chunk in range(0, num, 10000):
        s.bulk_insert_mappings(
            Customer,
            [
                {
                    "name": "customer name %d" % i,
                    "description": "customer description %d" % i,
                }
                for i in range(chunk, chunk + 10000)
            ],
        )
    s.commit()


@Profiler.profile
def test_orm_flush(n):
    """UPDATE statements via the ORM flush process."""
    session = Session(bind=engine)
    for chunk in range(0, n, 1000):
        customers = (
            session.query(Customer)
            .filter(Customer.id.between(chunk, chunk + 1000))
            .all()
        )
        for customer in customers:
            customer.description += "updated"
        session.flush()
    session.commit()
