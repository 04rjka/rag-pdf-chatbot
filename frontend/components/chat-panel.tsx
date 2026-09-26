"use client"
import { ChatMessage } from "./chat-message";
import { ChatInput } from "./chat-input";
export function ChatPanel() {
  return (
    <div className="flex flex-1 flex-col h-screen min-w-0">
      {/* Header */}
      <div className="flex h-14 items-center border-b px-4">
        <h2 className="text-sm font-medium">Document.pdf</h2>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 min-w-0">
        <div className="mx-auto max-w-3xl w-full">
          <ChatMessage role="user" content="What is this document about?" />
          <ChatMessage role="bot" content="This document covers..." />
        </div>
      </div>

      {/* Input */}
      <div className="border-t p-4 min-w-0">
        <div className="mx-auto max-w-3xl w-full">
          <ChatInput onSend={(msg) => console.log(msg)} />
        </div>
      </div>
    </div>
  );
}