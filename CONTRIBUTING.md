# Contributing to Branch Research Companion

Thank you for your interest in contributing! This document provides guidelines and information for contributors.

> **Important:** AI agents should also read `AGENTS.md` for detailed development guidelines.

## Development Setup

### Prerequisites

- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) (recommended) - Fast Python package manager
- Git
- A GitHub account

### Quick Setup with uv (Recommended)

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/branch-research-companion.git
cd branch-research-companion

# Setup environment (uv handles everything)
uv sync

# Install pre-commit hooks
uv run pre-commit install
```

### Alternative Setup with pip

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/branch-research-companion.git
cd branch-research-companion

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

## Development Workflow

### Branch Naming

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation changes
- `refactor/description` - Code refactoring

### Commit Messages

Follow conventional commits:
- `feat: add voice capture functionality`
- `fix: resolve PDF page anchoring issue`
- `docs: update installation instructions`
- `refactor: simplify idea fragment storage`

### Code Style

This project uses **Ruff** for both linting and formatting (replaces black, isort, flake8).

Run all checks:
```bash
# Format code
uv run ruff format src tests

# Lint code (with auto-fix)
uv run ruff check src tests --fix

# Type check
uv run mypy src

# Or run all at once
uv run ruff format src tests && uv run ruff check src tests && uv run mypy src
```

### Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/branch --cov-report=html

# Run specific test file
uv run pytest tests/test_models.py -v

# Run tests in parallel
uv run pytest -n auto
```

## Project Philosophy

When contributing, keep in mind the **North-Star Rule**:

> If a feature harms reading flow or suppresses idea emergence, it must be rejected.

### Design Principles

1. **Ideas are first-class citizens** - Every feature should make idea capture easier
2. **Organization is forbidden during reading** - Don't add categorization during capture
3. **Curiosity must never be punished** - Quick capture is essential
4. **Multi-modal thinking is respected** - Support text, voice, and stylus
5. **Tools must preserve flow** - Minimal interruption is key

## Pull Request Process

1. Update documentation for any new features
2. Add tests for new functionality
3. Ensure all checks pass: `uv run ruff format src tests && uv run ruff check src tests && uv run mypy src && uv run pytest`
4. Update the changelog if applicable
5. Request review from maintainers

## Questions?

Open an issue for:
- Bug reports
- Feature requests
- General questions

---

*Thank you for helping build a better reading experience!*
