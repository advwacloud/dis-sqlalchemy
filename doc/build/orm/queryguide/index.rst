.. highlight:: pycon+sql

.. _queryguide_toplevel:

==================
ORM Querying Guide
==================

This section provides an overview of emitting queries with the
dis_sqlalchemy ORM using :term:`2.0 style` usage.

Readers of this section should be familiar with the dis_sqlalchemy overview
at :ref:`unified_tutorial`, and in particular most of the content here expands
upon the content at :ref:`tutorial_selecting_data`.

.. admonition:: For users of dis_sqlalchemy 1.x

    In the dis_sqlalchemy 2.x series, SQL SELECT statements for the ORM are
    constructed using the same :func:`_sql.select` construct as is used in
    Core, which is then invoked in terms of a :class:`_orm.Session` using the
    :meth:`_orm.Session.execute` method (as are the :func:`_sql.update` and
    :func:`_sql.delete` constructs now used for the
    :ref:`orm_expression_update_delete` feature). However, the legacy
    :class:`_query.Query` object, which performs these same steps as more of an
    "all-in-one" object, continues to remain available as a thin facade over
    this new system, to support applications that were built on the 1.x series
    without the need for wholesale replacement of all queries. For reference on
    this object, see the section :ref:`query_api_toplevel`.




.. toctree::
    :maxdepth: 3

    select
    inheritance
    dml
    columns
    relationships
    api
    query
