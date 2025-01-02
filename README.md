# PDF Chatbot

A full-stack application that enables chatting with PDF documents. Built with FastAPI, React, and MinIO for object storage.

## Architecture

- **Backend**: FastAPI + SQLite + MinIO
- **Frontend**: React + Tanstack Router

## Prerequisites

- Python 3.8+
- Bun
- Docker & Docker Compose
- Ports 8000 and 5173 available

## API Documentation

Backend API documentation is available via Swagger UI at:

```
http://localhost:8000/docs
```

## API Endpoints

- `GET /health`: Health check
- `POST /api/v1/documents/upload`: Upload PDF
- `GET /api/v1/documents/download/{document_id}`: Download PDF
- `GET /api/v1/documents/{document_id}`: Get document info
- `POST /api/v1/chat/`: Chat endpoint

## Setup Instructions

### Backend Setup

1. Navigate to backend directory:

```bash
cd backend
```

2. Create environment file:

```bash
cp .env.example .env
# Configure environment variables as needed
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Start MinIO:

```bash
docker-compose up -d
```

5. Launch backend server:

```bash
python main.py
```

### Frontend Setup

1. Navigate to frontend directory:

```bash
cd frontend
```

2. Create environment file:

```bash
cp .env.example .env
# Configure environment variables as needed
```

3. Start development server:

```bash
bun run dev
```

Or build for production:

```bash
bun run build
```

## Usage

1. Access the application (default: http://localhost:5173)
2. Upload a PDF document and wait for processing
3. Start chatting about the PDF content
4. For API details, visit the Swagger documentation at http://localhost:8000/docs

## Notes

- Backend runs on port 8000
- Frontend development server runs on port 5173
- Ensure MinIO is running before starting the backend
