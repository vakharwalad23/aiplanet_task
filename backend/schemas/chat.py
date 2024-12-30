from pydantic import BaseModel
from typing import List

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    document_id: str
    message: str
    chat_history: List[Message]

class ChatResponse(BaseModel):
    document_id: str
    message: Message
    chat_history: List[Message]