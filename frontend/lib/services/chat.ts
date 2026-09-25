import { api } from "@/lib/api";
import { AxiosResponse } from "axios";

export interface Conversation {
  id: number;
  created_at: string;
  user_id: number;
  title: string;
}

export async function fetchChats():Promise<AxiosResponse<Conversation[]>>{
    const response = await api.get<Conversation[]>("/chat/conversations")
    return response
}