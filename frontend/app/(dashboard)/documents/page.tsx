"use client"
import { getDocuments, Document } from "@/lib/services/document";
import { useState, useEffect } from "react";
import Link from "next/link";
import { Loader2, FileText } from "lucide-react";
import { Button } from "@/components/ui/button";

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
        <div className="flex flex-1 flex-col items-center justify-center gap-3 text-center">
          <FileText className="h-10 w-10 text-muted-foreground" />
          <h2 className="text-lg font-medium">No documents yet</h2>
          <p className="text-sm text-muted-foreground max-w-xs">
            Upload a PDF and ask questions about it. Your documents will show up here.
          </p>
          <Button nativeButton={false} render={<Link href="/upload" />}>Upload a document</Button>
        </div>
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
