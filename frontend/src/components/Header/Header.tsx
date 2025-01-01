import React from "react";
import { Plus, FileText, Loader2 } from "lucide-react"; // Add Loader2 import

interface HeaderProps {
  currentPdf: string | null;
  onFileUpload: (event: React.ChangeEvent<HTMLInputElement>) => void;
  loading?: boolean; // Add loading prop
}

export const Header: React.FC<HeaderProps> = ({
  currentPdf,
  onFileUpload,
  loading = false,
}) => (
  <header className="flex items-center justify-between p-4 border-b">
    <div className="flex items-center space-x-2">
      <span className="font-medium">PDF Chat</span>
    </div>

    <div className="flex items-center space-x-4">
      {loading ? (
        <div className="flex items-center text-gray-600">
          <Loader2 className="w-4 h-4 mr-2 animate-spin" />
          <span>Loading PDF...</span>
        </div>
      ) : (
        currentPdf && (
          <div className="flex items-center text-green-600">
            <FileText className="w-4 h-4 mr-2" />
            <span>{currentPdf}</span>
          </div>
        )
      )}
      <label
        className={`flex items-center px-4 py-2 rounded-lg border border-gray-200 
        ${loading ? "opacity-50 cursor-not-allowed" : "hover:bg-gray-50 cursor-pointer"}`}
      >
        {loading ? (
          <Loader2 className="w-4 h-4 mr-2 animate-spin" />
        ) : (
          <Plus className="w-4 h-4 mr-2" />
        )}
        <span>Upload PDF</span>
        <input
          type="file"
          className="hidden"
          accept=".pdf"
          onChange={onFileUpload}
          disabled={loading}
        />
      </label>
    </div>
  </header>
);
