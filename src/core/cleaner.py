"""
PDF watermark removal.

This module contains the main logic for removing watermarks from PDF files.
"""

import fitz  # PyMuPDF
import os
from typing import Optional, Callable
from .detector import EdgeTextDetector
from .config import (
    REMOVE_WIDTH,
    REMOVE_HEIGHT,
    PDF_GARBAGE_LEVEL,
    PDF_DEFLATE,
    PDF_OUTPUT_SUFFIX,
)


class PDFCleaner:
    """
    Removes watermarks from PDF files.
    
    Supports two cleaning modes:
    1. Fixed bottom-right area removal
    2. Smart edge text detection
    """
    
    def __init__(
        self,
        remove_width: int = REMOVE_WIDTH,
        remove_height: int = REMOVE_HEIGHT,
        enable_edge_detection: bool = True,
        output_suffix: str = PDF_OUTPUT_SUFFIX,
        log_callback: Optional[Callable[[str], None]] = None,
    ):
        """
        Initialize the PDF cleaner.
        
        Args:
            remove_width: Width of bottom-right area to remove (in points)
            remove_height: Height of bottom-right area to remove (in points)
            enable_edge_detection: Whether to detect and remove edge text watermarks
            output_suffix: Suffix to add to output filenames
            log_callback: Optional callback function for logging messages
        """
        self.remove_width = remove_width
        self.remove_height = remove_height
        self.enable_edge_detection = enable_edge_detection
        self.output_suffix = output_suffix
        self.log_callback = log_callback or print
        
        if enable_edge_detection:
            self.detector = EdgeTextDetector()
        else:
            self.detector = None
    
    def _log(self, message: str):
        """Log a message using the configured callback."""
        if self.log_callback:
            self.log_callback(message)
    
    def clean_file(self, input_path: str) -> Optional[str]:
        """
        Clean a single PDF file.
        
        Args:
            input_path: Path to the input PDF file
            
        Returns:
            Path to the output file if successful, None otherwise
        """
        if not os.path.isfile(input_path):
            self._log(f"[ERROR] File not found: {input_path}")
            return None
        
        if not input_path.lower().endswith(".pdf"):
            self._log(f"[SKIP] Not a PDF: {input_path}")
            return None
        
        try:
            doc = fitz.open(input_path)
            modified = False
            
            for page_index in range(doc.page_count):
                page = doc.load_page(page_index)
                rect = page.rect
                width = rect.width
                height = rect.height
                
                redaction_rects = []
                
                # Add fixed bottom-right area if configured
                if self.remove_width > 0 and self.remove_height > 0:
                    target_area = fitz.Rect(
                        width - self.remove_width,    # x0 (left boundary)
                        height - self.remove_height,  # y0 (top boundary)
                        width,                        # x1 (right edge)
                        height                        # y1 (bottom edge)
                    )
                    redaction_rects.append(target_area)
                
                # Add edge text watermarks if detection is enabled
                if self.detector:
                    edge_rects = self.detector.find_watermark_rects(page)
                    redaction_rects.extend(edge_rects)
                
                # Apply all redactions
                for redact_rect in redaction_rects:
                    # Create a white redaction annotation
                    page.add_redact_annot(redact_rect, fill=(1, 1, 1))
                
                # Apply the redactions
                page.apply_redactions()
                modified = True
            
            if modified:
                # Generate output filename
                base, ext = os.path.splitext(input_path)
                output_path = f"{base}{self.output_suffix}{ext}"
                
                # Save with optimization
                doc.save(
                    output_path,
                    garbage=PDF_GARBAGE_LEVEL,
                    deflate=PDF_DEFLATE
                )
                
                self._log(f"[SUCCESS] Cleaned: {input_path} -> {os.path.basename(output_path)}")
                doc.close()
                return output_path
            else:
                self._log(f"[SKIP] No changes needed for: {input_path}")
                doc.close()
                return None
        
        except Exception as e:
            self._log(f"[ERROR] Could not process {input_path}: {e}")
            return None
    
    def clean_files(self, input_paths: list) -> list:
        """
        Clean multiple PDF files.
        
        Args:
            input_paths: List of input file paths
            
        Returns:
            List of successfully created output file paths
        """
        output_paths = []
        for path in input_paths:
            result = self.clean_file(path)
            if result:
                output_paths.append(result)
        return output_paths
