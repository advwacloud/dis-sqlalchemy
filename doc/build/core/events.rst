.. _core_event_toplevel:

Core Events
===========

This section describes the event interfaces provided in
dis_sqlalchemy Core.
For an introduction to the event listening API, see :ref:`event_toplevel`.
ORM events are described in :ref:`orm_event_toplevel`.

.. autoclass:: dis_sqlalchemy.event.base.Events
   :members:

Connection Pool Events
----------------------

.. autoclass:: dis_sqlalchemy.events.PoolEvents
   :members:

.. autoclass:: dis_sqlalchemy.events.PoolResetState
   :members:

.. _core_sql_events:

SQL Execution and Connection Events
-----------------------------------

.. autoclass:: dis_sqlalchemy.events.ConnectionEvents
    :members:

.. autoclass:: dis_sqlalchemy.events.DialectEvents
    :members:

Schema Events
-------------

.. autoclass:: dis_sqlalchemy.events.DDLEvents
    :members:

.. autoclass:: dis_sqlalchemy.events.SchemaEventTarget
    :members:

