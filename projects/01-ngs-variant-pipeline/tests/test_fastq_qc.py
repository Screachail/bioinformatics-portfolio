import pytest
from unittest.mock import MagicMock
from pathlib import Path
import sys
import logging

sys.path.insert(0, 'scripts')
from fastq_qc import (
    calculate_gc_content,
    calculate_base_quality,
    count_n_bases
)

@pytest.fixture
def mock_logger():
    """Return a mocked logger for testing."""
    return MagicMock(spec=logging.Logger)

@pytest.fixture
def tmp_fastq_high_gc(tmp_path):
    """FASTQ with 80% GC content - 4 reads."""
    content = (
        "@read1\n"
        "GCGCGCGCGCGCGCGCGCGC\n"  # 20 bases, 80% GC
        "+\n"
        "IIIIIIIIIIIIIIIIIIII\n"
    )
    file = tmp_path / "high_gc.fastq"
    file.write_text(content * 4)  # 4 reads
    return file

@pytest.fixture
def tmp_fastq_low_gc(tmp_path):
    """FASTQ with 20% GC content - 4 reads."""
    content = (
        "@read1\n"
        "ATCGATCGATCGATCGATCG\n"  # 20 bases, 20% GC
        "+\n"
        "IIIIIIIIIIIIIIIIIIII\n"
    )
    file = tmp_path / "low_gc.fastq"
    file.write_text(content * 4)
    return file

@pytest.fixture
def tmp_fastq_normal_gc(tmp_path):
    """FASTQ with 50% GC content - 4 reads."""
    content = (
        "@read1\n"
        "GATCGATCGATCGATCGATC\n"  # 20 bases, 50% GC
        "+\n"
        "IIIIIIIIIIIIIIIIIIII\n"
    )
    file = tmp_path / "normal_gc.fastq"
    file.write_text(content * 4)
    return file

@pytest.fixture
def tmp_fastq_good_quality(tmp_path):
    """FASTQ with high quality scores - Q30."""
    content = (
        "@read1\n"
        "ATCGATCGATCGATCGATCG\n"
        "+\n"
        "<<<<<<<<<<\n"  # Q30 is '<'
        # Repeat for multiple reads
    )
    file = tmp_path / "good_quality.fastq"
    file.write_text(content * 4)
    return file

@pytest.fixture
def tmp_fastq_poor_quality(tmp_path):
    """FASTQ with low quality scores - Q10."""
    content = (
        "@read1\n"
        "ATCGATCGATCGATCGATCG\n"
        "+\n"
        "++++\n"  # Q10 is '+'
        # Repeat for multiple reads
    )
    file = tmp_path / "poor_quality.fastq"
    file.write_text(content * 4)
    return file

@pytest.fixture
def tmp_fastq_with_n_bases(tmp_path):
    """FASTQ with 10% N bases."""
    sequence = "ATCGATCGATCGATCGATNN"  # 20 bases, 2 N = 10%
    content = f"@read1\n{sequence}\n+\n{'I'*20}\n"
    file = tmp_path / "with_n.fastq"
    file.write_text(content * 4)
    return file

@pytest.fixture
def tmp_fastq_no_n_bases(tmp_path):
    """FASTQ with no N bases."""
    sequence = "ATCGATCGATCGATCGATC"  # 20 bases, 0 N
    content = f"@read1\n{sequence}\n+\n{'I'*20}\n"
    file = tmp_path / "no_n.fastq"
    file.write_text(content * 4)
    return file

def test_gc_content_high(tmp_fastq_high_gc, mock_logger):
    """Test detection of high GC content."""
    result = calculate_gc_content(tmp_fastq_high_gc, mock_logger)
    assert result["gc_percentage"] == pytest.approx(80.0, abs=1.0)
    assert not result["in_expected_range"]
    assert result["status"] == "warning"
    assert "gc_bases" in result
    assert "at_bases" in result

def test_gc_content_low(tmp_fastq_low_gc, mock_logger):
    """Test detection of low GC content."""
    result = calculate_gc_content(tmp_fastq_low_gc, mock_logger)
    assert result["gc_percentage"] == pytest.approx(20.0, abs=1.0)
    assert not result["in_expected_range"]
    assert result["status"] == "warning"
    assert "gc_bases" in result
    assert "at_bases" in result

def test_gc_content_file_not_found(mock_logger):
    """Test FileNotFoundError for missing file."""
    with pytest.raises(FileNotFoundError):
        calculate_gc_content(Path("nonexistent.fastq"), mock_logger)

def test_base_quality_good(tmp_fastq_good_quality, mock_logger):
    """Test high quality scores."""
    result = calculate_base_quality(tmp_fastq_good_quality, mock_logger)
    assert result["mean_quality"] > 30
    assert result["q30_percentage"] > 90.0
    assert result["status"] == "excellent"
    assert "min_quality" in result
    assert "max_quality" in result

def test_base_quality_poor(tmp_fastq_poor_quality, mock_logger):
    """Test low quality scores."""
    result = calculate_base_quality(tmp_fastq_poor_quality, mock_logger)
    assert result["mean_quality"] < 20
    assert result["q30_percentage"] < 10.0
    assert result["status"] == "poor"
    assert "min_quality" in result
    assert "max_quality" in result

def test_base_quality_file_not_found(mock_logger):
    """Test FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        calculate_base_quality(Path("nonexistent.fastq"), mock_logger)

def test_n_bases_none(tmp_fastq_no_n_bases, mock_logger):
    """Test file with no N bases."""
    result = count_n_bases(tmp_fastq_no_n_bases, mock_logger)
    assert result["total_n"] == 0
    assert result["n_percentage"] == pytest.approx(0.0, abs=1e-6)
    assert result["status"] == "pass"

def test_n_bases_some(tmp_fastq_with_n_bases, mock_logger):
    """Test file with moderate N bases."""
    result = count_n_bases(tmp_fastq_with_n_bases, mock_logger)
    assert result["total_n"] > 0
    assert result["n_percentage"] == pytest.approx(10.0, abs=1.0)
    assert result["status"] in ["pass", "warning"]

def test_n_bases_file_not_found(mock_logger):
    """Test FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        count_n_bases(Path("nonexistent.fastq"), mock_logger)

def test_n_bases_percentage(tmp_fastq_with_n_bases, mock_logger):
    """Test correct percentage calculation."""
    result = count_n_bases(tmp_fastq_with_n_bases, mock_logger)
    assert result["n_percentage"] == pytest.approx((result["total_n"] / 
result["total_bases"]) * 100, abs=1e-6)

def test_gc_content_custom_range(tmp_fastq_high_gc, mock_logger):
    """Test custom expected range."""
    result = calculate_gc_content(tmp_fastq_high_gc, mock_logger, 
expected_range=(75.0, 85.0))
    assert result["gc_percentage"] == pytest.approx(80.0, abs=1.0)
    assert result["in_expected_range"]
    assert result["status"] in ["valid", "warning"]

def test_base_quality_statistics(tmp_fastq_good_quality, mock_logger):
    """Test statistical calculations."""
    result = calculate_base_quality(tmp_fastq_good_quality, mock_logger)
    assert all(key in result for key in ["mean_quality", "min_quality", 
"max_quality", "median_quality"])
    assert result["q30_percentage"] > 90.0
