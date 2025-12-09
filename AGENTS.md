# AI Agent Development Guidelines

This document provides strict guidelines for AI agents (GitHub Copilot, Codex, etc.) working on the Branch Research Companion project.

## 🎯 Prime Directive

> **If a feature harms reading flow or suppresses idea emergence, it must be rejected.**

Before implementing ANY feature, ask: "Does this preserve the user's reading flow?"

---

## ⚡ QUICK REFERENCE - USE THESE COMMANDS

> **🚨 STOP! Before running ANY Python/test/lint command, use the Makefile!**
> **🚨 ALWAYS use `uv` - NEVER use raw `pip` or `python` commands!**
> **🚨 NEVER commit directly to main - ALWAYS create a branch and PR!**

### Essential Make Commands (USE THESE!)

```bash
# SETUP (run first time)
make dev              # Setup complete dev environment with uv

# GIT WORKFLOW (REQUIRED for all work!)
make branch NAME=copilot/feat/my-feature  # Create feature branch
make commit MSG="feat(module): description"  # Commit changes
make pr TITLE="feat: description" BODY="..."  # Create pull request
make sync             # Sync branch with main

# BEFORE EVERY COMMIT (required!)
make check            # Run format + lint + type-check
make test             # Run all tests
make all              # Run everything (check + test)

# INDIVIDUAL COMMANDS
make format           # Format code with ruff
make lint             # Lint code with ruff (auto-fix)
make type-check       # Type check with mypy
make test-cov         # Run tests with coverage report

# ARCHITECTURE (after making changes)
make arch             # Regenerate architecture docs

# UTILITIES
make log              # Create today's log folder
make clean            # Remove build artifacts
make help             # Show all available commands
```

### ❌ NEVER DO THIS:
```bash
# WRONG - Don't commit to main directly!
git checkout main
git commit -m "..."   # NO! Create a branch first!

# WRONG - Don't use pip directly
pip install something
python -m pytest

# WRONG - Don't run tools without uv
ruff check src
pytest
mypy src
```

### ✅ ALWAYS DO THIS:
```bash
# CORRECT - Use make commands
make test
make check

# CORRECT - If you must run directly, use uv
uv run pytest
uv run ruff check src tests
uv add some-package        # To add dependencies
```

---

## 🔌 MCP (Model Context Protocol) Usage

**Prefer MCP tools when available!** They provide better integration and context.

### Available MCPs to Use
- **File operations**: Use MCP file tools instead of shell commands when possible
- **Git operations**: Use MCP git tools for status, diff, commit info
- **Search**: Use MCP search/grep tools for codebase exploration
- **Terminal**: Use MCP terminal for running make commands

### When to Use MCPs vs Terminal
| Task | Use MCP | Use Terminal (make) |
|------|---------|-------------------|
| Read file | ✅ MCP read_file | |
| Search code | ✅ MCP grep/search | |
| Edit file | ✅ MCP edit tools | |
| Run tests | | ✅ `make test` |
| Lint/format | | ✅ `make check` |
| Git commit | ✅ MCP or terminal | |
| Install deps | | ✅ `uv add <pkg>` |

---

## 👁️ Human Oversight Requirements

**All AI agent work is subject to human review.** These requirements ensure humans can always understand and verify changes.

### Before Making Changes
1. **MUST** read `docs/ARCHITECTURE.md` to understand current structure
2. **MUST** check `docs/architecture/CODE_STRUCTURE.md` for file inventory
3. **MUST** understand which modules will be affected by changes

### After Making Changes
1. **MUST** run `make arch` to regenerate architecture docs
2. **MUST** list all files changed in the dev-log entry
3. **MUST** explain impact on dependent modules
4. **MUST** update `docs/ARCHITECTURE.md` if adding new modules

### Change Documentation
Every change must include:
- **What** files were modified
- **Why** the change was made
- **Impact** on other modules
- **Tests** that verify the change

### Human Review Points
AI agents should explicitly flag for human review:
- Any new dependencies added
- Changes to core models
- Changes affecting multiple modules
- Security-related changes
- Performance-critical changes

---

