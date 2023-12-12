# ext/mypy/names.py
# Copyright (C) 2021 the dis_sqlalchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of dis_sqlalchemy and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php

from __future__ import annotations

from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Union

from mypy.nodes import ARG_POS
from mypy.nodes import CallExpr
from mypy.nodes import ClassDef
from mypy.nodes import Decorator
from mypy.nodes import Expression
from mypy.nodes import FuncDef
from mypy.nodes import MemberExpr
from mypy.nodes import NameExpr
from mypy.nodes import OverloadedFuncDef
from mypy.nodes import SymbolNode
from mypy.nodes import TypeAlias
from mypy.nodes import TypeInfo
from mypy.plugin import SemanticAnalyzerPluginInterface
from mypy.types import CallableType
from mypy.types import get_proper_type
from mypy.types import Instance
from mypy.types import UnboundType

from ... import util

COLUMN: int = util.symbol("COLUMN")  # type: ignore
RELATIONSHIP: int = util.symbol("RELATIONSHIP")  # type: ignore
REGISTRY: int = util.symbol("REGISTRY")  # type: ignore
COLUMN_PROPERTY: int = util.symbol("COLUMN_PROPERTY")  # type: ignore
TYPEENGINE: int = util.symbol("TYPEENGNE")  # type: ignore
MAPPED: int = util.symbol("MAPPED")  # type: ignore
DECLARATIVE_BASE: int = util.symbol("DECLARATIVE_BASE")  # type: ignore
DECLARATIVE_META: int = util.symbol("DECLARATIVE_META")  # type: ignore
MAPPED_DECORATOR: int = util.symbol("MAPPED_DECORATOR")  # type: ignore
COLUMN_PROPERTY: int = util.symbol("COLUMN_PROPERTY")  # type: ignore
SYNONYM_PROPERTY: int = util.symbol("SYNONYM_PROPERTY")  # type: ignore
COMPOSITE_PROPERTY: int = util.symbol("COMPOSITE_PROPERTY")  # type: ignore
DECLARED_ATTR: int = util.symbol("DECLARED_ATTR")  # type: ignore
MAPPER_PROPERTY: int = util.symbol("MAPPER_PROPERTY")  # type: ignore
AS_DECLARATIVE: int = util.symbol("AS_DECLARATIVE")  # type: ignore
AS_DECLARATIVE_BASE: int = util.symbol("AS_DECLARATIVE_BASE")  # type: ignore
DECLARATIVE_MIXIN: int = util.symbol("DECLARATIVE_MIXIN")  # type: ignore
QUERY_EXPRESSION: int = util.symbol("QUERY_EXPRESSION")  # type: ignore

# names that must succeed with mypy.api.named_type
NAMED_TYPE_BUILTINS_OBJECT = "builtins.object"
NAMED_TYPE_BUILTINS_STR = "builtins.str"
NAMED_TYPE_BUILTINS_LIST = "builtins.list"
NAMED_TYPE_SQLA_MAPPED = "dis_sqlalchemy.orm.base.Mapped"

