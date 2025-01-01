import React from "react";
import { Message } from "../../types";

interface ChatMessageProps {
  message: Message;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => (
  <div className="flex items-start space-x-3">
    <div
      className={`w-8 h-8 rounded-full flex items-center justify-center
      ${message.role === "user" ? "bg-purple-200" : "bg-green-100"}`}
    >
      {message.role === "user" ? "U" : "AI"}
    </div>
    <div className="flex-1">
      <p className="text-gray-800 whitespace-pre-wrap">{message.content}</p>
    </div>
  </div>
);
