import pytest
import pandas as pd
from bank_eda_profiler.banking.funnel import generate_funnel

class MockEngine:
    def execute_query(self, query):
        data = {
            "application_start_time_count": [1000],
            "otp_verified_flag_count": [900],
            "pan_verified_flag_count": [800]
        }
        return pd.DataFrame(data)

def test_funnel_generation():
    engine = MockEngine()
    df = generate_funnel(engine, "test_table", ["application_start_time", "otp_verified_flag", "pan_verified_flag"])
    
    assert not df.empty
    assert len(df) == 3
    assert df.iloc[0]["users_at_step"] == 1000
    assert df.iloc[1]["drop_count"] == 100
    assert df.iloc[2]["conversion_from_first"] == 80.0
