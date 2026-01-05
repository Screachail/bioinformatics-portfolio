# CAFA 6: Protein Function Prediction using Deep Learning & Ensemble Methods

**Competition:** [CAFA 6 Protein Function Prediction](https://www.kaggle.com/competitions/cafa-6-protein-function-prediction)  
**Goal:** Predict Gene Ontology (GO) terms for uncharacterized proteins based on amino acid sequences  
**Approach:** Hybrid system combining Protein Language Models (ESM-2) with ensemble learning (Neural Network + XGBoost)

---

## 🎯 Project Overview

This project addresses the Critical Assessment of Functional Annotation (CAFA) challenge - predicting biological functions of proteins from their amino acid sequences. The challenge involves:

- **Multi-label classification:** Each protein can have multiple GO terms (1-50+ labels)
- **Hierarchical structure:** GO terms form a Directed Acyclic Graph (DAG) requiring label propagation
- **Class imbalance:** 40,000+ possible GO terms with highly skewed distribution
- **Large scale:** 82,000+ training proteins, 224,000+ test proteins

**Evaluation Metric:** Weighted F-max score (information accretion weighted precision/recall)

---

## 🏗️ Architecture & Methodology

### 1. Data Processing & Label Propagation

**Challenge:** GO terms form a hierarchical DAG. If a protein has a specific function, it must also have all parent functions ("true path rule").

**Solution:**
- Used `networkx` and `obonet` to parse GO ontology structure
- Implemented automatic ancestor propagation for all annotations
- Selected top 1,500 most frequent GO terms for computational efficiency
- Created train/validation split (85/15) maintaining label distribution

```python
# Example: Propagation increases labels
Before propagation: Protein → 5 GO terms
After propagation: Protein → 15 GO terms (including ancestors)
```

**Results:**
- Training set: 70,043 proteins with 1,500 GO classes
- Validation set: 12,361 proteins
- Average labels per protein: ~15-20 (after propagation)

---

### 2. Feature Extraction: ESM-2 Protein Embeddings

**Challenge:** Amino acid sequences vary in length (50-2000+ residues). Traditional methods (one-hot encoding, k-mers) lose biological context.

**Solution:** Used Meta AI's ESM-2 (Evolutionary Scale Modeling) transformer model.

**Model Details:**
- **Version:** `esm2_t6_8M_UR50D` (8M parameters)
- **Input:** Raw amino acid sequences (up to 1024 residues)
- **Output:** 320-dimensional embeddings per protein
- **Key advantage:** Pre-trained on 250M protein sequences, captures evolutionary patterns

**Technical specifications:**
- Batch size: 32 sequences
- GPU memory: ~4GB VRAM
- Processing time: ~70 minutes for 224K test proteins (RTX 4050)
- Embeddings capture: sequence motifs, structural propensities, evolutionary conservation

```python
# Embedding pipeline
Sequence (MKTAYIAKQRQ...) 
    ↓ ESM-2 Tokenization
    ↓ Transformer Encoding (6 layers)
    ↓ Mean Pooling
→ 320D Vector [0.23, -0.45, 0.12, ...]
```

---

### 3. Model Architecture: Hybrid Ensemble

Built two complementary models and combined their predictions:

#### 3.1 Deep Neural Network (PyTorch)

**Architecture:**
```
Input (320) → Dense(512) → BatchNorm → ReLU → Dropout(0.3)
           → Dense(1024) → BatchNorm → ReLU → Dropout(0.3)
           → Dense(1500) → Sigmoid
```

**Training details:**
- Loss: BCEWithLogitsLoss (multi-label)
- Optimizer: AdamW (lr=1e-3, weight_decay=1e-4)
- Scheduler: ReduceLROnPlateau (patience=3)
- Early stopping: patience=5
- Batch size: 256
- Epochs: 14 (early stopped)

**Performance:**
- Training loss: 0.0921 → 0.0712
- Validation loss: 0.0808 → 0.0738
- Best validation F1: **0.442** (threshold=0.3)

#### 3.2 XGBoost Classifier

**Configuration:**
```python
XGBClassifier(
    tree_method='hist',
    device='cuda',
    n_estimators=100,
    max_depth=5,
    learning_rate=0.1
)
```

**Why XGBoost:**
- Captures non-linear feature interactions
- Robust to label imbalance
- Handles multi-output naturally via MultiOutputClassifier
- Faster inference than deep models

#### 3.3 Ensemble Strategy

**Method:** Weighted averaging of probability outputs

```python
y_final = (w_nn × y_pred_nn) + (w_xgb × y_pred_xgb)
```

**Optimization:** Grid search over:
- Weight combinations: (0.3-0.9 for NN, 0.1-0.7 for XGB)
- Thresholds: [0.01, 0.03, 0.05, 0.08, 0.1, 0.15, 0.2, 0.3]
- Validated on held-out validation set

**Best configuration:**
- NN weight: [TO BE UPDATED after ensemble finishes]
- XGB weight: [TO BE UPDATED]
- Threshold: [TO BE UPDATED]
- Validation F1: [TO BE UPDATED]

---

## 📊 Results

### Validation Performance

| Model | Threshold | Validation F1 |
|-------|-----------|---------------|
| Neural Network (NN) | 0.30 | 0.442 |
| XGBoost | [pending] | [pending] |
| Ensemble (NN + XGB) | [pending] | [pending] |

### Kaggle Public Leaderboard

| Submission | Public LB Score | Notes |
|------------|----------------|-------|
| NN only (threshold=0.3) | 0.164 | Baseline submission |
| Ensemble | [pending] | In progress |

**Observations:**
- Significant validation-LB gap (0.442 → 0.164) suggests distribution shift
- Test set proteins likely have different characteristics than training
- Threshold optimization on validation may not generalize
- Ensemble approach expected to improve robustness

---

## 🛠️ Technical Stack

**Core Libraries:**
- **Deep Learning:** PyTorch 2.x, Transformers (HuggingFace)
- **Embeddings:** ESM-2 (facebook/esm2_t6_8M_UR50D)
- **ML:** XGBoost, Scikit-learn
- **Bioinformatics:** Biopython, Obonet, NetworkX
- **Data:** Pandas, NumPy, PyArrow (Parquet)

**Infrastructure:**
- **Hardware:** HP Victus 16 (RTX 4050 6GB, 32GB RAM)
- **Development:** Jupyter Lab, Python 3.12
- **Optimization:** Mixed precision training, gradient accumulation, batch processing

---

## 📁 Project Structure

```
project/
├── data/
│   ├── bronze/          # Raw data from Kaggle
│   │   ├── Train/      # train_sequences.fasta, train_terms.tsv
│   │   └── Test/       # testsuperset.fasta
│   ├── silver/         # Intermediate processing
│   └── gold/           # Final processed data
│       ├── X_train_esm2.npy     (101MB) - Training embeddings
│       ├── X_test_esm2.npy      (274MB) - Test embeddings
│       ├── y_train_labels.npy   (802MB) - Training labels (propagated)
│       └── y_val_labels.npy     (141MB) - Validation labels
├── models/
│   ├── protein_nn.pth           (8.5MB) - Trained neural network
│   ├── top_terms_1500.pkl       (19KB) - Selected GO terms
│   └── training_history.png     - Loss curves
├── notebooks/
│   ├── 01_preprocessing.ipynb   - Label propagation & split
│   ├── 02_embeddings.ipynb      - ESM-2 feature extraction
│   ├── 03_training_nn.ipynb     - Neural network training
│   └── 04_ensemble.ipynb        - XGBoost + ensemble optimization
└── README.md
```

**Data Pipeline:**
```
Bronze (Raw) → Silver (Propagated) → Gold (Embeddings + Labels) → Models → Submission
```

---

## 🚀 Reproducibility

### Requirements
```bash
python 3.12+
torch>=2.0.0
transformers>=4.30.0
xgboost>=2.0.0
scikit-learn>=1.3.0
biopython>=1.81
obonet>=1.0.0
networkx>=3.0
```

### Running the Pipeline

```bash
# 1. Data preprocessing & label propagation (2 min)
jupyter notebook notebooks/01_preprocessing.ipynb

# 2. Generate ESM-2 embeddings (~70 min on RTX 4050)
jupyter notebook notebooks/02_embeddings.ipynb

# 3. Train neural network (~15 min)
jupyter notebook notebooks/03_training_nn.ipynb

# 4. Train ensemble & generate submission (~15 min)
jupyter notebook notebooks/04_ensemble.ipynb
```

**Total runtime:** ~100 minutes on consumer GPU

---

## 💡 Key Challenges & Solutions

### Challenge 1: Memory Constraints (6GB VRAM)
**Solution:**
- Selected ESM-2 small variant (8M params vs 650M)
- Batch size 32 for embeddings, 256 for training
- Saved embeddings to disk (.npy) to avoid recomputation

### Challenge 2: Hierarchical Label Structure
**Solution:**
- Implemented networkx-based ancestor propagation
- Ensured all child terms inherit parent terms
- Maintained GO DAG consistency

### Challenge 3: Class Imbalance (40K+ possible terms)
**Solution:**
- Selected top 1,500 most frequent terms (covers 95%+ of annotations)
- Used BCEWithLogitsLoss (handles multi-label naturally)
- XGBoost with weighted targets

### Challenge 4: Validation-LB Gap
**Status:** Under investigation
**Hypotheses:**
- Distribution shift in test proteins (different species/families)
- Threshold over-optimized on validation
- GO term frequency mismatch train/test

**Next steps:**
- Lower ensemble threshold (0.05-0.15 range)
- Increase predictions per protein
- Per-ontology threshold tuning (MF, BP, CC separately)

---

## 📈 Future Improvements

1. **Larger protein models:**
   - ESM-2 150M or 650M parameters (requires Kaggle GPU)
   - ProtT5 or ProtBERT alternatives

2. **Feature engineering:**
   - Sequence length, isoelectric point, molecular weight
   - Domain predictions (Pfam, InterPro)
   - Structural features (AlphaFold embeddings)

3. **Advanced ensembling:**
   - Stacking with meta-learner
   - Per-ontology specialized models (MF, BP, CC)

4. **Post-processing:**
   - GO graph consistency enforcement
   - Hierarchical softmax
   - Attention-based term selection

---

## 🎓 Learning Outcomes

This project demonstrates:
- **Bioinformatics + ML:** Applying state-of-art NLP techniques (transformers) to biological sequences
- **Domain expertise:** Understanding protein function annotation, GO ontology, multi-label classification
- **Production ML:** End-to-end pipeline from raw data to Kaggle submission
- **Resource optimization:** Working within consumer hardware constraints (6GB VRAM)
- **Research to code:** Implementing methods from CAFA literature (weighted F-max, label propagation)

---

## 📚 References

1. Jiang et al. (2016). "An expanded evaluation of protein function prediction methods." *Genome Biology* 17(1):184.
2. Lin et al. (2023). "Evolutionary-scale prediction of atomic-level protein structure with a language model." *Science*.
3. Radivojac et al. (2013). "A large-scale evaluation of computational protein function prediction." *Nature Methods* 10(3):221-227.

---

## 📧 Contact

**Author:** Kacper Szafraniec  
**Background:** Medical Biotechnology (MSc) + 5 years wet lab experience (NGS, biobanking) + transitioning to Data Engineering  
**LinkedIn:** [Your LinkedIn]  
**GitHub:** [Your GitHub]  
**Blog:** MonuMentalnie

---

## 📄 License

This project is for educational and competition purposes. Code is available under MIT license. Competition data is subject to CAFA/Kaggle terms.

---

*Last updated: January 2026*  
*Competition deadline: February 2, 2026*