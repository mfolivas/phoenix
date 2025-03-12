# Entity Extraction Application

This project is a proof-of-concept (POC) for extracting entities and relationships from unstructured text/Markdown using spaCy for Named Entity Recognition (NER). The application is built with FastAPI and follows Domain-Driven Design (DDD) and SOLID principles.

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

