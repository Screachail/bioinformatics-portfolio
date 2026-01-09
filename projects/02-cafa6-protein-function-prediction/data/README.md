# Data Directory

This directory contains datasets for the CAFA 6 protein function prediction project.

## 📁 Structure

```
data/
├── raw/              # Raw Kaggle competition data
├── embeddings/       # Pre-computed ESM2 embeddings (293MB) ✓
├── processed/        # Intermediate processed data
├── samples/          # Small example datasets
├── bronze/           # Archived (~/cafa6-archive/)
├── silver/           # Archived (~/cafa6-archive/)
└── gold/             # Archived (~/cafa6-archive/)
```

---

## ⬇️ Download Instructions

### Option 1: Kaggle CLI (Recommended)

```bash
# Install Kaggle CLI
pip install kaggle

# Setup authentication (one-time)
# 1. Go to: https://www.kaggle.com/YOUR_USERNAME/account
# 2. Click "Create New API Token"
# 3. Move downloaded kaggle.json to ~/.kaggle/
mkdir -p ~/.kaggle
mv ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json

# Download competition data
cd data/raw
kaggle competitions download -c cafa-6-protein-function-prediction

# Extract
unzip cafa-6-protein-function-prediction.zip
rm cafa-6-protein-function-prediction.zip
```

### Option 2: Manual Download

1. Visit: https://www.kaggle.com/competitions/cafa-6-protein-function-prediction/data
2. Accept competition rules (if not already)
3. Download files manually:
   - `Train.zip` (~200MB)
   - `Test.zip` (~150MB)
   - `IA.tsv` (~1MB)
4. Extract to `data/raw/`

---

## 📊 Dataset Overview

### Training Data

Located in `data/raw/Train/`:

| File | Size | Description |
|------|------|-------------|
| `train_sequences.fasta` | ~50MB | 82,404 protein sequences |
| `train_terms.tsv` | ~25MB | 537,027 protein-GO annotations |
| `train_taxonomy.tsv` | ~3MB | Taxonomic information |
| `go-basic.obo` | ~40MB | Gene Ontology structure |

### Test Data

Located in `data/raw/Test/`:

| File | Size | Description |
|------|------|-------------|
| `testsuperset.fasta` | ~120MB | 224,309 proteins to predict |

### Additional Files

| File | Size | Description |
|------|------|-------------|
| `IA.tsv` | ~1MB | Information accretion weights |

---

## 🧬 Pre-computed Embeddings

**Location:** `data/embeddings/`

Already included in repository (essential for EDA):

| File | Size | Shape | Description |
|------|------|-------|-------------|
| `train_esm2.npy` | 76MB | (82404, 480) | Train ESM2-150M embeddings |
| `test_esm2.npy` | 206MB | (224309, 480) | Test ESM2-150M embeddings |
| `train_ids.npy` | 3.2MB | (82404,) | Train protein IDs |
| `test_ids.npy` | 8.6MB | (224309,) | Test protein IDs |
| `selected_terms.pkl` | 51KB | - | Selected GO terms (4000) |

**How they were generated:**
```python
# ESM2-150M model
model = "facebook/esm2_t12_35M_UR50D"
embedding_dim = 480

# ~7-9h generation time on T4 GPU
# Saved for reuse in EDA and modeling
```

---

## 📈 Sample Data

**Location:** `data/samples/`

Small subsets for quick testing and examples:

```bash
# Coming soon: sample datasets
# - 1000 proteins
# - 100 GO terms
# - Perfect for notebook demos
```

---

## 🗃️ Archived Data

Heavy intermediate files moved to `~/cafa6-archive/`:

### Bronze Layer (~191MB)
- Raw data after initial parsing
- Protein sequences + metadata

### Silver Layer (~189MB)
- Cleaned and validated data
- Feature engineering intermediate

### Gold Layer (~2.7GB)
- ML-ready datasets
- Train/val/test splits
- Label matrices

**To restore:**
```bash
# If you need archived data
cp -r ~/cafa6-archive/bronze data/
cp -r ~/cafa6-archive/silver data/
cp -r ~/cafa6-archive/gold data/
```

---

## 🔄 Data Pipeline

```
Raw FASTA/TSV
    ↓
Bronze (parsed sequences)
    ↓
Silver (feature engineering)
    ↓
Gold (ML-ready matrices)
    ↓
Models & Predictions
```

**Note:** Pipeline scripts coming soon in `src/pipelines/`

---

## 📝 File Formats

### FASTA (.fasta)
```
>sp|P12345|PROT_HUMAN Protein name OS=Homo sapiens
MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNL...
```

### TSV (.tsv)
```
Protein_ID    GO_term      Ontology
Q5W0B1       GO:0000785   C
Q5W0B1       GO:0004842   F
```

### NumPy (.npy)
Binary format for efficient array storage.

```python
import numpy as np

# Load embeddings
embeddings = np.load('data/embeddings/train_esm2.npy')
ids = np.load('data/embeddings/train_ids.npy', allow_pickle=True)

print(f"Shape: {embeddings.shape}")  # (82404, 480)
```

---

## ⚠️ Important Notes

### Git Ignore Rules

The following are **not tracked** in Git (see `.gitignore`):
- ❌ Large FASTA files (>50MB)
- ❌ Intermediate parquet files
- ❌ Bronze/Silver/Gold data
- ✅ Embeddings ARE tracked (essential, 293MB)
- ✅ Samples ARE tracked (small examples)

### Storage Requirements

| Component | Size | Location |
|-----------|------|----------|
| **Repository** | 504MB | Git |
| Raw data | ~200MB | `data/raw/` |
| Embeddings | 293MB | `data/embeddings/` (in Git) |
| Archive | 3.3GB | `~/cafa6-archive/` |
| **Total** | ~4GB | |

### Regenerating Data

If you need to regenerate processed data:

```bash
# Step 1: Download raw data (see above)

# Step 2: Generate embeddings (if needed)
# python src/generate_embeddings.py  # ~7-9h on GPU

# Step 3: Process data
# python src/preprocess.py  # ~30min

# Step 4: Create ML datasets  
# python src/create_gold_data.py  # ~1h
```

---

## 🔗 External Resources

### Official Links
- [CAFA 6 Competition](https://www.kaggle.com/competitions/cafa-6-protein-function-prediction)
- [Gene Ontology](http://geneontology.org/)
- [UniProt Database](https://www.uniprot.org/)

### Model Weights
- [ESM2 Models](https://github.com/facebookresearch/esm) (HuggingFace)
- Our trained XGBoost: `models/` directory

---

## 📧 Questions?

If you have issues downloading or processing data:
- Check Kaggle CLI authentication
- Ensure sufficient disk space (5GB+)
- Review error logs in `logs/`

**Contact:** [kacu.1808@gmail.com](mailto:kacu.1808@gmail.com)

---

*Last updated: January 2026*
