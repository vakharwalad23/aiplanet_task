import React, { useRef, useEffect } from "react";
import { Message } from "../../types";
import { ChatMessage } from "../ChatMessage/ChatMessage";
import { MessageSkeleton } from "../MessageSkeleton/MessageSkeleton";

interface ChatAreaProps {
  messages: Message[];
  loading?: boolean;
}

export const ChatArea: React.FC<ChatAreaProps> = ({
  messages,
  loading = false,
}) => {
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {messages.map((message, index) => (
        <ChatMessage key={index} message={message} />
      ))}
      {loading && (
        <>
          <MessageSkeleton />
          <MessageSkeleton />
          <MessageSkeleton />
        </>
      )}
      <div ref={chatEndRef} />
    </div>
  );
};
