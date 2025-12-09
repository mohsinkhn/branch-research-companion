"""Tests for configuration management."""

import os
from pathlib import Path

import pytest


def test_config_defaults():
    """Test that config loads with default values."""
    from branch.config import Config

    assert Config.DATABASE_URL == os.getenv(
        "DATABASE_URL", "sqlite:///./data/branch.db"
    )
    assert isinstance(Config.DATA_DIR, Path)
    assert Config.LOG_LEVEL in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def test_config_singleton():
    """Test that config instance is available."""
    from branch.config import config

    assert config is not None
    assert hasattr(config, "DATABASE_URL")


def test_config_boolean_parsing():
    """Test boolean environment variable parsing."""
    from branch.config import Config

    assert isinstance(Config.ENABLE_AI_FEATURES, bool)
    assert isinstance(Config.ENABLE_VOICE_CAPTURE, bool)
    assert isinstance(Config.DEBUG, bool)
    assert isinstance(Config.TESTING, bool)


def test_config_ensure_directories(tmp_path, monkeypatch):
    """Test directory creation."""
    from branch.config import Config

    # Set temporary paths
    test_data_dir = tmp_path / "data"
    test_log_file = tmp_path / "logs" / "test.log"

    monkeypatch.setattr(Config, "DATA_DIR", test_data_dir)
    monkeypatch.setattr(Config, "LOG_FILE", test_log_file)

    # Directories should not exist yet
    assert not test_data_dir.exists()
    assert not test_log_file.parent.exists()

    # Create directories
    Config.ensure_directories()

    # Directories should now exist
    assert test_data_dir.exists()
    assert test_log_file.parent.exists()
