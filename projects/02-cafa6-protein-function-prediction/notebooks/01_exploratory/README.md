# Exploratory Data Analysis

This directory contains comprehensive exploratory analysis of the CAFA 6 dataset.

---

## 🎯 Overview

**Goal:** Understand protein sequences, GO terms, taxonomy, and embeddings through visualization and statistical analysis.

**Key Questions:**
- What do protein sequences look like?
- How are GO terms distributed?
- What patterns exist in embeddings?
- How does taxonomy relate to function?

---

## 📊 Analysis Topics

### 1. Dataset Overview
- Size and scope
- Data quality checks
- Missing values
- Distributions

### 2. GO Terms Analysis
- Frequency distributions (BP, MF, CC)
- Hierarchical structure
- Co-occurrence patterns
- Information content

### 3. Protein Sequences
- Length distributions
- Amino acid composition
- Sequence complexity
- Rare patterns

### 4. Taxonomy
- Species distribution
- Kingdom breakdown
- Functions per organism
- Phylogenetic patterns

### 5. Embeddings Exploration
- Dimensionality reduction (PCA, t-SNE, UMAP)
- Clustering analysis
- Distance metrics
- Nearest neighbors

### 6. Multi-label Patterns
- Labels per protein
- Class imbalance
- Co-occurrence networks
- Conditional probabilities

---

## 🚀 Quick Start

### Load Data

```python
import numpy as np
import pandas as pd
from Bio import SeqIO
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)

# Load embeddings
train_emb = np.load('../../data/embeddings/train_esm2.npy')
train_ids = np.load('../../data/embeddings/train_ids.npy', allow_pickle=True)
test_emb = np.load('../../data/embeddings/test_esm2.npy')
test_ids = np.load('../../data/embeddings/test_ids.npy', allow_pickle=True)

print(f"Train: {train_emb.shape}")
print(f"Test: {test_emb.shape}")

# Load annotations
df_terms = pd.read_csv(
    '../../data/raw/Train/train_terms.tsv',
    sep='\t',
    names=['Protein_ID', 'GO_term', 'Ontology'],
    skiprows=1
)

# Map ontology codes
ontology_mapping = {'P': 'BP', 'F': 'MF', 'C': 'CC'}
df_terms['Ontology'] = df_terms['Ontology'].map(ontology_mapping)

print(f"\nAnnotations: {len(df_terms):,}")
print(df_terms['Ontology'].value_counts())
```

---

## 📈 Example Analyses

### GO Terms Frequency

```python
import matplotlib.pyplot as plt

# Count GO terms
go_counts = df_terms['GO_term'].value_counts()

# Plot top 50
fig, ax = plt.subplots(figsize=(14, 8))
go_counts.head(50).plot(kind='bar', ax=ax)
ax.set_title('Top 50 Most Frequent GO Terms', fontsize=16)
ax.set_xlabel('GO Term', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig('../../figures/eda/go_frequency.png', dpi=300)
plt.show()
```

### Sequence Length Distribution

```python
from Bio import SeqIO

# Load sequences
sequences = SeqIO.parse('../../data/raw/Train/train_sequences.fasta', 'fasta')

# Get lengths
lengths = []
for record in sequences:
    lengths.append(len(record.seq))

# Plot
fig, ax = plt.subplots(figsize=(12, 6))
ax.hist(lengths, bins=50, edgecolor='black', alpha=0.7)
ax.axvline(np.median(lengths), color='red', linestyle='--', label=f'Median: {np.median(lengths):.0f}')
ax.set_title('Protein Sequence Length Distribution', fontsize=16)
ax.set_xlabel('Sequence Length (amino acids)', fontsize=12)
ax.set_ylabel('Count', fontsize=12)
ax.legend()
plt.tight_layout()
plt.savefig('../../figures/eda/sequence_lengths.png', dpi=300)
plt.show()

print(f"Min: {min(lengths)}")
print(f"Max: {max(lengths)}")
print(f"Mean: {np.mean(lengths):.1f}")
print(f"Median: {np.median(lengths):.1f}")
```

### Embedding Visualization (PCA)

```python
from sklearn.decomposition import PCA

# Sample for speed
n_samples = 5000
indices = np.random.choice(len(train_emb), n_samples, replace=False)
emb_sample = train_emb[indices]

# PCA
pca = PCA(n_components=2)
emb_2d = pca.fit_transform(emb_sample)

# Plot
fig, ax = plt.subplots(figsize=(12, 10))
scatter = ax.scatter(emb_2d[:, 0], emb_2d[:, 1], alpha=0.5, s=10)
ax.set_title(f'Protein Embedding Space (PCA)\n{n_samples:,} proteins sampled', fontsize=16)
ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)', fontsize=12)
ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)', fontsize=12)
plt.tight_layout()
plt.savefig('../../figures/eda/embeddings_pca.png', dpi=300)
plt.show()
```

### UMAP Clustering

