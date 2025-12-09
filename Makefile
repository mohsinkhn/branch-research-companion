.PHONY: help install dev lint format type-check test test-cov clean all check docs arch

# Default target
help:
	@echo "Branch Research Companion - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install     Install dependencies with uv"
	@echo "  make dev         Setup complete dev environment"
	@echo ""
	@echo "Quality:"
	@echo "  make format      Format code with ruff"
	@echo "  make lint        Lint code with ruff"
	@echo "  make type-check  Type check with mypy"
	@echo "  make check       Run all checks (format, lint, type-check)"
	@echo ""
	@echo "Testing:"
	@echo "  make test        Run tests"
	@echo "  make test-cov    Run tests with coverage"
	@echo ""
	@echo "Documentation & Architecture:"
	@echo "  make docs        Generate API documentation"
	@echo "  make arch        Generate architecture docs & dependency graphs"
	@echo "  make metrics     Show code complexity metrics"
	@echo ""
	@echo "Other:"
	@echo "  make clean       Remove build artifacts"
	@echo "  make all         Run all checks and tests"
	@echo "  make log         Create today's log folder"

# =============================================================================
# Setup
# =============================================================================

install:
	uv sync

dev: install
	uv run pre-commit install
	@echo "✅ Development environment ready!"

# =============================================================================
# Code Quality
# =============================================================================

format:
	uv run ruff format src tests

lint:
	uv run ruff check src tests --fix

type-check:
	uv run mypy src

check: format lint type-check
	@echo "✅ All checks passed!"

# =============================================================================
# Testing
# =============================================================================

test:
	uv run pytest

test-cov:
	uv run pytest --cov=src/branch --cov-report=html --cov-report=term-missing
	@echo "📊 Coverage report: htmlcov/index.html"

test-fast:
	uv run pytest -x -q

# =============================================================================
# Documentation & Architecture
# =============================================================================

docs:
	uv run pdoc src/branch -o docs/api/
	@echo "📚 API docs generated: docs/api/"

docs-serve:
	uv run pdoc src/branch --http localhost:8080

arch:
	uv run python scripts/generate_arch_docs.py
	@echo "🏗️ Architecture docs updated"

# Generate dependency graph (requires graphviz: brew install graphviz)
deps-graph:
	@mkdir -p docs/architecture
	uv run pydeps src/branch --cluster --max-bacon=2 -o docs/architecture/deps.svg 2>/dev/null || \
		echo "⚠️ Install graphviz for dependency graphs: brew install graphviz"
	@echo "📊 Dependency graph: docs/architecture/deps.svg"

metrics:
	@echo "📊 Code Complexity (Cyclomatic):"
	@uv run radon cc src/branch -a -s
	@echo ""
	@echo "📊 Maintainability Index:"
	@uv run radon mi src/branch -s

metrics-report:
	@mkdir -p docs/architecture
	uv run radon cc src/branch -a -j > docs/architecture/complexity.json
	uv run radon mi src/branch -j > docs/architecture/maintainability.json
	@echo "📊 Metrics saved to docs/architecture/"

# =============================================================================
# Combined
# =============================================================================

all: check test
	@echo "✅ All checks and tests passed!"

# =============================================================================
# Utilities
# =============================================================================

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "🧹 Cleaned!"

log:
	@mkdir -p "docs/dev-logs/$$(date +%Y/%m/%d)"
	@echo "📁 Created: docs/dev-logs/$$(date +%Y/%m/%d)/"

# Create a new log file for a contributor
# Usage: make new-log CONTRIBUTOR=copilot DESC=feature-work
new-log:
	@mkdir -p "docs/dev-logs/$$(date +%Y/%m/%d)"
	@touch "docs/dev-logs/$$(date +%Y/%m/%d)/$(CONTRIBUTOR)-$$(date +%H%M%S)-$(DESC).md"
	@echo "📝 Created: docs/dev-logs/$$(date +%Y/%m/%d)/$(CONTRIBUTOR)-$$(date +%H%M%S)-$(DESC).md"
