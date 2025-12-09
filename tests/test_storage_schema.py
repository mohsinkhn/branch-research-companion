"""Tests for SQLite schema and initialization."""

from __future__ import annotations

import sqlite3
from uuid import uuid4

import pytest

from branch.storage import SCHEMA_VERSION, apply_schema, initialize


def _table_names(connection: sqlite3.Connection) -> set[str]:
    rows = connection.execute(
        "SELECT name FROM sqlite_master "
        "WHERE type='table' AND name NOT LIKE 'sqlite_%';"
    )
    return {row[0] for row in rows.fetchall()}


def test_apply_schema_creates_expected_tables():
    """Schema creation should create core tables and record version."""
    connection = sqlite3.connect(":memory:")
    apply_schema(connection)

    names = _table_names(connection)
    assert {"documents", "sessions", "idea_fragments"}.issubset(names)

    version = connection.execute("PRAGMA user_version;").fetchone()[0]
    assert version == SCHEMA_VERSION

    foreign_keys = connection.execute("PRAGMA foreign_keys;").fetchone()[0]
    assert foreign_keys == 1


def test_foreign_keys_and_cascades():
    """Schema enforces relationships and keeps fragments on parent removal."""
    connection = initialize(":memory:")

    document_id = str(uuid4())
    session_id = str(uuid4())
    fragment_id = str(uuid4())

    connection.execute(
        "INSERT INTO documents (id, title, document_type) VALUES (?, ?, ?);",
        (document_id, "Paper", "pdf"),
    )

    connection.execute(
        "INSERT INTO sessions (id, document_id, start_page) VALUES (?, ?, ?);",
        (session_id, document_id, 1),
    )

    connection.execute(
        """
        INSERT INTO idea_fragments (
            id, content, document_id, session_id, status, capture_type
        ) VALUES (?, ?, ?, ?, ?, ?);
        """,
        (fragment_id, "A quick idea", document_id, session_id, "captured", "text"),
    )
    connection.commit()

    # Cannot insert a session for a missing document
    with pytest.raises(sqlite3.IntegrityError):
        connection.execute(
            "INSERT INTO sessions (id, document_id, start_page) VALUES (?, ?, ?);",
            (str(uuid4()), str(uuid4()), 1),
        )

    # Deleting the document cascades to sessions,
    # fragments keep content but drop anchors
    connection.execute("DELETE FROM documents WHERE id = ?;", (document_id,))
    connection.commit()

    fragment_row = connection.execute(
        "SELECT document_id, session_id FROM idea_fragments WHERE id = ?;",
        (fragment_id,),
    ).fetchone()

    assert fragment_row["document_id"] is None
    assert fragment_row["session_id"] is None
