# Code Architecture - Auto-Generated

> **Generated:** 2025-12-09 18:24:15
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
│   └── __init__.py
├── __init__.py
└── cli.py
```

---

## Module Inventory

| File | Lines | Classes | Functions | Description |
|------|-------|---------|-----------|-------------|
| `src/branch/__init__.py` | 20 | - | - | Branch - Reading-First Research Companion |
| `src/branch/buffer/__init__.py` | 1 | - | - | Branch Buffer module - post-reading review system. |
| `src/branch/capture/__init__.py` | 1 | - | - | Idea capture module for Branch. |
| `src/branch/cli.py` | 13 | - | main | Command-line interface for Branch. |
| `src/branch/models/__init__.py` | 12 | - | - | Data models for Branch. |
| `src/branch/models/document.py` | 85 | DocumentType, Document, Config | - | Document model for Branch. |
| `src/branch/models/idea_fragment.py` | 104 | FragmentStatus, TextAnchor, IdeaFragment, Config | - | IdeaFragment model - the core concept of Branch. |
| `src/branch/models/session.py` | 76 | BranchSession, Config | - | BranchSession model. |
| `src/branch/reader/__init__.py` | 1 | - | - | Document reader module for Branch. |
| `src/branch/storage/__init__.py` | 1 | - | - | Storage and persistence module for Branch. |

---

## Class Hierarchy

### `src/branch/models/document.py`

**DocumentType** (line 16)
> Supported document types.

**Document** (line 25)
> A document that can be read in Branch.
- Methods: `update_progress`, `from_file`

**Config** (line 53)
> Pydantic configuration.

### `src/branch/models/idea_fragment.py`

**FragmentStatus** (line 19)
> Status of an idea fragment in the Branch Buffer.

**TextAnchor** (line 29)
> Anchor point within a document for an idea fragment.

**IdeaFragment** (line 38)
> A spontaneous idea captured during reading.
- Methods: `resolve_lightly`, `mark_reviewed`, `develop`, `archive`, `discard`

**Config** (line 73)
> Pydantic configuration.

### `src/branch/models/session.py`

**BranchSession** (line 15)
> A reading session in Branch.
- Methods: `end_session`, `record_capture`, `record_dive_deep`, `duration_minutes`, `is_active`

**Config** (line 43)
> Pydantic configuration.


---

## Internal Dependencies

```
src.branch
  └── branch.models.idea_fragment
  └── branch.models.document
  └── branch.models.session
src.branch.models
  └── branch.models.idea_fragment
  └── branch.models.document
  └── branch.models.session
```

---

## Metrics Summary

Run `uv run radon cc src/branch -a` for complexity metrics.
Run `uv run radon mi src/branch` for maintainability index.

---

*This file is auto-generated. Run `uv run python scripts/generate_arch_docs.py` to update.*
