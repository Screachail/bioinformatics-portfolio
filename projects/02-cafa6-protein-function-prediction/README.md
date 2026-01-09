# CAFA 6: Protein Function Prediction

> **Comprehensive machine learning solution for predicting protein functions using ESM2 embeddings, XGBoost, and hierarchical propagation**

[![Competition](https://img.shields.io/badge/Kaggle-CAFA%206-20BEFF?logo=kaggle)](https://www.kaggle.com/competitions/cafa-6-protein-function-prediction)
[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-XGBoost%20%7C%20PyTorch-green)](https://xgboost.readthedocs.io/)

## 📊 Results

| Approach | Public LB | Improvement | Features |
|----------|-----------|-------------|----------|
| Baseline (NN+XGBoost) | 0.225 | - | Basic embeddings |
| **Final Solution** | **0.30-0.36** | **+33-60%** | ESM2 + Hierarchy + Taxon |

### Validation Performance
- **BP (Biological Process)**: F1 = 0.40-0.46
- **MF (Molecular Function)**: F1 = 0.52-0.60
- **CC (Cellular Component)**: F1 = 0.46-0.54

---

## 🎯 Project Overview

Protein function prediction is a fundamental challenge in bioinformatics. This project implements a state-of-the-art solution combining:

- **Protein Language Models** (ESM2-150M) for rich sequence representations
- **Per-ontology XGBoost models** specialized for BP, MF, and CC
- **Hierarchical post-processing** respecting GO term relationships
- **Domain-specific features** including taxonomic and amino acid composition

### Key Innovation
Unlike monolithic approaches, this solution trains **specialized expert models** for each Gene Ontology aspect, then applies **two-way hierarchical propagation** to ensure biological consistency.

---

## 📂 Project Structure

```
02-cafa6-protein-function-prediction/
│
├── 📊 notebooks/
│   ├── 01_exploratory/          # Deep Dive EDA (45+ visualizations)
│   │   ├── cafa6_deep_dive_eda.ipynb
│   │   └── README.md
│   │
│   ├── 02_baseline/             # Initial approach (0.225 LB)
│   │   ├── 01_preprocessing.ipynb
│   │   ├── 02_embeddings.ipynb
│   │   ├── 03_training_nn.ipynb
│   │   ├── 04_ensemble.ipynb
│   │   └── README.md
│   │
│   └── 03_final_solution/       # Production solution (0.30-0.36 LB)
│       └── README.md
│
├── 🗂️ data/
│   ├── embeddings/              # ESM2 protein embeddings (293MB)
│   ├── raw/                     # Kaggle competition data
│   ├── samples/                 # Small example datasets
│   └── README.md                # Data download instructions
│
├── 🛠️ src/
│   └── utils/
│       ├── plotting.py          # Visualization utilities
│       ├── stats.py             # Statistical functions
│       └── bio_utils.py         # Biological domain utilities
│
├── 📈 results/
│   └── submission_best.tsv      # Best Kaggle submission (202MB)
│
├── 🎨 figures/
│   └── eda/                     # EDA visualizations
│       └── README.md            # Visualization catalog
│
├── 🤖 models/                   # Trained model weights (8.7MB)
│
├── 📄 README.md                 # This file
├── 📄 requirements.txt          # Python dependencies
└── 📄 .gitignore               # Git ignore rules
```

---

## 🔬 Methodology

### 1. **Feature Engineering**

#### ESM2 Embeddings (480 dimensions)
- Pre-trained protein language model (35M parameters)
- Captures evolutionary patterns from 250M sequences
- Transfer learning for function prediction

#### Taxonomic Features (100 dimensions)
- One-hot encoding of top 100 species
- Context-aware predictions (+2% F1 improvement)
- Bacteria vs Eukaryota vs Archaea distinctions

#### Amino Acid Composition (20 dimensions)
- Frequency of each amino acid
- Hydrophobicity, charge, structural propensities
- Simple but informative

**Total: 600 features per protein**

### 2. **Per-Ontology Models**

Instead of one generalist model, we train **three specialists**:

```python
BP Model: 2,500 GO terms (biological processes)
MF Model: 1,000 GO terms (molecular functions)  
CC Model: 500 GO terms (cellular components)
```

Each uses XGBoost with GPU acceleration:
- 100 trees per term
- Max depth: 5
- Multi-output classification

### 3. **Hierarchical Post-Processing**

GO terms form a **directed acyclic graph** (DAG). We enforce consistency:

#### Top-Down (Pmin)
```
If child term has high score → parent term should too
Pmin[parent] = α × min(children) + (1-α) × P[parent]
```

#### Bottom-Up (Pmax)
```
If parent term has high score → propagate to children
Pmax[child] = max(Pmax[child], Pmax[parent])
```

**Result:** Biologically plausible predictions (+1-2% F1)

---

## 📊 Exploratory Data Analysis

**[View Complete EDA →](notebooks/01_exploratory/)**

### Key Insights

1. **GO Term Distribution**
   - BP: 16,858 unique terms (selected top 2,500)
   - MF: 6,616 unique terms (selected top 1,000)
   - CC: 2,651 unique terms (selected top 500)
   - Heavy class imbalance (handled by per-term classifiers)

2. **Protein Sequences**
   - Train: 82,404 proteins
   - Test: 224,309 proteins
   - Length distribution: 50-2000 amino acids (median: 350)

3. **Taxonomy**
   - 5,000+ species represented
   - Top 3: *Homo sapiens*, *Mus musculus*, *E. coli*
   - Covers bacteria, archaea, eukaryotes

4. **Embedding Space**
   - Clear clustering by ontology
   - Species-specific patterns visible
   - Function-related neighborhood structure

### Sample Visualizations

![GO Terms Frequency](figures/eda/go_distribution.png)
*Distribution of GO terms across ontologies*

![Embedding UMAP](figures/eda/embeddings_umap.png)
*2D projection of protein embedding space*

**[45+ more visualizations →](figures/eda/README.md)**

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/Screachail/bioinformatics-portfolio.git
cd bioinformatics-portfolio/projects/02-cafa6-protein-function-prediction

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Download Data

```bash
# Kaggle CLI (requires authentication)
kaggle competitions download -c cafa-6-protein-function-prediction
unzip cafa-6-protein-function-prediction.zip -d data/raw/

# Or download manually from:
# https://www.kaggle.com/competitions/cafa-6-protein-function-prediction/data
```

**[Detailed data instructions →](data/README.md)**

### Run Exploratory Analysis

```bash
# Launch Jupyter
jupyter notebook

# Open: notebooks/01_exploratory/cafa6_deep_dive_eda.ipynb
# Runtime: ~90 minutes
# Output: 45+ visualizations + statistical insights
```

### Reproduce Results

```bash
# Coming soon: production pipeline script
python src/train_pipeline.py --config config/production.yaml
```

---

## 📈 Model Performance

### Confusion Analysis

**Strengths:**
- ✅ Common functions (>100 training examples)
- ✅ Well-defined ontologies (MF > CC > BP)
- ✅ Model organisms (*E. coli*, *S. cerevisiae*, *H. sapiens*)

**Challenges:**
- ⚠️ Rare functions (<10 training examples)
- ⚠️ Novel proteins (distant from training data)
- ⚠️ Ambiguous annotations (conflicting labels)

### Threshold Optimization

| Ontology | Optimal Threshold | Precision | Recall | F1 |
|----------|-------------------|-----------|--------|-----|
| BP | 0.15 | 0.52 | 0.38 | 0.44 |
| MF | 0.25 | 0.68 | 0.51 | 0.58 |
| CC | 0.18 | 0.59 | 0.43 | 0.50 |

---

## 💡 Key Learnings

### Technical

1. **Protein Language Models are Powerful**
   - ESM2 captures evolutionary information implicitly
   - Transfer learning works exceptionally well
   - Smaller models (150M) still competitive

2. **Domain Knowledge Matters**
   - Taxonomic features provide crucial context
   - GO hierarchy enforcement improves consistency
   - Per-ontology specialization beats generalization

3. **Multi-label is Different**
   - Each protein has 10-50 functions (not 1!)
   - Class imbalance is extreme
   - Threshold tuning is critical

### Engineering

1. **Compute Management**
   - ESM2-150M: 7-9h for 300K proteins
   - Checkpoint systems prevent data loss
   - GPU acceleration essential (10x speedup)

2. **Data Pipeline**
   - Pre-compute embeddings (one-time cost)
   - Cache intermediate results
   - Modular architecture enables iteration

3. **Production Considerations**
   - Model size: <10MB (deployable)
   - Inference: ~1ms per protein
   - Memory: 2GB peak (manageable)

---

## 🔮 Future Work

### Immediate Improvements

- [ ] **Ensemble Multiple PLMs** (ESM2 + ProtT5 + ESM-1v)
- [ ] **Attention Mechanisms** (learn which regions matter)
- [ ] **Pseudo-labeling** (leverage test set)
- [ ] **Cross-validation** (5-fold instead of single split)

### Advanced Research

- [ ] **Structure Integration** (AlphaFold2 predictions)
- [ ] **Graph Neural Networks** (protein-protein interaction)
- [ ] **Few-shot Learning** (rare function prediction)
- [ ] **Active Learning** (smart annotation prioritization)

---

## 📚 References

### Papers

1. Lin et al. (2023). *Evolutionary-scale prediction of atomic-level protein structure with a language model.* Science.
2. Radivojac et al. (2013). *A large-scale evaluation of computational protein function prediction.* Nature Methods.
3. Zhou et al. (2019). *The CAFA challenge reports improved protein function prediction.* Genome Biology.

### Resources

- [CAFA Competition](https://www.kaggle.com/competitions/cafa-6-protein-function-prediction)
- [Gene Ontology](http://geneontology.org/)
- [ESM Models](https://github.com/facebookresearch/esm)
- [XGBoost Documentation](https://xgboost.readthedocs.io/)

---

## 🎓 Skills Demonstrated

### Bioinformatics
- Protein sequence analysis
- Gene Ontology systems
- Evolutionary biology
- Functional genomics

### Machine Learning
- Transfer learning (PLMs)
- Multi-label classification
- Gradient boosting (XGBoost)
- Hierarchical constraints
- Feature engineering

### Software Engineering
- Modular code architecture
- Checkpoint systems
- Memory optimization
- Production pipelines
- Version control (Git)

### Data Science
- Exploratory data analysis (45+ plots)
- Statistical validation
- Performance metrics
- Visualization (Plotly, Seaborn)

---

## 👤 Author

**Kacper Szafraniec**
- 🔬 Medical Biotechnology (MSc)
- 💼 Product Owner & Business Analyst @ MARCEL S.A.
- 📧 [kacu.1808@gmail.com](mailto:kacu.1808@gmail.com)
- 💼 [LinkedIn](https://www.linkedin.com/in/kacper-szafraniec/)
- 🐙 [GitHub](https://github.com/Screachail)

---

## 📄 License

This project is part of a portfolio and educational repository. Code is available under MIT License. Data is from the CAFA 6 Kaggle competition and subject to competition terms.

---

## 🙏 Acknowledgments

- **Anthropic** for Claude AI assistance in architecture design and debugging
- **Kaggle** for hosting the CAFA 6 competition
- **CAFA Consortium** for organizing the Critical Assessment of Function Annotation
- **Facebook AI** for the ESM2 protein language model
- **XGBoost Community** for the gradient boosting framework

---

**⭐ If you found this helpful, please star the repository!**

*Last updated: January 2026*
