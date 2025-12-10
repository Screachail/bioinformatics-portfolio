import argparse
import logging
import os
from typing import List, Tuple

from pysradb.sraweb import SRAweb

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def download_fastq(accession: str, output_dir: str = "data/raw") -> Tuple[bool, List[str]]:
    """
    Download FASTQ files from NCBI SRA for a given accession.

    Args:
        accession (str): SRA accession number (e.g., 'SRX123456')
        output_dir (str): Output directory path (default: 'data/raw')

    Returns:
        Tuple[bool, List[str]]: (success: bool, file_paths: List[str])
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize SRAweb
        sra_web = SRAweb()
        
        # Download FASTQ files
        logger.info(f"Downloading FASTQ files for accession {accession}")
        sra_web.download(
            accession=accession,
            out_dir=output_dir,
            file_format="fastq",
            split_files=True
        )
        
        # Get list of downloaded files
        file_paths = []
        for file_name in os.listdir(output_dir):
            if file_name.endswith('.fastq') or file_name.endswith('.fq'):
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
