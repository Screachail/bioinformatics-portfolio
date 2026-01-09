# Baseline Approach (0.225 Public LB)

This directory contains the initial baseline solution for CAFA 6 protein function prediction.

---

## 📊 Overview

**Result:** Public LB = 0.225

**Approach:**
- ESM2-8M embeddings (smaller model)
- Neural Network classifier
- XGBoost ensemble
- Basic feature set

---

## 📓 Notebooks

### 1. Preprocessing (`01_preprocessing.ipynb`)

**What it does:**
- Loads raw FASTA and TSV data
- Parses protein sequences
- Creates initial train/val split
- Basic data validation

**Key outputs:**
- `data/bronze/train_sequences.parquet`
- `data/bronze/train_annotations.parquet`

**Runtime:** ~10 minutes

---

### 2. Embeddings (`02_embeddings.ipynb`)

**What it does:**
- Generates ESM2-8M embeddings (320 dim)
- Processes train and test proteins
- Saves embeddings to disk

**Key outputs:**
- `data/silver/X_train_esm2.npy`
- `data/silver/X_test_esm2.npy`

**Runtime:** ~2-3 hours on GPU

**Model used:**
```python
model = "facebook/esm2_t6_8M_UR50D"
embedding_dim = 320
```

---

### 3. Training Neural Network (`03_training_nn.ipynb`)

**What it does:**
- Builds multi-label NN classifier
- Trains on embeddings + labels
- Generates predictions

**Architecture:**
```python
Input (320) 
  → Dense(512) + ReLU + Dropout(0.3)
  → Dense(256) + ReLU + Dropout(0.3)
  → Dense(4000) + Sigmoid
```

**Key outputs:**
- `data/gold/y_pred_nn.npy`
- `models/nn_baseline.pth`

**Runtime:** ~2 hours

**Hyperparameters:**
- Learning rate: 0.001
- Batch size: 128
- Epochs: 20
- Optimizer: Adam

---

### 4. Ensemble (`04_ensemble.ipynb`)

**What it does:**
- Trains XGBoost on NN predictions
- Applies threshold optimization
- Generates final submission

**Key outputs:**
- `results/submission_baseline.tsv`

**Runtime:** ~1 hour

**XGBoost params:**
```python
n_estimators = 50
max_depth = 3
learning_rate = 0.1
```

---

## 📈 Performance Analysis

### Validation Metrics

| Ontology | F1 Score | Threshold |
|----------|----------|-----------|
| BP | 0.32 | 0.20 |
| MF | 0.40 | 0.25 |
| CC | 0.35 | 0.22 |
| **Overall** | **0.35** | - |

### Public vs Private LB

- **Public LB:** 0.225
- **Validation:** 0.35
- **Gap:** -0.125 (overfitting!)

**Analysis:**
- Training set patterns don't fully generalize
- Need better features
- Need hierarchical constraints

---

## 🔍 What Worked

### Strengths

1. ✅ **Fast prototyping** (~6h total runtime)
2. ✅ **Simple architecture** (easy to debug)
3. ✅ **Good validation setup** (proper split)
4. ✅ **Ensemble approach** (NN + XGBoost)

### What Learned

1. 💡 ESM embeddings are powerful
2. 💡 Multi-label is challenging
3. 💡 Threshold tuning matters
4. 💡 Validation ≠ Test performance

---

## ❌ What Didn't Work

### Weaknesses

1. ❌ **Small ESM model** (8M vs 150M parameters)
   - Less expressive embeddings
   - Missing evolutionary patterns

2. ❌ **No hierarchical constraints**
   - Predictions violate GO structure
   - Parent-child inconsistencies

3. ❌ **Limited features**
   - Only ESM embeddings
   - No taxonomy information
   - No amino acid composition

4. ❌ **Generic model**
   - Single model for all ontologies
   - Doesn't specialize for BP/MF/CC

5. ❌ **No post-processing**
   - Raw probabilities
   - No GO propagation

---

## 🚀 Improvements Made in Final Solution

### Key Changes

| Aspect | Baseline | Final | Improvement |
|--------|----------|-------|-------------|
| **PLM** | ESM2-8M (320d) | ESM2-150M (480d) | +50% capacity |
| **Features** | Embeddings only | +Taxon +AA comp | +2% F1 |
| **Models** | 1 generic | 3 specialized | +3% F1 |
| **Processing** | None | Hierarchical | +1-2% F1 |
| **Result** | 0.225 | 0.30-0.36 | **+33-60%** |

