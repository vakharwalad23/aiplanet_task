from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.document import Document
from schemas.chat import Message, ChatRequest, ChatResponse
from services.document import document_service
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from prompts.prompt import PDFChatPrompts
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq

class ChatService:
    def create_chain(self, llm, prompt):
        chain = (
            {
                "context": RunnablePassthrough(),
                "chat_history": lambda x: x["chat_history"],
                "question": RunnablePassthrough()
            }
            | prompt
            | llm
            | StrOutputParser()
        )
        return chain

    async def process_chat(self, db: Session, chat_request: ChatRequest) -> ChatResponse:
        document = await document_service.get_document(db, chat_request.document_id)
        
        # Load vector store
        embeddings = OpenAIEmbeddings()
        vectorstore = Chroma(
            persist_directory=f"vectorstore/{chat_request.document_id}",
            embedding_function=embeddings
        )
        
         # Get vector store results
        docs = vectorstore.similarity_search(chat_request.message)
        context = "\n".join([doc.page_content for doc in docs])
        
        # Setup chat template with history
        llm = ChatGroq(temperature=0, model_name="llama-3.3-70b-versatile")
        template = PDFChatPrompts.get_chat_template()
        
        # Prepare inputs
        inputs = PDFChatPrompts.get_context_with_history(
            context=context,
            chat_history=chat_request.chat_history,
            question=chat_request.message
        )
        # Get response
        chain = self.create_chain(llm=llm, prompt=template)
        response = chain.invoke(inputs)
        
        # Create and save messages
        ai_message = Message(role="ai", content=response)
        user_message = Message(role="user", content=chat_request.message)
        new_history = chat_request.chat_history + [user_message, ai_message]
        
        # Update document history
        document.chat_history = [msg.model_dump() for msg in new_history]
        db.commit()
        
        return ChatResponse(
            document_id=chat_request.document_id,
            message=ai_message,
            chat_history=new_history
        )

chat_service = ChatService()