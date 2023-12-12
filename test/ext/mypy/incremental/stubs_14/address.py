from typing import TYPE_CHECKING

from . import Base
from .user import HasUser

if TYPE_CHECKING:
    from dis_sqlalchemy import Column  # noqa
    from dis_sqlalchemy import Integer  # noqa
    from dis_sqlalchemy.orm import RelationshipProperty  # noqa
    from .user import User  # noqa


class Address(Base, HasUser):
    pass
