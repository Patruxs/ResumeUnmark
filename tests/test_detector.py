"""
Tests for the EdgeTextDetector class.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.detector import EdgeTextDetector
import fitz


class TestEdgeTextDetector:
    """Test suite for EdgeTextDetector."""
    
    def test_initialization_default(self):
        """Test EdgeTextDetector initialization with defaults."""
        detector = EdgeTextDetector()
        assert detector.max_chars == 40
        assert detector.padding == 2.0
    
    def test_initialization_custom(self):
        """Test EdgeTextDetector initialization with custom parameters."""
        detector = EdgeTextDetector(max_chars=50, padding=5.0)
        assert detector.max_chars == 50
        assert detector.padding == 5.0
    
    def test_clamp_rect_to_page(self):
        """Test rectangle clamping to page boundaries."""
        page_rect = fitz.Rect(0, 0, 100, 100)
        
        # Rect within bounds
        rect1 = fitz.Rect(10, 10, 50, 50)
        clamped1 = EdgeTextDetector._clamp_rect_to_page(rect1, page_rect)
        assert clamped1 == rect1
        
        # Rect exceeding bounds
        rect2 = fitz.Rect(-10, -10, 110, 110)
        clamped2 = EdgeTextDetector._clamp_rect_to_page(rect2, page_rect)
        assert clamped2.x0 == 0
        assert clamped2.y0 == 0
        assert clamped2.x1 == 100
        assert clamped2.y1 == 100
        
        # Partially exceeding bounds
        rect3 = fitz.Rect(50, 50, 110, 80)
        clamped3 = EdgeTextDetector._clamp_rect_to_page(rect3, page_rect)
        assert clamped3.x0 == 50
        assert clamped3.y0 == 50
        assert clamped3.x1 == 100
        assert clamped3.y1 == 80


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
