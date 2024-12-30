from sqlalchemy import Column, String, DateTime, JSON
from db.session import Base
from datetime import datetime

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(String, primary_key=True)
    filename = Column(String, nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)
    object_name = Column(String, nullable=False)
    chat_history = Column(JSON, default=list)
    
    def __repr__(self):
        return f"<Document {self.filename}>"