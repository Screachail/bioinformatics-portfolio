# 🚀 CAFA 6 Quick Start Guide

Complete setup instructions for the CAFA 6 protein function prediction project.

---

## 📋 Prerequisites

- **Python 3.10+** (tested on 3.12)
- **8GB+ RAM** (16GB recommended)
- **5GB disk space** (for data + models)
- **GPU** (optional, but 10x faster for embeddings)

---

## ⚡ Quick Setup (5 minutes)

### 1. Clone & Navigate

```bash
git clone https://github.com/Screachail/bioinformatics-portfolio.git
cd bioinformatics-portfolio/projects/02-cafa6-protein-function-prediction
```

### 2. Create Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate
source .venv/bin/activate  # Linux/Mac
# OR
.venv\Scripts\activate     # Windows
```

### 3. Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Verify installation
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA: {torch.cuda.is_available()}')"
```

### 4. Download Data

**Option A: Kaggle CLI** (fastest)
```bash
# Setup Kaggle API (one-time)
pip install kaggle
mkdir -p ~/.kaggle
# Download kaggle.json from https://www.kaggle.com/settings
mv ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json

# Download data
cd data/raw
kaggle competitions download -c cafa-6-protein-function-prediction
unzip cafa-6-protein-function-prediction.zip
rm *.zip
cd ../..
```

**Option B: Manual** (if no Kaggle CLI)
- Visit: https://www.kaggle.com/competitions/cafa-6-protein-function-prediction/data
- Download Train.zip, Test.zip, IA.tsv
- Extract to `data/raw/`

### 5. Verify Setup

```bash
python -c "
import os
import numpy as np

# Check embeddings
assert os.path.exists('data/embeddings/train_esm2.npy'), 'Missing train embeddings'
assert os.path.exists('data/embeddings/test_esm2.npy'), 'Missing test embeddings'

# Check raw data
assert os.path.exists('data/raw/Train/train_sequences.fasta'), 'Missing raw data - run download!'

print('✅ Setup complete!')
print('   Embeddings: Found')
print('   Raw data: Found')
print('   Ready to go!')
"
```

---

## 📊 Running the Analysis

### Exploratory Data Analysis

```bash
# Launch Jupyter
jupyter notebook

# Open: notebooks/01_exploratory/cafa6_deep_dive_eda.ipynb
# Runtime: ~90 minutes
# Output: 45+ visualizations
```

**Or create your own custom EDA:**
```python
import numpy as np
import pandas as pd

# Load embeddings
train_emb = np.load('data/embeddings/train_esm2.npy')
train_ids = np.load('data/embeddings/train_ids.npy', allow_pickle=True)

print(f"Train shape: {train_emb.shape}")  # (82404, 480)
print(f"First ID: {train_ids[0]}")

# Your analysis here!
```

### Baseline Model (0.225 LB)

```bash
# Run notebooks sequentially
jupyter notebook notebooks/02_baseline/01_preprocessing.ipynb
jupyter notebook notebooks/02_baseline/02_embeddings.ipynb
jupyter notebook notebooks/02_baseline/03_training_nn.ipynb
jupyter notebook notebooks/02_baseline/04_ensemble.ipynb
```

### Production Solution (0.30-0.36 LB)

```bash
# Coming soon: automated pipeline
python src/train_pipeline.py --config config/production.yaml
```

---

## 🔧 Development Workflow

### Create Feature Branch

```bash
git checkout -b feature/my-improvement
```

### Run Tests (if available)

```bash
pytest tests/
```

### Lint Code

```bash
# Install linters
pip install black flake8 isort

# Format code
black src/ notebooks/
isort src/

# Check style
flake8 src/
```

### Commit Changes

```bash
git add .
git commit -m "feat: add my improvement"
git push origin feature/my-improvement
```

---

## 💾 Data Management

### Archived Data

Heavy processed data is archived locally (not in Git):

```bash
# Location: ~/cafa6-archive/
~/cafa6-archive/
├── bronze/  (191MB)
├── silver/  (189MB)
└── gold/    (2.7GB)
```

**To restore archived data:**
```bash
cp -r ~/cafa6-archive/bronze data/
cp -r ~/cafa6-archive/silver data/
cp -r ~/cafa6-archive/gold data/
```

### Regenerate Embeddings (if needed)

```bash
# WARNING: Takes 7-9h on T4 GPU!
python src/generate_embeddings.py \
  --model facebook/esm2_t12_35M_UR50D \
  --input data/raw/Train/train_sequences.fasta \
  --output data/embeddings/train_esm2.npy
```

---

## 📦 Project Structure Reference

```
02-cafa6-protein-function-prediction/
│
├── 📊 notebooks/
│   ├── 01_exploratory/          # EDA (start here!)
│   ├── 02_baseline/             # Baseline approach
│   └── 03_final_solution/       # Production model
│
├── 🗂️ data/
│   ├── raw/                     # Kaggle data (download)
│   ├── embeddings/              # ESM2 (already included!)
│   ├── samples/                 # Small examples
│   └── README.md                # Data guide
│
├── 🛠️ src/
│   └── utils/                   # Helper functions
│
├── 📈 results/
│   └── submission_best.tsv      # Best submission
│
├── 🤖 models/                   # Trained weights
│
└── 📄 README.md                 # Main documentation
```

