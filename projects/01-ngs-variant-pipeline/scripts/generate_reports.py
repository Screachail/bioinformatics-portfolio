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
