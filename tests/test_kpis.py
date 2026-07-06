import pytest
from bank_eda_profiler.banking.kpi_definitions import calculate_activation_percent

def test_activation_percent():
    assert calculate_activation_percent(100, 50) == 50.0
    assert calculate_activation_percent(0, 0) == 0.0
    assert calculate_activation_percent(200, 20) == 10.0
