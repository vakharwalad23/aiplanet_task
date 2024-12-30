from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from services.document import document_service
from schemas.document import DocumentResponse
from config import settings

router = APIRouter()

@router.post("/upload", response_model=DocumentResponse)
async def upload_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    content = await file.read()
    if len(content) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=400, detail="File too large")
    
    document = await document_service.create_document(db, content, file.filename)
    return {"document_id": document.id, "filename": document.filename}

@router.get("/download/{document_id}")
async def get_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    url = await document_service.get_download_url(db, document_id)
    return {"url": url}

@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    await document_service.delete_document(db, document_id)
    return {"message": "Document deleted successfully"}