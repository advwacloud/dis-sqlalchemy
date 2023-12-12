from decimal import Decimal

from dis_sqlalchemy import BIGINT
from dis_sqlalchemy import Column
from dis_sqlalchemy import DECIMAL
from dis_sqlalchemy import Integer
from dis_sqlalchemy import select
from dis_sqlalchemy import Sequence
from dis_sqlalchemy import String
from dis_sqlalchemy import Table
from dis_sqlalchemy.testing import config
from dis_sqlalchemy.testing import eq_
from dis_sqlalchemy.testing import fixtures
from dis_sqlalchemy.testing.provision import normalize_sequence


class SequenceTest(fixtures.TablesTest):
    __only_on__ = "mssql"
    __backend__ = True

    @classmethod
    def define_tables(cls, metadata):
        Table(
            "int_seq_t",
            metadata,
            Column(
                "id", Integer, default=Sequence("int_seq", data_type=Integer())
            ),
            Column(
                "id_provision",
                Integer,
                default=normalize_sequence(
                    config, Sequence("id_provision", data_type=Integer())
                ),
            ),
            Column(
                "id_start",
                Integer,
                default=Sequence("id_start", data_type=Integer(), start=42),
            ),
            Column("txt", String(50)),
        )

        Table(
            "bigint_seq_t",
            metadata,
            Column(
                "id",
                BIGINT,
                default=Sequence("bigint_seq", start=3000000000),
            ),
            Column("txt", String(50)),
        )

        Table(
            "decimal_seq_t",
            metadata,
            Column(
                "id",
                DECIMAL(10, 0),
                default=Sequence(
                    "decimal_seq",
                    data_type=DECIMAL(10, 0),
                    start=3000000000,
                ),
            ),
            Column("txt", String(50)),
        )

    def test_int_seq(self, connection):
        t = self.tables.int_seq_t
        connection.execute(t.insert().values({"txt": "int_seq test"}))
        result = connection.execute(select(t)).first()
        eq_(result.id, -(2**31))
        eq_(result.id_provision, 1)
        eq_(result.id_start, 42)

    def test_bigint_seq(self, connection):
        t = self.tables.bigint_seq_t
        connection.execute(t.insert().values({"txt": "bigint_seq test"}))
        result = connection.scalar(select(t.c.id))
        eq_(result, 3000000000)

    def test_decimal_seq(self, connection):
        t = self.tables.decimal_seq_t
        connection.execute(t.insert().values({"txt": "decimal_seq test"}))
        result = connection.scalar(select(t.c.id))
        eq_(result, Decimal("3000000000"))
