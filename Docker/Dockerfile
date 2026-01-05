# Use an official Python image as a base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install SRA Toolkit which is required for fasterq-dump
RUN wget -O - https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/2.11.0/sratoolkit.2.11.0-ubuntu64.tar.gz | tar -xz -C /opt \
    && ln -s /opt/sratoolkit.2.11.0-ubuntu64/bin/* /usr/local/bin/

# Copy the rest of the application
COPY . .

# Create data directory
RUN mkdir -p data/raw

# Set environment variables
ENV PATH="/opt/sratoolkit.2.11.0-ubuntu64/bin:$PATH"

# Define the command to run the app
CMD ["python", "scripts/download_sra.py"]
