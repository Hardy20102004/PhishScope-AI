import structlog
from typing import List
import re

logger = structlog.get_logger("phoenix.rag.chunking")

class ChunkingEngine:
    def __init__(self, default_chunk_size: int = 1000, default_overlap: int = 150):
        self.chunk_size = default_chunk_size
        self.overlap = default_overlap

    def chunk_fixed(self, text: str) -> List[str]:
        """
        Naive fixed-length string chunking (by characters rather than true tokens for simplicity).
        """
        chunks = []
        if not text:
            return chunks
            
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += self.chunk_size - self.overlap
            
        return chunks

    def chunk_paragraph(self, text: str) -> List[str]:
        """
        Split text by double newlines to retain paragraph boundaries.
        """
        if not text:
            return []
            
        paragraphs = re.split(r'\n\s*\n', text)
        return [p.strip() for p in paragraphs if p.strip()]

    def chunk_semantic(self, text: str) -> List[str]:
        """
        A semantic chunking mock. In a real system, this uses an NLP model (e.g. spacy, or NLTK) 
        to split on sentences, and group them until they hit the token limit.
        """
        # For prototype, fallback to paragraph chunking which is pseudo-semantic
        return self.chunk_paragraph(text)
