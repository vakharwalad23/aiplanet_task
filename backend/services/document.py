from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.document import Document
from services.minio import minio_service
# from services.pdf import pdf_service
from typing import List, Optional
import uuid

class DocumentService:
    @staticmethod
    async def create_document(db: Session, file_content: bytes, filename: str) -> Document:
        doc_id = str(uuid.uuid4())
        object_name = f"{doc_id}/{filename}"
        
        # Upload to MinIO
        await minio_service.upload_file(file_content, object_name)
        
        # Process PDF
        # text = await pdf_service.extract_text(file_content)
        # await pdf_service.create_vector_store(text, doc_id)
        
        # Create database entry
        db_document = Document(
            id=doc_id,
            filename=filename,
            object_name=object_name
        )
        db.add(db_document)
        db.commit()
        db.refresh(db_document)
        
        return db_document
    
    @staticmethod
    async def get_document(db: Session, document_id: str) -> Optional[Document]:
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        return document
    
    @staticmethod
    async def delete_document(db: Session, document_id: str) -> bool:
        document = await DocumentService.get_document(db, document_id)
        await minio_service.delete_file(document.object_name)
        
        db.delete(document)
        db.commit()
        return True
    
    @staticmethod
    async def get_download_url(db: Session, document_id: str) -> str:
        document = await DocumentService.get_document(db, document_id)
        return minio_service.get_presigned_url(document.object_name)

document_service = DocumentService()