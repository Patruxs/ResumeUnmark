"""Utility functions for file and folder processing."""

import os
from typing import List


def find_pdf_files(path: str, exclude_cleaned: bool = True) -> List[str]:
    """
    Find all PDF files in a path (file or directory).
    
    Args:
        path: File path or directory path
        exclude_cleaned: If True, exclude files already ending with '_clean.pdf'
        
    Returns:
        List of PDF file paths
    """
    pdf_files = []
    
    if os.path.isfile(path):
        if path.lower().endswith(".pdf"):
            if not exclude_cleaned or "_clean" not in path:
                pdf_files.append(path)
    
    elif os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.lower().endswith(".pdf"):
                    if not exclude_cleaned or "_clean" not in file:
                        pdf_files.append(os.path.join(root, file))
    
    return pdf_files


def get_file_size_mb(path: str) -> float:
    """
    Get file size in megabytes.
    
    Args:
        path: File path
        
    Returns:
        File size in MB
    """
    if not os.path.isfile(path):
        return 0.0
    return os.path.getsize(path) / (1024 * 1024)


def normalize_path(path: str) -> str:
    """
    Normalize a file path by removing quotes and expanding user home.
    
    Args:
        path: Raw path string
        
    Returns:
        Normalized path
    """
    return os.path.expanduser(path.strip('"').strip("'"))
