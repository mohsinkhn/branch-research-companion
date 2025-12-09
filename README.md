# Branch - Reading-First Research Companion

> If a feature harms reading flow or suppresses idea emergence, it must be rejected.

A reading-first system that helps users safely capture, defer, and later develop ideas generated during reading.

## 🎯 Vision

Branch exists to enable **idea-first reading without breaking flow**. While reading long, technical documents, users frequently generate ideas, hypotheses, and connections they want to explore. Existing tools force users to either interrupt reading or suppress curiosity. Branch solves this.

## 🚀 Features (V1 Scope)

- **Document-first reader** (PDF/text)
- **Multi-modal idea capture** (text, voice, stylus)
- **Idea Fragments** anchored to document context
- **Branch Buffer** for post-reading review
- **Lightweight local AI assistance** (optional)

## 📖 Core Concept: Idea Fragment

An Idea Fragment is a spontaneous hypothesis, comparison, or insight captured mid-reading:
- Anchored to document context
- Allowed to be incomplete
- Stored without forced structure

## 🎮 Reading Interaction Model

Only three actions during reading:
1. **Capture Idea** - Quick, flow-preserving capture
2. **Resolve Lightly** - Small clarifications without deep diving
3. **Dive Deep** - Explicit, intentional exploration

## 🏗️ Project Status

See [PROJECT_LOG.md](PROJECT_LOG.md) for detailed progress tracking.

## 🛠️ Development

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) - Fast Python package manager

### Quick Setup with uv (Recommended)

```bash
# Install uv (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/mohsinkhn/branch-research-companion.git
cd branch-research-companion

# Setup environment and install dependencies (uv handles everything)
uv sync

# Install pre-commit hooks
uv run pre-commit install

# Run tests
uv run pytest

# Run all checks (format, lint, type-check, test)
uv run ruff format src tests && uv run ruff check src tests && uv run mypy src && uv run pytest
```

### Alternative Setup with pip

```bash
# Clone the repository
git clone https://github.com/mohsinkhn/branch-research-companion.git
cd branch-research-companion

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest
```

### Development Commands

```bash
# Format code
uv run ruff format src tests

# Lint code (with auto-fix)
uv run ruff check src tests --fix

# Type check
uv run mypy src

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src/branch --cov-report=html

# Run all checks before commit
uv run ruff format src tests && uv run ruff check src tests && uv run mypy src && uv run pytest
```

### Project Structure

```
branch-research-companion/
├── src/
│   └── branch/
│       ├── __init__.py
│       ├── models/          # Data models
│       ├── reader/          # Document reading
│       ├── capture/         # Idea capture
│       ├── buffer/          # Branch Buffer
│       └── storage/         # Persistence
├── tests/
├── docs/
│   ├── dev-logs/           # Development session logs
│   └── copilot-chats/      # AI assistant conversation logs
├── pyproject.toml
└── PROJECT_LOG.md
```

## 📄 License

MIT License - See [LICENSE](LICENSE)

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

*Built for thinkers who read deeply and think originally.*
