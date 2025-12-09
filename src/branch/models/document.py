"""Document model for Branch.

Represents a document being read (PDF, text, markdown, etc.)
"""

from datetime import datetime
from enum import Enum
from pathlib import Path
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    """Supported document types."""

    PDF = "pdf"
    TEXT = "text"
    MARKDOWN = "markdown"
    HTML = "html"


class Document(BaseModel):
    """A document that can be read in Branch.

    Documents are the context for reading sessions and the anchors
    for idea fragments.
    """

    id: UUID = Field(default_factory=uuid4)

    # Document identification
    title: str
    file_path: Path | None = None
    url: str | None = None

    # Document metadata
    document_type: DocumentType = DocumentType.PDF
    page_count: int | None = None
    author: str | None = None

    # Timestamps
    added_at: datetime = Field(default_factory=datetime.utcnow)
    last_opened_at: datetime | None = None

    # Reading progress
    last_page: int = 1
    read_percentage: float = 0.0

    class Config:
        """Pydantic configuration."""

        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v),
            Path: lambda v: str(v),
        }

    def update_progress(self, current_page: int) -> None:
        """Update reading progress."""
        self.last_page = current_page
        self.last_opened_at = datetime.utcnow()
        if self.page_count:
            self.read_percentage = (current_page / self.page_count) * 100

    @classmethod
    def from_file(cls, file_path: Path) -> "Document":
        """Create a Document from a file path."""
        suffix = file_path.suffix.lower()
        doc_type_map = {
            ".pdf": DocumentType.PDF,
            ".txt": DocumentType.TEXT,
            ".md": DocumentType.MARKDOWN,
            ".html": DocumentType.HTML,
            ".htm": DocumentType.HTML,
        }

        return cls(
            title=file_path.stem,
            file_path=file_path,
            document_type=doc_type_map.get(suffix, DocumentType.TEXT),
        )
