"""BranchSession model.

A reading session that groups idea fragments captured during
a single reading period.
"""

from collections.abc import Callable
from datetime import datetime
from typing import Any, ClassVar
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class BranchSession(BaseModel):
    """A reading session in Branch.

    Sessions group idea fragments captured during a single reading period.
    They help with context and review.
    """

    id: UUID = Field(default_factory=uuid4)

    # Associated document
    document_id: UUID

    # Session timing
    started_at: datetime = Field(default_factory=datetime.utcnow)
    ended_at: datetime | None = None

    # Reading context
    start_page: int = 1
    end_page: int | None = None

    # Session stats
    fragments_captured: int = 0
    dive_deeps: int = 0  # How many times "Dive Deep" was used

    # Optional notes about the session
    notes: str | None = None

    class Config:
        """Pydantic configuration."""

        json_encoders: ClassVar[dict[type[Any], Callable[[Any], str]]] = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v),
        }

    def end_session(self, end_page: int | None = None) -> None:
        """End the reading session."""
        self.ended_at = datetime.utcnow()
        if end_page:
            self.end_page = end_page

    def record_capture(self) -> None:
        """Record that an idea fragment was captured."""
        self.fragments_captured += 1

    def record_dive_deep(self) -> None:
        """Record that user chose to dive deep."""
        self.dive_deeps += 1

    @property
    def duration_minutes(self) -> float | None:
        """Get session duration in minutes."""
        if self.ended_at:
            delta = self.ended_at - self.started_at
            return delta.total_seconds() / 60
        return None

    @property
    def is_active(self) -> bool:
        """Check if session is still active."""
        return self.ended_at is None
