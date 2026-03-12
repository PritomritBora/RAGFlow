from typing import List, Dict
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter

class AdvancedChunker:
    """Smart chunking that preserves semantic boundaries"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
            length_function=len
        )
    
    def chunk_with_context(self, text: str, metadata: Dict) -> List[Dict]:
        """Chunk text while preserving section headers and context"""
        
        # Extract sections (markdown-style headers)
        sections = self._extract_sections(text)
        
        chunks = []
        for section_title, section_text in sections:
            section_chunks = self.splitter.split_text(section_text)
            
            for i, chunk_text in enumerate(section_chunks):
                chunks.append({
                    "text": chunk_text,
                    "metadata": {
                        **metadata,
                        "section": section_title,
                        "chunk_index": len(chunks),
                        "section_chunk": i
                    }
                })
        
        return chunks
    
    def _extract_sections(self, text: str) -> List[tuple]:
        """Extract sections based on headers"""
        
        # Match markdown headers (# Header, ## Header, etc.)
        header_pattern = r'^(#{1,6})\s+(.+)$'
        lines = text.split('\n')
        
        sections = []
        current_section = "Introduction"
        current_text = []
        
        for line in lines:
            match = re.match(header_pattern, line)
            if match:
                # Save previous section
                if current_text:
                    sections.append((current_section, '\n'.join(current_text)))
                
                # Start new section
                current_section = match.group(2).strip()
                current_text = []
            else:
                current_text.append(line)
        
        # Add last section
        if current_text:
            sections.append((current_section, '\n'.join(current_text)))
        
        return sections if sections else [("Document", text)]
