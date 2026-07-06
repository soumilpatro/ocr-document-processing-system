# OCR Document Processing System

## Overview

The OCR Document Processing System is a FastAPI-based backend application that extracts structured information from bank statement PDFs. It supports OCR-based text extraction, document parsing, validation, confidence scoring, document storage, and REST APIs for document management.

---

## Features

- Upload PDF bank statements
- OCR and text extraction
- Header extraction
  - Account Holder
  - Account Number
  - Branch
  - IFSC
  - Statement Date
  - Statement Period
- Transaction extraction
  - Date
  - Description
  - Debit
  - Credit
  - Balance
- Confidence scoring
- Document validation
- Duplicate document detection
- Search documents
- Retrieve document details
- Document status classification
- SQLite database storage
- Swagger API documentation
- Pytest unit testing
- Postman collection

---

## Tech Stack

- Python 3.13
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- PyPDF
- pdf2image
- Tesseract OCR
- Pillow
- Pytest
- Postman

---

## Project Structure

```
app/
│
├── config/
├── database/
├── models/
├── routers/
├── schemas/
├── services/
│   ├── confidence/
│   ├── extraction/
│   └── validation/
│
├── exceptions.py
├── error_handler.py
└── main.py

tests/

postman/

uploads/
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/soumilpatro/ocr-document-processing-system.git
```

Move into the project

```bash
cd ocr-document-processing-system
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the FastAPI server

```bash
uvicorn app.main:app --reload
```

Server

```
http://127.0.0.1:8000
```

Swagger UI

```
http://127.0.0.1:8000/docs
```

---

## Available APIs

### Upload Document

```
POST /api/documents/upload
```

Uploads a PDF and performs OCR, extraction, validation, and storage.

---

### Get All Documents

```
GET /api/documents
```

Returns all processed documents.

---

### Search Documents

```
GET /api/documents/search
```

Supports search by filename and status.

Example

```
/api/documents/search?filename=bank
```

```
/api/documents/search?status=OK
```

---

### Get Document by ID

```
GET /api/documents/{document_id}
```

Returns document details.

---

### Validate Document

```
POST /api/documents/{document_id}/validate
```

Returns

- Validation Errors
- Confidence Scores
- Document Status

---

## Running Tests

Execute all tests

```bash
pytest
```

Execute a specific test

```bash
pytest tests/test_upload.py
```

---

## Postman

The project includes a Postman collection inside the `postman/` folder for testing all APIs.

---

## Error Handling

The application handles

- Unsupported file type
- Empty PDF
- Duplicate document
- File too large
- Missing document
- Validation failures

---

## Future Improvements

- Multi-bank support
- Export extracted data to Excel/CSV
- JWT authentication
- Docker deployment
- Cloud database integration

---

## Author

Soumil Patro