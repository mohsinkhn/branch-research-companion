# Contributing to Branch Research Companion

Thank you for your interest in contributing! This document provides guidelines and information for contributors.

## Development Setup

### Prerequisites

- Python 3.11 or higher
- Git
- A GitHub account

### Local Development

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/branch-research-companion.git
   cd branch-research-companion
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Install pre-commit hooks**
   ```bash
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

This project uses:
- **Black** for code formatting
- **Ruff** for linting
- **MyPy** for type checking

Run all checks:
```bash
black src tests
ruff check src tests
mypy src
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/branch

# Run specific test file
pytest tests/test_models.py
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
3. Ensure all tests pass
4. Update the changelog if applicable
5. Request review from maintainers

## Questions?

Open an issue for:
- Bug reports
- Feature requests
- General questions

---

*Thank you for helping build a better reading experience!*
