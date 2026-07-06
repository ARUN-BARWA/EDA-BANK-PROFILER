# Pre-defined KPI logic

def calculate_activation_percent(accounts_opened: int, funded_accounts: int) -> float:
    if accounts_opened == 0:
        return 0.0
    return (funded_accounts / accounts_opened) * 100.0