_lookup: Dict[str, Tuple[int, Set[str]]] = {
    "Column": (
        COLUMN,
        {
            "dis_sqlalchemy.sql.schema.Column",
            "dis_sqlalchemy.sql.Column",
        },
    ),
    "Relationship": (
        RELATIONSHIP,
        {
            "dis_sqlalchemy.orm.relationships.Relationship",
            "dis_sqlalchemy.orm.relationships.RelationshipProperty",
            "dis_sqlalchemy.orm.Relationship",
            "dis_sqlalchemy.orm.RelationshipProperty",
        },
    ),
    "RelationshipProperty": (
        RELATIONSHIP,
        {
            "dis_sqlalchemy.orm.relationships.Relationship",
            "dis_sqlalchemy.orm.relationships.RelationshipProperty",
            "dis_sqlalchemy.orm.Relationship",
            "dis_sqlalchemy.orm.RelationshipProperty",
        },
    ),
    "registry": (
        REGISTRY,
        {
            "dis_sqlalchemy.orm.decl_api.registry",
            "dis_sqlalchemy.orm.registry",
        },
    ),
    "ColumnProperty": (
        COLUMN_PROPERTY,
        {
            "dis_sqlalchemy.orm.properties.MappedSQLExpression",
            "dis_sqlalchemy.orm.MappedSQLExpression",
            "dis_sqlalchemy.orm.properties.ColumnProperty",
            "dis_sqlalchemy.orm.ColumnProperty",
        },
    ),
    "MappedSQLExpression": (
        COLUMN_PROPERTY,
        {
            "dis_sqlalchemy.orm.properties.MappedSQLExpression",
            "dis_sqlalchemy.orm.MappedSQLExpression",
            "dis_sqlalchemy.orm.properties.ColumnProperty",
            "dis_sqlalchemy.orm.ColumnProperty",
        },
    ),
    "Synonym": (
        SYNONYM_PROPERTY,
        {
            "dis_sqlalchemy.orm.descriptor_props.Synonym",
            "dis_sqlalchemy.orm.Synonym",
            "dis_sqlalchemy.orm.descriptor_props.SynonymProperty",
            "dis_sqlalchemy.orm.SynonymProperty",
        },
    ),
    "SynonymProperty": (
        SYNONYM_PROPERTY,
        {
            "dis_sqlalchemy.orm.descriptor_props.Synonym",
            "dis_sqlalchemy.orm.Synonym",
            "dis_sqlalchemy.orm.descriptor_props.SynonymProperty",
            "dis_sqlalchemy.orm.SynonymProperty",
        },
    ),
    "Composite": (
        COMPOSITE_PROPERTY,
        {
            "dis_sqlalchemy.orm.descriptor_props.Composite",
            "dis_sqlalchemy.orm.Composite",
            "dis_sqlalchemy.orm.descriptor_props.CompositeProperty",
            "dis_sqlalchemy.orm.CompositeProperty",
        },
    ),
    "CompositeProperty": (
        COMPOSITE_PROPERTY,
        {
            "dis_sqlalchemy.orm.descriptor_props.Composite",
            "dis_sqlalchemy.orm.Composite",
            "dis_sqlalchemy.orm.descriptor_props.CompositeProperty",
            "dis_sqlalchemy.orm.CompositeProperty",
        },
    ),
    "MapperProperty": (
        MAPPER_PROPERTY,
        {
            "dis_sqlalchemy.orm.interfaces.MapperProperty",
            "dis_sqlalchemy.orm.MapperProperty",
        },
    ),
    "TypeEngine": (TYPEENGINE, {"dis_sqlalchemy.sql.type_api.TypeEngine"}),
    "Mapped": (MAPPED, {NAMED_TYPE_SQLA_MAPPED}),
    "declarative_base": (
        DECLARATIVE_BASE,
        {
            "dis_sqlalchemy.ext.declarative.declarative_base",
            "dis_sqlalchemy.orm.declarative_base",
            "dis_sqlalchemy.orm.decl_api.declarative_base",
        },
    ),
    "DeclarativeMeta": (
        DECLARATIVE_META,
        {
            "dis_sqlalchemy.ext.declarative.DeclarativeMeta",
            "dis_sqlalchemy.orm.DeclarativeMeta",
            "dis_sqlalchemy.orm.decl_api.DeclarativeMeta",
        },
    ),
    "mapped": (
        MAPPED_DECORATOR,
        {
            "dis_sqlalchemy.orm.decl_api.registry.mapped",
            "dis_sqlalchemy.orm.registry.mapped",
        },
    ),
    "as_declarative": (
        AS_DECLARATIVE,
        {
            "dis_sqlalchemy.ext.declarative.as_declarative",
            "dis_sqlalchemy.orm.decl_api.as_declarative",
            "dis_sqlalchemy.orm.as_declarative",
        },
    ),
    "as_declarative_base": (
        AS_DECLARATIVE_BASE,
        {
            "dis_sqlalchemy.orm.decl_api.registry.as_declarative_base",
            "dis_sqlalchemy.orm.registry.as_declarative_base",
        },
    ),
    "declared_attr": (
        DECLARED_ATTR,
        {
            "dis_sqlalchemy.orm.decl_api.declared_attr",
            "dis_sqlalchemy.orm.declared_attr",
        },
    ),
    "declarative_mixin": (
        DECLARATIVE_MIXIN,
        {
            "dis_sqlalchemy.orm.decl_api.declarative_mixin",
            "dis_sqlalchemy.orm.declarative_mixin",
        },
    ),
    "query_expression": (
        QUERY_EXPRESSION,
        {
            "dis_sqlalchemy.orm.query_expression",
            "dis_sqlalchemy.orm._orm_constructors.query_expression",
        },
    ),
}


