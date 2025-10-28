import pandas as pd
import numpy as np

# Stwórz realistyczny dataset RNA-seq
np.random.seed(42)

# 2000 genów
gene_names = [f"GENE_{i:04d}" for i in range(1, 2001)]

# 6 próbek: 3 Control, 3 Treatment
samples = ['Control_1', 'Control_2', 'Control_3',
           'Treatment_1', 'Treatment_2', 'Treatment_3']

# Generuj dane
data = {}
for sample in samples:
    if 'Control' in sample:
        # Control: baseline expression
        data[sample] = np.random.negative_binomial(5, 0.1, 2000) * 10.0
    else:
        # Treatment: niektóre geny up/down regulated
        expression = np.random.negative_binomial(5, 0.1, 2000) * 10.0
        expression = expression.astype(float)  # FIX: konwersja na float
        
        # 10% genów upregulated (2-3x)
        upregulated = np.random.choice(2000, 200, replace=False)
        expression[upregulated] = expression[upregulated] * np.random.uniform(2, 3, 200)
        
        # 5% genów downregulated (0.3-0.5x)
        downregulated = np.random.choice(2000, 100, replace=False)
        expression[downregulated] = expression[downregulated] * np.random.uniform(0.3, 0.5, 100)
        
        data[sample] = expression

# Stwórz DataFrame
df = pd.DataFrame(data, index=gene_names)

# Zapisz
df.to_csv('gene_expression.tsv', sep='\t')
print("✅ Dataset stworzony: gene_expression.tsv")
print(f"📊 Wymiary: {df.shape}")

