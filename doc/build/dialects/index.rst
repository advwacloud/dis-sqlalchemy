.. _dialect_toplevel:

Dialects
========

The **dialect** is the system dis_sqlalchemy uses to communicate with various types of :term:`DBAPI` implementations and databases.
The sections that follow contain reference documentation and notes specific to the usage of each backend, as well as notes
for the various DBAPIs.

All dialects require that an appropriate DBAPI driver is installed.

.. _included_dialects:

Included Dialects
-----------------

.. toctree::
    :maxdepth: 1
    :glob:

    postgresql
    mysql
    sqlite
    oracle
    mssql

Support Levels for Included Dialects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following table summarizes the support level for each included dialect.

.. dialect-table:: **Supported database versions for included dialects**
  :header-rows: 1

Support Definitions
^^^^^^^^^^^^^^^^^^^

.. glossary::

    Fully tested in CI
        **Fully tested in CI** indicates a version that is tested in the dis_sqlalchemy
        CI system and passes all the tests in the test suite.

    Normal support
        **Normal support** indicates that most features should work,
        but not all versions are tested in the ci configuration so there may
        be some not supported edge cases. We will try to fix issues that affect
        these versions.

    Best effort
        **Best effort** indicates that we try to support basic features on them,
        but most likely there will be unsupported features or errors in some use cases.
        Pull requests with associated issues may be accepted to continue supporting
        older versions, which are reviewed on a case-by-case basis.

.. _external_toplevel:

External Dialects
-----------------

Currently maintained external dialect projects for dis_sqlalchemy include:

+------------------------------------------------+---------------------------------------+
| Database                                       | Dialect                               |
+================================================+=======================================+
| Actian Avalanche, Vector, Actian X, and Ingres | dis_sqlalchemy-ingres_                    |
+------------------------------------------------+---------------------------------------+
| Amazon Athena                                  | pyathena_                             |
+------------------------------------------------+---------------------------------------+
| Amazon Redshift (via psycopg2)                 | dis_sqlalchemy-redshift_                  |
+------------------------------------------------+---------------------------------------+
| Apache Drill                                   | dis_sqlalchemy-drill_                     |
+------------------------------------------------+---------------------------------------+
| Apache Druid                                   | pydruid_                              |
+------------------------------------------------+---------------------------------------+
| Apache Hive and Presto                         | PyHive_                               |
+------------------------------------------------+---------------------------------------+
| Apache Solr                                    | dis_sqlalchemy-solr_                      |
+------------------------------------------------+---------------------------------------+
| CockroachDB                                    | dis_sqlalchemy-cockroachdb_               |
+------------------------------------------------+---------------------------------------+
| CrateDB                                        | crate-python_                         |
+------------------------------------------------+---------------------------------------+
| EXASolution                                    | dis_sqlalchemy_exasol_                    |
+------------------------------------------------+---------------------------------------+
| Elasticsearch (readonly)                       | elasticsearch-dbapi_                  |
+------------------------------------------------+---------------------------------------+
| Firebird                                       | dis_sqlalchemy-firebird_                  |
+------------------------------------------------+---------------------------------------+
| Firebolt                                       | firebolt-dis_sqlalchemy_                  |
+------------------------------------------------+---------------------------------------+
| Google BigQuery                                | pybigquery_                           |
+------------------------------------------------+---------------------------------------+
| Google Sheets                                  | gsheets_                              |
+------------------------------------------------+---------------------------------------+
| IBM DB2 and Informix                           | ibm-db-sa_                            |
+------------------------------------------------+---------------------------------------+
| IBM Netezza Performance Server [1]_            | nzalchemy_                            |
+------------------------------------------------+---------------------------------------+
| Microsoft Access (via pyodbc)                  | dis_sqlalchemy-access_                    |
+------------------------------------------------+---------------------------------------+
| Microsoft SQL Server (via python-tds)          | dis_sqlalchemy-tds_                       |
+------------------------------------------------+---------------------------------------+
| Microsoft SQL Server (via turbodbc)            | dis_sqlalchemy-turbodbc_                  |
+------------------------------------------------+---------------------------------------+
| MonetDB [1]_                                   | dis_sqlalchemy-monetdb_                   |
+------------------------------------------------+---------------------------------------+
| OpenGauss                                      | openGauss-dis_sqlalchemy_                 |
+------------------------------------------------+---------------------------------------+
| Rockset                                        | rockset-dis_sqlalchemy_                   |
+------------------------------------------------+---------------------------------------+
| SAP ASE (fork of former Sybase dialect)        | dis_sqlalchemy-sybase_                    |
+------------------------------------------------+---------------------------------------+
| SAP Hana [1]_                                  | dis_sqlalchemy-hana_                      |
+------------------------------------------------+---------------------------------------+
| SAP Sybase SQL Anywhere                        | dis_sqlalchemy-sqlany_                    |
+------------------------------------------------+---------------------------------------+
| Snowflake                                      | snowflake-dis_sqlalchemy_                 |
+------------------------------------------------+---------------------------------------+
| Teradata Vantage                               | teradatadis_sqlalchemy_                   |
+------------------------------------------------+---------------------------------------+

