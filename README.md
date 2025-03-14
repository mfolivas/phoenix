# Entity Extraction Application

This project is a proof-of-concept (POC) for extracting entities and relationships from unstructured text/Markdown using spaCy for Named Entity Recognition (NER). The application is built with FastAPI and follows Domain-Driven Design (DDD) and SOLID principles.

## Overview

### Entity Extraction from Unstructured Text/Markdown
This application provides an approach to extract entities (e.g., people, organizations, locations) and identify relationships within text/Markdown files.

### Development of an API Endpoint
The application exposes a Python-based API endpoint using FastAPI that:
- Accepts text/Markdown content as input
- Returns detected entities and their relationships in a structured format (JSON, CSV, Excel, or Parquet)

### Tools and Methodologies
- **NER Framework**: spaCy for named entity recognition with the en_core_web_md model
- **API Framework**: FastAPI for creating RESTful API endpoints
- **Architecture**: Domain-Driven Design (DDD) and SOLID principles

### Additional Features
- **Graph Visualization**: Visualize extracted nodes and their relationships
- **Configurable Entity Types & Relationship Threshold**: Configure entity types and set a threshold for the "strength" of relationships
- **Document Parsing from PDFs**: Parse PDF documents to extract text before performing entity extraction

## Project Structure

- **docs/**: Contains documentation, including the ProjectPhoenixPlan.md.
- **src/**: Source code for the application.
  - **api/**: FastAPI application code.
  - **domain/**: Domain models and service interfaces.
  - **infrastructure/**: Implementations of NER using spaCy (and AWS as an alternative) and PDF parsing.
  - **config/**: Configuration settings.
- **tests/**: BDD-style tests using pytest.
- **requirements.txt**: Python dependencies.
- **README.md**: Project overview and instructions.

## Running the Application

1. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    python -m spacy download en_core_web_md
    ```
2. **Run the FastAPI server:**
    ```bash
    uvicorn src.api.main:app --reload
    ```
3. **Access the API documentation** at [http://localhost:8000/docs](http://localhost:8000/docs).

## Testing

Run tests with:
```bash
pytest tests/
```
