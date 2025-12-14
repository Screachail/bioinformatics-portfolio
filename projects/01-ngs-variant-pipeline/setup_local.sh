#!/bin/bash
# Local Development Environment Setup Script
# For NGS Variant Calling Pipeline

set -e  # Exit on error

echo "=========================================="
echo "NGS Pipeline - Local Environment Setup"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo -e "${YELLOW}Warning: This script is designed for Ubuntu/Debian Linux${NC}"
    echo "For other systems, please follow LOCAL_SETUP.md manually"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check for sudo access
if ! sudo -v; then
    echo -e "${RED}Error: This script requires sudo access${NC}"
    exit 1
fi

echo -e "${GREEN}Step 1: Installing system dependencies...${NC}"
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

echo ""
echo -e "${GREEN}Step 2: Installing SRA Toolkit...${NC}"
if [ ! -d "/opt/sratoolkit" ]; then
    cd /tmp
    wget -q https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/3.0.10/sratoolkit.3.0.10-ubuntu64.tar.gz
    tar -xzf sratoolkit.3.0.10-ubuntu64.tar.gz
    sudo mv sratoolkit.3.0.10-ubuntu64 /opt/sratoolkit
    rm sratoolkit.3.0.10-ubuntu64.tar.gz
    echo 'export PATH="/opt/sratoolkit/bin:$PATH"' >> ~/.bashrc
    export PATH="/opt/sratoolkit/bin:$PATH"
    echo -e "${GREEN}✓ SRA Toolkit installed${NC}"
else
    echo -e "${YELLOW}✓ SRA Toolkit already installed${NC}"
fi

echo ""
echo -e "${GREEN}Step 3: Installing SAMtools...${NC}"
if [ ! -d "/opt/samtools" ]; then
    cd /tmp
    wget -q https://github.com/samtools/samtools/releases/download/1.19.2/samtools-1.19.2.tar.bz2
    tar -xjf samtools-1.19.2.tar.bz2
    cd samtools-1.19.2
    ./configure --prefix=/opt/samtools --quiet
    make -s
    sudo make install -s
    cd /tmp
    rm -rf samtools-1.19.2*
    echo 'export PATH="/opt/samtools/bin:$PATH"' >> ~/.bashrc
    export PATH="/opt/samtools/bin:$PATH"
    echo -e "${GREEN}✓ SAMtools installed${NC}"
else
    echo -e "${YELLOW}✓ SAMtools already installed${NC}"
fi

echo ""
echo -e "${GREEN}Step 4: Installing BWA-MEM2...${NC}"
if [ ! -d "/opt/bwa-mem2" ]; then
    cd /tmp
    wget -q https://github.com/bwa-mem2/bwa-mem2/releases/download/v2.2.1/bwa-mem2-2.2.1_x64-linux.tar.bz2
    tar -xjf bwa-mem2-2.2.1_x64-linux.tar.bz2
    sudo mv bwa-mem2-2.2.1_x64-linux /opt/bwa-mem2
    rm bwa-mem2-2.2.1_x64-linux.tar.bz2
    echo 'export PATH="/opt/bwa-mem2:$PATH"' >> ~/.bashrc
    export PATH="/opt/bwa-mem2:$PATH"
    echo -e "${GREEN}✓ BWA-MEM2 installed${NC}"
else
    echo -e "${YELLOW}✓ BWA-MEM2 already installed${NC}"
fi

echo ""
echo -e "${GREEN}Step 5: Installing GATK...${NC}"
if [ ! -d "/opt/gatk-4.5.0.0" ]; then
    cd /tmp
    wget -q https://github.com/broadinstitute/gatk/releases/download/4.5.0.0/gatk-4.5.0.0.zip
    unzip -q gatk-4.5.0.0.zip
    sudo mv gatk-4.5.0.0 /opt/gatk-4.5.0.0
    rm gatk-4.5.0.0.zip
    echo 'export PATH="/opt/gatk-4.5.0.0:$PATH"' >> ~/.bashrc
    export PATH="/opt/gatk-4.5.0.0:$PATH"
    echo -e "${GREEN}✓ GATK installed${NC}"
else
    echo -e "${YELLOW}✓ GATK already installed${NC}"
fi

echo ""
echo -e "${GREEN}Step 6: Setting up Python virtual environment...${NC}"
cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    python3.12 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${YELLOW}✓ Virtual environment already exists${NC}"
fi

source venv/bin/activate

echo ""
echo -e "${GREEN}Step 7: Installing Python dependencies...${NC}"
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo -e "${GREEN}✓ Python packages installed${NC}"

echo ""
echo -e "${GREEN}Step 8: Creating data directories...${NC}"
mkdir -p data/raw data/processed logs
echo -e "${GREEN}✓ Directories created${NC}"

echo ""
echo "=========================================="
echo -e "${GREEN}✓ Setup Complete!${NC}"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Activate the environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Verify installation:"
echo "   python -c 'import pysradb; print(pysradb.__version__)'"
echo "   fasterq-dump --version"
echo "   samtools --version"
echo "   bwa-mem2 version"
echo "   gatk --version"
echo ""
echo "3. Run tests:"
echo "   pytest tests/ -v"
echo ""
echo "4. Download test data:"
echo "   python scripts/download_sra.py --accession SRR000001 --output-dir data/raw/test"
echo ""
echo -e "${YELLOW}Note: Restart your terminal or run 'source ~/.bashrc' to update PATH${NC}"
