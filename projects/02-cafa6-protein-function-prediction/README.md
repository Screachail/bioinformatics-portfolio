CAFA 6 Protein Function Prediction Pipeline

🇵🇱 Opis Projektu (Polish)

Ten projekt to kompletny system klasy Automated Protein Function Prediction (AFP). 
Celem jest przypisanie adnotacji biologicznych (Gene Ontology) do nieznanych sekwencji białkowych. 
Wykorzystałem podejście hybrydowe: Large Protein Language Models (PLMs) oraz Ensemble Learning.

Architektura i Metodologia

Projekt został zoptymalizowany pod kątem stabilności na lokalnej stacji roboczej (32GB RAM + GPU)
 i podzielony na moduły:

    Propagacja Etykiet (Label Propagation): Wykorzystałem strukturę grafu skierowanego (DAG) z bazy Gene Ontology. 
    Za pomocą biblioteki networkx zaimplementowałem mechanizm "true path rule" – jeśli białko posiada specyficzną 
    funkcję, algorytm automatycznie przypisuje mu wszystkie funkcje nadrzędne w hierarchii.

    Reprezentacja Sekwencji (ESM-2 Embeddings): Zamiast prostych metod (jak One-Hot Encoding), 
    użyłem modelu transformera ESM-2 (esm2_t6_8M_UR50D) od Meta AI. Model ten "rozumie" język ewolucji, 
    zamieniając sekwencję aminokwasów na wektory cech (embeddings), które kodują informację o strukturze 
    i funkcji białka.

    Klasyfikacja Hybrydowa (Ensemble):

        Deep Learning: Sieć neuronowa (MLP) w PyTorch, która świetnie generalizuje globalne cechy białek.

        XGBoost: Wykorzystany jako potężny klasyfikator dla 1500 etykiet jednocześnie, wyłapujący nieliniowe
         zależności między cechami.

        Blending: Finalny wynik to średnia ważona obu modeli, co pozwoliło na osiągnięcie stabilniejszych predykcji.

🇬🇧 Project Description (English)

This project presents a comprehensive Automated Protein Function Prediction (AFP) pipeline. 
The goal is to assign biological annotations (Gene Ontology terms) to uncharacterized protein sequences using
 a hybrid approach: Large Protein Language Models (PLMs) and Ensemble Learning.

Architecture & Methodology

The project is optimized for stability on a local workstation (32GB RAM + GPU) and is divided into modular steps:

    Label Propagation: I leveraged the Directed Acyclic Graph (DAG) structure of the Gene Ontology. 
    Using networkx, I implemented the "true path rule" – ensuring that if a protein is annotated with 
    a specific term, all its parental terms in the hierarchy are also included.

    Sequence Representation (ESM-2 Embeddings): Instead of traditional methods, I utilized Meta AI's ESM-2
    transformer model (esm2_t6_8M_UR50D). This model captures the "language of evolution," converting 
    amino acid sequences into dense embeddings that encode structural and functional information.

    Hybrid Classification (Ensemble):

        Deep Learning: A PyTorch-based Multi-Layer Perceptron (MLP) designed for multi-label classification 
        using BCEWithLogitsLoss.

        XGBoost: A robust gradient boosting model trained on the TOP 1500 GO terms to capture fine-grained 
        correlations.

        Blending: The final submission is a weighted average of both models, resulting in superior predictive 
        performance.

Tech Stack / Technologie

    Modeling: PyTorch, XGBoost, Scikit-Learn

    Embeddings: Transformers (HuggingFace), ESM-2

    Bioinformatics: Biopython, Obonet, NetworkX

    Data Handling: Pandas, NumPy, Parquet

Performance Note / Uwagi o wydajności

🇬🇧 English: The system efficiently processes over 224,000 test proteins, generating predictions across 
the 1,500 most frequent GO classes. By utilizing the .npy binary format and a modular notebook structure, 
the pipeline ensures optimized VRAM management and high-throughput processing, even when handling large-scale
biological datasets on consumer-grade hardware.

🇵🇱 Polski: System efektywnie przetwarza ponad 224 000 białek testowych, generując predykcje dla 1500 
najczęstszych klas GO. Zastosowanie binarnego formatu .npy oraz modularnej struktury notebooków pozwoliło 
na optymalne zarządzanie pamięcią VRAM i wysoką przepustowość obliczeniową, nawet przy pracy z wielkoskalowymi 
zbiorami danych biologicznych na sprzęcie klasy konsumenckiej.
