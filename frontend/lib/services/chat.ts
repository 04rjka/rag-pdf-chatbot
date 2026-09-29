import { api } from "@/lib/api";
import { AxiosResponse } from "axios";

export interface Conversation {
  id: number;
  created_at: string;
  user_id: number;
  title: string;
}

export interface Message {
  id: number;
  role: "user" | "bot";
  content: string;
  created_at: string;
}

export async function fetchChats():Promise<AxiosResponse<Conversation[]>>{
    const response = await api.get<Conversation[]>("/chat/conversations")
    return response
}

export async function fetchMessages(conversationId: number): Promise<AxiosResponse<Message[]>> {
  return api.get<Message[]>(`/chat/conversations/${conversationId}/messages`);
}

export async function askQuestion(
  question: string,
  conversationId: number | undefined,
  documentId: number | undefined,
  onMetadata: (conversationId: number) => void,
  onToken: (token: string) => void
): Promise<void> {
  const res = await fetch(`/api/v1/chat`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    question,
    conversation_id: conversationId ?? null,
    document_id: documentId ?? null,
  }),
});

  if (!res.body) throw new Error("No response body");

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });

    const lines = buffer.split("\n\n");
    buffer = lines.pop() ?? "";

    for (const line of lines) {
      if (!line.startsWith("data: ")) continue;
      const data = line.slice(6);
      if (data === "[DONE]") return;

      const parsed = JSON.parse(data);
      if (parsed.type === "metadata") onMetadata(parsed.conversation_id);
      if (parsed.type === "token") onToken(parsed.content);
    }
  }
}