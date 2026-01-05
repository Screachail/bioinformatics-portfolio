import os
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from typing import List, Tuple

# Import the module to test
import sys
sys.path.insert(0, 'scripts')
from download_sra import download_fastq, main

@pytest.fixture
def tmp_path(tmp_path_factory):
    """Create a temporary directory path."""
    return tmp_path_factory.mktemp("test_download_sra")

@pytest.fixture
def mock_sraweb():
    """Create a mock SRAweb object."""
    mock = MagicMock()
    return mock

def test_download_fastq_success(tmp_path, monkeypatch, mock_sraweb):
    """Test successful download with valid accession."""
    # Mock the SRAweb object
    monkeypatch.setattr('pysradb.SRAweb', lambda: mock_sraweb)
    
    # Mock the download function to return a list of files
    mock_sraweb.download.return_value = [
        "SRR123456_1.fastq.gz",
        "SRR123456_2.fastq.gz"
    ]
    
    # Call the function
    result = download_fastq("SRR123456", str(tmp_path))
    
    # Verify the result
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert result[0] is True  # Success
    assert isinstance(result[1], list)
    assert len(result[1]) == 2
    assert "SRR123456_1.fastq.gz" in result[1]
    assert "SRR123456_2.fastq.gz" in result[1]
    
    # Verify that download was called with correct arguments
    mock_sraweb.download.assert_called_once_with(
        accession="SRR123456",
        out_dir=str(tmp_path),
        split_files=True,
        verbose=False
    )

def test_download_fastq_invalid_accession(tmp_path, monkeypatch, mock_sraweb):
    """Test error handling for invalid SRA ID."""
    # Mock the SRAweb object
    monkeypatch.setattr('pysradb.SRAweb', lambda: mock_sraweb)
    
    # Mock the download function to raise an exception
    mock_sraweb.download.side_effect = Exception("Invalid accession")
    
    # Call the function
    result = download_fastq("INVALID123", str(tmp_path))
    
    # Verify the result
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert result[0] is False  # Failure
    assert isinstance(result[1], list)
    assert len(result[1]) == 0

def test_download_fastq_creates_directory(tmp_path, monkeypatch, mock_sraweb):
    """Test that output directory is created if it doesn't exist."""
    # Mock the SRAweb object
    monkeypatch.setattr('pysradb.SRAweb', lambda: mock_sraweb)
    
    # Mock the download function to return a list of files
    mock_sraweb.download.return_value = ["SRR123456_1.fastq.gz"]
    
    # Create a non-existent directory path
    output_dir = os.path.join(tmp_path, "nonexistent", "subdir")
    
    # Call the function
    result = download_fastq("SRR123456", output_dir)
    
    # Verify that the directory was created
    assert os.path.exists(output_dir)
    
    # Verify the result
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert result[0] is True  # Success
    assert len(result[1]) == 1

def test_download_fastq_network_error(tmp_path, monkeypatch, mock_sraweb):
    """Test error handling for network failure."""
    # Mock the SRAweb object
    monkeypatch.setattr('pysradb.SRAweb', lambda: mock_sraweb)
    
    # Mock the download function to raise a network error
    mock_sraweb.download.side_effect = Exception("Network error")
    
    # Call the function
    result = download_fastq("SRR123456", str(tmp_path))
    
    # Verify the result
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert result[0] is False  # Failure
    assert isinstance(result[1], list)
    assert len(result[1]) == 0

def test_main_function(monkeypatch, tmp_path):
    """Test CLI argument parsing in main function."""
    # Mock the download_fastq function
    with patch('download_sra.download_fastq') as mock_download:
        mock_download.return_value = (True, ["SRR123456_1.fastq.gz"])
        
        # Mock sys.argv to simulate command line arguments
        monkeypatch.setattr('sys.argv', ['download_sra.py', 'SRR123456'])
        
        # Call main function
        main()
        
        # Verify that download_fastq was called with correct arguments
        mock_download.assert_called_once_with('SRR123456', 'data/raw')