.. [1] Supports version 1.3.x only at the moment.

.. _openGauss-dis_sqlalchemy: https://gitee.com/opengauss/openGauss-dis_sqlalchemy
.. _rockset-dis_sqlalchemy: https://pypi.org/project/rockset-dis_sqlalchemy
.. _dis_sqlalchemy-ingres: https://github.com/clach04/ingres_sa_dialect
.. _nzalchemy: https://pypi.org/project/nzalchemy/
.. _ibm-db-sa: https://pypi.org/project/ibm-db-sa/
.. _PyHive: https://github.com/dropbox/PyHive#dis_sqlalchemy
.. _teradatadis_sqlalchemy: https://pypi.org/project/teradatadis_sqlalchemy/
.. _pybigquery: https://github.com/mxmzdlv/pybigquery/
.. _dis_sqlalchemy-redshift: https://pypi.org/project/dis_sqlalchemy-redshift
.. _dis_sqlalchemy-drill: https://github.com/JohnOmernik/dis_sqlalchemy-drill
.. _dis_sqlalchemy-hana: https://github.com/SAP/dis_sqlalchemy-hana
.. _dis_sqlalchemy-solr: https://github.com/aadel/dis_sqlalchemy-solr
.. _dis_sqlalchemy_exasol: https://github.com/blue-yonder/dis_sqlalchemy_exasol
.. _dis_sqlalchemy-sqlany: https://github.com/sqlanywhere/dis_sqlalchemy-sqlany
.. _dis_sqlalchemy-monetdb: https://github.com/gijzelaerr/dis_sqlalchemy-monetdb
.. _snowflake-dis_sqlalchemy: https://github.com/snowflakedb/snowflake-dis_sqlalchemy
.. _dis_sqlalchemy-tds: https://github.com/m32/dis_sqlalchemy-tds
.. _crate-python: https://github.com/crate/crate-python
.. _dis_sqlalchemy-access: https://pypi.org/project/dis_sqlalchemy-access/
.. _elasticsearch-dbapi: https://github.com/preset-io/elasticsearch-dbapi/
.. _pydruid: https://github.com/druid-io/pydruid
.. _gsheets: https://github.com/betodealmeida/gsheets-db-api
.. _dis_sqlalchemy-firebird: https://github.com/pauldex/dis_sqlalchemy-firebird
.. _dis_sqlalchemy-cockroachdb: https://github.com/cockroachdb/dis_sqlalchemy-cockroachdb
.. _dis_sqlalchemy-turbodbc: https://pypi.org/project/dis_sqlalchemy-turbodbc/
.. _dis_sqlalchemy-sybase: https://pypi.org/project/dis_sqlalchemy-sybase/
.. _firebolt-dis_sqlalchemy: https://pypi.org/project/firebolt-dis_sqlalchemy/
.. _pyathena: https://github.com/laughingman7743/PyAthena/
