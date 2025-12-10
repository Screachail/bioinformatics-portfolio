# NGS Variant Calling Pipeline

Cloud-native bioinformatics workflow for genomic variant analysis.

## Overview

End-to-end automated pipeline from raw sequencing data (FASTQ) to variant analysis. Demonstrates modern data engineering applied to bioinformatics.

## Architecture

### Data Flow
1. **Ingestion**: NCBI SRA → GCS (Bronze - raw FASTQ)
2. **Processing**: Docker (BWA-MEM2, GATK) → GCS (Silver - BAM, VCF)
3. **Transformation**: dbt → BigQuery (Gold - analyzed variants)
4. **Orchestration**: Airflow DAGs
5. **Visualization**: Looker Studio

### Medallion Layers
- **Bronze**: Raw FASTQ files
- **Silver**: Aligned BAM, called VCF
- **Gold**: Annotated variants in BigQuery

## Tech Stack

**Languages**: Python 3.12, SQL, Bash

**Infrastructure**: GCP, Docker, Airflow

**Bioinformatics**: BWA-MEM2, GATK, SAMtools, pysradb, BioPython

**Data Engineering**: dbt, Great Expectations, Looker Studio

## Timeline

**7-Month Project (Dec 2024 - Jun 2025)**

| Month | Phase | Status |
|-------|-------|--------|
| 0 | Environment setup | ✅ COMPLETE |
| 1 | Local pipeline MVP | 🔄 IN PROGRESS |
| 2 | Cloud migration | Planned |
| 3 | Airflow orchestration | Planned |
| 4 | dbt transformations | Planned |
| 5 | Data quality + deployment | Planned |
| 6 | Looker dashboards | Planned |
| 7 | Optimization | Planned |

## Prerequisites

- Python 3.12+
- Docker and Docker Compose
- GCP account
- Git

## Installation
```bash
cd projects/01-ngs-variant-pipeline
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

Pipeline under active development.

## Data Source

NCBI Sequence Read Archive (SRA) public datasets.

## Future Enhancements

- Real-time variant annotation
- Multi-sample joint calling
- Clinical genomics integration
- Cloud cost optimization
- Parallelization strategies

## References

- [BWA-MEM2](https://github.com/bwa-mem2/bwa-mem2)
- [GATK Best Practices](https://gatk.broadinstitute.org/hc/en-us/sections/360007226651-Best-Practices-Workflows)
- [Apache Airflow](https://airflow.apache.org/docs/)
- [dbt](https://docs.getdbt.com/)
- [Great Expectations](https://docs.greatexpectations.io/)

## License

MIT License - see repository root.

---

[Back to Portfolio](../../README.md)
