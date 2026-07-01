export interface DocumentMeta {
  id: string;
  name: string;
  file_path: string;
  language: string;
  type: string;
  category: string;
  extraction_type: string;
  source: string;
  status: string;
}

export interface UploadResult {
  document: DocumentMeta;
  chunks_indexed: number;
}
