"""
ResumeUnmark - Remove watermarks from PDF files.

A Python package for removing bottom-right watermarks and isolated 
right-edge text from PDFs.
"""

__version__ = "2.0.0"
__author__ = "patrickzs"
__license__ = "MIT"

from .core import PDFCleaner, EdgeTextDetector
from .cli import main

__all__ = [
    'PDFCleaner',
    'EdgeTextDetector',
    'main',
]
