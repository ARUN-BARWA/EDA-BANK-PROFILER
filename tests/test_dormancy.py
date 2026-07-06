import pytest
import pandas as pd
from bank_eda_profiler.banking.dormancy import generate_dormancy_report

class MockEngine:
    def execute_query(self, query):
        data = {
            "customer_id": [1, 2],
            "account_id": [10, 20],
            "region": ["North", "South"],
            "branch_code": ["B1", "B2"],
            "account_open_date": ["2023-01-01", "2023-01-01"],
            "first_funding_date": ["2023-01-02", "2023-01-02"],
            "first_transaction_date": ["2023-01-03", None],
            "last_transaction_date": ["2023-09-01", None],
            "current_balance": [1000, 0],
            "dormant_30_flag": [False, True],
            "dormant_60_flag": [False, True],
            "dormant_90_flag": [False, True],
            "opened_but_never_funded_flag": [False, False],
            "funded_but_never_transacted_flag": [False, True]
        }
        return pd.DataFrame(data)

def test_dormancy_generation():
    engine = MockEngine()
    df = generate_dormancy_report(engine, "test_table")
    
    assert not df.empty
    assert len(df) == 2
    assert df.iloc[1]["funded_but_never_transacted_flag"] == True
