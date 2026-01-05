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
            validation_result = validate_fastq(file, logger)
            qc_results['valid'] = validation_result['valid']
            qc_results['total_reads'] = validation_result['total_reads']
            qc_results['errors'] = validation_result['errors']
            qc_results['file_size_mb'] = validation_result['file_size_mb']
            
            # Get GC content metrics
            gc_result = calculate_gc_content(file, logger)
            qc_results['gc_percentage'] = round(gc_result['gc_percentage'], 2)
            qc_results['gc_status'] = gc_result['status']
            
            # Get base quality metrics
            qual_result = calculate_base_quality(file, logger)
            qc_results['mean_quality'] = round(qual_result['mean_quality'], 1)
            qc_results['q30_percentage'] = round(qual_result['q30_percentage'], 1)
            qc_results['quality_status'] = qual_result['status']
            
            # Get N bases metrics
            n_result = count_n_bases(file, logger)
            qc_results['n_percentage'] = round(n_result['n_percentage'], 2)
            qc_results['n_status'] = n_result['status']

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


def export_json(df: pd.DataFrame, output_path: pathlib.Path, logger: logging.Logger) -> None:
    """Export DataFrame to JSON file with specified formatting.
    
    Args:
        df: DataFrame to be exported.
        output_path: Path where the JSON file will be saved.
        logger: Logger instance for logging messages.
        
    Returns:
        None
        
    Raises:
        IOError: If there is an error writing the file.
        
    Example:
        >>> df = aggregate_qc_results(Path('data/'), logger)
        >>> export_json(df, Path('reports/qc.json'), logger)
    """
    try:
        # Log start
        logger.info(f"Exporting JSON report to {output_path}")
        
        # Create parent directories if they don't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert DataFrame to dictionary of records
        data = df.to_dict(orient='records')
        
        # Write JSON file with UTF-8 encoding
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Log successful export with file size
        size_kb = output_path.stat().st_size / 1024
        logger.info(f"JSON report saved: {output_path} ({size_kb:.1f} KB)")
        
    except IOError as e:
        logger.error(f"Failed to write JSON: {e}")
        raise
