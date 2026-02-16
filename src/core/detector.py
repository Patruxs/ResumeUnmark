"""
Edge text watermark detection.

This module contains the heuristic algorithm for detecting small,
isolated text blocks on the right edge of PDF pages.
"""

import fitz  # PyMuPDF
from typing import List
from .config import EDGE_WATERMARK_MAX_CHARS, EDGE_WATERMARK_PADDING


class EdgeTextDetector:
    """
    Detects edge/footer watermark text using a robust heuristic.
    
    Algorithm:
    1. Identify "body content" as text blocks starting on the LEFT half of the page
    2. Find the bottom-most point of this body content
    3. Mark small text blocks on the RIGHT half that are BELOW this point as watermarks
    """
    
    def __init__(self, max_chars: int = EDGE_WATERMARK_MAX_CHARS, 
                 padding: float = EDGE_WATERMARK_PADDING):
        """
        Initialize the detector.
        
        Args:
            max_chars: Maximum character count for a text block to be considered a watermark
            padding: Padding to add around detected watermark rectangles (in points)
        """
        self.max_chars = max_chars
        self.padding = padding
    
    @staticmethod
    def _clamp_rect_to_page(rect: fitz.Rect, page_rect: fitz.Rect) -> fitz.Rect:
        """Ensure a rectangle stays within page boundaries."""
        return fitz.Rect(
            max(page_rect.x0, rect.x0),
            max(page_rect.y0, rect.y0),
            min(page_rect.x1, rect.x1),
            min(page_rect.y1, rect.y1),
        )
    
    def find_watermark_rects(self, page: fitz.Page) -> List[fitz.Rect]:
        """
        Find watermark rectangles on a page.
        
        Args:
            page: PyMuPDF page object
            
        Returns:
            List of rectangles containing detected watermarks
        """
        page_rect = page.rect
        half_width = page_rect.width * 0.5
        
        # Get all text blocks: (x0, y0, x1, y1, "text", block_no, block_type)
        blocks = page.get_text("blocks") or []
        
        # Step 1: Find the bottom of the "body" content (text starting on the left)
        last_body_y = 0.0
        
        for b in blocks:
            x0, y0, x1, y1, text, _, block_type = b[:7]
            
            # Ignore images/graphics for body text calculations
            if block_type != 0:
                continue
            
            # If block starts on the left side, it's part of the main document body
            if x0 < half_width:
                if text.strip():  # Only count non-empty text
                    last_body_y = max(last_body_y, y1)
        
        redaction_rects: List[fitz.Rect] = []
        
        # Step 2: Find candidates on the right side that are below the body content
        for b in blocks:
            x0, y0, x1, y1, text, _, block_type = b[:7]
            text = (text or "").strip()
            
            # Must be text
            if block_type != 0 or not text:
                continue
            
            # Must be small (watermark-like) - remove spaces to verify length
            if len(text.replace(" ", "")) > self.max_chars:
                continue
            
            # Must be on the RIGHT side
            if x0 < half_width:
                continue
            
            # Must be BELOW the last line of the main body
            if y0 < last_body_y:
                continue
            
            # If it passes all checks, mark it for redaction
            r = fitz.Rect(x0, y0, x1, y1)
            padded_rect = fitz.Rect(
                r.x0 - self.padding,
                r.y0 - self.padding,
                r.x1 + self.padding,
                r.y1 + self.padding
            )
            redaction_rects.append(self._clamp_rect_to_page(padded_rect, page_rect))
        
        return redaction_rects
