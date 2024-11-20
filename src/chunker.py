import os

from src.summarizer import summarize_text_with_ollama

def chunk_text(text, chunk_size=int(os.getenv("CHUNK_SIZE", 256))):
    """
    Split the text into chunks of specified size.

    Parameters:
    text (str): The text to be chunked.
    chunk_size (int): The size of each chunk. Default is 256.

    Returns:
    generator: A generator that yields chunks of text.
    """
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield ' '.join(words[i:i + chunk_size])

def return_summarized_chunks(chunks):
    """
    Summarize each chunk of text.

    Parameters:
    chunks (list): A list of text chunks.

    Returns:
    list: A list of summarized text chunks.
    """
    chunk_summaries = []
    for i, chunk in enumerate(chunks):
        summary = summarize_text_with_ollama(chunk)
        chunk_summaries.append(summary)
    return chunk_summaries

def recursive_summarized_chunking(cycles, chunks):
    """
    Recursively summarize text chunks for a specified number of cycles.

    Parameters:
    cycles (int): The number of summarization cycles.
    chunks (list): A list of text chunks.

    Returns:
    list: A list of recursively summarized text chunks.
    """
    while cycles > 0:
        chunk_summaries = return_summarized_chunks(chunks)
        chunks = ["\n\n".join(chunk_summaries)]
        cycles -= 1
    return chunks
