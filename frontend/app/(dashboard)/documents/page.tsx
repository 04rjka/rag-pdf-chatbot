"use client"
import { getDocuments, Document } from "@/lib/services/document";
import { useState, useEffect } from "react";
import Link from "next/link";
import { Loader2 } from "lucide-react";

export default function DocumentPage() {
  const [documents, setDocuments] = useState<Document[]>([])
  const [loading, setLoading] = useState(true)
  useEffect(() => {
    getDocuments().then((res) => setDocuments(res.data))
      .catch(() => setDocuments([]))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return (
    <div className="flex flex-1 items-center justify-center">
      <Loader2 className="h-5 w-5 animate-spin text-muted-foreground" />
    </div>
  )

  return (
    <div className="flex flex-col flex-1 items-center justify-start bg-background font-sans p-3">
      {documents.length === 0 ? (
        <p className="text-sm text-muted-foreground">No documents yet</p>
      ) : (
        documents.map((doc) => (
          <Link
            key={doc.id}
            href={`/chats/new?document=${doc.id}`}
            className="mb-2 rounded-lg border border-border p-3 flex justify-between items-center hover:bg-muted w-full max-w-xl"
          >
            <div className="min-w-0">
              <p className="font-medium text-foreground truncate">{doc.filename}</p>
              <p className="text-xs text-muted-foreground">
                Uploaded {new Date(doc.created_at).toLocaleString()}
              </p>
            </div>
            <span className="text-sm text-primary whitespace-nowrap">Start chat →</span>
          </Link>
        ))
      )}
    </div>
  )
}
