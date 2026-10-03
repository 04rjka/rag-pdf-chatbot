"use client"
import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Loader2, FileText } from "lucide-react"
import { uploadDocument } from "@/lib/services/document"

export default function UploadPage() {
    const [file, setFile] = useState<File | null>(null)
    const [uploading, setUploading] = useState(false)
    const [error, setError] = useState("")
    const router = useRouter()

    async function handleUpload() {
        if (!file) return
        setUploading(true)
        setError("")
        try {
            const res = await uploadDocument(file)
            router.push(`/chats/new?document=${res.data.id}`)
        } catch (err) {
            setError("Upload failed.")
            setUploading(false)
        }
    }
    return (
        <div className="flex flex-1 items-center justify-center p-4">
            <div className="w-full max-w-md space-y-4 text-center">
                <FileText className="mx-auto h-10 w-10 text-muted-foreground" />
                <h1 className="text-lg font-medium">Upload a document</h1>
                <p className="text-sm text-muted-foreground">
                    Upload a PDF to start chatting about it.
                </p>

                <input
                    type="file"
                    accept="application/pdf"
                    onChange={(e) => setFile(e.target.files?.[0] ?? null)}
                    disabled={uploading}
                    className="w-full text-sm"
                />

                {error && <p className="text-sm text-destructive">{error}</p>}

                <Button onClick={handleUpload} disabled={!file || uploading} className="w-full">
                    {uploading ? (
                        <>
                            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                            Uploading...
                        </>
                    ) : (
                        "Upload and start chat"
                    )}
                </Button>
            </div>
        </div>
    )
}