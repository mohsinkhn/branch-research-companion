# Human Oversight & Code Review Guide

This document provides tools and processes for maintaining human oversight over the codebase, especially important when AI agents are making changes.

## 🎯 Purpose

> **Humans must always be able to understand the impact of any change on the overall codebase.**

This guide ensures:
1. Clear visibility into code structure
2. Understanding of module dependencies
3. Impact analysis for changes
4. Audit trail of all modifications

---

## 📊 Architecture Overview

### High-Level Module Structure

```
┌─────────────────────────────────────────────────────────────────────┐
│                          CLI / Entry Points                          │
│                            (branch.cli)                              │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                           Branch Buffer                              │
│                         (branch.buffer)                              │
│                                                                      │
│  • Manages idea queue                                                │
│  • Review workflow                                                   │
│  • Session management                                                │
└─────────────────────────────────────────────────────────────────────┘
                    │                               │
                    ▼                               ▼
┌───────────────────────────────┐   ┌───────────────────────────────┐
│         Capture               │   │          Reader               │
│     (branch.capture)          │   │       (branch.reader)         │
│                               │   │                               │
│  • Text input                 │   │  • PDF parsing                │
│  • Voice input                │   │  • Text extraction            │
│  • Context anchoring          │   │  • Position mapping           │
└───────────────────────────────┘   └───────────────────────────────┘
                    │                               │
                    └───────────────┬───────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                            Models                                    │
│                        (branch.models)                               │
│                                                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                 │
│  │IdeaFragment │  │  Document   │  │BranchSession│                 │
│  └─────────────┘  └─────────────┘  └─────────────┘                 │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                           Storage                                    │
│                        (branch.storage)                              │
│                                                                      │
│  • SQLite persistence                                                │
│  • Repository pattern                                                │
│  • Migrations                                                        │
└─────────────────────────────────────────────────────────────────────┘
```

### Module Dependency Matrix

| Module | Depends On | Depended By |
|--------|------------|-------------|
| `models` | (none - base layer) | capture, reader, buffer, storage |
| `storage` | models | buffer |
| `reader` | models | buffer |
| `capture` | models | buffer |
| `buffer` | models, storage, capture, reader | cli |
| `cli` | buffer | (entry point) |

---

## 📁 File-Level Structure

### Current File Inventory

```
src/branch/
├── __init__.py              [EXPORTS: IdeaFragment, Document, BranchSession]
├── cli.py                   [ENTRY: main()]
│
├── models/                  [DATA LAYER - No external deps]
│   ├── __init__.py          [EXPORTS: All models]
│   ├── idea_fragment.py     [CLASS: IdeaFragment, FragmentStatus, TextAnchor]
│   ├── document.py          [CLASS: Document, DocumentType]
│   └── session.py           [CLASS: BranchSession]
│
├── reader/                  [DOCUMENT PARSING]
│   └── __init__.py          [PLACEHOLDER]
│
├── capture/                 [INPUT HANDLING]
│   └── __init__.py          [PLACEHOLDER]
│
├── buffer/                  [IDEA MANAGEMENT]
│   └── __init__.py          [PLACEHOLDER]
│
└── storage/                 [PERSISTENCE]
    └── __init__.py          [PLACEHOLDER]
```

### File Responsibilities

Each file should have a single, clear responsibility:

| File | Responsibility | Key Classes/Functions |
|------|----------------|----------------------|
| `models/idea_fragment.py` | Idea data structure | `IdeaFragment`, `FragmentStatus`, `TextAnchor` |
| `models/document.py` | Document metadata | `Document`, `DocumentType` |
| `models/session.py` | Reading session tracking | `BranchSession` |

---

## 🔧 Automated Tools for Code Visibility

### 1. Generate Dependency Graph

```bash
# Install pydeps
uv add --dev pydeps

# Generate visual dependency graph
uv run pydeps src/branch --cluster --max-bacon=2 -o docs/architecture/deps.svg

# Generate text-based dependency list
uv run pydeps src/branch --show-deps --no-show
```

### 2. Generate Code Documentation

