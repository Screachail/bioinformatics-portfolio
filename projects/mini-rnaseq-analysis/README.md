# Mini RNA-seq Analysis: Breast Cancer Gene Expression

## 🎯 Cel
Analiza eksploracyjna danych ekspresji genów z badania raka piersi.

## 📊 Dataset
- **Źródło:** RNA-seq tutorial (Griffith Lab)
- **Organizm:** Homo sapiens
- **Typ:** Breast cancer samples
- **Geny:** ~10,000+ (po filtracji: ~2,000)
- **Próbki:** Multiple samples

## 🔬 Metody
1. **Quality Control:** Filtrowanie low-expressed genes
2. **Normalizacja:** Log2 transformation
3. **Wizualizacja:** Heatmapy, PCA
4. **Analiza korelacji:** Sample clustering

## 📈 Kluczowe wyniki
- Zidentyfikowano top 50 najbardziej zmiennych genów
- PCA pokazuje grupowanie próbek
- Średnia korelacja między próbkami: ~0.9

## 🛠️ Narzędzia
- Python: pandas, numpy, matplotlib, seaborn
- Scikit-learn: PCA analysis
- Jupyter Notebook

## 📁 Pliki
- `breast_cancer_expression_analysis.ipynb` - główna analiza
- `gene_expression.tsv` - dane wejściowe

## 🚀 Jak uruchomić
```bash
cd ~/bioinformatics-portfolio/projects/mini-rnaseq-analysis
jupyter notebook --no-browser
# Otwórz breast_cancer_expression_analysis.ipynb
```

## 📚 Następne kroki
- Differential expression analysis (DESeq2)
- Gene Ontology enrichment
- Pathway analysis
