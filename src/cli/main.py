"""
Command-line interface for ResumeUnmark.

This module provides the CLI entry point for the desktop application.
"""

import sys
import os
from typing import NoReturn

from ..core import PDFCleaner
from ..utils import find_pdf_files, normalize_path


def main() -> NoReturn:
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("╔════════════════════════════════════════════════════════╗")
        print("║              ResumeUnmark - PDF Cleaner               ║")
        print("╚════════════════════════════════════════════════════════╝")
        print()
        print("Usage:")
        print("  • Drag & Drop PDF files or folders onto ResumeUnmark.exe")
        print("  • Or run: ResumeUnmark.exe <path_to_pdf_or_folder>")
        print()
        print("The cleaned files will be saved with '_clean.pdf' suffix.")
        print()
        input("Press Enter to exit...")
        sys.exit(0)
    
   
    cleaner = PDFCleaner()
    
    total_processed = 0
    total_success = 0
    
    # Process all provided paths
    for target_path in sys.argv[1:]:
        target_path = normalize_path(target_path)
        
        if not os.path.exists(target_path):
            print(f"[ERROR] Path not found: {target_path}")
            continue
        
        # Find all PDF files in the path
        pdf_files = find_pdf_files(target_path)
        
        if not pdf_files:
            if os.path.isdir(target_path):
                print(f"[INFO] No PDF files found in: {target_path}")
            else:
                print(f"[SKIP] Not a PDF: {target_path}")
            continue
        
        if os.path.isdir(target_path):
            print(f"\n📁 Processing folder: {target_path}")
            print(f"   Found {len(pdf_files)} PDF file(s)")
        
        # Process all found PDFs
        for pdf_file in pdf_files:
            total_processed += 1
            result = cleaner.clean_file(pdf_file)
            if result:
                total_success += 1
    
    # Summary
    print("\n" + "═" * 60)
    print(f"✨ Finished! Processed: {total_processed} | Success: {total_success}")
    print("═" * 60)
    
    # Keep window open for user to see results
    input("\nPress Enter to exit...")
    sys.exit(0)


if __name__ == "__main__":
    main()
