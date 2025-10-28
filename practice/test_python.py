import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("=" * 50)
print("TEST PYTHON - Analiza ekspresji genów")
print("=" * 50)

# Stwórz przykładowe dane (symulacja ekspresji genów)
data = {
    'sample': ['Control_1', 'Control_2', 'Control_3', 'Treatment_1', 'Treatment_2', 'Treatment_3'],
    'gene_A': [100, 95, 105, 250, 240, 260],
    'gene_B': [200, 210, 195, 180, 190, 185],
    'gene_C': [50, 55, 48, 150, 145, 155],
    'condition': ['Control', 'Control', 'Control', 'Treatment', 'Treatment', 'Treatment']
}

# Stwórz DataFrame
df = pd.DataFrame(data)

# Wyświetl dane
print("\n📊 Dane ekspresji:")
print(df)

# Podstawowe statystyki
print("\n📈 Statystyki opisowe:")
print(df[['gene_A', 'gene_B', 'gene_C']].describe())

# Średnia ekspresja dla każdego genu
print("\n🧬 Średnia ekspresja dla każdego genu:")
for gene in ['gene_A', 'gene_B', 'gene_C']:
    mean_val = df[gene].mean()
    print(f"  {gene}: {mean_val:.2f}")

# Wykres 1: Bar plot ekspresji
plt.figure(figsize=(10, 6))
df_plot = df.set_index('sample')[['gene_A', 'gene_B', 'gene_C']]
df_plot.plot(kind='bar', width=0.8)
plt.title('Gene Expression Levels Across Samples', fontsize=14, fontweight='bold')
plt.xlabel('Sample', fontsize=12)
plt.ylabel('Expression Level', fontsize=12)
plt.legend(title='Genes')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('expression_barplot.png', dpi=300)
print("\n✅ Wykres zapisany: expression_barplot.png")

# Wykres 2: Boxplot porównanie Control vs Treatment
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
genes = ['gene_A', 'gene_B', 'gene_C']

for i, gene in enumerate(genes):
    sns.boxplot(data=df, x='condition', y=gene, ax=axes[i], palette='Set2')
    axes[i].set_title(f'{gene} Expression', fontsize=12, fontweight='bold')
    axes[i].set_xlabel('Condition', fontsize=10)
    axes[i].set_ylabel('Expression Level', fontsize=10)

plt.tight_layout()
plt.savefig('expression_boxplot.png', dpi=300)
print("✅ Wykres zapisany: expression_boxplot.png")

# Porównanie średnich Control vs Treatment
print("\n🔬 Porównanie Control vs Treatment:")
for gene in ['gene_A', 'gene_B', 'gene_C']:
    control_mean = df[df['condition'] == 'Control'][gene].mean()
    treatment_mean = df[df['condition'] == 'Treatment'][gene].mean()
    fold_change = treatment_mean / control_mean
    print(f"  {gene}:")
    print(f"    Control: {control_mean:.2f}")
    print(f"    Treatment: {treatment_mean:.2f}")
    print(f"    Fold Change: {fold_change:.2f}x")

print("\n" + "=" * 50)
print("✅ Analiza zakończona!")
print("=" * 50)