### Architecture Evolution

**Baseline:**
```
Sequences → ESM2-8M → NN → XGBoost → Predictions
```

**Final:**
```
Sequences → ESM2-150M ┐
Taxonomy → One-hot ───┼→ XGBoost-BP ┐
AA comp → Features ───┘  XGBoost-MF ├→ Propagation → Predictions
                         XGBoost-CC ┘
```

---

## 🎓 Key Learnings

### Domain Knowledge Matters

```python
# Baseline: Ignore biology
predictions = model(embeddings)

# Final: Respect GO structure
predictions = hierarchical_propagate(
    model(embeddings + taxon + aa_comp),
    go_graph
)
```

### Specialization > Generalization

```python
# Baseline: One model for everything
model_all = train(X, y_all)

# Final: Experts per ontology
model_bp = train(X, y_bp)
model_mf = train(X, y_mf)
model_cc = train(X, y_cc)
```

### Feature Engineering Compounds

```python
Embeddings alone: 0.225
+ Taxonomy: 0.25 (+11%)
+ AA composition: 0.27 (+20%)
+ Hierarchy: 0.30+ (+33%+)
```

---

## 🔄 Reproducing Baseline

### Quick Reproduction

```bash
# 1. Setup environment
source .venv/bin/activate

# 2. Run notebooks in order
jupyter notebook 01_preprocessing.ipynb
jupyter notebook 02_embeddings.ipynb
jupyter notebook 03_training_nn.ipynb
jupyter notebook 04_ensemble.ipynb

# 3. Submit results/submission_baseline.tsv
```

### Expected Timeline

```
Preprocessing: 10 min
Embeddings: 2-3h (GPU)
Training NN: 2h
Ensemble: 1h

Total: ~5-6h
```

---

## 🔬 Experiment Ideas

### Easy Wins (~1h each)

1. **Larger ESM model**
   ```python
   model = "facebook/esm2_t12_35M_UR50D"  # 150M params
   ```

2. **Add taxonomy**
   ```python
   features = concat(embeddings, taxon_onehot)
   ```

3. **Per-ontology models**
   ```python
   model_bp = train(X, y_bp)
   model_mf = train(X, y_mf)
   model_cc = train(X, y_cc)
   ```

### Advanced (~1 day each)

1. **Hierarchical constraints**
2. **Cross-validation** (5-fold)
3. **Attention mechanisms**
4. **Multi-model ensemble**

---

## 📚 References

### Papers Used

1. Lin et al. (2023). *Language models of protein sequences at the scale of evolution enable accurate structure prediction.* Science.
2. Zhou et al. (2019). *The CAFA challenge reports improved protein function prediction and new functional annotations.* Genome Biology.

### Code References

- ESM2: https://github.com/facebookresearch/esm
- XGBoost: https://xgboost.readthedocs.io/
- Scikit-learn: https://scikit-learn.org/

---

## 💡 Tips for Learning

### Understanding the Code

1. **Start with data flow**
   - Trace one protein through pipeline
   - Print shapes at each step
   - Visualize intermediate results

2. **Experiment systematically**
   - Change one thing at a time
   - Track all experiments
   - Compare to baseline

3. **Learn from errors**
   - Analyze misclassifications
   - Check label distribution
   - Visualize confusion patterns

### Common Pitfalls

1. ❌ Not setting random seeds → irreproducible
2. ❌ Data leakage in splits → inflated metrics
3. ❌ Overfitting to validation → poor test
4. ❌ Ignoring class imbalance → biased model

---

## 📊 Detailed Results

### Per-Ontology Breakdown

**Biological Process (BP):**
```
Terms: 2,500 selected
Validation F1: 0.32
Common errors: Broad processes
Best predictions: Specific pathways
```

**Molecular Function (MF):**
```
Terms: 1,000 selected
Validation F1: 0.40
Common errors: Enzyme activities
Best predictions: Binding functions
```

**Cellular Component (CC):**
```
Terms: 500 selected  
Validation F1: 0.35
Common errors: Membrane vs cytoplasm
Best predictions: Organelles
```

---

## 🎯 Next Steps

After understanding baseline:

1. [ ] Review final solution improvements
2. [ ] Implement hierarchical processing
3. [ ] Add taxonomic features
4. [ ] Try per-ontology models
5. [ ] Compare results!

---

**See:** `../03_final_solution/` for improved approach! 🚀

---

*Last updated: January 2026*
