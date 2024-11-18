from typing import List
import os

def concatenate_markdown_files(output_path: str) -> str:
    """
    Concatenate all markdown files in a directory into a single file.

    Parameters:
    output_path (str): The path to the directory containing markdown files.

    Returns:
    str: The concatenated content of all markdown files.
    """
    markdown_files = [f for f in os.listdir(output_path) if f.endswith(".md")]
    concatenated_content = ""

    for file in markdown_files:
        with open(os.path.join(output_path, file), "r") as f:
            concatenated_content += f.read()

    return concatenated_content