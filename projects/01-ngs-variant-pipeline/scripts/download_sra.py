import argparse
import logging
import os
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Any, Tuple
from pysradb.sraweb import SRAweb

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def validate_fastq(file_path: Path, logger: logging.Logger) -> Dict[str, Any]:
    """
    Validate the structure of a FASTQ file.
    
    Args:
        file_path: Path to the FASTQ file to validate
        logger: Logger instance for logging messages
        
    Returns:
        Dictionary containing validation results with keys:
        - "valid": Boolean indicating if the file is valid
        - "total_reads": Number of reads in the file
        - "errors": List of error descriptions
        - "file_size_mb": Size of the file in megabytes
    """
    # Initialize return values
    result = {
        "valid": True,
        "total_reads": 0,
        "errors": [],
        "file_size_mb": 0.0
    }
    
    # Check if file exists
    if not file_path.exists():
        raise FileNotFoundError(f"FASTQ file not found: {file_path}")
    
    # Check if file is readable
    if not os.access(file_path, os.R_OK):
        raise IOError(f"FASTQ file not readable: {file_path}")
    
    # Get file size
    file_size = file_path.stat().st_size
    result["file_size_mb"] = file_size / (1024 * 1024)
    
    logger.info(f"Validating {file_path.name}...")
    logger.info(f"File size: {result['file_size_mb']:.2f} MB")
    
    # Initialize counters
    total_reads = 0
    error_count = 0
    valid_nucleotides = set('ATCGNatcgN')
    
    try:
        with file_path.open('r') as f:
            line_num = 0
            read_lines = []
            
            for line in f:
                line_num += 1
                line = line.strip()
                
                # Store the line for this read
                read_lines.append(line)
                
                # Process complete read (4 lines)
                if len(read_lines) == 4:
                    # Check header line (starts with @)
                    if not read_lines[0].startswith('@'):
                        error_count += 1
                        result["valid"] = False
                        logger.error(f"Line {line_num-3}: Header line does not start with '@'")
                        result["errors"].append(f"Line {line_num-3}: Header line does not start with '@'")
                        if error_count > 10:
                            break
                    
                    # Check separator line (starts with +)
                    if not read_lines[2].startswith('+'):
                        error_count += 1
                        result["valid"] = False
                        logger.error(f"Line {line_num-1}: Separator line does not start with '+'")
                        result["errors"].append(f"Line {line_num-1}: Separator line does not start with '+'")
                        if error_count > 10:
                            break
                    
                    # Check sequence and quality lengths match
                    seq_len = len(read_lines[1])
                    qual_len = len(read_lines[3])
                    if seq_len != qual_len:
                        error_count += 1
                        result["valid"] = False
                        logger.error(f"Line {line_num-2}: Sequence length ({seq_len}) does not match quality length ({qual_len})")
                        result["errors"].append(f"Line {line_num-2}: Sequence length ({seq_len}) does not match quality length ({qual_len})")
                        if error_count > 10:
                            break
                    
                    # Check sequence contains only valid nucleotides
                    if seq_len > 0:
                        if not all(nucleotide in valid_nucleotides for nucleotide in read_lines[1]):
                            error_count += 1
                            result["valid"] = False
                            logger.error(f"Line {line_num-2}: Sequence contains invalid nucleotides")
                            result["errors"].append(f"Line {line_num-2}: Sequence contains invalid nucleotides")
                            if error_count > 10:
                                break
                    
                    # Reset for next read
                    read_lines = []
                    total_reads += 1
                    
                    # Log progress every 100K reads
                    if total_reads % 100000 == 0:
                        logger.info(f"Processed {total_reads} reads...")
            
            # Check if file has correct number of lines (divisible by 4)
            if line_num % 4 != 0:
                error_count += 1
                result["valid"] = False
                logger.error(f"File has {line_num} lines, which is not divisible by 4")
                result["errors"].append(f"File has {line_num} lines, which is not divisible by 4")
            
            # Check if file is empty
            if total_reads == 0 and line_num > 0:
                error_count += 1
                result["valid"] = False
                logger.error("File is empty or contains no valid reads")
                result["errors"].append("File is empty or contains no valid reads")
                
    except Exception as e:
        logger.error(f"Error reading FASTQ file: {str(e)}")
        raise IOError(f"Error reading FASTQ file: {str(e)}")
    
    logger.info(f"Validation complete: {total_reads} reads, {len(result['errors'])} errors")
    result["total_reads"] = total_reads
    
    return result


def get_read_counts(file_path: Path, logger: logging.Logger) -> int:
    """
    Get the number of reads in a FASTQ file by fast line counting.
    
    Args:
        file_path: Path to the FASTQ file
        logger: Logger instance for logging messages
        
    Returns:
        int: Number of reads in the file
    """
    start_time = time.time()
    
    # Validate file exists and is readable
    if not file_path.exists():
        raise FileNotFoundError(f"FASTQ file not found: {file_path}")
    
    if not os.access(file_path, os.R_OK):
        raise IOError(f"FASTQ file not readable: {file_path}")
    
    # Fast line counting: sum(1 for _ in file) // 4
    try:
        with file_path.open('r') as f:
            line_count = sum(1 for _ in f)
            
        # Validate lines are divisible by 4
        if line_count % 4 != 0:
            raise ValueError(f"FASTQ file has {line_count} lines, which is not divisible by 4")
            
        read_count = line_count // 4
        
    except Exception as e:
        logger.error(f"Error counting reads in FASTQ file: {str(e)}")
        raise IOError(f"Error counting reads in FASTQ file: {str(e)}")
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    if elapsed_time > 1:
        logger.info(f"Read count took {elapsed_time:.2f} seconds for {read_count} reads")
    
    return read_count


