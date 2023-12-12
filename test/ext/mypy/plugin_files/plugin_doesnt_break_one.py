from dis_sqlalchemy import Column
from dis_sqlalchemy import Integer
from dis_sqlalchemy import String
from dis_sqlalchemy.orm import registry

reg: registry = registry()


@reg.mapped
class Foo:
    pass
    id: int = Column(Integer())
    name: str = Column(String)


f1 = Foo()


# EXPECTED_MYPY: Name 'u1' is not defined
p: str = u1.name  # noqa
