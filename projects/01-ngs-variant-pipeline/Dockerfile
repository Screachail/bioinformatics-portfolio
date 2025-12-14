# Multi-stage build for NGS Variant Calling Pipeline
# Stage 1: Build tools
FROM ubuntu:22.04 AS builder

# Prevent interactive prompts during build
ENV DEBIAN_FRONTEND=noninteractive

# Install build dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    git \
    build-essential \
    cmake \
    zlib1g-dev \
    libbz2-dev \
    liblzma-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    libncurses5-dev \
    autoconf \
    && rm -rf /var/lib/apt/lists/*

# Install SRA Toolkit (3.0.10)
WORKDIR /tmp
RUN wget https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/3.0.10/sratoolkit.3.0.10-ubuntu64.tar.gz \
    && tar -xzf sratoolkit.3.0.10-ubuntu64.tar.gz \
    && mv sratoolkit.3.0.10-ubuntu64 /opt/sratoolkit \
    && rm sratoolkit.3.0.10-ubuntu64.tar.gz

# Install SAMtools (1.19.2)
RUN wget https://github.com/samtools/samtools/releases/download/1.19.2/samtools-1.19.2.tar.bz2 \
    && tar -xjf samtools-1.19.2.tar.bz2 \
    && cd samtools-1.19.2 \
    && ./configure --prefix=/opt/samtools \
    && make \
    && make install \
    && cd .. \
    && rm -rf samtools-1.19.2*

# Install BWA-MEM2 (2.2.1)
RUN wget https://github.com/bwa-mem2/bwa-mem2/releases/download/v2.2.1/bwa-mem2-2.2.1_x64-linux.tar.bz2 \
    && tar -xjf bwa-mem2-2.2.1_x64-linux.tar.bz2 \
    && mv bwa-mem2-2.2.1_x64-linux /opt/bwa-mem2 \
    && rm bwa-mem2-2.2.1_x64-linux.tar.bz2

# Stage 2: Final image
FROM ubuntu:22.04

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install runtime dependencies and Python 3.12
RUN apt-get update && apt-get install -y \
    python3.12 \
    python3.12-venv \
    python3-pip \
    wget \
    curl \
    git \
    default-jre \
    zlib1g \
    libbz2-1.0 \
    liblzma5 \
    libcurl4 \
    libssl3 \
    libncurses5 \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.12 as default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1 \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3.12 1

# Copy compiled tools from builder stage
COPY --from=builder /opt/sratoolkit /opt/sratoolkit
COPY --from=builder /opt/samtools /opt/samtools
COPY --from=builder /opt/bwa-mem2 /opt/bwa-mem2

# Install GATK (4.5.0.0)
WORKDIR /opt
RUN wget https://github.com/broadinstitute/gatk/releases/download/4.5.0.0/gatk-4.5.0.0.zip \
    && unzip gatk-4.5.0.0.zip \
    && rm gatk-4.5.0.0.zip

# Add tools to PATH
ENV PATH="/opt/sratoolkit/bin:/opt/samtools/bin:/opt/bwa-mem2:/opt/gatk-4.5.0.0:${PATH}"

# Set working directory
WORKDIR /workspace

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Create data directories
RUN mkdir -p /workspace/data/raw /workspace/data/processed /workspace/logs

# Set default command
CMD ["/bin/bash"]
