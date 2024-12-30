from pydantic import BaseModel
from typing import List

class DocumentResponse(BaseModel):
    document_id: str
    filename: str