```python
import umap

# UMAP projection
reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, random_state=42)
emb_umap = reducer.fit_transform(emb_sample)

# Plot
fig, ax = plt.subplots(figsize=(12, 10))
scatter = ax.scatter(emb_umap[:, 0], emb_umap[:, 1], alpha=0.5, s=10)
ax.set_title(f'Protein Embedding Space (UMAP)\n{n_samples:,} proteins', fontsize=16)
ax.set_xlabel('UMAP 1', fontsize=12)
ax.set_ylabel('UMAP 2', fontsize=12)
plt.tight_layout()
plt.savefig('../../figures/eda/embeddings_umap.png', dpi=300)
plt.show()
```

### Taxonomy Distribution

```python
# Load taxonomy
df_tax = pd.read_csv(
    '../../data/raw/Train/train_taxonomy.tsv',
    sep='\t',
    names=['Protein_ID', 'Taxon_ID'],
    skiprows=1
)

# Top species
top_taxa = df_tax['Taxon_ID'].value_counts().head(20)

# Plot
fig, ax = plt.subplots(figsize=(12, 8))
top_taxa.plot(kind='barh', ax=ax)
ax.set_title('Top 20 Species by Protein Count', fontsize=16)
ax.set_xlabel('Number of Proteins', fontsize=12)
ax.set_ylabel('Taxon ID', fontsize=12)
ax.invert_yaxis()
plt.tight_layout()
plt.savefig('../../figures/eda/taxonomy_distribution.png', dpi=300)
plt.show()
```

### Multi-label Statistics

```python
# Labels per protein
labels_per_protein = df_terms.groupby('Protein_ID').size()

# Plot
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Histogram
axes[0].hist(labels_per_protein, bins=50, edgecolor='black', alpha=0.7)
axes[0].axvline(labels_per_protein.median(), color='red', linestyle='--', 
                label=f'Median: {labels_per_protein.median():.0f}')
axes[0].set_title('Labels per Protein', fontsize=14)
axes[0].set_xlabel('Number of GO Terms', fontsize=12)
axes[0].set_ylabel('Count', fontsize=12)
axes[0].legend()

# Per ontology
labels_per_ont = df_terms.groupby(['Protein_ID', 'Ontology']).size().unstack(fill_value=0)
labels_per_ont.plot(kind='hist', bins=30, alpha=0.7, ax=axes[1])
axes[1].set_title('Labels per Protein by Ontology', fontsize=14)
axes[1].set_xlabel('Number of GO Terms', fontsize=12)
axes[1].set_ylabel('Count', fontsize=12)

plt.tight_layout()
plt.savefig('../../figures/eda/labels_distribution.png', dpi=300)
plt.show()

print("\nStatistics:")
print(f"Mean labels per protein: {labels_per_protein.mean():.1f}")
print(f"Median labels per protein: {labels_per_protein.median():.0f}")
print(f"Max labels: {labels_per_protein.max()}")
```

### GO Term Co-occurrence

```python
from itertools import combinations
from collections import Counter

# Get terms per protein
protein_terms = df_terms.groupby('Protein_ID')['GO_term'].apply(list).to_dict()

# Count co-occurrences (top 100 terms only for speed)
top_terms = df_terms['GO_term'].value_counts().head(100).index
cooccur = Counter()

for terms in protein_terms.values():
    # Filter to top terms
    terms_filtered = [t for t in terms if t in top_terms]
    # Count pairs
    for pair in combinations(sorted(terms_filtered), 2):
        cooccur[pair] += 1

# Convert to matrix
import pandas as pd
from scipy.sparse import lil_matrix

term_to_idx = {t: i for i, t in enumerate(top_terms)}
matrix = lil_matrix((len(top_terms), len(top_terms)))

for (t1, t2), count in cooccur.items():
    i, j = term_to_idx[t1], term_to_idx[t2]
    matrix[i, j] = count
    matrix[j, i] = count

# Plot heatmap (sample)
sample_size = 30
sample_terms = top_terms[:sample_size]
sample_matrix = matrix[:sample_size, :sample_size].toarray()

fig, ax = plt.subplots(figsize=(14, 12))
sns.heatmap(sample_matrix, cmap='YlOrRd', ax=ax, cbar_kws={'label': 'Co-occurrence Count'})
ax.set_title(f'GO Term Co-occurrence (Top {sample_size} Terms)', fontsize=16)
ax.set_xlabel('GO Term', fontsize=12)
ax.set_ylabel('GO Term', fontsize=12)
plt.tight_layout()
plt.savefig('../../figures/eda/cooccurrence_heatmap.png', dpi=300)
plt.show()
```

---

## 🎨 Visualization Tips

### Color Palettes

```python
# For ontologies
ontology_colors = {
    'BP': '#1f77b4',  # Blue
    'MF': '#ff7f0e',  # Orange
    'CC': '#2ca02c'   # Green
}

# For general plots
sns.set_palette('husl')  # Colorful
# OR
sns.set_palette('colorblind')  # Accessible
```

