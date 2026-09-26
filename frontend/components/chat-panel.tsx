"use client"
import { ChatMessage } from "./chat-message";
import { ChatInput } from "./chat-input";
import { useState, useEffect } from "react";
import { fetchMessages, Message } from "@/lib/services/chat";

export function ChatPanel({ conversationId }: { conversationId?: number }) {
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState(!!conversationId)

  useEffect(() => {
    if (!conversationId) return
    fetchMessages(conversationId)
      .then((res) => setMessages(res.data))
      .catch(() => setMessages([]))
      .finally(() => setLoading(false))

    console.log(conversationId, messages)
  }, [conversationId])

  return (
    <div className="flex flex-1 flex-col h-screen min-w-0">
      {/* Header */}
      <div className="flex h-14 items-center border-b px-4">
        <h2 className="text-sm font-medium">Document.pdf</h2>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 min-w-0">
        <div className="mx-auto max-w-3xl w-full">
          {messages.map((message) => (
            <ChatMessage key={message.id} role={message.role} content={message.content} />
          ))}
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