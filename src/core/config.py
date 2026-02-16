"""
Configuration constants for ResumeUnmark.

This module contains all configurable parameters for watermark detection
and removal algorithms.
"""

# Bottom-right area removal settings
REMOVE_WIDTH = 200  # Width in points
REMOVE_HEIGHT = 70  # Height in points

# Edge text watermark detection settings
EDGE_WATERMARK_MIN_RIGHT_RATIO = 0.70  # Candidate starts in right-most 30% of page
EDGE_WATERMARK_MIN_DOWN_RATIO = 0.35   # Ignore top header area
EDGE_WATERMARK_MAX_CHARS = 40          # Only small text blocks/lines
EDGE_WATERMARK_MIN_DISTANCE = 25.0     # Must be isolated from main content (points)
EDGE_WATERMARK_PADDING = 2.0           # Padding around redaction rects (points)

# PDF processing settings
PDF_GARBAGE_LEVEL = 4     # Garbage collection level (0-4)
PDF_DEFLATE = True        # Enable compression
PDF_OUTPUT_SUFFIX = "_clean"  # Suffix for output files