def validate_paired_reads(
    r1_path: Path,
    r2_path: Path,
    logger: logging.Logger
) -> Dict[str, Any]:
    """
    Validate that paired-end FASTQ files have matching reads and headers.

    Args:
        r1_path (Path): Path to read 1 FASTQ file.
        r2_path (Path): Path to read 2 FASTQ file.
        logger (logging.Logger): Logger for logging progress.

    Returns:
        Dict[str, Any]: Dictionary with keys:
            - 'paired' (bool): True if paired correctly.
            - 'r1_reads' (int): Number of reads in R1.
            - 'r2_reads' (int): Number of reads in R2.
            - 'mismatches' (List[str]): List of mismatched headers.

    Raises:
        FileNotFoundError: If either file is missing.
    """
    # Check if files exist
    if not r1_path.exists() or not r2_path.exists():
        logger.error("One or both FASTQ files do not exist.")
        raise FileNotFoundError("Files are missing")

    try:
        # Get read counts
        r1_count = get_read_counts(r1_path, logger)
        r2_count = get_read_counts(r2_path, logger)

        if r1_count != r2_count:
            logger.error(f"Read count mismatch: R1={r1_count}, R2={r2_count}")
            return {
                'paired': False,
                'r1_reads': r1_count,
                'r2_reads': r2_count,
                'mismatches': []
            }

        # Sample first 100 reads to check headers
        max_samples = min(100, r1_count)
        mismatches = []

        # Read headers from both files
        r1_headers = []
        r2_headers = []
        
        with open(r1_path, 'r') as f1, open(r2_path, 'r') as f2:
            # Read first max_samples reads from each file
            for i in range(max_samples):
                # Read 4 lines for R1
                r1_header = f1.readline().strip()
                f1.readline()  # sequence
                f1.readline()  # separator
                f1.readline()  # quality
                
                # Read 4 lines for R2
                r2_header = f2.readline().strip()
                f2.readline()  # sequence
                f2.readline()  # separator
                f2.readline()  # quality
                
                # Extract base header (remove /1, /2, .1, .2 suffixes)
                r1_base = r1_header.lstrip('@').rstrip('/1 /2 .1 .2')
                r2_base = r2_header.lstrip('@').rstrip('/1 /2 .1 .2')
                
                r1_headers.append(r1_base)
                r2_headers.append(r2_base)
                
                # Check if headers match
                if r1_base != r2_base:
                    mismatches.append(f"{r1_base} vs {r2_base}")
                    if len(mismatches) >= 10:
                        break

        return {
            'paired': len(mismatches) == 0,
            'r1_reads': r1_count,
            'r2_reads': r2_count,
            'mismatches': mismatches
        }

    except Exception as e:
        logger.error(f"Error validating paired reads: {str(e)}")
        raise


def download_fastq(accession: str, output_dir: str = "data/raw") -> Tuple[bool, List[str]]:
    """
    Download FASTQ files from NCBI SRA for a given accession using fasterq-dump.

    Args:
        accession (str): SRA accession number (e.g., 'SRX123456')
        output_dir (str): Output directory path (default: 'data/raw')

    Returns:
        Tuple[bool, List[str]]: (success: bool, file_paths: List[str])
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Check if fasterq-dump is available
        try:
            subprocess.run(['fasterq-dump', '--version'], check=True, 
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError("fasterq-dump not found. Please install SRA Toolkit.")
        
        # Initialize SRAweb to get metadata
        logger.info("Initializing SRAweb connection...")
        try:
            sra_web = SRAweb()
        except Exception as e:
            logger.error(f"Failed to initialize SRAweb: {str(e)}")
            raise RuntimeError(f"Failed to initialize SRAweb: {str(e)}")
        
        # Get SRA metadata
        logger.info(f"Fetching metadata for accession {accession}")
        metadata = sra_web.sra_metadata(accession)
        
        # Extract run accessions (SRR IDs)
        run_accessions = metadata['run_accession'].tolist()
        logger.info(f"Found {len(run_accessions)} runs to download")
        
        # Download each run using fasterq-dump
        file_paths = []
        for run_accession in run_accessions:
            logger.info(f"Downloading run {run_accession}")
            
            # Use fasterq-dump to download
            result = subprocess.run([
                'fasterq-dump', 
                run_accession, 
                '-O', output_dir,
                '--split-files'
            ], check=True, capture_output=True, text=True)
            
            # Find downloaded files
            for file_name in os.listdir(output_dir):
                if file_name.startswith(run_accession) and (file_name.endswith('.fastq') or file_name.endswith('.fq')):
                    file_paths.append(os.path.join(output_dir, file_name))
        
        logger.info(f"Successfully downloaded {len(file_paths)} FASTQ files")
        return (True, file_paths)
        
    except Exception as e:
        logger.error(f"Error downloading FASTQ files for {accession}: {str(e)}")
        return (False, [])


def main():
    """Main function to handle command-line arguments and execute download."""
    parser = argparse.ArgumentParser(description="Download FASTQ files from NCBI SRA")
    parser.add_argument("--accession", required=True, help="SRA accession number")
    parser.add_argument("--output-dir", default="data/raw", help="Output directory path (default: data/raw)")
    
    args = parser.parse_args()
    
    success, file_paths = download_fastq(args.accession, args.output_dir)
    
    if success:
        logger.info(f"Downloaded files: {file_paths}")
    else:
        logger.error("Download failed")
        exit(1)


if __name__ == "__main__":
    main()
