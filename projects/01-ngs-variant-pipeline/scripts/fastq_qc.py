"""
FASTQ Quality Control Module

This module provides functions for quality control of FASTQ files,
including GC content calculation and validation.
"""

from pathlib import Path
import logging
from collections import Counter
from typing import Dict, Any, Tuple

def calculate_gc_content(file_path: Path, logger: logging.Logger, 
expected_range: Tuple[float, float] = (50.0, 51.0)) -> Dict[str, Any]:
    """
    Calculate GC content percentage for a FASTQ file and validate against 
an expected range.
    
    Args:
        file_path: Path to the FASTQ file.
        logger: Logger instance for logging progress and results.
        expected_range: Tuple specifying the acceptable range for GC 
percentage (default: (50.0, 51.0)).
        
    Returns:
        Dictionary containing GC statistics and validation status.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If no valid bases are found in the file.
    """
    gc_bases = 0
    at_bases = 0
    n_bases = 0
    total_sequences = 0

    try:
        with open(file_path, 'r') as file:
            lines = iter(file)
            
            for i, line in enumerate(lines):
                if i % 4 == 1:  # Sequence is the second line (index 1) of each record
                    sequence = line.strip().upper()
                    base_counts = Counter(sequence)
                    
                    gc_bases += base_counts.get('G', 0) + base_counts.get('C', 0)
                    at_bases += base_counts.get('A', 0) + base_counts.get('T', 0)
                    n_bases += base_counts.get('N', 0)
                    
                    total_sequences += 1
                    
                    # Log progress every 100,000 reads
                    if (i // 4) % 100000 == 0:
                        logger.info(f"Processed {total_sequences} sequences.")
                        
            # Calculate GC percentage
            total_bases = gc_bases + at_bases
            if total_bases == 0:
                raise ValueError("No valid bases found in the FASTQ file.")
            
            gc_percentage = (gc_bases / total_bases) * 100
            rounded_gc = round(gc_percentage, 2)
            
            # Check against expected range
            in_range = expected_range[0] <= rounded_gc <= expected_range[1]
            status = "valid" if in_range else "warning"
            
            logger.info(f"GC Percentage: {rounded_gc:.2f}%")
            
            if not in_range:
                logger.warning("GC content is outside the expected range.")
                
            return {
                "gc_percentage": rounded_gc,
                "total_bases": total_bases + n_bases,
                "gc_bases": gc_bases,
                "at_bases": at_bases,
                "n_bases": n_bases,
                "in_expected_range": in_range,
                "status": status
            }
            
    except FileNotFoundError:
        logger.error(f"File '{file_path}' not found.")
        raise
    except IOError as e:
        logger.error(f"Error reading file: {str(e)}")
        raise
    except ValueError as e:
        logger.error(str(e))
        raise
