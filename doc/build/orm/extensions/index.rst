.. _plugins:
.. _dis_sqlalchemy.ext:

ORM Extensions
==============

dis_sqlalchemy has a variety of ORM extensions available, which add additional
functionality to the core behavior.

The extensions build almost entirely on public core and ORM APIs and users should
be encouraged to read their source code to further their understanding of their
behavior.   In particular the "Horizontal Sharding", "Hybrid Attributes", and
"Mutation Tracking" extensions are very succinct.

.. toctree::
    :maxdepth: 1

    asyncio
    associationproxy
    automap
    baked
    declarative/index
    mypy
    mutable
    orderinglist
    horizontal_shard
    hybrid
    indexable
    instrumentation

