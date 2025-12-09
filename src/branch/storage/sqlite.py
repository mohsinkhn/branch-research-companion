"""SQLite helpers for Branch storage.

Connections created here enable foreign key enforcement and expose a helper
to apply the current schema.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

from branch.storage.schema import apply_schema


SQLitePath = str | Path


def connect(database: SQLitePath = ":memory:") -> sqlite3.Connection:
    """Create a SQLite connection with sane defaults for Branch.

    - Enables foreign key enforcement
    - Uses row factory for dict-style access
    """
    connection = sqlite3.connect(str(database))
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON;")
    return connection


def initialize(database: SQLitePath = ":memory:") -> sqlite3.Connection:
    """Connect to SQLite and ensure the Branch schema exists.

    Returns the open connection for immediate use.
    """
    connection = connect(database)
    apply_schema(connection)
    return connection