## 🔴 MUST Rules (Never Violate)

### Code Quality
1. **MUST** run `make check` before committing - zero errors allowed
2. **MUST** run `make test` before committing - all tests must pass
3. **MUST** write tests for new functionality - no untested code
4. **MUST** maintain >80% code coverage for new code

### Git Workflow - BRANCHING REQUIRED
1. **MUST** create a feature branch for any work (NEVER commit directly to main)
2. **MUST** use branch naming: `{contributor}/{type}/{description}`
   - Examples: `copilot/feat/voice-capture`, `codex/fix/pdf-parsing`, `mohsin/refactor/models`
3. **MUST** create a Pull Request when work is complete
4. **MUST** wait for human approval before merging
5. **MUST** create atomic commits (one logical change per commit)
6. **MUST** use conventional commit messages (feat:, fix:, docs:, refactor:, test:)
7. **MUST** never force push to any branch
8. **MUST** never delete other contributors' log files
9. **MUST** create a log entry for each development session

### Branch Workflow Commands
```bash
# START of work session - create branch
git checkout main
git pull origin main
git checkout -b copilot/feat/my-feature

# DURING work - commit frequently
git add -A
git commit -m "feat(module): description"

# END of work session - push and create PR
git push -u origin copilot/feat/my-feature
gh pr create --title "feat: description" --body "## Summary\n..."

# Or use make command
make pr TITLE="feat: my feature" BODY="Description here"
```

### Documentation
1. **MUST** add docstrings to all public functions/classes
2. **MUST** update README if adding new features
3. **MUST** log decisions in dev-logs with rationale

### Architecture
1. **MUST** follow existing code patterns and structure
2. **MUST** keep models in `src/branch/models/`
3. **MUST** use Pydantic for data validation
4. **MUST** use type hints everywhere

---

## 🟡 SHOULD Rules (Strong Preference)

### Code Style
1. **SHOULD** prefer composition over inheritance
2. **SHOULD** keep functions under 50 lines
3. **SHOULD** keep files under 500 lines
4. **SHOULD** use descriptive variable names (no single letters except loops)
5. **SHOULD** group imports: stdlib, third-party, local

### Testing
1. **SHOULD** write tests first (TDD) for complex logic
2. **SHOULD** use pytest fixtures for shared test setup
3. **SHOULD** test edge cases and error conditions
4. **SHOULD** mock external dependencies

### Performance
1. **SHOULD** consider lazy loading for large resources
2. **SHOULD** avoid blocking operations in main thread
3. **SHOULD** profile before optimizing

---

## 🟢 MAY Rules (Optional but Encouraged)

1. **MAY** add helpful comments for complex algorithms
2. **MAY** create utility functions for repeated patterns
3. **MAY** add debug logging (with appropriate log levels)
4. **MAY** suggest architecture improvements in log files

---

## 📋 Pre-Commit Checklist

Before every commit, AI agents MUST verify using **make commands**:

```bash
# Option 1: Run everything at once (RECOMMENDED)
make all

# Option 2: Run individually
make format           # Format code
make lint             # Lint and auto-fix
make type-check       # Type check
make test             # Run tests
```

### If make is unavailable (fallback only):
```bash
uv run ruff format src tests
uv run ruff check src tests --fix
uv run mypy src
uv run pytest
```

All commands must pass with zero errors.

---

## 📝 Commit Message Format

```
<type>(<scope>): <short description>

<body - what and why>

<footer - breaking changes, issue refs>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting (no code change)
- `refactor`: Code restructuring (no behavior change)
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

### Examples
```
feat(capture): add voice input support

Implement speech-to-text capture using Whisper model.
Voice input allows hands-free idea capture during reading.

Closes #12
```

```
fix(models): correct timestamp timezone handling

IdeaFragment.captured_at now uses UTC consistently.
Previously mixed local and UTC times caused sorting issues.
```

---

## 🗂️ Session Logging Requirements

Every development session MUST create a log file:

**Location:** `docs/dev-logs/YYYY/MM/DD/{contributor}-{HHMMSS}-{description}.md`

**Required Sections:**
1. **Goals** - What you intended to accomplish
2. **Work Done** - Timestamped actions taken
3. **Decisions Made** - Choices and rationale
4. **Files Changed** - List of modified files
5. **Tests Added/Modified** - Testing coverage
6. **Next Steps** - Handoff for next session

**Template:**
```markdown
# {Description}

