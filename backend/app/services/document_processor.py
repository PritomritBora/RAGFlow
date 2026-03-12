from typing import List, Dict
import PyPDF2
from pathlib import Path
from .advanced_chunker import AdvancedChunker

class DocumentProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunker = AdvancedChunker(chunk_size, chunk_overlap)
    
    def process_pdf(self, file_path: str, metadata: Dict) -> List[Dict]:
        """Process PDF with advanced chunking"""
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page_num, page in enumerate(reader.pages):
                page_text = page.extract_text()
                text += f"\n\n--- Page {page_num + 1} ---\n\n{page_text}"
            
            metadata["source"] = Path(file_path).name
            metadata["total_pages"] = len(reader.pages)
            
            return self.chunker.chunk_with_context(text, metadata)
    
    def process_markdown(self, file_path: str, metadata: Dict) -> List[Dict]:
        """Process Markdown with section awareness"""
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        metadata["source"] = Path(file_path).name
        return self.chunker.chunk_with_context(text, metadata)
    
    def process_text(self, text: str, metadata: Dict) -> List[Dict]:
        """Process raw text"""
        return self.chunker.chunk_with_context(text, metadata)