---

## 🎯 Common Tasks

### View Sample Data

```python
from Bio import SeqIO

# Read first 5 sequences
for i, record in enumerate(SeqIO.parse('data/raw/Train/train_sequences.fasta', 'fasta')):
    if i >= 5: break
    print(f"ID: {record.id}")
    print(f"Seq: {str(record.seq)[:50]}...")
    print()
```

### Load GO Terms

```python
import pandas as pd

# Load annotations
df_terms = pd.read_csv(
    'data/raw/Train/train_terms.tsv',
    sep='\t',
    names=['Protein_ID', 'GO_term', 'Ontology'],
    skiprows=1
)

print(df_terms.head())
print(f"Total annotations: {len(df_terms):,}")
```

### Visualize Embeddings

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# Load embeddings
embeddings = np.load('data/embeddings/train_esm2.npy')

# PCA projection
pca = PCA(n_components=2)
emb_2d = pca.fit_transform(embeddings[:1000])  # First 1000

# Plot
plt.figure(figsize=(10, 8))
plt.scatter(emb_2d[:, 0], emb_2d[:, 1], alpha=0.5)
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('Protein Embedding Space (PCA)')
plt.show()
```

---

## 🐛 Troubleshooting

### ImportError: No module named 'torch'

```bash
pip install torch torchvision torchaudio
```

### CUDA not available

```bash
# Check GPU
nvidia-smi

# Install CUDA-enabled PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Out of Memory (OOM)

```python
# Reduce batch size
BATCH_SIZE = 8  # Instead of 16

# Clear cache
import torch
torch.cuda.empty_cache()
```

### Kaggle API not working

```bash
# Check credentials
cat ~/.kaggle/kaggle.json

# Verify permissions
chmod 600 ~/.kaggle/kaggle.json

# Test API
kaggle competitions list
```

### Git LFS errors (large files)

```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.npy"
git lfs track "*.tsv"

# Push
git lfs push origin main
```

---

## 📚 Additional Resources

### Documentation
- [Main README](README.md)
- [Data Guide](data/README.md)
- [EDA Guide](notebooks/01_exploratory/README.md)
- [Baseline Guide](notebooks/02_baseline/README.md)

### External Links
- [CAFA Competition](https://www.kaggle.com/competitions/cafa-6-protein-function-prediction)
- [ESM Models](https://github.com/facebookresearch/esm)
- [XGBoost Docs](https://xgboost.readthedocs.io/)
- [Gene Ontology](http://geneontology.org/)

### Tutorials
- [Protein Language Models Guide](https://www.biorxiv.org/content/10.1101/2021.07.09.450648v2)
- [Multi-label Classification](https://scikit-learn.org/stable/modules/multiclass.html)
- [GO Ontology Tutorial](http://geneontology.org/docs/go-annotations/)

---

## 💡 Tips for Success

### Performance Optimization
1. **Use GPU** - 10x faster embedding generation
2. **Cache embeddings** - Don't regenerate unnecessarily
3. **Batch processing** - Process in chunks for memory efficiency
4. **Parallel jobs** - Use multiprocessing for CPU tasks

### Code Quality
1. **Modular functions** - Keep functions small and focused
2. **Type hints** - Use Python type annotations
3. **Docstrings** - Document all public functions
4. **Tests** - Write unit tests for utilities

### Experimentation
1. **Version control** - Commit frequently
2. **Track experiments** - Use MLflow or similar
3. **Document findings** - Keep notes in notebooks
4. **Reproducibility** - Set random seeds

---

## 🎓 Learning Path

### Beginner
1. ✅ Run EDA notebook
2. ✅ Understand data structure
3. ✅ Run baseline notebooks
4. ✅ Read GO ontology basics

### Intermediate
1. ⭐ Modify feature engineering
2. ⭐ Experiment with models
3. ⭐ Tune hyperparameters
4. ⭐ Analyze errors

### Advanced
1. 🚀 Implement new architectures
2. 🚀 Add structure information
3. 🚀 Ensemble multiple PLMs
4. 🚀 Publish improvements

---

## 📧 Getting Help

**Issues?**
- Check [Troubleshooting](#troubleshooting) section
- Review error logs in `logs/`
- Search GitHub issues

**Questions?**
- Email: kacu.1808@gmail.com
- LinkedIn: [Kacper Szafraniec](https://www.linkedin.com/in/kacper-szafraniec/)

---

## ⭐ Next Steps

After setup:
1. [ ] Run EDA notebook to understand data
2. [ ] Review baseline approach
3. [ ] Try reproducing results
4. [ ] Experiment with improvements!

**Happy analyzing! 🧬**

---

*Last updated: January 2026*
