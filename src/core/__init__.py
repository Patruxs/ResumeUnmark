"""
Core watermark removal functionality.
"""

from .cleaner import PDFCleaner
from .detector import EdgeTextDetector
from .config import *

__all__ = [
    'PDFCleaner',
    'EdgeTextDetector',
]
