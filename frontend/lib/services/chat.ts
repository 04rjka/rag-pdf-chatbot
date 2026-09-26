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