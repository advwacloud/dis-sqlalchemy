"""Generic mapping to Select statements"""
import dis_sqlalchemy as sa
from dis_sqlalchemy import column
from dis_sqlalchemy import Integer
from dis_sqlalchemy import select
from dis_sqlalchemy import String
from dis_sqlalchemy import testing
from dis_sqlalchemy.orm import Session
from dis_sqlalchemy.testing import assert_raises
from dis_sqlalchemy.testing import assert_raises_message
from dis_sqlalchemy.testing import AssertsCompiledSQL
from dis_sqlalchemy.testing import eq_
from dis_sqlalchemy.testing import fixtures
from dis_sqlalchemy.testing.fixtures import fixture_session
from dis_sqlalchemy.testing.schema import Column
from dis_sqlalchemy.testing.schema import Table


# TODO: more tests mapping to selects


class SelectableNoFromsTest(fixtures.MappedTest, AssertsCompiledSQL):
    @classmethod
    def define_tables(cls, metadata):
        Table(
            "common",
            metadata,
            Column(
                "id", Integer, primary_key=True, test_needs_autoincrement=True
            ),
            Column("data", Integer),
            Column("extra", String(45)),
        )

    @classmethod
    def setup_classes(cls):
        class Subset(cls.Comparable):
            pass

    def test_no_tables(self):
        Subset = self.classes.Subset

        selectable = select(column("x"), column("y"), column("z")).alias()
        self.mapper_registry.map_imperatively(
            Subset, selectable, primary_key=[selectable.c.x]
        )

        self.assert_compile(
            fixture_session().query(Subset),
            "SELECT anon_1.x AS anon_1_x, anon_1.y AS anon_1_y, "
            "anon_1.z AS anon_1_z FROM (SELECT x, y, z) AS anon_1",
            use_default_dialect=True,
        )

    def test_no_table_needs_pl(self):
        Subset = self.classes.Subset

        selectable = select(column("x"), column("y"), column("z")).alias()
        assert_raises_message(
            sa.exc.ArgumentError,
            "could not assemble any primary key columns",
            self.mapper_registry.map_imperatively,
            Subset,
            selectable,
        )

    def test_no_selects(self):
        Subset, common = self.classes.Subset, self.tables.common

        subset_select = select(common.c.id, common.c.data)
        assert_raises(
            sa.exc.ArgumentError,
            self.mapper_registry.map_imperatively,
            Subset,
            subset_select,
        )

    def test_basic(self):
        Subset, common = self.classes.Subset, self.tables.common

        subset_select = select(common.c.id, common.c.data).alias()
        self.mapper_registry.map_imperatively(Subset, subset_select)
        sess = Session(bind=testing.db)
        sess.add(Subset(data=1))
        sess.flush()
        sess.expunge_all()

        eq_(sess.query(Subset).all(), [Subset(data=1)])
        eq_(sess.query(Subset).filter(Subset.data == 1).one(), Subset(data=1))
        eq_(sess.query(Subset).filter(Subset.data != 1).first(), None)

        subset_select = sa.orm.class_mapper(Subset).persist_selectable
        eq_(
            sess.query(Subset).filter(subset_select.c.data == 1).one(),
            Subset(data=1),
        )
