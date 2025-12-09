"""SQLite schema definitions for Branch storage.

The schema is intentionally minimal: it persists documents, reading sessions,
and idea fragments while keeping user-facing reading flow unchanged.
"""

from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    import sqlite3
    from collections.abc import Iterable, Sequence


SCHEMA_VERSION = 1

# Table DDL statements. Keep small and composable for migrations later.
CREATE_TABLE_STATEMENTS: Sequence[str] = (
    """
    CREATE TABLE IF NOT EXISTS documents (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        file_path TEXT,
        url TEXT,
        document_type TEXT NOT NULL DEFAULT 'pdf'
            CHECK (document_type IN ('pdf', 'text', 'markdown', 'html')),
        page_count INTEGER CHECK (page_count IS NULL OR page_count >= 0),
        author TEXT,
        added_at TEXT NOT NULL DEFAULT (CURRENT_TIMESTAMP),
        last_opened_at TEXT,
        last_page INTEGER NOT NULL DEFAULT 1 CHECK (last_page >= 1),
        read_percentage REAL NOT NULL DEFAULT 0.0
            CHECK (
                read_percentage >= 0.0 AND read_percentage <= 100.0
            )
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS sessions (
        id TEXT PRIMARY KEY,
        document_id TEXT NOT NULL
            REFERENCES documents(id) ON DELETE CASCADE ON UPDATE CASCADE,
        started_at TEXT NOT NULL DEFAULT (CURRENT_TIMESTAMP),
        ended_at TEXT,
        start_page INTEGER NOT NULL DEFAULT 1 CHECK (start_page >= 1),
        end_page INTEGER CHECK (end_page IS NULL OR end_page >= 1),
        fragments_captured INTEGER NOT NULL DEFAULT 0 CHECK (fragments_captured >= 0),
        dive_deeps INTEGER NOT NULL DEFAULT 0 CHECK (dive_deeps >= 0),
        notes TEXT
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS idea_fragments (
        id TEXT PRIMARY KEY,
        content TEXT NOT NULL,
        anchor_page_number INTEGER,
        anchor_start_position INTEGER,
        anchor_end_position INTEGER,
        anchor_selected_text TEXT,
        document_id TEXT
            REFERENCES documents(id) ON DELETE SET NULL ON UPDATE CASCADE,
        session_id TEXT
            REFERENCES sessions(id) ON DELETE SET NULL ON UPDATE CASCADE,
        captured_at TEXT NOT NULL DEFAULT (CURRENT_TIMESTAMP),
        updated_at TEXT,
        status TEXT NOT NULL DEFAULT 'captured'
            CHECK (
                status IN (
                    'captured', 'reviewed', 'developed', 'archived', 'discarded'
                )
            ),
        capture_type TEXT NOT NULL DEFAULT 'text',
        resolution_note TEXT
    );
    """,
)

CREATE_INDEX_STATEMENTS: Sequence[str] = (
    "CREATE INDEX IF NOT EXISTS idx_sessions_document_id ON sessions(document_id);",
    "CREATE INDEX IF NOT EXISTS "
    "idx_fragments_document_id ON idea_fragments(document_id);",
    "CREATE INDEX IF NOT EXISTS "
    "idx_fragments_session_id ON idea_fragments(session_id);",
    "CREATE INDEX IF NOT EXISTS idx_fragments_status ON idea_fragments(status);",
)


def apply_schema(connection: sqlite3.Connection) -> None:
    """Create all tables and indexes for the current schema version.

    PRAGMAs are set to enforce foreign keys, and `user_version` is recorded
    to support future migrations.
    """
    connection.execute("PRAGMA foreign_keys = ON;")

    for statement in CREATE_TABLE_STATEMENTS:
        connection.execute(statement)

    for statement in CREATE_INDEX_STATEMENTS:
        connection.execute(statement)

    connection.execute(f"PRAGMA user_version = {SCHEMA_VERSION};")
    connection.commit()


def current_schema_objects() -> dict[str, Iterable[str] | tuple[int, ...]]:
    """Provide a simple view of the schema objects for debugging and documentation.

    Returns a mapping containing the DDL for tables and indexes.
    """
    return {
        "tables": CREATE_TABLE_STATEMENTS,
        "indexes": CREATE_INDEX_STATEMENTS,
        "version": (SCHEMA_VERSION,),
    }
