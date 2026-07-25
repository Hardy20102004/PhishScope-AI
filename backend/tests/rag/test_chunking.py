from app.rag.chunking import ChunkingEngine

def test_chunk_fixed():
    engine = ChunkingEngine(default_chunk_size=10, default_overlap=2)
    text = "0123456789ABCDEF"
    
    chunks = engine.chunk_fixed(text)
    assert len(chunks) == 2
    assert chunks[0] == "0123456789"
    assert chunks[1] == "89ABCDEF"

def test_chunk_paragraph():
    engine = ChunkingEngine()
    text = "Para 1.\n\nPara 2.\n\nPara 3."
    
    chunks = engine.chunk_paragraph(text)
    assert len(chunks) == 3
    assert chunks[0] == "Para 1."
    assert chunks[2] == "Para 3."
