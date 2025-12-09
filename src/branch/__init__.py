"""Branch - Reading-First Research Companion

A reading-first system that helps users safely capture, defer,
and later develop ideas generated during reading.
"""

__version__ = "0.1.0"
__author__ = "Your Name"

from branch.models.document import Document
from branch.models.idea_fragment import IdeaFragment
from branch.models.session import BranchSession


__all__ = [
    "BranchSession",
    "Document",
    "IdeaFragment",
    "__version__",
]
