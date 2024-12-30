from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from typing import List
from schemas.chat import Message

class PDFChatPrompts:
    SYSTEM_TEMPLATE = """You are an AI assistant analyzing PDF documents. Your role is to:
- Provide accurate answers based on document content
- Stay within the context provided
- Be clear and concise in responses
- Admit when information is not available in the context

Context from the PDF:
{context}

Previous conversation:
{chat_history}"""

    @classmethod
    def get_chat_template(cls) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(cls.SYSTEM_TEMPLATE),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{question}")
        ])
    
    @classmethod
    def format_chat_history(cls, messages: List[Message]) -> List[dict]:
        formatted_messages = []
        for msg in messages:
            formatted_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        return formatted_messages
    
    @classmethod
    def get_context_with_history(cls, context: str, chat_history: List[Message], question: str) -> dict:
        return {
            "context": context,
            "chat_history": cls.format_chat_history(chat_history),
            "question": question
        }