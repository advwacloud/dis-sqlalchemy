from typing import Optional

from dis_sqlalchemy import Column
from dis_sqlalchemy import Integer
from dis_sqlalchemy import String
from dis_sqlalchemy.orm import registry

reg: registry = registry()


@reg.mapped
class User:
    __tablename__ = "user"

    id = Column(Integer(), primary_key=True)

    # we will call this "semi-inferred", since the real
    # type will be Mapped[Optional[str]], but the Optional[str]
    # which is not inferred, we use that to create it
    name: Optional[str] = Column(String)


u1 = User()

# EXPECTED_MYPY: Incompatible types in assignment (expression has type "Optional[str]", variable has type "str")  # noqa: E501
p: str = u1.name
