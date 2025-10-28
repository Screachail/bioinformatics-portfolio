# Test R - Analiza ekspresji genów
# ================================

cat("\n==================================================\n")
cat("TEST R - Analiza ekspresji genów\n")
cat("==================================================\n\n")

# Załaduj biblioteki
library(ggplot2)
library(dplyr)

# Stwórz dane (symulacja ekspresji genów)
data <- data.frame(
  sample = c('Control_1', 'Control_2', 'Control_3', 
             'Treatment_1', 'Treatment_2', 'Treatment_3'),
  gene_A = c(100, 95, 105, 250, 240, 260),
  gene_B = c(200, 210, 195, 180, 190, 185),
  gene_C = c(50, 55, 48, 150, 145, 155),
  condition = c('Control', 'Control', 'Control', 
                'Treatment', 'Treatment', 'Treatment')
)

# Wyświetl dane
cat("📊 Dane ekspresji:\n")
print(data)

# Podstawowe statystyki
cat("\n📈 Statystyki opisowe:\n")
summary(data[, c('gene_A', 'gene_B', 'gene_C')])

# Średnia dla każdego genu
cat("\n🧬 Średnia ekspresja dla każdego genu:\n")
cat(sprintf("  gene_A: %.2f\n", mean(data$gene_A)))
cat(sprintf("  gene_B: %.2f\n", mean(data$gene_B)))
cat(sprintf("  gene_C: %.2f\n", mean(data$gene_C)))

# Przekształć dane do formatu długiego (dla ggplot2)
library(tidyr)
data_long <- data %>%
  pivot_longer(cols = c(gene_A, gene_B, gene_C),
               names_to = "gene",
               values_to = "expression")

# Wykres 1: Bar plot
p1 <- ggplot(data_long, aes(x = sample, y = expression, fill = gene)) +
  geom_bar(stat = "identity", position = "dodge") +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
  labs(title = "Gene Expression Levels Across Samples",
       x = "Sample",
       y = "Expression Level",
       fill = "Gene") +
  theme(plot.title = element_text(face = "bold", size = 14))

ggsave("expression_barplot_r.png", plot = p1, width = 10, height = 6, dpi = 300)
cat("\n✅ Wykres zapisany: expression_barplot_r.png\n")

# Wykres 2: Boxplot
p2 <- ggplot(data_long, aes(x = condition, y = expression, fill = condition)) +
  geom_boxplot() +
  facet_wrap(~gene, scales = "free_y") +
  theme_bw() +
  scale_fill_brewer(palette = "Set2") +
  labs(title = "Gene Expression: Control vs Treatment",
       x = "Condition",
       y = "Expression Level") +
  theme(plot.title = element_text(face = "bold", size = 14),
        legend.position = "none")

ggsave("expression_boxplot_r.png", plot = p2, width = 12, height = 4, dpi = 300)
cat("✅ Wykres zapisany: expression_boxplot_r.png\n")

# Porównanie Control vs Treatment
cat("\n🔬 Porównanie Control vs Treatment:\n")
for(gene in c('gene_A', 'gene_B', 'gene_C')) {
  control_mean <- mean(data[data$condition == 'Control', gene])
  treatment_mean <- mean(data[data$condition == 'Treatment', gene])
  fold_change <- treatment_mean / control_mean
  
  cat(sprintf("  %s:\n", gene))
  cat(sprintf("    Control: %.2f\n", control_mean))
  cat(sprintf("    Treatment: %.2f\n", treatment_mean))
  cat(sprintf("    Fold Change: %.2fx\n", fold_change))
}

cat("\n==================================================\n")
cat("✅ Analiza zakończona!\n")
cat("==================================================\n\n")
