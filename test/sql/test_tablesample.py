from dis_sqlalchemy import Column
from dis_sqlalchemy import column
from dis_sqlalchemy import Integer
from dis_sqlalchemy import String
from dis_sqlalchemy import Table
from dis_sqlalchemy import table
from dis_sqlalchemy import tablesample
from dis_sqlalchemy.engine import default
from dis_sqlalchemy.sql import func
from dis_sqlalchemy.sql import select
from dis_sqlalchemy.sql import text
from dis_sqlalchemy.sql.selectable import TableSample
from dis_sqlalchemy.testing import assert_raises_message
from dis_sqlalchemy.testing import AssertsCompiledSQL
from dis_sqlalchemy.testing import fixtures


class TableSampleTest(fixtures.TablesTest, AssertsCompiledSQL):
    __dialect__ = default.DefaultDialect(supports_native_boolean=True)

    run_setup_bind = None

    run_create_tables = None

    @classmethod
    def define_tables(cls, metadata):
        Table(
            "people",
            metadata,
            Column("people_id", Integer, primary_key=True),
            Column("age", Integer),
            Column("name", String(30)),
        )

    def test_standalone(self):
        table1 = self.tables.people

        # no special alias handling even though clause is not in the
        # context of a FROM clause
        self.assert_compile(
            tablesample(table1, 1, name="alias"),
            "people AS alias TABLESAMPLE system(:system_1)",
        )

        self.assert_compile(
            table1.tablesample(1, name="alias"),
            "people AS alias TABLESAMPLE system(:system_1)",
        )

        self.assert_compile(
            tablesample(
                table1, func.bernoulli(1), name="alias", seed=func.random()
            ),
            "people AS alias TABLESAMPLE bernoulli(:bernoulli_1) "
            "REPEATABLE (random())",
        )

    def test_select_from(self):
        table1 = self.tables.people

        self.assert_compile(
            select(table1.tablesample(text("1"), name="alias").c.people_id),
            "SELECT alias.people_id FROM "
            "people AS alias TABLESAMPLE system(1)",
        )

    def test_no_alias_construct(self):
        a = table("a", column("x"))

        assert_raises_message(
            NotImplementedError,
            "The TableSample class is not intended to be constructed "
            "directly.  "
            r"Please use the tablesample\(\) standalone",
            TableSample,
            a,
            "foo",
        )
