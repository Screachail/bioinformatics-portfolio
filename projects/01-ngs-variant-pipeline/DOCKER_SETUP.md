# Docker Setup Guide

## Why Docker?

Docker provides a **consistent, reproducible environment** with all bioinformatics tools pre-installed:
- ✅ No dependency conflicts
- ✅ Same environment across all machines
- ✅ Includes SRA Toolkit, BWA-MEM2, GATK, SAMtools
- ✅ All Python packages pre-configured

## Prerequisites

### Install Docker

#### Ubuntu/Debian
```bash
# Update package index
sudo apt-get update

# Install dependencies
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker's official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Add your user to docker group (avoid using sudo)
sudo usermod -aG docker $USER
newgrp docker

# Verify installation
docker --version
docker compose version
```

#### macOS
```bash
# Using Homebrew
brew install --cask docker

# Or download Docker Desktop from:
# https://www.docker.com/products/docker-desktop
```

#### Windows
Download and install Docker Desktop:
https://www.docker.com/products/docker-desktop

## Build the Docker Image

```bash
cd projects/01-ngs-variant-pipeline

# Build the image (takes ~10-15 minutes first time)
docker compose build

# Or use docker build directly
docker build -t ngs-pipeline:latest .
```

## Usage

### Option 1: Using Docker Compose (Recommended)

```bash
# Start interactive container
docker compose run --rm ngs-pipeline

# Inside container, test imports
python3 -c "import pysradb; print('pysradb:', pysradb.__version__)"

# Run the download script
python3 scripts/download_sra.py --accession SRR000001 --output-dir data/raw/test

# Run tests
pytest tests/

# Exit container
exit
```

### Option 2: Using Docker directly

```bash
# Run interactive container
docker run -it --rm \
  -v $(pwd):/workspace \
  -w /workspace \
  ngs-pipeline:latest \
  /bin/bash

# Run specific command
docker run --rm \
  -v $(pwd):/workspace \
  -w /workspace \
  ngs-pipeline:latest \
  python3 scripts/download_sra.py --accession SRR000001 --output-dir data/raw/test
```

### Verify All Tools

```bash
docker compose run --rm ngs-pipeline /bin/bash -c "
  echo 'Testing installed tools...'
  echo ''
  echo 'Python:' && python3 --version
  echo 'pysradb:' && python3 -c 'import pysradb; print(pysradb.__version__)'
  echo 'BioPython:' && python3 -c 'import Bio; print(Bio.__version__)'
  echo ''
  echo 'SRA Toolkit:' && fasterq-dump --version 2>&1 | head -1
  echo 'BWA-MEM2:' && bwa-mem2 version
  echo 'SAMtools:' && samtools --version | head -1
  echo 'GATK:' && gatk --version | head -2
"
```

## Development Workflow

1. **Code on your host machine** using your preferred IDE
2. **Run in Docker** for consistent environment
3. **Data persists** via volume mounts in `data/` directory

```bash
# Example: Run tests in Docker
docker compose run --rm ngs-pipeline pytest tests/ -v

# Example: Download data
docker compose run --rm ngs-pipeline \
  python3 scripts/download_sra.py --accession SRR000001 --output-dir data/raw/test

# Example: Python interactive shell
docker compose run --rm ngs-pipeline python3
```

## Troubleshooting

### Permission Issues
```bash
# If you see permission denied errors
sudo chown -R $USER:$USER data/ logs/
```

### Build Failures
```bash
# Clean build (removes cache)
docker compose build --no-cache

# Check disk space
docker system df
```

### Container Not Starting
```bash
# Check logs
docker compose logs

# Remove old containers
docker compose down
docker system prune -a
```

## Resource Configuration

Edit `docker-compose.yml` to adjust:
```yaml
deploy:
  resources:
    limits:
      cpus: '4'      # Adjust based on your system
      memory: 8G     # Adjust based on your system
```

## Next Steps

Once Docker is working:
1. ✅ Test pysradb import
2. ✅ Download test dataset
3. ✅ Run alignment pipeline
4. ✅ Develop in isolated environment

---

**Alternative:** If you can't use Docker, see [LOCAL_SETUP.md](LOCAL_SETUP.md) for virtual environment setup.
