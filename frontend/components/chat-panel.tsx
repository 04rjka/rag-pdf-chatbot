"use client"
import { ChatMessage } from "./chat-message";
import { ChatInput } from "./chat-input";
import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { fetchMessages, Message, askQuestion } from "@/lib/services/chat";
import { Loader2 } from "lucide-react";

export function ChatPanel({ conversationId, documentId }: { conversationId?: number, documentId?: number }) {
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState(!!conversationId)
  const [sending, setSending] = useState(false)
  const router = useRouter()
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!conversationId) return
    fetchMessages(conversationId)
      .then((res) => setMessages(res.data))
      .catch(() => setMessages([]))
      .finally(() => setLoading(false))

    console.log(conversationId, messages)
  }, [conversationId])

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  async function handleSend(question: string) {
    const userMsg: Message = { id: Date.now(), role: "user", content: question, created_at: "" }
    const botMsg: Message = { id: Date.now() + 1, role: "bot", content: "", created_at: "" }
    setMessages((prev) => [...prev, userMsg, botMsg])

    setSending(true)
    await askQuestion(question, conversationId, documentId, (newConversationId) => {
      if (!conversationId) router.replace(`chat/${newConversationId}`)
    },
      (token) => {
        setMessages((prev) => {
          const updated = [...prev]
          updated[updated.length - 1] = {
            ...updated[updated.length - 1],
            content: updated[updated.length - 1].content + token,
          }
          return updated
        })
      })
    setSending(false)
  }
  return (
    <div className="flex flex-1 flex-col h-full min-w-0">
      {/* Header */}
      <div className="flex h-14 items-center border-b px-4">
        <h2 className="text-sm font-medium">Document.pdf</h2>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 min-w-0">
        {
          loading ? (
            <div className="flex items-center justify-center h-full">
              <Loader2 className="h-5 w-5 animate-spin text-muted-foreground" />
            </div>
          ) : (
            <div className="mx-auto max-w-3xl w-full">
              {messages.map((message) => (
                <ChatMessage key={message.id} role={message.role} content={message.content} />
              ))}
              {sending && (
                <div className="text-sm text-muted-foreground px-1">Thinking...</div>
              )}
              <div ref={bottomRef} />
            </div>
          )
        }

      </div>

      {/* Input */}
      <div className="border-t p-4 min-w-0">
        <div className="mx-auto max-w-3xl w-full">
          <ChatInput onSend={handleSend} disabled={loading || sending} />
        </div>
      </div>
    </div>
  );
}