# Local Development Setup (Without Docker)

**⚠️ Note:** Docker is the recommended approach. Use this guide only if Docker isn't available.

## Prerequisites

- Python 3.12+
- Ubuntu/Debian Linux (or macOS/WSL)
- Root/sudo access for tool installation

## Automated Setup

```bash
cd projects/01-ngs-variant-pipeline

# Make setup script executable
chmod +x setup_local.sh

# Run setup (installs all tools)
./setup_local.sh

# Activate virtual environment
source venv/bin/activate
```

## Manual Setup

### 1. Install System Dependencies

```bash
sudo apt-get update
sudo apt-get install -y \
    python3.12 \
    python3.12-venv \
    python3-pip \
    wget \
    curl \
    git \
    default-jre \
    build-essential \
    cmake \
    zlib1g-dev \
    libbz2-dev \
    liblzma-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    libncurses5-dev
```

### 2. Install SRA Toolkit

```bash
cd /tmp
wget https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/3.0.10/sratoolkit.3.0.10-ubuntu64.tar.gz
tar -xzf sratoolkit.3.0.10-ubuntu64.tar.gz
sudo mv sratoolkit.3.0.10-ubuntu64 /opt/sratoolkit
rm sratoolkit.3.0.10-ubuntu64.tar.gz

# Add to PATH
echo 'export PATH="/opt/sratoolkit/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Verify
fasterq-dump --version
```

### 3. Install SAMtools

```bash
cd /tmp
wget https://github.com/samtools/samtools/releases/download/1.19.2/samtools-1.19.2.tar.bz2
tar -xjf samtools-1.19.2.tar.bz2
cd samtools-1.19.2
./configure --prefix=/opt/samtools
make
sudo make install
cd ..
rm -rf samtools-1.19.2*

# Add to PATH
echo 'export PATH="/opt/samtools/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Verify
samtools --version
```

### 4. Install BWA-MEM2

```bash
cd /tmp
wget https://github.com/bwa-mem2/bwa-mem2/releases/download/v2.2.1/bwa-mem2-2.2.1_x64-linux.tar.bz2
tar -xjf bwa-mem2-2.2.1_x64-linux.tar.bz2
sudo mv bwa-mem2-2.2.1_x64-linux /opt/bwa-mem2
rm bwa-mem2-2.2.1_x64-linux.tar.bz2

# Add to PATH
echo 'export PATH="/opt/bwa-mem2:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Verify
bwa-mem2 version
```

### 5. Install GATK

```bash
cd /tmp
wget https://github.com/broadinstitute/gatk/releases/download/4.5.0.0/gatk-4.5.0.0.zip
unzip gatk-4.5.0.0.zip
sudo mv gatk-4.5.0.0 /opt/gatk-4.5.0.0
rm gatk-4.5.0.0.zip

# Add to PATH
echo 'export PATH="/opt/gatk-4.5.0.0:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Verify
gatk --version
```

### 6. Set Up Python Environment

```bash
cd projects/01-ngs-variant-pipeline

# Create virtual environment
python3.12 -m venv venv

# Activate
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt

# Verify pysradb
python -c "import pysradb; print('pysradb version:', pysradb.__version__)"
```

## Verify Installation

```bash
source venv/bin/activate

# Run verification script
python3 << 'EOF'
import sys
import subprocess

def check_command(cmd, name):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(f"✅ {name}: OK")
        return True
    except FileNotFoundError:
        print(f"❌ {name}: NOT FOUND")
        return False

def check_import(module_name):
    try:
        __import__(module_name)
        print(f"✅ {module_name}: OK")
        return True
    except ImportError:
        print(f"❌ {module_name}: NOT FOUND")
        return False

print("=" * 50)
print("Environment Verification")
print("=" * 50)

print("\nPython Packages:")
check_import("pysradb")
check_import("Bio")
check_import("pandas")
check_import("numpy")

print("\nBioinformatics Tools:")
check_command(["fasterq-dump", "--version"], "SRA Toolkit")
check_command(["samtools", "--version"], "SAMtools")
check_command(["bwa-mem2", "version"], "BWA-MEM2")
check_command(["gatk", "--version"], "GATK")

print("\n" + "=" * 50)
EOF
```

## Development Workflow

```bash
# Always activate environment first
source venv/bin/activate

# Run scripts
python scripts/download_sra.py --accession SRR000001 --output-dir data/raw/test

# Run tests
pytest tests/ -v

# Deactivate when done
deactivate
```

## Troubleshooting

### pysradb Import Error
```bash
# Reinstall in virtual environment
source venv/bin/activate
pip install --force-reinstall pysradb==2.2.1
```

### Tool Not Found
```bash
# Check PATH
echo $PATH

# Reload bashrc
source ~/.bashrc
```

### Permission Denied
```bash
# Make directories writable
mkdir -p data/raw data/processed logs
chmod -R u+w data/ logs/
```

## Switching to Docker Later

To migrate to Docker after local setup:
1. Follow [DOCKER_SETUP.md](DOCKER_SETUP.md)
2. Your code and data will work seamlessly
3. Volume mounts preserve your files

---

[Back to Main README](README.md) | [Docker Setup](DOCKER_SETUP.md)
