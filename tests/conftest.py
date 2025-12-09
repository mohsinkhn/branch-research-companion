"""Pytest configuration for Branch tests."""

import pytest


@pytest.fixture
def sample_fragment():
    """Create a sample idea fragment for testing."""
    from branch.models import IdeaFragment
    from branch.models.idea_fragment import TextAnchor

    return IdeaFragment(
        content="This is a test idea",
        anchor=TextAnchor(page_number=1, selected_text="test text"),
    )


@pytest.fixture
def sample_document():
    """Create a sample document for testing."""
    from branch.models import Document

    return Document(title="Test Document", page_count=100)


@pytest.fixture
def sample_session(sample_document):
    """Create a sample session for testing."""
    from branch.models import BranchSession

    return BranchSession(document_id=sample_document.id)
