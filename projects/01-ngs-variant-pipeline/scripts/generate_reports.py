"""
This module handles the generation of quality control (QC) reports for 
FASTQ files in an NGS pipeline. It aggregates QC metrics, generates 
visualizations,
and exports results in multiple formats including JSON, CSV, HTML.

The module provides functionality to:
- Aggregate QC results from multiple FASTQ files.
- Generate plots using matplotlib.
- Export aggregated data and plots to various output formats.
"""

import pathlib
import logging
from typing import Dict, List, Optional
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import json
import base64
import io

# Set matplotlib backend for non-interactive use
plt.switch_backend('Agg')

# Import QC functions from fastq_qc module
from scripts.fastq_qc import calculate_gc_content, calculate_base_quality, count_n_bases
# Import validation function from download_sra module
from scripts.download_sra import validate_fastq

# Module-level logger configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def aggregate_qc_results(fastq_dir: pathlib.Path, logger: logging.Logger) -> pd.DataFrame:
    """
    Aggregate quality control metrics from multiple FASTQ files in a directory.
    
    Args:
        fastq_dir (pathlib.Path): Directory containing FASTQ files to process.
        logger (logging.Logger): Logger instance for logging processing steps and errors.
        
    Returns:
        pd.DataFrame: DataFrame containing aggregated QC metrics for all processed files.
    """
    files = list(fastq_dir.glob("*.fastq"))
    
    if not files:
        logger.info(f"No FASTQ files found in {fastq_dir}")
        return pd.DataFrame()
    
    results = []
    
    for file in files:
        try:
            # Initialize QC results dictionary
            qc_results = {
                "filename": str(file.name),
                "file_size_mb": round(file.stat().st_size / (1024 * 1024), 2)
            }

            # Run validation and QC checks
            validate_fastq(file, qc_results)
            calculate_gc_content(file, qc_results)
            calculate_base_quality(file, qc_results)
            count_n_bases(file, qc_results)

            results.append(qc_results)
            logger.info(f"Successfully processed {file.name}")

        except FileNotFoundError as e:
            logger.warning(f"File not found: {file}. Skipping.")
            continue
        except ValueError as e:
            logger.warning(f"Invalid data in file {file}: {e}")
            continue
        except Exception as e:
            logger.warning(f"Failed to process {file}: {str(e)}")
            continue

    # Convert results list to DataFrame and sort by filename
    df = pd.DataFrame(results).sort_values(by="filename")

    logger.info(f"Completed: {len(df)} files processed successfully")
    
    return df
