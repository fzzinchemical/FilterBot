from typing import List
import os

def concatenate_markdown_files(output_path: str) -> str:
    """Concatenate all markdown files in a directory into a single file."""
    markdown_files = [f for f in os.listdir(output_path) if f.endswith(".md")]
    concatenated_content = ""

    for file in markdown_files:
        with open(os.path.join(output_path, file), "r") as f:
            concatenated_content += f.read()

    return concatenated_content