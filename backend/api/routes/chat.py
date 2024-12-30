from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from services.chat import chat_service
from schemas.chat import ChatRequest, ChatResponse

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat_with_pdf(
    chat_request: ChatRequest,
    db: Session = Depends(get_db)
):
    response = await chat_service.process_chat(db, chat_request)
    return response