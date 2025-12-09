# Code Architecture - Auto-Generated

> **Generated:** 2025-12-09 19:25:48
> **Generator:** `scripts/generate_arch_docs.py`

This document is automatically generated. Do not edit manually.
For the human-maintained architecture guide, see [ARCHITECTURE.md](ARCHITECTURE.md).

---

## File Tree

```
├── buffer/
│   └── __init__.py
├── capture/
│   └── __init__.py
├── models/
│   ├── __init__.py
│   ├── document.py
│   ├── idea_fragment.py
│   └── session.py
├── reader/
│   └── __init__.py
├── storage/
│   ├── __init__.py
│   ├── repository.py
│   ├── schema.py
│   └── sqlite.py
├── __init__.py
└── cli.py
```

---

## Module Inventory

| File | Lines | Classes | Functions | Description |
|------|-------|---------|-----------|-------------|
| `src/branch/__init__.py` | 20 | - | - | Branch - Reading-First Research Companion. |
| `src/branch/buffer/__init__.py` | 1 | - | - | Branch Buffer module - post-reading review system. |
| `src/branch/capture/__init__.py` | 1 | - | - | Idea capture module for Branch. |
| `src/branch/cli.py` | 13 | - | main | Command-line interface for Branch. |
| `src/branch/models/__init__.py` | 13 | - | - | Data models for Branch. |
| `src/branch/models/document.py` | 84 | DocumentType, Document, Config | - | Document model for Branch. |
| `src/branch/models/idea_fragment.py` | 103 | FragmentStatus, TextAnchor, IdeaFragment, Config | - | IdeaFragment model - the core concept of Branch. |
| `src/branch/models/session.py` | 75 | BranchSession, Config | - | BranchSession model. |
| `src/branch/reader/__init__.py` | 1 | - | - | Document reader module for Branch. |
| `src/branch/storage/__init__.py` | 16 | - | - | Storage and persistence module for Branch. |
| `src/branch/storage/repository.py` | 45 | StorageError, BranchRepository | - | Repository interfaces for Branch storage. |
| `src/branch/storage/schema.py` | 128 | - | apply_schema, current_schema_objects | SQLite schema definitions for Branch storage. |
| `src/branch/storage/sqlite.py` | 37 | - | connect, initialize | SQLite helpers for Branch storage. |

---

## Class Hierarchy

### `src/branch/models/document.py`

**DocumentType** (line 16)
> Supported document types.

**Document** (line 25)
> A document that can be read in Branch.
- Methods: `update_progress`, `from_file`

**Config** (line 52)
> Pydantic configuration.

### `src/branch/models/idea_fragment.py`

**FragmentStatus** (line 19)
> Status of an idea fragment in the Branch Buffer.

**TextAnchor** (line 29)
> Anchor point within a document for an idea fragment.

**IdeaFragment** (line 38)
> A spontaneous idea captured during reading.
- Methods: `resolve_lightly`, `mark_reviewed`, `develop`, `archive`, `discard`

**Config** (line 72)
> Pydantic configuration.

### `src/branch/models/session.py`

**BranchSession** (line 15)
> A reading session in Branch.
- Methods: `end_session`, `record_capture`, `record_dive_deep`, `duration_minutes`, `is_active`

**Config** (line 42)
> Pydantic configuration.

### `src/branch/storage/repository.py`

**StorageError** (line 19)
> Base exception for storage-related failures.

**BranchRepository** (line 23)
> Abstract interface for Branch storage backends.
- Methods: `upsert_document`, `get_document`, `upsert_session`, `get_session`, `upsert_fragment`, `get_fragment`, `list_fragments_for_document`


---

## Internal Dependencies

```
src.branch
  └── branch.models.document
  └── branch.models.idea_fragment
  └── branch.models.session
src.branch.models
  └── branch.models.document
  └── branch.models.idea_fragment
  └── branch.models.session
src.branch.storage
  └── branch.storage.repository
  └── branch.storage.schema
  └── branch.storage.sqlite
src.branch.storage.repository
  └── branch.models
src.branch.storage.sqlite
  └── branch.storage.schema
```

---

## Metrics Summary

Run `uv run radon cc src/branch -a` for complexity metrics.
Run `uv run radon mi src/branch` for maintainability index.

---

*This file is auto-generated. Run `uv run python scripts/generate_arch_docs.py` to update.*
