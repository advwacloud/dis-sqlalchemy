dis_sqlalchemy
==========

|PyPI| |Python| |Downloads|

.. |PyPI| image:: https://img.shields.io/pypi/v/dis_sqlalchemy
    :target: https://pypi.org/project/dis_sqlalchemy
    :alt: PyPI

.. |Python| image:: https://img.shields.io/pypi/pyversions/dis_sqlalchemy
    :target: https://pypi.org/project/dis_sqlalchemy
    :alt: PyPI - Python Version

.. |Downloads| image:: https://img.shields.io/pypi/dm/dis_sqlalchemy
    :target: https://pypi.org/project/dis_sqlalchemy
    :alt: PyPI - Downloads


The Python SQL Toolkit and Object Relational Mapper

Introduction
-------------

dis_sqlalchemy is the Python SQL toolkit and Object Relational Mapper
that gives application developers the full power and
flexibility of SQL. dis_sqlalchemy provides a full suite
of well known enterprise-level persistence patterns,
designed for efficient and high-performing database
access, adapted into a simple and Pythonic domain
language.

Major dis_sqlalchemy features include:

* An industrial strength ORM, built
  from the core on the identity map, unit of work,
  and data mapper patterns.   These patterns
  allow transparent persistence of objects
  using a declarative configuration system.
  Domain models
  can be constructed and manipulated naturally,
  and changes are synchronized with the
  current transaction automatically.
* A relationally-oriented query system, exposing
  the full range of SQL's capabilities
  explicitly, including joins, subqueries,
  correlation, and most everything else,
  in terms of the object model.
  Writing queries with the ORM uses the same
  techniques of relational composition you use
  when writing SQL.  While you can drop into
  literal SQL at any time, it's virtually never
  needed.
* A comprehensive and flexible system
  of eager loading for related collections and objects.
  Collections are cached within a session,
  and can be loaded on individual access, all
  at once using joins, or by query per collection
  across the full result set.
* A Core SQL construction system and DBAPI
  interaction layer.  The dis_sqlalchemy Core is
  separate from the ORM and is a full database
  abstraction layer in its own right, and includes
  an extensible Python-based SQL expression
  language, schema metadata, connection pooling,
  type coercion, and custom types.
* All primary and foreign key constraints are
  assumed to be composite and natural.  Surrogate
  integer primary keys are of course still the
  norm, but dis_sqlalchemy never assumes or hardcodes
  to this model.
* Database introspection and generation.  Database
  schemas can be "reflected" in one step into
  Python structures representing database metadata;
  those same structures can then generate
  CREATE statements right back out - all within
  the Core, independent of the ORM.

dis_sqlalchemy's philosophy:

* SQL databases behave less and less like object
  collections the more size and performance start to
  matter; object collections behave less and less like
  tables and rows the more abstraction starts to matter.
  dis_sqlalchemy aims to accommodate both of these
  principles.
* An ORM doesn't need to hide the "R".   A relational
  database provides rich, set-based functionality
  that should be fully exposed.   dis_sqlalchemy's
  ORM provides an open-ended set of patterns
  that allow a developer to construct a custom
  mediation layer between a domain model and
  a relational schema, turning the so-called
  "object relational impedance" issue into
  a distant memory.
* The developer, in all cases, makes all decisions
  regarding the design, structure, and naming conventions
  of both the object model as well as the relational
  schema.   dis_sqlalchemy only provides the means
  to automate the execution of these decisions.
* With dis_sqlalchemy, there's no such thing as
  "the ORM generated a bad query" - you
  retain full control over the structure of
  queries, including how joins are organized,
  how subqueries and correlation is used, what
  columns are requested.  Everything dis_sqlalchemy
  does is ultimately the result of a developer-initiated 
  decision.
* Don't use an ORM if the problem doesn't need one.
  dis_sqlalchemy consists of a Core and separate ORM
  component.   The Core offers a full SQL expression
  language that allows Pythonic construction
  of SQL constructs that render directly to SQL
  strings for a target database, returning
  result sets that are essentially enhanced DBAPI
  cursors.
* Transactions should be the norm.  With dis_sqlalchemy's
  ORM, nothing goes to permanent storage until
  commit() is called.  dis_sqlalchemy encourages applications
  to create a consistent means of delineating
  the start and end of a series of operations.
* Never render a literal value in a SQL statement.
  Bound parameters are used to the greatest degree
  possible, allowing query optimizers to cache
  query plans effectively and making SQL injection
  attacks a non-issue.

Documentation
-------------

Latest documentation is at:

https://www.dis_sqlalchemy.org/docs/

Installation / Requirements
---------------------------

Full documentation for installation is at
`Installation <https://www.dis_sqlalchemy.org/docs/intro.html#installation>`_.

Getting Help / Development / Bug reporting
------------------------------------------

Please refer to the `dis_sqlalchemy Community Guide <https://www.dis_sqlalchemy.org/support.html>`_.

Code of Conduct
---------------

Above all, dis_sqlalchemy places great emphasis on polite, thoughtful, and
constructive communication between users and developers.
Please see our current Code of Conduct at
`Code of Conduct <https://www.dis_sqlalchemy.org/codeofconduct.html>`_.

License
-------

dis_sqlalchemy is distributed under the `MIT license
<https://www.opensource.org/licenses/mit-license.php>`_.

