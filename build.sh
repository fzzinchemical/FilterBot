#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Build the Docker image
echo "Building Docker image..."
docker-compose build

# Run Docker Compose to start the services
echo "Starting Docker Compose services..."
docker-compose up --abort-on-container-exit --exit-code-from pyllama_summary