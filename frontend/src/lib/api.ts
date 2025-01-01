import { ChatRequest, ChatResponse, DocumentResponse, Message } from "../types";

export const api = {
  async uploadPdf(file: File): Promise<DocumentResponse> {
    const formData = new FormData();
    formData.append("file", file);
    const response = await fetch("/api/documents/upload", {
      method: "POST",
      body: formData,
    });
    return response.json();
  },

  async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(request),
    });
    return response.json();
  },

  async loadChatHistory(docId: string): Promise<Message[]> {
    const response = await fetch(`s/api/chat_history/${docId}`);
    return response.json();
  },
};
