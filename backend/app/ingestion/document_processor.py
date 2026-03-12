from typing import List, Dict
from pypdf import PdfReader
import re

class DocumentProcessor:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def process_pdf(self, file_path: str, metadata: Dict = None) -> List[Dict]:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        
        return self._chunk_text(text, metadata or {"source": file_path})
    
    def process_text(self, text: str, metadata: Dict = None) -> List[Dict]:
        return self._chunk_text(text, metadata or {})
    
    def _chunk_text(self, text: str, metadata: Dict) -> List[Dict]:
        text = re.sub(r'\s+', ' ', text).strip()
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end]
            
            if chunk:
                chunks.append({
                    "text": chunk,
                    "metadata": {
                        **metadata,
                        "chunk_index": len(chunks)
                    }
                })
            
            start += self.chunk_size - self.chunk_overlap
        
        return chunks
