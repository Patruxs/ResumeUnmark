"""
Tests for the PDFCleaner class.
"""

import pytest
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.cleaner import PDFCleaner
from core.config import PDF_OUTPUT_SUFFIX


class TestPDFCleaner:
    """Test suite for PDFCleaner."""
    
    def test_initialization_default(self):
        """Test PDFCleaner initialization with defaults."""
        cleaner = PDFCleaner()
        assert cleaner.remove_width == 200
        assert cleaner.remove_height == 70
        assert cleaner.enable_edge_detection is True
        assert cleaner.output_suffix == PDF_OUTPUT_SUFFIX
        assert cleaner.detector is not None
    
    def test_initialization_custom(self):
        """Test PDFCleaner initialization with custom parameters."""
        cleaner = PDFCleaner(
            remove_width=150,
            remove_height=50,
            enable_edge_detection=False,
            output_suffix="_cleaned"
        )
        assert cleaner.remove_width == 150
        assert cleaner.remove_height == 50
        assert cleaner.enable_edge_detection is False
        assert cleaner.output_suffix == "_cleaned"
        assert cleaner.detector is None
    
    def test_log_callback(self):
        """Test that log callback is called."""
        messages = []
        
        def custom_log(msg):
            messages.append(msg)
        
        cleaner = PDFCleaner(log_callback=custom_log)
        cleaner._log("Test message")
        
        assert len(messages) == 1
        assert messages[0] == "Test message"
    
    def test_clean_nonexistent_file(self):
        """Test cleaning a file that doesn't exist."""
        cleaner = PDFCleaner(log_callback=lambda x: None)
        result = cleaner.clean_file("nonexistent.pdf")
        assert result is None
    
    def test_clean_non_pdf_file(self):
        """Test cleaning a non-PDF file."""
        cleaner = PDFCleaner(log_callback=lambda x: None)
        result = cleaner.clean_file("test.txt")
        assert result is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
