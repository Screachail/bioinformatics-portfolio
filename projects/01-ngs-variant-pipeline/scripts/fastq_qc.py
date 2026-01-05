"""
FASTQ Quality Control Module

This module provides functions for quality control of FASTQ files,
including GC content calculation and validation.

Hey there! This is a handy tool for checking your FASTQ files.
"""

from pathlib import Path
import logging
from collections import Counter
from typing import Dict, Any, Tuple
import statistics

def calculate_gc_content(file_path: Path, logger: logging.Logger, 
expected_range: Tuple[float, float] = (30.0, 70.0)) -> Dict[str, Any]:
    """
    Calculate GC content percentage for a FASTQ file and validate against 
    an expected range.
    
    Hey there! This function will help you figure out the GC content of your FASTQ file.
    
    Args:
        file_path: Path to the FASTQ file.
        logger: Logger instance for logging progress and results.
        expected_range: Tuple specifying the acceptable range for GC 
percentage (default: (30.0, 70.0)).
        
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
            status = "valid" if in_range else "invalid"
            
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

def calculate_base_quality(file_path: Path, logger: logging.Logger) -> Dict[str, Any]:
    """
    Calculate base quality scores for a FASTQ file.
    
    Args:
        file_path: Path to the FASTQ file.
        logger: Logger instance for logging progress and results.
        
    Returns:
        Dictionary containing base quality statistics.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If no valid bases are found in the file.
    """
    total_bases = 0
    quality_scores = []
    total_sequences = 0

    try:
        with open(file_path, 'r') as file:
            lines = iter(file)
            
            for i, line in enumerate(lines):
                if i % 4 == 3:  # Quality is the fourth line (index 3) of each record
                    quality_line = line.strip()
                    # Convert ASCII quality scores to numeric values
                    for char in quality_line:
                        quality_scores.append(ord(char) - 33)  # Phred+33 encoding
                    total_bases += len(quality_line)
                    total_sequences += 1
                    
                    # Log progress every 100,000 reads
                    if (i // 4) % 100000 == 0:
                        logger.info(f"Processed {total_sequences} sequences.")
                        
            if not quality_scores:
                raise ValueError("No valid quality scores found in the FASTQ file.")
            
            # Calculate statistics
            mean_quality = sum(quality_scores) / len(quality_scores)
            min_quality = min(quality_scores)
            max_quality = max(quality_scores)
            median_quality = statistics.median(quality_scores)
            
            # Calculate Q30+ percentage
            q30_count = sum(1 for q in quality_scores if q >= 30)
            q30_percentage = (q30_count / len(quality_scores)) * 100
            
            # Determine status based on quality thresholds
            if mean_quality >= 30 and q30_percentage >= 90:
                status = "excellent"
            elif mean_quality >= 25 and q30_percentage >= 80:
                status = "good"
            else:
                status = "poor"
            
            logger.info(f"Base quality - Mean: {mean_quality:.1f}, Q30+: {q30_percentage:.1f}%")
            
            return {
                "mean_quality": mean_quality,
                "min_quality": min_quality,
                "max_quality": max_quality,
                "median_quality": median_quality,
                "q30_percentage": q30_percentage,
                "total_bases": total_bases,
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

def count_n_bases(file_path: Path, logger: logging.Logger) -> Dict[str, Any]:
    """
    Count N bases in a FASTQ file.
    
    Args:
        file_path: Path to the FASTQ file.
        logger: Logger instance for logging progress and results.
        
    Returns:
        Dictionary containing N base statistics.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If no valid bases are found in the file.
    """
    total_bases = 0
    n_bases = 0
    total_sequences = 0

    try:
        with open(file_path, 'r') as file:
            lines = iter(file)
            
            for i, line in enumerate(lines):
                if i % 4 == 1:  # Sequence is the second line (index 1) of each record
                    sequence = line.strip().upper()
                    n_bases += sequence.count('N')
                    total_bases += len(sequence)
                    total_sequences += 1
                    
                    # Log progress every 100,000 reads
                    if (i // 4) % 100000 == 0:
                        logger.info(f"Processed {total_sequences} sequences.")
                        
            if total_bases == 0:
                raise ValueError("No valid bases found in the FASTQ file.")
            
            n_percentage = (n_bases / total_bases) * 100
            
            # Determine status based on N base threshold
            if n_percentage < 5:
                status = "pass"
            elif n_percentage < 10:
                status = "warning"
            else:
                status = "fail"
            
            logger.info(f"N bases - Total: {n_bases}, Percentage: {n_percentage:.2f}%")
            
            return {
                "total_n": n_bases,
                "total_bases": total_bases,
                "n_percentage": n_percentage,
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

def setup_timestamped_logging(log_file: str = "fastq_qc.log") -> logging.Logger:
    """
    Set up logging with timestamps for FASTQ quality control operations.
    
    This function configures a logger that writes messages to a file with 
    timestamps included in each log entry.
    
    Args:
        log_file: Name of the log file to write to (default: "fastq_qc.log")
        
    Returns:
        Configured logger instance with timestamp formatting
    """
    # Configure the logging format to include timestamps
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename=log_file,
        filemode='a'  # Append mode
    )
    
    # Create and return a logger instance
    logger = logging.getLogger(__name__)
    return logger

def log_fastq_operation(logger: logging.Logger, operation: str, 
                       file_path: str, details: Dict[str, Any] = None) -> None:
    """
    Log a FASTQ quality control operation with timestamp and details.
    
    Args:
        logger: Logger instance to use for logging
        operation: Type of operation being performed (e.g., "GC calculation", "Validation")
        file_path: Path to the FASTQ file being processed
        details: Optional dictionary with additional details about the operation
    """
    message = f"Operation: {operation} on file: {file_path}"
    
    if details:
        message += f" | Details: {details}"
    
    logger.info(message)
