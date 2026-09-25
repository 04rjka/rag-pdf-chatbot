"use client"
import { useEffect, useState } from "react";
import { fetchChats, Conversation } from "@/lib/services/chat"

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

  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div className="flex flex-col flex-1 items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      CONV
      {chats.length === 0 ? (
        <p className="text-sm text-muted-foreground">No conversations yet</p>
      ) : (
        chats.map((c) => (
          <div key={c.id} className="rounded-lg border p-3">
            <h3 className="font-medium">{c.title}</h3>
            <p className="text-sm text-muted-foreground">
              {new Date(c.created_at).toLocaleString()}
            </p>
          </div>
        ))
      )}
    </div>
  );
}
