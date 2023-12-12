Visitor and Traversal Utilities
================================

The :mod:`dis_sqlalchemy.sql.visitors` module consists of classes and functions
that serve the purpose of generically **traversing** a Core SQL expression
structure.   This is not unlike the Python ``ast`` module in that is presents
a system by which a program can operate upon each component of a SQL
expression.   Common purposes this serves are locating various kinds of
elements such as :class:`_schema.Table` or :class:`.BindParameter` objects,
as well as altering the state of the structure such as replacing certain FROM
clauses with others.

.. note:: the :mod:`dis_sqlalchemy.sql.visitors` module is an internal API and
   is not fully public.    It is subject to change and may additionally not
   function as expected for use patterns that aren't considered within
   dis_sqlalchemy's own internals.

The :mod:`dis_sqlalchemy.sql.visitors` module is part of the **internals** of
dis_sqlalchemy and it is not usually used by calling application code.  It is
however used in certain edge cases such as when constructing caching routines
as well as when building out custom SQL expressions using the
:ref:`Custom SQL Constructs and Compilation Extension <dis_sqlalchemy.ext.compiler_toplevel>`.

.. automodule:: dis_sqlalchemy.sql.visitors
   :members:
   :private-members:

