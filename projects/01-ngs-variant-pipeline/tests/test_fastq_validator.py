import os
import pytest
from unittest.mock import MagicMock
from pathlib import Path

# Import the module to test
import sys
sys.path.insert(0, 'scripts')
from download_sra import validate_fastq

@pytest.fixture
def mock_logger():
    """Create a mock Logger object."""
    return MagicMock()

@pytest.fixture
def tmp_valid_fastq(tmp_path):
    """Create a valid FASTQ file with one read."""
    fastq_file = tmp_path / "valid.fastq"
    fastq_file.write_text(
        "@SRR000001.1 ILLUMINA-52179E_0001:1:1:1260:13059/2\n"
        "GATTTGGGGTTCAAAGCAGTATCGATCAAATAGTAAATCCATTTGTTCAACTCACAGTTT\n"
        "+\n"
        "!''*((((***+))%%%++)(%%%%).1***-+*''))**55CCF>>>>>>CCCCCCC65\n"
    )
    return fastq_file

@pytest.fixture
def tmp_invalid_header(tmp_path):
    """Create a FASTQ file with invalid header (starts with > instead of @)."""
    fastq_file = tmp_path / "invalid_header.fastq"
    fastq_file.write_text(
        ">SRR000001.1\n"
        "GATTTGGGGTTCAAAGCAGTATCGATCAAATAGTAAATCCATTTGTTCAACTCACAGTTT\n"
        "+\n"
        "!''*((((***+))%%%++)(%%%%).1***-+*''))**55CCF>>>>>>CCCCCCC65\n"
    )
    return fastq_file

@pytest.fixture
def tmp_length_mismatch(tmp_path):
    """Create a FASTQ file with sequence and quality length mismatch."""
    fastq_file = tmp_path / "length_mismatch.fastq"
    fastq_file.write_text(
        "@SRR000001.1\n"
        "GATTTGGGG\n"
        "+\n"
        "!''*((((***+))%%%++)(%%%%).1***-+*''))**55CCF>>>>>>CCCCCCC65\n"
    )
    return fastq_file

@pytest.fixture
def tmp_empty_fastq(tmp_path):
    """Create an empty FASTQ file."""
    fastq_file = tmp_path / "empty.fastq"
    fastq_file.write_text("")
    return fastq_file

@pytest.fixture
def tmp_multiple_reads(tmp_path):
    """Create a FASTQ file with multiple valid reads."""
    fastq_file = tmp_path / "multiple_reads.fastq"
    fastq_file.write_text(
        "@SRR000001.1 ILLUMINA-52179E_0001:1:1:1260:13059/2\n"
        "GATTTGGGGTTCAAAGCAGTATCGATCAAATAGTAAATCCATTTGTTCAACTCACAGTTT\n"
        "+\n"
        "!''*((((***+))%%%++)(%%%%).1***-+*''))**55CCF>>>>>>CCCCCCC65\n"
        "@SRR000002.1 ILLUMINA-52179E_0001:1:1:1260:13059/2\n"
        "GATTTGGGGTTCAAAGCAGTATCGATCAAATAGTAAATCCATTTGTTCAACTCACAGTTT\n"
        "+\n"
        "!''*((((***+))%%%++)(%%%%).1***-+*''))**55CCF>>>>>>CCCCCCC65\n"
        "@SRR000003.1 ILLUMINA-52179E_0001:1:1:1260:13059/2\n"
        "GATTTGGGGTTCAAAGCAGTATCGATCAAATAGTAAATCCATTTGTTCAACTCACAGTTT\n"
        "+\n"
        "!''*((((***+))%%%++)(%%%%).1***-+*''))**55CCF>>>>>>CCCCCCC65\n"
    )
    return fastq_file

@pytest.fixture
def tmp_partial_read(tmp_path):
    """Create a FASTQ file with incomplete read (7 lines)."""
    fastq_file = tmp_path / "partial_read.fastq"
    fastq_file.write_text(
        "@SRR000001.1 ILLUMINA-52179E_0001:1:1:1260:13059/2\n"
        "GATTTGGGGTTCAAAGCAGTATCGATCAAATAGTAAATCCATTTGTTCAACTCACAGTTT\n"
        "+\n"
        "!''*((((***+))%%%++)(%%%%).1***-+*''))**55CCF>>>>>>CCCCCCC65\n"
        "@SRR000002.1 ILLUMINA-52179E_0001:1:1:1260:13059/2\n"
        "GATTTGGGGTTCAAAGCAGTATCGATCAAATAGTAAATCCATTTGTTCAACTCACAGTTT\n"
    )
    return fastq_file

def test_validate_fastq_valid_file(tmp_valid_fastq, mock_logger):
    """Test validation of valid FASTQ file."""
    result = validate_fastq(tmp_valid_fastq, mock_logger)
    assert result["valid"] is True
    assert result["total_reads"] == 1
    assert len(result["errors"]) == 0
    assert result["file_size_mb"] > 0

def test_validate_fastq_invalid_header(tmp_invalid_header, mock_logger):
    """Test detection of invalid header line."""
    result = validate_fastq(tmp_invalid_header, mock_logger)
    assert result["valid"] is False
    assert len(result["errors"]) > 0
    assert "header" in result["errors"][0].lower() or "@" in result["errors"][0]

def test_validate_fastq_length_mismatch(tmp_length_mismatch, mock_logger):
    """Test detection of sequence/quality length mismatch."""
    result = validate_fastq(tmp_length_mismatch, mock_logger)
    assert result["valid"] is False
    assert any("length" in err.lower() for err in result["errors"])

def test_validate_fastq_file_not_found(mock_logger):
    """Test FileNotFoundError for non-existent file."""
    with pytest.raises(FileNotFoundError):
        validate_fastq(Path("nonexistent.fastq"), mock_logger)

def test_validate_fastq_empty_file(tmp_empty_fastq, mock_logger):
    """Test handling of empty file."""
    result = validate_fastq(tmp_empty_fastq, mock_logger)
    assert result["total_reads"] == 0
    assert result["file_size_mb"] == 0.0

def test_validate_fastq_multiple_reads(tmp_multiple_reads, mock_logger):
    """Test validation of file with multiple reads."""
    result = validate_fastq(tmp_multiple_reads, mock_logger)
    assert result["valid"] is True
    assert result["total_reads"] == 3
    assert len(result["errors"]) == 0

def test_validate_fastq_partial_read(tmp_partial_read, mock_logger):
    """Test detection of incomplete read (not divisible by 4)."""
    result = validate_fastq(tmp_partial_read, mock_logger)
    assert result["valid"] is False
    assert any("divisible by 4" in err for err in result["errors"])