**Date:** YYYY-MM-DD HH:MM:SS  
**Contributor:** {copilot|codex|mohsin}  
**Duration:** {time}  
**Status:** {in-progress|completed|blocked}

---

## Goals
- [ ] Goal 1

## Work Done
### HH:MM - Action
Description...

## Decisions Made
| Decision | Choice | Rationale |
|----------|--------|-----------|
| ... | ... | ... |

## Files Changed
- `path/to/file.py` - Description of change

## Tests Added/Modified
- `tests/test_file.py::test_name` - What it tests

## Next Steps
- [ ] Next action

## Blockers/Questions
- Any issues encountered
```

---

## 🏗️ Architecture Guidelines

### Directory Structure
```
src/branch/
├── __init__.py          # Package exports
├── cli.py               # CLI entry point
├── models/              # Pydantic data models
│   ├── __init__.py
│   ├── idea_fragment.py
│   ├── document.py
│   └── session.py
├── reader/              # Document reading
│   ├── __init__.py
│   ├── base.py          # Abstract base reader
│   ├── pdf.py           # PDF implementation
│   └── markdown.py      # Markdown implementation
├── capture/             # Idea capture
│   ├── __init__.py
│   ├── text.py
│   └── voice.py
├── buffer/              # Branch Buffer
│   ├── __init__.py
│   └── manager.py
├── storage/             # Persistence
│   ├── __init__.py
│   ├── repository.py    # Repository pattern
│   └── sqlite.py        # SQLite implementation
└── config.py            # Configuration management
```

### Dependency Flow
```
CLI → Buffer → Capture → Models
         ↓        ↓
      Storage ← Reader
```

### Model Responsibilities
- **Models**: Pure data classes, validation, serialization
- **Reader**: Document parsing, text extraction, position mapping
- **Capture**: Input handling, context anchoring
- **Buffer**: Idea queue management, review workflow
- **Storage**: Persistence, queries, migrations

---

## 🧪 Testing Guidelines

### Test File Naming
- `test_{module}.py` - Unit tests for a module
- `test_{feature}_integration.py` - Integration tests

### Test Function Naming
```python
def test_{function}_{scenario}_{expected_result}():
    """Test that {function} does {expected} when {scenario}."""
```

### Example
```python
def test_idea_fragment_resolve_lightly_updates_timestamp():
    """Test that resolve_lightly updates the updated_at timestamp."""
    fragment = IdeaFragment(content="test")
    original_time = fragment.updated_at
    
    fragment.resolve_lightly("resolution note")
    
    assert fragment.updated_at > original_time
    assert fragment.resolution_note == "resolution note"
```

---

## ⚠️ Common Mistakes to Avoid

1. **Don't** add organization features during capture (violates design principle)
2. **Don't** block the UI thread with long operations
3. **Don't** store sensitive data without encryption
4. **Don't** hardcode file paths (use pathlib)
5. **Don't** catch generic exceptions without re-raising
6. **Don't** use mutable default arguments
7. **Don't** import from `__init__.py` within the same package (circular imports)

---

## 🔧 Development Commands Quick Reference

```bash
# Setup environment
make dev              # Setup complete dev environment with uv

# Run all checks
make all              # Run everything (check + test)

# Run specific test
uv run pytest tests/test_models.py -v

# Run with coverage
make test-cov         # Run tests with coverage report

# Add a dependency
uv add <package>

# Add a dev dependency
uv add --dev <package>

# Create today's log folder
make log              # Create today's log folder
```

---

## 📚 Reference Documents

- **PRD**: `Branch_PRD_Reading_First_Research_Companion.pdf`
- **Project Log**: `PROJECT_LOG.md`
- **Dev Logs**: `docs/dev-logs/`
- **This Guide**: `AGENTS.md`

---

*Last Updated: December 9, 2025*
