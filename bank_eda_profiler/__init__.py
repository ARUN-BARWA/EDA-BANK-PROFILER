"""
bank_eda_profiler - Scalable EDA and MIS reporting for banking datasets.
"""

__version__ = "0.1.0"

from .profiler import BankProfiler
from .config import ReportConfig

__all__ = ["BankProfiler", "ReportConfig"]
