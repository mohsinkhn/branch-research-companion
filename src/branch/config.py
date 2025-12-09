"""Configuration management for Branch application.

Loads settings from environment variables with sensible defaults.
Uses python-dotenv to load .env file if present.
"""

import os
from pathlib import Path

from dotenv import load_dotenv


# Load .env file if it exists
load_dotenv()


class Config:
    """Application configuration loaded from environment variables."""

    # Storage
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data/branch.db")
    DATA_DIR: Path = Path(os.getenv("DATA_DIR", "./data"))

    # AI Features (optional)
    ENABLE_AI_FEATURES: bool = (
        os.getenv("ENABLE_AI_FEATURES", "false").lower() == "true"
    )
    OLLAMA_API_URL: str = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama2")
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")

    # Voice Capture (optional)
    ENABLE_VOICE_CAPTURE: bool = (
        os.getenv("ENABLE_VOICE_CAPTURE", "false").lower() == "true"
    )
    WHISPER_MODEL_SIZE: str = os.getenv("WHISPER_MODEL_SIZE", "base")

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
    LOG_FILE: Path = Path(os.getenv("LOG_FILE", "./logs/branch.log"))

    # Development
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    TESTING: bool = os.getenv("TESTING", "false").lower() == "true"

    @classmethod
    def ensure_directories(cls) -> None:
        """Ensure required directories exist."""
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.LOG_FILE.parent.mkdir(parents=True, exist_ok=True)


# Default configuration instance
config = Config()
