"""Repository interfaces for Branch storage.

Concrete implementations should translate between Pydantic models and the
underlying persistence layer while keeping read flow latency low.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol


if TYPE_CHECKING:
    from collections.abc import Iterable
    from uuid import UUID

    from branch.models import BranchSession, Document, IdeaFragment


class StorageError(Exception):
    """Base exception for storage-related failures."""


class BranchRepository(Protocol):
    """Abstract interface for Branch storage backends."""

    def upsert_document(self, document: Document) -> None:
        """Insert or update a document record."""

    def get_document(self, document_id: UUID) -> Document | None:
        """Fetch a document by id."""

    def upsert_session(self, session: BranchSession) -> None:
        """Insert or update a reading session."""

    def get_session(self, session_id: UUID) -> BranchSession | None:
        """Fetch a session by id."""

    def upsert_fragment(self, fragment: IdeaFragment) -> None:
        """Insert or update an idea fragment."""

    def get_fragment(self, fragment_id: UUID) -> IdeaFragment | None:
        """Fetch an idea fragment by id."""

    def list_fragments_for_document(self, document_id: UUID) -> Iterable[IdeaFragment]:
        """Return all fragments anchored to a document."""
