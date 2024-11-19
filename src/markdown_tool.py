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

def write_md(title, text, output_dir):
    """
    Write the given text to a markdown file with the specified title in the output directory.
    :param title: The title of the markdown file (without extension).
    :type title: str
    :param text: The text content to be written to the markdown file.
    :type text: str
    :param output_dir: The directory where the markdown file will be saved.
    :type output_dir: str
    """
    
    md_path = output_dir + f"/{title}.md"
    with open(md_path, 'w', encoding="utf-16-le") as f:
        f.write(text)
        f.close()