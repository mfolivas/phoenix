"""
Module: config
Holds configuration settings for the application.
"""

# Extraction mode can be set to "local" for spaCy or "aws" for AWS Comprehend.
EXTRACTION_MODE = "local"

# spaCy model configuration
SPACY_MODEL = "en_core_web_md"

# Logging configuration can be set here or in the entry point of the application.