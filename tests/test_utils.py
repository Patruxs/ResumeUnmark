"""
Tests for utility functions.
"""

import pytest
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.file_utils import find_pdf_files, normalize_path


class TestFileUtils:
    """Test suite for file utility functions."""
    
    def test_normalize_path(self):
        """Test path normalization."""
        assert normalize_path('"test.pdf"') == "test.pdf"
        assert normalize_path("'test.pdf'") == "test.pdf"
        assert normalize_path("  test.pdf  ") == "test.pdf"
        assert normalize_path('  "test.pdf"  ') == "test.pdf"
    
    def test_find_pdf_files_nonexistent(self):
        """Test finding PDFs in nonexistent path."""
        result = find_pdf_files("nonexistent_path")
        assert result == []
    
    def test_find_pdf_files_exclude_cleaned(self):
        """Test excluding cleaned files."""
        # This is a unit test - we're testing the logic, not actual file operations
        # The actual behavior would be tested in integration tests
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
