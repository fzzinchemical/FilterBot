# main.py
import os
from pdf_reader import extract_text_from_pdf
from summarizer import summarize_text_with_ollama

def chunk_text(text, chunk_size=1000):
    """Split the text into chunks of specified size."""
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield ' '.join(words[i:i + chunk_size])

def main(input_path, output_path):
    print(f"Reading PDFs from {input_path}\n")
    
    # List all PDF files in the folder
    pdf_files = [f for f in os.listdir(input_path) if f.endswith('.pdf')]
    
    if not pdf_files:
        print("No PDF files found in the specified folder.")
        return
    
    # Ensure the output directory exists
    os.makedirs(output_path, exist_ok=True)
    
    for pdf_file in pdf_files:
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
        chunk_summaries = []

        for i, chunk in enumerate(chunks):
            summary = summarize_text_with_ollama(chunk)
            chunk_summaries.append(summary)

        
        # Combine individual summaries
        final_summary = summarize_text_with_ollama("\n\n".join(chunk_summaries))
        
        # Create a markdown file for each PDF
        md_filename = os.path.splitext(pdf_file)[0] + ".md"
        md_filepath = os.path.join(output_path, md_filename)

        with open(md_filepath, "w") as md_file:
            md_file.write(f"{final_summary}\n")
        
        print(f"Summary for {pdf_file} written to {md_filepath}\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python main.py <input_folder_path> <output_folder_path>")
    else:
        main(sys.argv[1], sys.argv[2])