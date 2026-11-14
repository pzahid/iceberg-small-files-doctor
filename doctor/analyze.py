"""Detect small-file problems from a data-file listing and suggest a fix.

Input is a CSV with columns: path,size_bytes (for example exported from
Iceberg's $files metadata, or an object-store listing).
"""
import csv
import statistics
from dataclasses import dataclass

MB = 1024 * 1024


@dataclass
class Report:
    total_files: int
    total_bytes: int
    small_files: int
    small_ratio: float
    median_mb: float
    severity: str


def load(path):
    with open(path, newline="") as f:
        return [int(r["size_bytes"]) for r in csv.DictReader(f)]


def analyze(sizes, target_mb=128, small_fraction=0.25):
    """A file is small when it is under small_fraction of the target size."""
    if not sizes:
        return Report(0, 0, 0, 0.0, 0.0, "none")
    cutoff = target_mb * MB * small_fraction
    small = sum(1 for s in sizes if s < cutoff)
    ratio = small / len(sizes)
    severity = "high" if ratio > 0.6 else "medium" if ratio > 0.3 else "low"
    return Report(len(sizes), sum(sizes), small, ratio,
                  statistics.median(sizes) / MB, severity)


def suggest(table, report):
    if report.severity == "low":
        return "-- No compaction needed."
    return f"OPTIMIZE TABLE {table} REWRITE DATA USING BIN_PACK;"
