from itertools import zip_longest

from dis_sqlalchemy import bindparam
from dis_sqlalchemy import Column
from dis_sqlalchemy import Integer
from dis_sqlalchemy import MetaData
from dis_sqlalchemy import select
from dis_sqlalchemy import String
from dis_sqlalchemy import Table
from dis_sqlalchemy import testing
from dis_sqlalchemy import TypeDecorator
from dis_sqlalchemy.sql import base as sql_base
from dis_sqlalchemy.sql import coercions
from dis_sqlalchemy.sql import column
from dis_sqlalchemy.sql import ColumnElement
from dis_sqlalchemy.sql import roles
from dis_sqlalchemy.sql import util as sql_util
from dis_sqlalchemy.testing import assert_raises
from dis_sqlalchemy.testing import assert_raises_message
from dis_sqlalchemy.testing import eq_
from dis_sqlalchemy.testing import expect_raises_message
from dis_sqlalchemy.testing import fixtures
from dis_sqlalchemy.testing import is_
from dis_sqlalchemy.testing import is_not_none


class MiscTest(fixtures.TestBase):
    def test_column_element_no_visit(self):
        class MyElement(ColumnElement):
            _traverse_internals = []

        eq_(sql_util.find_tables(MyElement(), check_columns=True), [])

    def test_find_tables_selectable(self):
        metadata = MetaData()
        common = Table(
            "common",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("data", Integer),
            Column("extra", String(45)),
        )

        subset_select = select(common.c.id, common.c.data).alias()

        eq_(set(sql_util.find_tables(subset_select)), {common})

    @testing.variation("has_cache_key", [True, False])
    def test_get_embedded_bindparams(self, has_cache_key):
        bp = bindparam("x")

        if not has_cache_key:

            class NotCacheable(TypeDecorator):
                impl = String
                cache_ok = False

            stmt = select(column("q", NotCacheable())).where(column("y") == bp)

        else:
            stmt = select(column("q")).where(column("y") == bp)

        eq_(stmt._get_embedded_bindparams(), [bp])

        if not has_cache_key:
            is_(stmt._generate_cache_key(), None)
        else:
            is_not_none(stmt._generate_cache_key())

    def test_find_tables_aliases(self):
        metadata = MetaData()
        common = Table(
            "common",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("data", Integer),
            Column("extra", String(45)),
        )

        calias = common.alias()
        subset_select = select(common.c.id, calias.c.data).subquery()

        eq_(
            set(sql_util.find_tables(subset_select, include_aliases=True)),
            {common, calias, subset_select},
        )

    def test_incompatible_options_add_clslevel(self):
        class opt1(sql_base.CacheableOptions):
            _cache_key_traversal = []
            foo = "bar"

        with expect_raises_message(
            TypeError,
            "dictionary contains attributes not covered by "
            "Options class .*opt1.* .*'bar'.*",
        ):
            o1 = opt1

            o1 += {"foo": "f", "bar": "b"}

    def test_incompatible_options_add_instancelevel(self):
        class opt1(sql_base.CacheableOptions):
            _cache_key_traversal = []
            foo = "bar"

        o1 = opt1(foo="bat")

        with expect_raises_message(
            TypeError,
            "dictionary contains attributes not covered by "
            "Options class .*opt1.* .*'bar'.*",
        ):
            o1 += {"foo": "f", "bar": "b"}

    def test_options_merge(self):
        class opt1(sql_base.CacheableOptions):
            _cache_key_traversal = []

        class opt2(sql_base.CacheableOptions):
            _cache_key_traversal = []

            foo = "bar"

        class opt3(sql_base.CacheableOptions):
            _cache_key_traversal = []

            foo = "bar"
            bat = "hi"

        o2 = opt2.safe_merge(opt1)
        eq_(o2.__dict__, {})
        eq_(o2.foo, "bar")

        assert_raises_message(
            TypeError,
            r"other element .*opt2.* is not empty, is not of type .*opt1.*, "
            r"and contains attributes not covered here .*'foo'.*",
            opt1.safe_merge,
            opt2,
        )

        o2 = opt2 + {"foo": "bat"}
        o3 = opt2.safe_merge(o2)

        eq_(o3.foo, "bat")

        o4 = opt3.safe_merge(o2)
        eq_(o4.foo, "bat")
        eq_(o4.bat, "hi")

        assert_raises(TypeError, opt2.safe_merge, o4)

    @testing.combinations(
        (column("q"), [column("q")]),
        (column("q").desc(), [column("q")]),
        (column("q").desc().label(None), [column("q")]),
        (column("q").label(None).desc(), [column("q")]),
        (column("q").label(None).desc().label(None), [column("q")]),
        ("foo", []),  # textual label reference
        (
            select(column("q")).scalar_subquery().label(None),
            [select(column("q")).scalar_subquery().label(None)],
        ),
        (
            select(column("q")).scalar_subquery().label(None).desc(),
            [select(column("q")).scalar_subquery().label(None)],
        ),
    )
    def test_unwrap_order_by(self, expr, expected):
        expr = coercions.expect(roles.OrderByRole, expr)

        unwrapped = sql_util.unwrap_order_by(expr)

        for a, b in zip_longest(unwrapped, expected):
            assert a is not None and a.compare(b)