```bash
# Install pdoc
uv add --dev pdoc

# Generate HTML documentation
uv run pdoc src/branch -o docs/api/

# Serve documentation locally
uv run pdoc src/branch --http localhost:8080
```

### 3. Generate UML Diagrams

```bash
# Install pyreverse (part of pylint)
uv add --dev pylint

# Generate class diagrams
uv run pyreverse -o png -p branch src/branch
mv classes_branch.png docs/architecture/
mv packages_branch.png docs/architecture/
```

### 4. Code Statistics

```bash
# Install radon for code metrics
uv add --dev radon

# Cyclomatic complexity
uv run radon cc src/branch -a -s

# Maintainability index
uv run radon mi src/branch -s

# Raw metrics (LOC, comments, etc.)
uv run radon raw src/branch -s
```

---

## 📋 Change Impact Analysis

Before approving any PR, reviewers should check:

### 1. What files changed?
```bash
git diff --stat main
```

### 2. What modules are affected?
```bash
# List changed modules
git diff --name-only main | grep "^src/branch" | cut -d'/' -f3 | sort -u
```

### 3. What depends on changed files?
```bash
# Find reverse dependencies
uv run pydeps src/branch --reverse --only <changed_module>
```

### 4. Test coverage of changed code
```bash
# Run tests with coverage for changed files only
uv run pytest --cov=src/branch --cov-report=term-missing
```

---

## 🔍 Code Review Checklist

### For Human Reviewers

Before approving any change (especially from AI agents):

#### Architecture Impact
- [ ] Does this change respect the dependency hierarchy?
- [ ] Are new dependencies justified and documented?
- [ ] Does it follow the single-responsibility principle?

#### Code Quality
- [ ] Are all functions/classes documented?
- [ ] Are type hints complete and correct?
- [ ] Is the code readable without excessive comments?

#### Testing
- [ ] Are there tests for new functionality?
- [ ] Do existing tests still pass?
- [ ] Is edge case handling tested?

#### Design Principles
- [ ] Does this preserve reading flow? (North-Star Rule)
- [ ] Does it avoid adding organization during capture?
- [ ] Is the user's curiosity respected?

#### Documentation
- [ ] Is ARCHITECTURE.md updated if structure changed?
- [ ] Are dev-logs updated with rationale?
- [ ] Is README updated for new features?

---

## 📊 Periodic Architecture Review

### Weekly Tasks
1. Regenerate dependency graphs
2. Check for circular dependencies
3. Review code complexity metrics
4. Update file inventory if changed

### Monthly Tasks
1. Full architecture review
2. Dependency audit (are all deps needed?)
3. Code coverage review
4. Documentation freshness check

### Commands for Architecture Health

```bash
# Check for circular imports
uv run pydeps src/branch --show-cycles

# Find most complex functions (potential refactor candidates)
uv run radon cc src/branch -a -nc

# Check import health
uv run ruff check src --select=I --statistics
```

---

## 🚨 Red Flags for Reviewers

Watch out for these patterns:

1. **Circular dependencies** - Modules importing each other
2. **God classes** - Classes with too many responsibilities
3. **Deep nesting** - Functions with >3 levels of indentation
4. **Missing tests** - New code without corresponding tests
5. **Undocumented public APIs** - Public functions without docstrings
6. **Magic numbers** - Hardcoded values without explanation
7. **Broad exceptions** - `except Exception:` without re-raising
8. **Cross-layer dependencies** - e.g., CLI directly accessing storage

---

## 📝 Documentation Requirements

### Every Module Must Have

1. **Module docstring** - What this module does
2. **Public API documentation** - All public classes/functions documented
3. **Type hints** - All parameters and returns typed

### Every Change Must Have

1. **Commit message** - Following conventional commits
2. **Dev log entry** - If significant change
3. **Architecture update** - If structure changes

---

## 🔄 Keeping This Document Updated

This document should be updated when:

1. New modules are added
2. Module dependencies change
3. New tools are adopted
4. Review processes change

**Last Updated:** December 9, 2025
**Updated By:** copilot
