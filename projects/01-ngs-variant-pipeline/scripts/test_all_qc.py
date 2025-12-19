#!/usr/bin/env python3
"""Test all QC functions on real E. coli data."""

import logging
from pathlib import Path
import sys

sys.path.insert(0, 'scripts')
from fastq_qc import (
    calculate_gc_content,
    calculate_base_quality,
    count_n_bases
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

test_file = Path('data/raw/test/SRR000001_2.fastq')

print("\n" + "="*70)
print("FASTQ QUALITY CONTROL COMPREHENSIVE REPORT")
print("="*70)
print(f"File: {test_file.name}")
print(f"Size: {test_file.stat().st_size / 1024 / 1024:.2f} MB\n")

# 1. GC Content
print("1. GC CONTENT ANALYSIS")
print("-" * 70)
gc = calculate_gc_content(test_file, logger)
print(f"   GC Percentage: {gc['gc_percentage']:.2f}%")
print(f"   Total Bases: {gc['total_bases']:,}")
print(f"   GC Bases: {gc['gc_bases']:,}")
print(f"   AT Bases: {gc['at_bases']:,}")
print(f"   N Bases: {gc['n_bases']:,}")
print(f"   Expected Range: 50-51% (E. coli)")
print(f"   In Range: {gc['in_expected_range']}")
print(f"   Status: {gc['status']}\n")

# 2. Base Quality
print("2. BASE QUALITY SCORES")
print("-" * 70)
qual = calculate_base_quality(test_file, logger)
print(f"   Mean Quality: Q{qual['mean_quality']:.1f}")
print(f"   Min Quality: Q{qual['min_quality']}")
print(f"   Max Quality: Q{qual['max_quality']}")
print(f"   Median Quality: Q{qual['median_quality']:.1f}")
print(f"   Q30+ Percentage: {qual['q30_percentage']:.1f}%")
print(f"   Total Bases: {qual['total_bases']:,}")
print(f"   Status: {qual['status']}\n")

# 3. N Bases
print("3. AMBIGUOUS BASE (N) ANALYSIS")
print("-" * 70)
n_bases = count_n_bases(test_file, logger)
print(f"   Total N Bases: {n_bases['total_n']:,}")
print(f"   Total Bases: {n_bases['total_bases']:,}")
print(f"   N Percentage: {n_bases['n_percentage']:.2f}%")
print(f"   Threshold: <5% (good quality)")
print(f"   Status: {n_bases['status']}\n")

# Summary
print("="*70)
print("SUMMARY")
print("="*70)
all_pass = (
    gc['status'] == 'valid' and
    qual['status'] in ['excellent', 'good'] and
    n_bases['status'] == 'pass'
)
print(f"Overall Quality: {'✓ PASS' if all_pass else '✗ ISSUES DETECTED'}")
print("="*70 + "\n")
