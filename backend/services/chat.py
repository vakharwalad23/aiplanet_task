from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.document import Document
from schemas.chat import Message, ChatRequest, ChatResponse
from services.document import document_service
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI

class ChatService:
    def __init__(self):
        self.conversation_memories = {}
    
    def get_or_create_memory(self, document_id: str):
        if document_id not in self.conversation_memories:
            self.conversation_memories[document_id] = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
        return self.conversation_memories[document_id]
    
    async def process_chat(self, db: Session, chat_request: ChatRequest) -> ChatResponse:
        document = await document_service.get_document(db, chat_request.document_id)
        
        # Load vector store
        embeddings = OpenAIEmbeddings()
        vectorstore = Chroma(
            persist_directory=f"vectorstore/{chat_request.document_id}",
            embedding_function=embeddings
        )
        
        # Get conversation memory
        memory = self.get_or_create_memory(chat_request.document_id)
        
        # Create QA chain
        qa_chain = load_qa_chain(
            OpenAI(temperature=0),
            chain_type="stuff",
            memory=memory
        )
        
        # Get relevant documents
        docs = vectorstore.similarity_search(chat_request.message)
        
        # Get answer
        response = qa_chain.run(
            input_documents=docs,
            question=chat_request.message
        )
        
        # Create messages
        ai_message = Message(role="ai", content=response)
        user_message = Message(role="user", content=chat_request.message)
        
        # Update chat history
        new_history = chat_request.chat_history + [user_message, ai_message]
        document.chat_history = [msg.model_dump() for msg in new_history]
        db.commit()
        
        return ChatResponse(
            document_id=chat_request.document_id,
            message=ai_message,
            chat_history=new_history
        )

chat_service = ChatService()