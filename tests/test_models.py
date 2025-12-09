"""Tests for Branch data models."""

import pytest
from datetime import datetime
from uuid import UUID

from branch.models import IdeaFragment, FragmentStatus, Document, BranchSession
from branch.models.idea_fragment import TextAnchor
from branch.models.document import DocumentType


class TestIdeaFragment:
    """Tests for IdeaFragment model."""

    def test_create_basic_fragment(self):
        """Test creating a basic idea fragment."""
        fragment = IdeaFragment(content="This is an interesting connection!")

        assert fragment.content == "This is an interesting connection!"
        assert fragment.status == FragmentStatus.CAPTURED
        assert fragment.capture_type == "text"
        assert isinstance(fragment.id, UUID)
        assert isinstance(fragment.captured_at, datetime)

    def test_fragment_with_anchor(self):
        """Test creating a fragment with document anchor."""
        anchor = TextAnchor(
            page_number=42,
            start_position=100,
            end_position=150,
            selected_text="key insight here"
        )
        fragment = IdeaFragment(
            content="This relates to my previous research",
            anchor=anchor
        )

        assert fragment.anchor is not None
        assert fragment.anchor.page_number == 42
        assert fragment.anchor.selected_text == "key insight here"

    def test_resolve_lightly(self):
        """Test the resolve lightly functionality."""
        fragment = IdeaFragment(content="What does this term mean?")
        fragment.resolve_lightly("It refers to X concept")

        assert fragment.resolution_note == "It refers to X concept"
        assert fragment.updated_at is not None

    def test_status_transitions(self):
        """Test fragment status transitions."""
        fragment = IdeaFragment(content="Test idea")

        assert fragment.status == FragmentStatus.CAPTURED

        fragment.mark_reviewed()
        assert fragment.status == FragmentStatus.REVIEWED

        fragment.develop()
        assert fragment.status == FragmentStatus.DEVELOPED

        # Can also archive or discard
        fragment2 = IdeaFragment(content="Another idea")
        fragment2.archive()
        assert fragment2.status == FragmentStatus.ARCHIVED

        fragment3 = IdeaFragment(content="Third idea")
        fragment3.discard()
        assert fragment3.status == FragmentStatus.DISCARDED


class TestDocument:
    """Tests for Document model."""

    def test_create_document(self):
        """Test creating a document."""
        doc = Document(title="Research Paper")

        assert doc.title == "Research Paper"
        assert doc.document_type == DocumentType.PDF
        assert doc.last_page == 1
        assert doc.read_percentage == 0.0

    def test_update_progress(self):
        """Test updating reading progress."""
        doc = Document(title="Long Paper", page_count=100)
        doc.update_progress(25)

        assert doc.last_page == 25
        assert doc.read_percentage == 25.0
        assert doc.last_opened_at is not None


class TestBranchSession:
    """Tests for BranchSession model."""

    def test_create_session(self):
        """Test creating a reading session."""
        from uuid import uuid4
        doc_id = uuid4()

        session = BranchSession(document_id=doc_id)

        assert session.document_id == doc_id
        assert session.is_active is True
        assert session.fragments_captured == 0

    def test_end_session(self):
        """Test ending a session."""
        from uuid import uuid4
        session = BranchSession(document_id=uuid4())
        session.end_session(end_page=50)

        assert session.is_active is False
        assert session.end_page == 50
        assert session.ended_at is not None

    def test_record_captures(self):
        """Test recording captured fragments."""
        from uuid import uuid4
        session = BranchSession(document_id=uuid4())

        session.record_capture()
        session.record_capture()
        session.record_capture()

        assert session.fragments_captured == 3

    def test_record_dive_deeps(self):
        """Test recording dive deep actions."""
        from uuid import uuid4
        session = BranchSession(document_id=uuid4())

        session.record_dive_deep()
        session.record_dive_deep()

        assert session.dive_deeps == 2
