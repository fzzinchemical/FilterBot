import os
from src.summarizer import summarize_text_with_ollama

def chunk_text(text, chunk_size=int(os.getenv("CHUNK_SIZE", 256))):
    """Split the text into chunks of specified size."""
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield ' '.join(words[i:i + chunk_size])
        
def return_summarized_chunks(chunks):
    chunk_summaries = []
    for i, chunk in enumerate(chunks):
        summary = summarize_text_with_ollama(chunk)
        chunk_summaries.append(summary)
    return chunk_summaries

def recursive_summarized_chunking(cycles, chunks):
    while cycles > 0:
        chunk_summaries = return_summarized_chunks(chunks)
        chunks = list("\n\n".join(chunk_summaries))
        cycles -= 1
    return chunks