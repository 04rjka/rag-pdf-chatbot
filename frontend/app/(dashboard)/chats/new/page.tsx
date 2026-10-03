"use client"
import { useSearchParams } from "next/navigation";
import { ChatPanel } from "@/components/chat-panel";

export default function NewChatPage() {
  const searchParams = useSearchParams();
  const documentId = searchParams.get("document");

  return (
    <ChatPanel documentId={documentId ? Number(documentId) : undefined} />
  );
}