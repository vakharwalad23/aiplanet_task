# PDF Chatbot Architecture

## System Components

### Backend Components

1. **FastAPI Application Layer**
   - Handles HTTP requests and routing
   - Manages API endpoints for document operations and chat
   - Implements OpenAPI/Swagger documentation

2. **Database Layer (SQLite)**
   - Stores document metadata
   - Manages chat history
   - Tracks document processing status

3. **Storage Layer (MinIO)**
   - Object storage for PDF documents
   - Handles document upload/download
   - Manages file persistence

4. **Document Processing Service**
   - PDF text extraction
   - Document preprocessing
   - Vector embeddings generation
   - Chunk management

5. **Chat Service**
   - Manages conversation context
   - Processes user queries
   - Generates responses based on document content

### Frontend Components

1. **React Application**
   - Document upload interface
   - Chat interface
   - Document management UI

2. **Tanstack Router**
   - Route management
   - Navigation state
   - URL handling

## Data Flow

1. **Document Upload Flow**
```
User → Frontend → Backend API → MinIO Storage
                            → SQLite (metadata)
                            → Document Processing
```

2. **Chat Flow**
```
User Query → Frontend → Backend API → Chat Service
                                  → Document Retrieval
                                  → Response Generation
```

## Component Interactions

1. **Document Processing**
   - Frontend uploads PDF to `/api/v1/documents/upload`
   - Backend stores file in MinIO
   - Processing service extracts text and generates embeddings
   - Metadata stored in SQLite

2. **Chat Processing**
   - Frontend sends query to `/api/v1/chat/`
   - Chat service retrieves relevant document chunks
   - Generates contextual response
   - Returns formatted response to frontend

## Security & Performance

- Document size limits
- Chunked upload/download
- Concurrent request handling
- Database connection pooling
