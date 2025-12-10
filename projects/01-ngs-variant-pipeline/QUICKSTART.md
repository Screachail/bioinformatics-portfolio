# Quick Start - NGS Variant Calling Pipeline

## ✅ Prerequisites Installed

- Python 3.12+
- SRA Toolkit (fasterq-dump)
- Virtual environment with dependencies

## 🚀 Download Test Data
```bash
# Activate environment
source projects/01-ngs-variant-pipeline/venv/bin/activate

# Download small E. coli dataset
python projects/01-ngs-variant-pipeline/scripts/download_sra.py \
  --accession SRR000001 \
  --output-dir projects/01-ngs-variant-pipeline/data/raw/test

# Verify download
ls -lh projects/01-ngs-variant-pipeline/data/raw/test/
```

## 📊 Expected Results

- **Time:** 5-10 minutes
- **Files:** 14 FASTQ files (paired-end)
- **Size:** ~500MB total
- **Reads:** ~470,000 per file

## 🔍 Verify Data Quality
```bash
# Check FASTQ format
head -4 projects/01-ngs-variant-pipeline/data/raw/test/SRR000001_2.fastq

# Count reads (divide by 4)
wc -l projects/01-ngs-variant-pipeline/data/raw/test/*.fastq

# Check file sizes
du -sh projects/01-ngs-variant-pipeline/data/raw/test/
```

## ✅ Month 0 Complete!

- [x] Development environment setup
- [x] SRA download script working
- [x] Real data successfully downloaded
- [x] Data validated

## 📅 What's Next?

**Month 1 (January 2025):**
- Quality control scripts
- FASTQ validation
- Alignment with BWA-MEM2 (Docker)
- Variant calling with GATK (Docker)

See main [README.md](README.md) for full roadmap.
