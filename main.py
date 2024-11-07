import os
from pdf_reader import extract_text_from_pdf
from summarizer import summarize_text_with_ollama

def chunk_text(text, chunk_size=500):
    """Split the text into chunks of specified size."""
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield ' '.join(words[i:i + chunk_size])

def concatenate_markdown_files(output_path):
    """Concatenate all markdown files in the output_path into a single file."""
    concatenated_content = ""
    for md_file in sorted(os.listdir(output_path)):
        if md_file.endswith('.md'):
            md_filepath = os.path.join(output_path, md_file)
            with open(md_filepath, "r") as infile:
                concatenated_content += infile.read()
                concatenated_content += "\n\n"  # Add a newline between files
    return concatenated_content

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
        
        # Create a markdown file named Result.md
        md_filepath = os.path.join(output_path, md_filename)
        with open(md_filepath, "w") as md_file:
            md_file.write(f"{final_summary}\n")
        
        print(f"Summary for {pdf_file} written to {md_filepath}\n")
    
    # Concatenate all markdown files into a single file
    concatenated_content = concatenate_markdown_files(output_path)
    
    chunks = list(chunk_text(concatenated_content))
    chunk_summaries = []

    for i, chunk in enumerate(chunks):
        summary = summarize_text_with_ollama(chunk)
        chunk_summaries.append(summary)
    
    
    final_summary_filepath = os.path.join(output_path, "Result.md")
    final_summary = summarize_text_with_ollama("\n\n".join(chunk_summaries))
    with open(final_summary_filepath, "w") as final_file:
        final_file.write(final_summary)
    print(f"All summaries concatenated into {final_summary_filepath}\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python main.py <input_folder_path> <output_folder_path>")
    else:
        main(sys.argv[1], sys.argv[2])