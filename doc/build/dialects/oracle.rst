.. _oracle_toplevel:

Oracle
======

.. automodule:: dis_sqlalchemy.dialects.oracle.base

Oracle Data Types
-----------------

As with all dis_sqlalchemy dialects, all UPPERCASE types that are known to be
valid with Oracle are importable from the top level dialect, whether
they originate from :mod:`dis_sqlalchemy.types` or from the local dialect::

    from dis_sqlalchemy.dialects.oracle import (
        BFILE,
        BLOB,
        CHAR,
        CLOB,
        DATE,
        DOUBLE_PRECISION,
        FLOAT,
        INTERVAL,
        LONG,
        NCLOB,
        NCHAR,
        NUMBER,
        NVARCHAR,
        NVARCHAR2,
        RAW,
        TIMESTAMP,
        VARCHAR,
        VARCHAR2,
    )

.. versionadded:: 1.2.19 Added :class:`_types.NCHAR` to the list of datatypes
   exported by the Oracle dialect.

Types which are specific to Oracle, or have Oracle-specific
construction arguments, are as follows:

.. currentmodule:: dis_sqlalchemy.dialects.oracle

.. autoclass:: BFILE
  :members: __init__

.. autoclass:: BINARY_DOUBLE
  :members: __init__

.. autoclass:: BINARY_FLOAT
  :members: __init__

.. autoclass:: DATE
   :members: __init__

.. autoclass:: FLOAT
   :members: __init__

.. autoclass:: INTERVAL
  :members: __init__

.. autoclass:: NCLOB
  :members: __init__

.. autoclass:: NVARCHAR2
   :members: __init__

.. autoclass:: NUMBER
   :members: __init__

.. autoclass:: LONG
  :members: __init__

.. autoclass:: RAW
  :members: __init__

.. autoclass:: ROWID
  :members: __init__

.. autoclass:: TIMESTAMP
  :members: __init__

.. _cx_oracle:

cx_Oracle
---------

.. automodule:: dis_sqlalchemy.dialects.oracle.cx_oracle

.. _oracledb:

python-oracledb
---------------

.. automodule:: dis_sqlalchemy.dialects.oracle.oracledb

