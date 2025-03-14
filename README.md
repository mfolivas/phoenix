# Entity Extraction Application

This project is a proof-of-concept (POC) for extracting named entities and their relationships from unstructured text/Markdown files. It is built with FastAPI and uses spaCy for Named Entity Recognition (NER). Our design follows Domain-Driven Design (DDD), SOLID principles, and Test-Driven Development (TDD) best practices.

> **Note:** The default spaCy model (`en_core_web_md`) may misclassify some entities (e.g., "São Paulo" as a PERSON). This README explains how you can train a custom NER model with your own annotated data to better capture domain-specific entities like locations and employee counts.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [Installation](#installation)
5. [Running the Application](#running-the-application)
6. [API Usage](#api-usage)
7. [Custom NER Model Training](#custom-ner-model-training)
8. [Running Tests](#running-tests)
9. [Docker Support](#docker-support)
10. [Additional Notes](#additional-notes)

---

## 1. Overview

The goal of this application is to:
- Extract entities (e.g., people, organizations, locations, employee counts) from unstructured text/Markdown files.
- Identify relationships between these entities based on their proximity in sentences.
- Provide an API endpoint that accepts a file upload and returns the extracted entities and relationships in a structured JSON format.

---

## 2. Features

- **Entity Extraction:**  
  Uses spaCy’s pre-trained model (`en_core_web_md`) to extract entities. (Custom training is supported to improve accuracy.)
  
- **Relationship Identification:**  
  Applies a simple heuristic to infer relationships between entities found in the same sentence, with a computed "strength" based on token distance.

- **API Endpoint:**  
  A file upload endpoint (`/upload-file`) built with FastAPI that accepts multipart/form-data.

- **Custom NER Model Support:**  
  A directory (`custom_ner_model`) is provided for custom model training, so you can improve entity recognition (e.g., ensuring that "São Paulo" is classified as a location and "2,000 employees" is recognized as employee count).

- **Extensible and Modular Design:**  
  The project follows DDD and SOLID principles, making it easy to swap out components (like using AWS Comprehend instead of spaCy) without affecting the rest of the system.

---

## 3. Project Structure

Below is the project structure:

```bash
.
├── Dockerfile
├── README.md
├── custom_ner_model
│   └── (custom model files, config.cfg, training data, etc.)
├── docs
│   └── ProjectPhoenixPlan.md
├── requirements.txt
├── requirements-dev.txt
├── src
│   ├── api
│   │   └── main.py
│   ├── config
│   │   └── config.py
│   ├── domain
│   │   ├── entities.py
│   │   └── services.py
│   └── infrastructure
│       ├── local_extraction.py
│       ├── aws_extraction.py
│       └── pdf_parser.py
└── tests
    └── test_entity_extraction.py
```

## 4. Installation

### Production Dependencies

Install the required libraries by running:

```bash
pip install -r requirements.txt
```
### Development Dependencies

For testing and development tools, run:
```bash 
pip install -r requirements-dev.txt
```
## 5. Running the Application

Start the FastAPI server with Uvicorn by executing:

```bash
uvicorn src.api.main:app --reload
```

Once the server is running, open your browser and navigate to:
`http://localhost:8000/docs`

This URL provides interactive API documentation (Swagger UI) where you can test the endpoints.

## 6. API Usage

### Endpoint

**POST** `/upoad-file`
This endpoint accepts a file (plain text or Markdown) and optional form parameters.

### Form Data Fields

The API expects a JSON object with the following fields:
- **file**: The file to upload.
- **entity_types (optional)**: A comma-separated list of entity types to filter (e.g., PERSON,ORG).
- **relationship_threshold (optional)**: A number indicating the minimum relationship strength to consider. Default is 0.5.


#### Sample Request using cURL

```bash
curl -X POST "http://localhost:8000/upload-file" \
     -F "file=@docs/ProjectPhoenixPlan.md" \
     -F "entity_types=PERSON,ORG" \
     -F "relationship_threshold=0.5"
```

### Response

The API returns a JSON object with:
- **entities:** An array of entities (each with name, type, and confidence).
- **relationships:** An array of relationships (each with source, target, relation, and strength).

#### Sample Response
```json
{
  "entities": [
    { "name": "Expand Redwood Tech Solutions", "type": "ORG", "confidence": 1.0 },
    { "name": "Michael Lansing", "type": "PERSON", "confidence": 1.0 },
    { "name": "Sasha Petrov", "type": "PERSON", "confidence": 1.0 },
    { "name": "Redwood City, California", "type": "GPE", "confidence": 1.0 },
    { "name": "London", "type": "GPE", "confidence": 1.0 },
    { "name": "Tokyo", "type": "GPE", "confidence": 1.0 },
    { "name": "São Paulo", "type": "GPE", "confidence": 1.0 },
    { "name": "Melbourne", "type": "GPE", "confidence": 1.0 }
    // ... additional entities ...
  ],
  "relationships": [
    { "source": "Michael Lansing", "target": "Sasha Petrov", "relation": "related_to", "strength": 0.33 },
    { "source": "London", "target": "Tokyo", "relation": "related_to", "strength": 0.25 },
    // ... additional relationships ...
  ]
}
```
*Note:* Relationship strength values are based on token distances and may vary with different text inputs.

## 7. Example Using docs/ProjectPhoenixPlan.md

The file `docs/ProjectPhoenixPlan.md` contains sample text outlining the project plan. You can use it as input to the `/extract` endpoint.

For example, using cURL:
```bash
curl -X POST "http://localhost:8000/extract" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "'"$(cat docs/ProjectPhoenixPlan.md)"'",
    "entity_types": null,
    "relationship_threshold": 0.5
  }'
```

This command sends the contents of `ProjectPhoenixPlan.md` as the request payload. The response will include the entities and relationships extracted from that document.

## 8. Running Tests

To run the tests, execute:
```bash
pytest tests/
```

This will run all tests, including those that use the sample file `docs/ProjectPhoenixPlan.md` as input.

## 9. Docker Support

### Building the Docker Image

Build the Docker image by running:

```bash
docker build -t entity-extraction-app .
```
### Running the Container

Run the container with:

```bash
docker run -p 8000:8000 entity-extraction-app
```
The application will then be accessible at:

```bash
http://localhost:8000
```
## 10. Additional Notes

- **Custom NER Model:**  
  The `custom_ner_model` directory contains files for a custom spaCy NER model. To use this model, update your extraction service (in `src/infrastructure/local_extraction.py`) to load the custom model if desired.

- **Future Enhancements:**  
  Consider refining the relationship extraction logic using dependency parsing or additional heuristics. Configuration options for these enhancements can be added in `src/config/config.py`.

- **Logging:**  
  The application uses Python's built-in logging module. Logs are configured in `src/api/main.py` for consistent formatting and management.

---

Happy coding! For any questions or further assistance, please feel free to reach out.