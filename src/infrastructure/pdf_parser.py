"""
Module: pdf_parser
Provides functionality to parse and extract text from PDF files.
"""

import pdfminer.high_level
import logging

# Get a logger for this module
logger = logging.getLogger(__name__)

def parse_pdf(file_path: str) -> str:
    """
    Extracts text from the specified PDF file.
    
    Args:
        file_path (str): The path to the PDF file.
        
    Returns:
        str: The extracted text from the PDF.
    """
    try:
        logger.info("Parsing PDF file: %s", file_path)
        text = pdfminer.high_level.extract_text(file_path)
        logger.info("PDF parsing successful.")
        return text
    except Exception as e:
        logger.exception("Error parsing PDF file: %s", e)
        raise