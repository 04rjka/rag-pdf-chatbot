"use client"
import { useEffect, useState } from "react";
import { fetchChats, Conversation } from "@/lib/services/chat"
import Link from "next/link";
import { Loader2 } from "lucide-react";

export default function Home() {
  const [chats, setChats] = useState<Conversation[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchChats()
      .then((res) => {
        console.log("API response:", res.data);
        setChats(res.data)
      })
      .catch(() => setError("Failed to load chats"))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return (
  <div className="flex flex-1 items-center justify-center">
    <Loader2 className="h-5 w-5 animate-spin text-muted-foreground" />
  </div>
)
  if (error) return <p>{error}</p>;

  return (<div className="flex flex-col flex-1 items-center justify-start bg-background font-sans p-3">
    {chats.length === 0 ? (
      <p className="text-sm text-muted-foreground">No conversations yet</p>
    ) : (
      chats.map((c) => (
        <Link key={c.id} href={`chats/${c.id}`} className="mb-2 rounded-lg border border-border p-3 flex gap-5 justify-between items-center hover:bg-muted w-full max-w-xl">
          <h3 className="font-medium text-foreground truncate min-w-0">{c.title}</h3>
          <p className="text-sm text-muted-foreground">
            {new Date(c.created_at).toLocaleString()}
          </p>
        </Link>
      ))
    )}
  </div>
  );
}
