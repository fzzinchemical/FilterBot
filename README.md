# PDF Dechonker

**Attention, this is an AI tool, use at your own risk!**

This repository contains a Python script to summarize PDF documents using the Ollama API. The script extracts text from PDF files, chunks the text into manageable sections, summarizes each chunk, and combines the summaries into a final summary. The final summaries are saved as Markdown files.

## Features

- Extract text from PDF files
- Filter out headers and footers from the extracted text
- Chunk large text into smaller sections
- Summarize each chunk using the Ollama API
- Combine chunk summaries into a final summary
- Save the final summary as a Markdown file
- **Chunk Conversion**

## Requirements

- Python 3.x
  - PyMuPDF (fitz)
  - Requests
- Docker
- Docker Compose
- (Optional) Ollama

## Setup

1. **Clone the repository:**

    ```sh
    git clone https://github.com/fzzinchemichal/PDF-Dechonker.git
    cd pdf-summarizer
    ```

2. **Install Python dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

3. **Ensure Docker and Docker Compose are installed:**

    - [Docker Installation Guide](https://docs.docker.com/get-docker/)
    - [Docker Compose Installation Guide](https://docs.docker.com/compose/install/)

## Usage

1. **Prepare the input and output directories:**

    - Place the PDF files you want to summarize in a directory, e.g., `/this/is/an/example/input`.
    - Ensure the output directory exists, e.g., `/this/is/an/example/output`.

2. **Create a `.env` file:**

    Modify the `.env.example` file in the root directory of your project to the requested paths and change the rename it to `.env` once it has been modified.

3. **Run the Docker Compose setup:**

    ```sh
    docker-compose up --abort-on-container-exit --exit-code-from pyllama_summary
    ```

    This command will start the Ollama service and the summarization script. The script will process the PDF files, generate summaries, and save them as Markdown files in the specified output directory.

## Directory Structure

```txt
    pdf-summarizer/ 
        ├── Dockerfile 
        ├── docker-compose.yml 
        ├── main.py 
        ├── pdf_reader.py 
        ├── summarizer.py 
        ├── requirements.txt 
        └── README.md
```

## Configuration

- **Docker Compose File (`docker-compose.yml`) for AMD:**
    Please verify if the paths from `devices:` matches with the ones from the `compose.yaml` a way to do this is to use the command `sudo lshw -short`

    ```yaml
    services:
      ollama:
        image: ollama/ollama:rocm
        networks:
          - my_network
        volumes:
          - ${OLLAMA_CONFIG_PATH}:/root/.ollama # shared ollama configuration
        devices:
          - /dev/kfd:/dev/kfd
          - /dev/dri:/dev/dri
        command: ["serve"] # Add the command to start ollama
        ports:
          - "11434:11434"
      
      pyllama_summary:
        build: .
        networks:
          - my_network
        depends_on:
          - ollama
        volumes:
          - .:/app
          - ${INPUT_FOLDER_PATH}:/shared_data
          - ${OUTPUT_FOLDER_PATH}:/shared_data/summary
        command: ["python", "main.py", "/shared_data/", "/shared_data/summary/"]

    networks:
      my_network:
    ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
