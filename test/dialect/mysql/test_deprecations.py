from dis_sqlalchemy import select
from dis_sqlalchemy import table
from dis_sqlalchemy.dialects.mysql import base as mysql
from dis_sqlalchemy.testing import AssertsCompiledSQL
from dis_sqlalchemy.testing import expect_deprecated
from dis_sqlalchemy.testing import fixtures


class CompileTest(AssertsCompiledSQL, fixtures.TestBase):
    __dialect__ = mysql.dialect()

    def test_distinct_string(self):
        s = select("*").select_from(table("foo"))
        s._distinct = "foo"

        with expect_deprecated(
            "Sending string values for 'distinct' is deprecated in the MySQL "
            "dialect and will be removed in a future release"
        ):
            self.assert_compile(s, "SELECT FOO * FROM foo")
