"""IdeaFragment model - the core concept of Branch.

An Idea Fragment is a spontaneous hypothesis, comparison, or insight
captured mid-reading. It is:
- Anchored to document context
- Allowed to be incomplete
- Stored without forced structure
"""

from collections.abc import Callable
from datetime import datetime
from enum import Enum
from typing import Any, ClassVar
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class FragmentStatus(str, Enum):
    """Status of an idea fragment in the Branch Buffer."""

    CAPTURED = "captured"  # Just captured, unprocessed
    REVIEWED = "reviewed"  # Looked at during review session
    DEVELOPED = "developed"  # Expanded into fuller notes
    ARCHIVED = "archived"  # Kept but not active
    DISCARDED = "discarded"  # Marked for removal


class TextAnchor(BaseModel):
    """Anchor point within a document for an idea fragment."""

    page_number: int | None = None
    start_position: int | None = None  # Character offset
    end_position: int | None = None
    selected_text: str | None = None  # The highlighted/selected text


class IdeaFragment(BaseModel):
    """A spontaneous idea captured during reading.

    This is the first-class citizen of Branch. Ideas are captured quickly
    without forced organization, preserving reading flow.
    """

    id: UUID = Field(default_factory=uuid4)

    # Core content - can be text, could be transcribed voice, etc.
    content: str

    # Where in the document this idea was captured
    anchor: TextAnchor | None = None

    # Reference to the source document
    document_id: UUID | None = None

    # Reference to the reading session
    session_id: UUID | None = None

    # Timestamps
    captured_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = None

    # Status in the Branch Buffer
    status: FragmentStatus = FragmentStatus.CAPTURED

    # Capture modality
    capture_type: str = "text"  # "text", "voice", "stylus"

    # Optional: light resolution notes (from "Resolve Lightly" action)
    resolution_note: str | None = None

    class Config:
        """Pydantic configuration."""

        json_encoders: ClassVar[dict[type[Any], Callable[[Any], str]]] = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v),
        }

    def resolve_lightly(self, note: str) -> None:
        """Add a light resolution note without deep diving."""
        self.resolution_note = note
        self.updated_at = datetime.utcnow()

    def mark_reviewed(self) -> None:
        """Mark this fragment as reviewed in Branch Buffer."""
        self.status = FragmentStatus.REVIEWED
        self.updated_at = datetime.utcnow()

    def develop(self) -> None:
        """Mark this fragment as developed into fuller notes."""
        self.status = FragmentStatus.DEVELOPED
        self.updated_at = datetime.utcnow()

    def archive(self) -> None:
        """Archive this fragment."""
        self.status = FragmentStatus.ARCHIVED
        self.updated_at = datetime.utcnow()

    def discard(self) -> None:
        """Mark this fragment for removal."""
        self.status = FragmentStatus.DISCARDED
        self.updated_at = datetime.utcnow()
