import React from "react";
import { Send } from "lucide-react";

interface MessageInputProps {
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onSubmit: (e: React.FormEvent) => void;
  disabled: boolean;
  loading: boolean;
}

export const MessageInput: React.FC<MessageInputProps> = ({
  value,
  onChange,
  onSubmit,
  disabled,
  loading,
}) => (
  <form onSubmit={onSubmit} className="p-4 border-t">
    <div className="flex items-center bg-gray-50 rounded-lg px-4 py-2">
      <input
        type="text"
        value={value}
        onChange={onChange}
        placeholder="Send a message..."
        className="flex-1 bg-transparent outline-none"
        disabled={disabled || loading}
      />
      <button
        type="submit"
        className={`ml-2 ${loading ? "text-gray-300" : "text-gray-400 hover:text-gray-600"}`}
        disabled={disabled || loading}
      >
        <Send className="w-5 h-5" />
      </button>
    </div>
  </form>
);
