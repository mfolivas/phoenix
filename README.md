# Entity Extraction Application

This project is a proof-of-concept (POC) for extracting named entities and their relationships from unstructured text/Markdown files. It is built with FastAPI, uses spaCy for Named Entity Recognition (NER), and implements a simple heuristic for relationship identification. The code follows Domain-Driven Design (DDD), SOLID principles, and Test-Driven Development (TDD) best practices.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [Installation](#installation)
5. [Running the Application](#running-the-application)
6. [API Usage](#api-usage)
7. [Example Using docs/ProjectPhoenixPlan.md](#example-using-docsprojectphoenixplanmd)
8. [Running Tests](#running-tests)
9. [Docker Support](#docker-support)
10. [Additional Notes](#additional-notes)

---

## 1. Overview

The goal of this application is to:
- Extract entities (such as people, organizations, and locations) from unstructured text/Markdown files.
- Identify relationships between these entities based on their proximity in sentences.
- Provide an API endpoint that accepts text/Markdown input and returns the extracted entities and relationships in a structured JSON format.

---

## 2. Features

- **Entity Extraction:** Uses spaCy's pre-trained model to extract entities.
- **Relationship Identification:** Applies a simple heuristic to infer relationships between entities appearing in the same sentence.
- **API Endpoint:** Built with FastAPI to facilitate development and testing.
- **Custom NER Model Support:** A directory (`custom_ner_model`) is provided to support custom spaCy NER models.
- **Testing:** The project follows TDD and BDD practices. Sample tests use the file `docs/ProjectPhoenixPlan.md` as input.

---

## 3. Project Structure

Below is the project structure:

```bash
.
├── Dockerfile
├── README.md
├── custom_ner_model
│   └── (custom model files)
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

**POST** `/extract`

### Request Body

The API expects a JSON object with the following fields:
- **content** (string): The unstructured text or Markdown content.
- **entity_types** (array of strings, optional): Specify entity types to filter (e.g., `["PERSON", "ORG"]`).
- **relationship_threshold** (number, optional): A threshold for filtering weak relationships (for future enhancements).

#### Sample Request

```json
{
  "content": "Alice and Bob visited Paris. They met with Charlie in the city.",
  "entity_types": null,
  "relationship_threshold": 0.5
}
```

### Response

The API returns a JSON object with:
- **entities:** An array of entities (each with name, type, and confidence).
- **relationships:** An array of relationships (each with source, target, relation, and strength).

#### Sample Response
```json
{
  "entities": [
    { "name": "Alice", "type": "PERSON", "confidence": 1.0 },
    { "name": "Bob", "type": "PERSON", "confidence": 1.0 },
    { "name": "Paris", "type": "GPE", "confidence": 1.0 },
    { "name": "Charlie", "type": "PERSON", "confidence": 1.0 }
  ],
  "relationships": [
    { "source": "Alice", "target": "Bob", "relation": "related_to", "strength": 1.0 },
    { "source": "Alice", "target": "Paris", "relation": "related_to", "strength": 0.5 },
    { "source": "Bob", "target": "Paris", "relation": "related_to", "strength": 0.5 },
    { "source": "Bob", "target": "Charlie", "relation": "related_to", "strength": 0.33 },
    { "source": "Paris", "target": "Charlie", "relation": "related_to", "strength": 0.33 }
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