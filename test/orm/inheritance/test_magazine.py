"""A legacy test for a particular somewhat complicated mapping."""

from dis_sqlalchemy import CHAR
from dis_sqlalchemy import ForeignKey
from dis_sqlalchemy import Integer
from dis_sqlalchemy import String
from dis_sqlalchemy import testing
from dis_sqlalchemy import Text
from dis_sqlalchemy.orm import backref
from dis_sqlalchemy.orm import polymorphic_union
from dis_sqlalchemy.orm import relationship
from dis_sqlalchemy.testing import eq_
from dis_sqlalchemy.testing import fixtures
from dis_sqlalchemy.testing.fixtures import fixture_session
from dis_sqlalchemy.testing.schema import Column
from dis_sqlalchemy.testing.schema import Table


class MagazineTest(fixtures.MappedTest):
    @classmethod
    def setup_classes(cls):
        Base = cls.Comparable

        class Publication(Base):
            pass

        class Issue(Base):
            pass

        class Location(Base):
            pass

        class LocationName(Base):
            pass

        class PageSize(Base):
            pass

        class Magazine(Base):
            pass

        class Page(Base):
            pass

        class MagazinePage(Page):
            pass

        class ClassifiedPage(MagazinePage):
            pass

    @classmethod
    def define_tables(cls, metadata):
        Table(
            "publication",
            metadata,
            Column(
                "id", Integer, primary_key=True, test_needs_autoincrement=True
            ),
            Column("name", String(45), default=""),
        )
        Table(
            "issue",
            metadata,
            Column(
                "id", Integer, primary_key=True, test_needs_autoincrement=True
            ),
            Column("publication_id", Integer, ForeignKey("publication.id")),
            Column("issue", Integer),
        )
        Table(
            "location",
            metadata,
            Column(
                "id", Integer, primary_key=True, test_needs_autoincrement=True
            ),
            Column("issue_id", Integer, ForeignKey("issue.id")),
            Column("ref", CHAR(3), default=""),
            Column(
                "location_name_id", Integer, ForeignKey("location_name.id")
            ),
        )
        Table(
            "location_name",
            metadata,
            Column(
                "id", Integer, primary_key=True, test_needs_autoincrement=True
            ),
            Column("name", String(45), default=""),
        )
        Table(
            "magazine",
            metadata,
            Column(
                "id", Integer, primary_key=True, test_needs_autoincrement=True
            ),
            Column("location_id", Integer, ForeignKey("location.id")),
            Column("page_size_id", Integer, ForeignKey("page_size.id")),
        )
        Table(
            "page",
            metadata,
            Column(
                "id", Integer, primary_key=True, test_needs_autoincrement=True
            ),
            Column("page_no", Integer),
            Column("type", CHAR(1), default="p"),
        )
        Table(
            "magazine_page",
            metadata,
            Column(
                "page_id", Integer, ForeignKey("page.id"), primary_key=True
            ),
            Column("magazine_id", Integer, ForeignKey("magazine.id")),
            Column("orders", Text, default=""),
        )
        Table(
            "classified_page",
            metadata,
            Column(
                "magazine_page_id",
                Integer,
                ForeignKey("magazine_page.page_id"),
                primary_key=True,
            ),
            Column("titles", String(45), default=""),
        )
        Table(
            "page_size",
            metadata,
            Column(
                "id", Integer, primary_key=True, test_needs_autoincrement=True
            ),
            Column("width", Integer),
            Column("height", Integer),
            Column("name", String(45), default=""),
        )

    def _generate_data(self):
        (
            Publication,
            Issue,
            Location,
            LocationName,
            PageSize,
            Magazine,
            Page,
            MagazinePage,
            ClassifiedPage,
        ) = self.classes(
            "Publication",
            "Issue",
            "Location",
            "LocationName",
            "PageSize",
            "Magazine",
            "Page",
            "MagazinePage",
            "ClassifiedPage",
        )
        london = LocationName(name="London")
        pub = Publication(name="Test")
        issue = Issue(issue=46, publication=pub)
        location = Location(ref="ABC", name=london, issue=issue)

        page_size = PageSize(name="A4", width=210, height=297)

        magazine = Magazine(location=location, size=page_size)

        ClassifiedPage(magazine=magazine, page_no=1)
        MagazinePage(magazine=magazine, page_no=2)
        ClassifiedPage(magazine=magazine, page_no=3)

        return pub

    def _setup_mapping(self, use_unions, use_joins):
        (
            Publication,
            Issue,
            Location,
            LocationName,
            PageSize,
            Magazine,
            Page,
            MagazinePage,
            ClassifiedPage,
        ) = self.classes(
            "Publication",
            "Issue",
            "Location",
            "LocationName",
            "PageSize",
            "Magazine",
            "Page",
            "MagazinePage",
            "ClassifiedPage",
        )
        self.mapper_registry.map_imperatively(
            Publication, self.tables.publication
        )

        self.mapper_registry.map_imperatively(
            Issue,
            self.tables.issue,
            properties={
                "publication": relationship(
                    Publication,
                    backref=backref("issues", cascade="all, delete-orphan"),
                )
            },
        )

        self.mapper_registry.map_imperatively(
            LocationName, self.tables.location_name
        )

        self.mapper_registry.map_imperatively(
            Location,
            self.tables.location,
            properties={
                "issue": relationship(
                    Issue,
                    backref=backref(
                        "locations",
                        lazy="joined",
                        cascade="all, delete-orphan",
                    ),
                ),
                "name": relationship(LocationName),
            },
        )

        self.mapper_registry.map_imperatively(PageSize, self.tables.page_size)

        self.mapper_registry.map_imperatively(
            Magazine,
            self.tables.magazine,
            properties={
                "location": relationship(
                    Location, backref=backref("magazine", uselist=False)
                ),
                "size": relationship(PageSize),
            },
        )

        if use_unions:
            page_join = polymorphic_union(
                {
                    "m": self.tables.page.join(self.tables.magazine_page),
                    "c": self.tables.page.join(self.tables.magazine_page).join(
                        self.tables.classified_page
                    ),
                    "p": self.tables.page.select()
                    .where(self.tables.page.c.type == "p")
                    .subquery(),
                },
                None,
                "page_join",
            )
            page_mapper = self.mapper_registry.map_imperatively(
                Page,
                self.tables.page,
                with_polymorphic=("*", page_join),
                polymorphic_on=page_join.c.type,
                polymorphic_identity="p",
            )
        elif use_joins:
            page_join = self.tables.page.outerjoin(
                self.tables.magazine_page
            ).outerjoin(self.tables.classified_page)
            page_mapper = self.mapper_registry.map_imperatively(
                Page,
                self.tables.page,
                with_polymorphic=("*", page_join),
                polymorphic_on=self.tables.page.c.type,
                polymorphic_identity="p",
            )
        else:
            page_mapper = self.mapper_registry.map_imperatively(
                Page,
                self.tables.page,
                polymorphic_on=self.tables.page.c.type,
                polymorphic_identity="p",
            )

        if use_unions:
            magazine_join = polymorphic_union(
                {
                    "m": self.tables.page.join(self.tables.magazine_page),
                    "c": self.tables.page.join(self.tables.magazine_page).join(
                        self.tables.classified_page
                    ),
                },
                None,
                "page_join",
            )
            magazine_page_mapper = self.mapper_registry.map_imperatively(
                MagazinePage,
                self.tables.magazine_page,
                with_polymorphic=("*", magazine_join),
                inherits=page_mapper,
                polymorphic_identity="m",
                properties={
                    "magazine": relationship(
                        Magazine,
                        backref=backref(
                            "pages", order_by=magazine_join.c.page_no
                        ),
                    )
                },
            )
        elif use_joins:
            magazine_join = self.tables.page.join(
                self.tables.magazine_page
            ).outerjoin(self.tables.classified_page)
            magazine_page_mapper = self.mapper_registry.map_imperatively(
                MagazinePage,
                self.tables.magazine_page,
                with_polymorphic=("*", magazine_join),
                inherits=page_mapper,
                polymorphic_identity="m",
                properties={
                    "magazine": relationship(
                        Magazine,
                        backref=backref(
                            "pages", order_by=self.tables.page.c.page_no
                        ),
                    )
                },
            )
        else:
            magazine_page_mapper = self.mapper_registry.map_imperatively(
                MagazinePage,
                self.tables.magazine_page,
                inherits=page_mapper,
                polymorphic_identity="m",
                properties={
                    "magazine": relationship(
                        Magazine,
                        backref=backref(
                            "pages", order_by=self.tables.page.c.page_no
                        ),
                    )
                },
            )

        self.mapper_registry.map_imperatively(
            ClassifiedPage,
            self.tables.classified_page,
            inherits=magazine_page_mapper,
            polymorphic_identity="c",
            primary_key=[self.tables.page.c.id],
        )

    @testing.combinations(
        ("unions", True, False),
        ("joins", False, True),
        ("plain", False, False),
        id_="iaa",
    )
    def test_magazine_round_trip(self, use_unions, use_joins):
        self._setup_mapping(use_unions, use_joins)

        Publication = self.classes.Publication

        session = fixture_session()

        pub = self._generate_data()
        session.add(pub)
        session.commit()
        session.close()

        p = session.query(Publication).filter(Publication.name == "Test").one()

        test_pub = self._generate_data()
        eq_(p, test_pub)
        eq_(
            p.issues[0].locations[0].magazine.pages,
            test_pub.issues[0].locations[0].magazine.pages,
        )
