export interface Message {
  role: string;
  content: string;
}

export interface DocumentResponse {
  document_id: string;
  filename: string;
}

export interface ChatResponse {
  document_id: string;
  message: Message;
  chat_history: Message[];
}

export interface ChatRequest {
  document_id: string;
  message: string;
  chat_history: Message[];
}
