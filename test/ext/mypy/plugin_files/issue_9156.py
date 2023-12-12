from typing import Any
from typing import Type

from dis_sqlalchemy.sql.elements import ColumnElement
from dis_sqlalchemy.sql.type_api import TypeEngine

col: ColumnElement[Any]
type_: Type[TypeEngine[Any]]
obj: TypeEngine[Any]

col.cast(type_)
col.cast(obj)
