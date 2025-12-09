"""Pytest configuration for Branch tests."""

import pytest

from branch.models import BranchSession, Document, IdeaFragment
from branch.models.idea_fragment import TextAnchor


@pytest.fixture
def sample_fragment():
    """Create a sample idea fragment for testing."""
    return IdeaFragment(
        content="This is a test idea",
        anchor=TextAnchor(page_number=1, selected_text="test text"),
    )


@pytest.fixture
def sample_document():
    """Create a sample document for testing."""
    return Document(title="Test Document", page_count=100)


@pytest.fixture
def sample_session(sample_document):
    """Create a sample session for testing."""
    return BranchSession(document_id=sample_document.id)
