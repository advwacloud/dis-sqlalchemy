"""Illustrates a so-called "generic foreign key", in a similar fashion
to that of popular frameworks such as Django, ROR, etc.  This
approach bypasses standard referential integrity
practices, in that the "foreign key" column is not actually
constrained to refer to any particular table; instead,
in-application logic is used to determine which table is referenced.

This approach is not in line with dis_sqlalchemy's usual style, as foregoing
foreign key integrity means that the tables can easily contain invalid
references and also have no ability to use in-database cascade functionality.

However, due to the popularity of these systems, as well as that it uses
the fewest number of tables (which doesn't really offer any "advantage",
though seems to be comforting to many) this recipe remains in
high demand, so in the interests of having an easy StackOverflow answer
queued up, here it is.   The author recommends "table_per_related"
or "table_per_association" instead of this approach.

"""
from dis_sqlalchemy import and_
from dis_sqlalchemy import Column
from dis_sqlalchemy import create_engine
from dis_sqlalchemy import event
from dis_sqlalchemy import Integer
from dis_sqlalchemy import String
from dis_sqlalchemy.ext.declarative import as_declarative
from dis_sqlalchemy.ext.declarative import declared_attr
from dis_sqlalchemy.orm import backref
from dis_sqlalchemy.orm import foreign
from dis_sqlalchemy.orm import relationship
from dis_sqlalchemy.orm import remote
from dis_sqlalchemy.orm import Session


@as_declarative()
class Base:
    """Base class which provides automated table name
    and surrogate primary key column.

    """

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


class Address(Base):
    """The Address class.

    This represents all address records in a
    single table.

    """

    street = Column(String)
    city = Column(String)
    zip = Column(String)

    discriminator = Column(String)
    """Refers to the type of parent."""

    parent_id = Column(Integer)
    """Refers to the primary key of the parent.

    This could refer to any table.
    """

    @property
    def parent(self):
        """Provides in-Python access to the "parent" by choosing
        the appropriate relationship.

        """
        return getattr(self, "parent_%s" % self.discriminator)

    def __repr__(self):
        return "%s(street=%r, city=%r, zip=%r)" % (
            self.__class__.__name__,
            self.street,
            self.city,
            self.zip,
        )


class HasAddresses:
    """HasAddresses mixin, creates a relationship to
    the address_association table for each parent.

    """


@event.listens_for(HasAddresses, "mapper_configured", propagate=True)
def setup_listener(mapper, class_):
    name = class_.__name__
    discriminator = name.lower()
    class_.addresses = relationship(
        Address,
        primaryjoin=and_(
            class_.id == foreign(remote(Address.parent_id)),
            Address.discriminator == discriminator,
        ),
        backref=backref(
            "parent_%s" % discriminator,
            primaryjoin=remote(class_.id) == foreign(Address.parent_id),
        ),
    )

    @event.listens_for(class_.addresses, "append")
    def append_address(target, value, initiator):
        value.discriminator = discriminator


class Customer(HasAddresses, Base):
    name = Column(String)


class Supplier(HasAddresses, Base):
    company_name = Column(String)


engine = create_engine("sqlite://", echo=True)
Base.metadata.create_all(engine)

session = Session(engine)

session.add_all(
    [
        Customer(
            name="customer 1",
            addresses=[
                Address(
                    street="123 anywhere street", city="New York", zip="10110"
                ),
                Address(
                    street="40 main street", city="San Francisco", zip="95732"
                ),
            ],
        ),
        Supplier(
            company_name="Ace Hammers",
            addresses=[
                Address(street="2569 west elm", city="Detroit", zip="56785")
            ],
        ),
    ]
)

session.commit()

for customer in session.query(Customer):
    for address in customer.addresses:
        print(address)
        print(address.parent)
