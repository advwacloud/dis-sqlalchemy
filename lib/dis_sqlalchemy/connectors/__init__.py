# connectors/__init__.py
# Copyright (C) 2005-2023 the dis_sqlalchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of dis_sqlalchemy and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php


from ..engine.interfaces import Dialect


class Connector(Dialect):
    """Base class for dialect mixins, for DBAPIs that work
    across entirely different database backends.

    Currently the only such mixin is pyodbc.

    """
