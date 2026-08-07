from typing import List

from app.schemas.rag import RAGSearchResult


class CitationEngine:
    def format_citations(self, results: List[RAGSearchResult]) -> str:
        """
        Formats retrieved chunks into a standard Evidence Citation block for the LLM context window.
        """
        if not results:
            return "No relevant enterprise knowledge found."
            
        formatted_blocks = []
        for i, res in enumerate(results):
            block = f"--- EVIDENCE [{i+1}] ---\n"
            block += f"Source Document: {res.asset_title}\n"
            block += f"Chunk ID: {res.chunk_id}\n"
            if res.metadata_json:
                for k, v in res.metadata_json.items():
                    block += f"{k.title()}: {v}\n"
            block += f"Confidence Score: {res.score:.2f}\n"
            block += f"Content:\n{res.content}\n"
            formatted_blocks.append(block)
            
        return "\n\n".join(formatted_blocks)