def has_base_type_id(info: TypeInfo, type_id: int) -> bool:
    for mr in info.mro:
        check_type_id, fullnames = _lookup.get(mr.name, (None, None))
        if check_type_id == type_id:
            break
    else:
        return False

    if fullnames is None:
        return False

    return mr.fullname in fullnames


def mro_has_id(mro: List[TypeInfo], type_id: int) -> bool:
    for mr in mro:
        check_type_id, fullnames = _lookup.get(mr.name, (None, None))
        if check_type_id == type_id:
            break
    else:
        return False

    if fullnames is None:
        return False

    return mr.fullname in fullnames


def type_id_for_unbound_type(
    type_: UnboundType, cls: ClassDef, api: SemanticAnalyzerPluginInterface
) -> Optional[int]:
    sym = api.lookup_qualified(type_.name, type_)
    if sym is not None:
        if isinstance(sym.node, TypeAlias):
            target_type = get_proper_type(sym.node.target)
            if isinstance(target_type, Instance):
                return type_id_for_named_node(target_type.type)
        elif isinstance(sym.node, TypeInfo):
            return type_id_for_named_node(sym.node)

    return None


def type_id_for_callee(callee: Expression) -> Optional[int]:
    if isinstance(callee, (MemberExpr, NameExpr)):
        if isinstance(callee.node, Decorator) and isinstance(
            callee.node.func, FuncDef
        ):
            if callee.node.func.type and isinstance(
                callee.node.func.type, CallableType
            ):
                ret_type = get_proper_type(callee.node.func.type.ret_type)

                if isinstance(ret_type, Instance):
                    return type_id_for_fullname(ret_type.type.fullname)

            return None

        elif isinstance(callee.node, OverloadedFuncDef):
            if (
                callee.node.impl
                and callee.node.impl.type
                and isinstance(callee.node.impl.type, CallableType)
            ):
                ret_type = get_proper_type(callee.node.impl.type.ret_type)

                if isinstance(ret_type, Instance):
                    return type_id_for_fullname(ret_type.type.fullname)

            return None
        elif isinstance(callee.node, FuncDef):
            if callee.node.type and isinstance(callee.node.type, CallableType):
                ret_type = get_proper_type(callee.node.type.ret_type)

                if isinstance(ret_type, Instance):
                    return type_id_for_fullname(ret_type.type.fullname)

            return None
        elif isinstance(callee.node, TypeAlias):
            target_type = get_proper_type(callee.node.target)
            if isinstance(target_type, Instance):
                return type_id_for_fullname(target_type.type.fullname)
        elif isinstance(callee.node, TypeInfo):
            return type_id_for_named_node(callee)
    return None


def type_id_for_named_node(
    node: Union[NameExpr, MemberExpr, SymbolNode]
) -> Optional[int]:
    type_id, fullnames = _lookup.get(node.name, (None, None))

    if type_id is None or fullnames is None:
        return None
    elif node.fullname in fullnames:
        return type_id
    else:
        return None


def type_id_for_fullname(fullname: str) -> Optional[int]:
    tokens = fullname.split(".")
    immediate = tokens[-1]

    type_id, fullnames = _lookup.get(immediate, (None, None))

    if type_id is None or fullnames is None:
        return None
    elif fullname in fullnames:
        return type_id
    else:
        return None


def expr_to_mapped_constructor(expr: Expression) -> CallExpr:
    column_descriptor = NameExpr("__sa_Mapped")
    column_descriptor.fullname = NAMED_TYPE_SQLA_MAPPED
    member_expr = MemberExpr(column_descriptor, "_empty_constructor")
    return CallExpr(
        member_expr,
        [expr],
        [ARG_POS],
        ["arg1"],
    )
