import os
import dotenv
from src.pdf_reader import extract_text_from_pdf
from src.summarizer import summarize_text_with_ollama
from src.chunker import chunk_text, return_summarized_chunks, recursive_summarized_chunking
from src.markdown_tool import concatenate_markdown_files


dotenv.load_dotenv()

def main(input_path, output_path):
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
    print(f'Using Model: {OLLAMA_MODEL}')
    print(f"Reading PDFs from {input_path}\n")
    
    # List all PDF files in the folder
    pdf_files = [f for f in os.listdir(input_path) if f.endswith('.pdf')]
    
    # Sort PDF files by name
    pdf_files.sort()
    
    if not pdf_files:
        print("No PDF files found in the specified folder.")
        return
    
    # Ensure the output directory exists
    os.makedirs(output_path, exist_ok=True)
    
    for pdf_file in pdf_files:
        print(f"Processing {pdf_file}\n")
        md_filename = os.path.splitext(pdf_file)[0] + ".md"
        md_filepath = os.path.join(output_path, md_filename)
        # Check if the markdown file already exists
        if os.path.exists(md_filepath):
            print(f"Markdown file for {pdf_file} already exists. Skipping...")
            continue
        
        pdf_path = os.path.join(input_path, pdf_file)
        print(f"Processing {pdf_path}\n")
        
        text = extract_text_from_pdf(pdf_path)
        
        # Chunk the text
        chunks = list(chunk_text(text))
        print(f"{pdf_file} chunked into {len(chunks)} parts\n")
        chunk_summaries = recursive_summarized_chunking(int(os.getenv("CHUNKING_CYCLES")), chunks)
        
        # Combine individual summaries
        final_summary = "\n\n".join(chunk_summaries)
        print(f"Writing {final_summary.__sizeof__()} bytes to {md_filepath}\n")
        
        # Create a markdown file named Result.md
        md_filepath = os.path.join(output_path, md_filename)
        with open(md_filepath, "w") as md_file:
            md_file.write(f"{final_summary}\n")
            md_file.close()
        
        print(f"Summary for {pdf_file} written to {md_filepath}\n")
    
    # Concatenate all markdown files into a single file
    # concatenated_content = concatenate_markdown_files(output_path)

    # for i, chunk in enumerate(chunks):
    #     summary = summarize_text_with_ollama(chunk)
    #     chunk_summaries.append(summary)
    
    
    # final_summary_filepath = os.path.join(output_path, "Result.md")
    # final_summary = summarize_text_with_ollama("\n\n".join(chunk_summaries))
    # with open(final_summary_filepath, "w") as final_file:
    #     final_file.write(final_summary)
    # print(f"All summaries concatenated into {final_summary_filepath}\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python main.py <input_folder_path> <output_folder_path>")
    else:
        main(sys.argv[1], sys.argv[2])