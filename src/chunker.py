"""Function Library that chunks texts
Returns:
    _type_: Summarized Chunks
Yields:
    _type_: Chunks
"""
import os
import dotenv
from src.summarizer import summarize_text_with_ollama

dotenv.load_dotenv()


def chunk_text(text, chunk_size=int(os.getenv("CHUNK_SIZE", "256"))):
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
    for _, chunk in enumerate(chunks):
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
        chunks_str = ' '.join(chunk_summaries)
        if cycles > 0:
            chunks = list(chunk_text(chunks_str, int(os.getenv("OLLAMA_CHUNK_SIZE"))))
            print(f"Chunked again into {len(chunks)} parts")
            cycles -= 1
    return ' '.join(chunks)
