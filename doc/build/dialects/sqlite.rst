.. _sqlite_toplevel:

SQLite
======

.. automodule:: dis_sqlalchemy.dialects.sqlite.base

SQLite Data Types
-----------------

As with all dis_sqlalchemy dialects, all UPPERCASE types that are known to be
valid with SQLite are importable from the top level dialect, whether
they originate from :mod:`dis_sqlalchemy.types` or from the local dialect::

    from dis_sqlalchemy.dialects.sqlite import (
        BLOB,
        BOOLEAN,
        CHAR,
        DATE,
        DATETIME,
        DECIMAL,
        FLOAT,
        INTEGER,
        NUMERIC,
        JSON,
        SMALLINT,
        TEXT,
        TIME,
        TIMESTAMP,
        VARCHAR,
    )

.. module:: dis_sqlalchemy.dialects.sqlite

.. autoclass:: DATETIME

.. autoclass:: DATE

.. autoclass:: JSON

.. autoclass:: TIME

SQLite DML Constructs
-------------------------

.. autofunction:: dis_sqlalchemy.dialects.sqlite.insert

.. autoclass:: dis_sqlalchemy.dialects.sqlite.Insert
  :members:

.. _pysqlite:

Pysqlite
--------

.. automodule:: dis_sqlalchemy.dialects.sqlite.pysqlite

.. _aiosqlite:

Aiosqlite
---------

.. automodule:: dis_sqlalchemy.dialects.sqlite.aiosqlite


.. _pysqlcipher:

Pysqlcipher
-----------

.. automodule:: dis_sqlalchemy.dialects.sqlite.pysqlcipher
