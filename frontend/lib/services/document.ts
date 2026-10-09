import { api } from "@/lib/api";

export interface Document {
  id: number;
  filename: string;
  file_path: string;
  created_at: string;
}

export async function uploadDocument(file: File) {
  const formData = new FormData();
  formData.append("file", file);
  return api.post<Document>("/documents/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
}

export async function getDocuments() {
  const response = await api.get("/documents")
  return response
}

export function fetchDocument(id: number) {
  return api.get<Document>(`/documents/${id}`);
}