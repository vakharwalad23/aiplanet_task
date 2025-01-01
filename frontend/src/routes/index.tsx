import React, { useState } from "react";
import { Header } from "../components/Header/Header";
import { ChatArea } from "../components/ChatArea/ChatArea";
import { MessageInput } from "../components/MessageInput/MessageInput";
import { Message } from "../types";
import { api } from "../lib/api";
import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/")({
  component: Index,
});

function Index(): JSX.Element {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState("");
  const [currentPdf, setCurrentPdf] = useState<string | null>(null);
  const [documentId, setDocumentId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [fileUploading, setFileUploading] = useState(false);
  const handleFileUpload = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];
    if (file && file.type === "application/pdf") {
      setFileUploading(true);
      try {
        const data = await api.uploadPdf(file);
        setDocumentId(data.document_id);
        setCurrentPdf(data.filename);
        setMessages([]);
      } catch (error) {
        console.error("Error uploading file:", error);
      } finally {
        setFileUploading(false);
      }
    }
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (inputMessage.trim() && documentId) {
      setLoading(true);
      try {
        const response = await api.sendMessage({
          document_id: documentId,
          message: inputMessage,
          chat_history: messages,
        });
        setMessages(response.chat_history);
      } catch (error) {
        console.error("Error sending message:", error);
      } finally {
        setLoading(false);
        setInputMessage("");
      }
    }
  };

  return (
    <div className="flex flex-col h-screen bg-white">
      <Header
        currentPdf={currentPdf}
        onFileUpload={handleFileUpload}
        loading={fileUploading}
      />
      <ChatArea messages={messages} loading={loading} />
      <MessageInput
        value={inputMessage}
        onChange={(e) => setInputMessage(e.target.value)}
        onSubmit={handleSendMessage}
        disabled={!documentId}
        loading={loading}
      />
    </div>
  );
}