### Interactive Plots (Plotly)

```python
import plotly.express as px

# Interactive scatter
fig = px.scatter(
    x=emb_2d[:, 0], 
    y=emb_2d[:, 1],
    hover_data={'Protein': train_ids[indices]},
    title='Interactive Embedding Space',
    labels={'x': 'PC1', 'y': 'PC2'}
)
fig.write_html('../../figures/eda/embeddings_interactive.html')
fig.show()
```

### Publication Quality

```python
# High DPI
plt.savefig('figure.png', dpi=300, bbox_inches='tight')

# Vector format
plt.savefig('figure.svg', bbox_inches='tight')

# Multiple formats
for fmt in ['png', 'svg', 'pdf']:
    plt.savefig(f'figure.{fmt}', dpi=300, bbox_inches='tight')
```

---

## 📚 Advanced Analyses

### GO Hierarchy Visualization

```python
import obonet
import networkx as nx

# Load GO graph
graph = obonet.read_obo('../../data/raw/Train/go-basic.obo')

# Sample subgraph
root = 'GO:0008150'  # Biological process
subgraph = nx.ego_graph(graph, root, radius=2, undirected=True)

# Plot
pos = nx.spring_layout(subgraph)
nx.draw(subgraph, pos, with_labels=True, node_size=50, font_size=8)
plt.title('GO Term Hierarchy (2 levels from root)')
plt.tight_layout()
plt.savefig('../../figures/eda/go_hierarchy.png', dpi=300)
plt.show()
```

### Clustering Analysis

```python
from sklearn.cluster import KMeans

# K-means on embeddings
n_clusters = 10
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
clusters = kmeans.fit_predict(emb_sample)

# Plot with colors
fig, ax = plt.subplots(figsize=(12, 10))
scatter = ax.scatter(emb_2d[:, 0], emb_2d[:, 1], c=clusters, cmap='tab10', alpha=0.6, s=20)
ax.set_title(f'Embedding Clusters (K={n_clusters})', fontsize=16)
plt.colorbar(scatter, label='Cluster')
plt.tight_layout()
plt.savefig('../../figures/eda/embedding_clusters.png', dpi=300)
plt.show()
```

### Statistical Tests

```python
from scipy import stats

# Compare ontology distributions
bp_lengths = labels_per_ont['BP'].dropna()
mf_lengths = labels_per_ont['MF'].dropna()

statistic, pvalue = stats.mannwhitneyu(bp_lengths, mf_lengths)
print(f"Mann-Whitney U test: p={pvalue:.4f}")

if pvalue < 0.05:
    print("✅ Significant difference between BP and MF label counts")
else:
    print("❌ No significant difference")
```

---

## 💾 Saving Results

### Create Figures Directory

```python
import os

# Create if doesn't exist
os.makedirs('../../figures/eda', exist_ok=True)

# Save systematically
plot_name = 'go_distribution'
for ext in ['png', 'svg']:
    plt.savefig(f'../../figures/eda/{plot_name}.{ext}', dpi=300, bbox_inches='tight')
```

### Export Statistics

```python
# Save summary stats to CSV
stats_df = pd.DataFrame({
    'Metric': ['Total Proteins', 'Total Annotations', 'Avg Labels/Protein'],
    'Value': [len(train_ids), len(df_terms), labels_per_protein.mean()]
})

stats_df.to_csv('../../figures/eda/summary_statistics.csv', index=False)
```

---

## 🎓 Learning Resources

### Tutorials
- [Seaborn Gallery](https://seaborn.pydata.org/examples/index.html)
- [Plotly Examples](https://plotly.com/python/)
- [Matplotlib Cheatsheet](https://matplotlib.org/cheatsheets/)

### Books
- *Python Data Science Handbook* by Jake VanderPlas
- *Fundamentals of Data Visualization* by Claus O. Wilke

### Courses
- [DataCamp: Data Visualization with Python](https://www.datacamp.com/)
- [Coursera: Applied Data Science with Python](https://www.coursera.org/)

---

## 📊 Suggested Analysis Plan

### Day 1: Dataset Overview
- [ ] Load and explore data
- [ ] Basic statistics
- [ ] Data quality checks
- [ ] Distribution plots

### Day 2: Deep Dive
- [ ] GO term analysis
- [ ] Sequence patterns
- [ ] Taxonomy exploration
- [ ] Multi-label statistics

### Day 3: Embeddings
- [ ] PCA visualization
- [ ] UMAP clustering
- [ ] Distance analysis
- [ ] Nearest neighbors

### Day 4: Insights
- [ ] Correlation analysis
- [ ] Statistical tests
- [ ] Pattern discovery
- [ ] Document findings

---

## 📧 Questions?

For help with EDA:
- Review examples above
- Check visualization libraries docs
- Experiment iteratively

**Contact:** kacu.1808@gmail.com

---

**Happy Exploring! 🔬**

---

*Last updated: January 2026*
