import argparse
import os
import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker('en_IN')

def generate_campaigns(n=10):
    data = []
    for i in range(1, n+1):
        data.append({
            "campaign_id": f"CAMP_{i:03d}",
            "campaign_name": f"Campaign {fake.word().capitalize()}",
            "campaign_type": random.choice(["Email", "SMS", "Social", "Search"]),
            "start_date": fake.date_between(start_date="-1y", end_date="-6m"),
            "end_date": fake.date_between(start_date="-5m", end_date="today"),
            "channel": random.choice(["Digital", "Branch"]),
            "target_segment": random.choice(["Mass", "Affluent", "Youth"]),
            "target_region": random.choice(["North", "South", "East", "West", "All"]),
            "campaign_cost": random.randint(10000, 500000),
            "impressions": random.randint(100000, 5000000),
            "clicks": random.randint(1000, 50000),
            "leads_generated": random.randint(500, 10000),
            "applications_started": random.randint(200, 5000),
            "accounts_opened": random.randint(100, 2000),
            "funded_accounts": random.randint(50, 1500)
        })
    return pd.DataFrame(data)

def generate_sales_hierarchy(n=50):
    data = []
    regions = ["North", "South", "East", "West"]
    for i in range(1, n+1):
        data.append({
            "sales_user_id": f"SU_{i:04d}",
            "employee_code": f"EMP{10000+i}",
            "employee_name_masked": f"{fake.first_name()[0]}*** {fake.last_name()}",
            "role": random.choice(["RM", "BDE", "Branch Manager"]),
            "branch_code": f"BR_{random.randint(1, 20):03d}",
            "branch_name": f"{fake.city()} Branch",
            "city": fake.city(),
            "state": fake.state(),
            "region": random.choice(regions),
            "zone": random.choice(["Zone A", "Zone B", "Zone C"]),
            "manager_user_id": f"SU_{random.randint(1, 10):04d}",
            "joining_date": fake.date_between(start_date="-3y", end_date="-1m"),
            "active_flag": random.choice([True, True, True, False])
        })
    return pd.DataFrame(data)

def generate_leads(n: int, campaigns: pd.DataFrame, sales: pd.DataFrame) -> pd.DataFrame:
    data = []
    camp_ids = campaigns["campaign_id"].tolist() + [None]*3 # some organically
    sales_ids = sales["sales_user_id"].tolist() + [None]*5
    branches = sales["branch_code"].unique().tolist()
    
    for i in range(1, n+1):
        created_at = fake.date_time_between(start_date="-1y", end_date="now")
        data.append({
            "lead_id": f"L_{100000+i}",
            "mobile_hash": fake.sha256()[:16],
            "lead_created_at": created_at,
            "lead_source": random.choice(["Organic", "Campaign", "Referral"]),
            "campaign_id": random.choice(camp_ids),
            "utm_source": random.choice(["google", "facebook", "direct", None]),
            "utm_medium": random.choice(["cpc", "social", "none"]),
            "utm_campaign": random.choice(["summer_promo", "festive", None]),
            "device_type": random.choice(["Android", "iOS", "Desktop"]),
            "city": fake.city(),
            "state": fake.state(),
            "pincode": fake.postcode(),
            "region": random.choice(["North", "South", "East", "West"]),
            "assigned_sales_user_id": random.choice(sales_ids),
            "assigned_branch_code": random.choice(branches),
            "lead_status": random.choice(["NEW", "CONTACTED", "CONVERTED", "DROPPED"]),
            "drop_stage": random.choice(["Initial", "Followup", "Doc Collection", None]),
            "last_followup_date": created_at + timedelta(days=random.randint(1, 5)),
            "next_followup_date": created_at + timedelta(days=random.randint(6, 15))
        })
    return pd.DataFrame(data)

def generate_customers_and_accounts(leads: pd.DataFrame, sales: pd.DataFrame):
    converted_leads = leads[leads["lead_status"] == "CONVERTED"].copy()
    num_converted = len(converted_leads)
    
    apps_data = []
    vkyc_data = []
    cust_data = []
    acct_data = []
    holdings_data = []
    
    sales_ids = sales["sales_user_id"].tolist()
    
    for i, (_, lead) in enumerate(converted_leads.iterrows()):
        app_id = f"APP_{200000+i}"
        cust_id = f"C_{300000+i}"
        acct_id = f"A_{400000+i}"
        
        start_time = lead["lead_created_at"] + timedelta(hours=random.randint(1, 48))
        vkyc_req = random.choice([True, False])
        
        # Applications
        apps_data.append({
            "application_id": app_id,
            "lead_id": lead["lead_id"],
            "customer_id": cust_id,
            "application_start_time": start_time,
            "application_submit_time": start_time + timedelta(minutes=random.randint(10, 60)),
            "otp_verified_flag": True,
            "pan_verified_flag": True,
            "aadhaar_verified_flag": True,
            "personal_details_done": True,
            "nominee_added_flag": random.choice([True, False]),
            "vkyc_required_flag": vkyc_req,
            "vkyc_scheduled_time": start_time + timedelta(hours=1) if vkyc_req else None,
            "vkyc_completed_time": start_time + timedelta(hours=2) if vkyc_req else None,
            "vkyc_status": "COMPLETED" if vkyc_req else None,
            "vkyc_failure_reason": None,
            "account_opened_flag": True,
            "account_opened_date": start_time + timedelta(hours=3),
            "application_status": "APPROVED",
            "rejection_reason": None,
            "total_time_to_open_min": random.randint(30, 240),
            "region": lead["region"],
            "branch": lead["assigned_branch_code"],
            "sales_user_id": lead["assigned_sales_user_id"]
        })
        
        # VKYC
        if vkyc_req:
            vkyc_data.append({
                "vkyc_session_id": f"VKYC_{500000+i}",
                "application_id": app_id,
                "customer_id": cust_id,
                "scheduled_time": start_time + timedelta(hours=1),
                "started_time": start_time + timedelta(hours=1, minutes=5),
                "completed_time": start_time + timedelta(hours=1, minutes=15),
                "agent_id": f"AGT_{random.randint(1,50):03d}",
                "language": random.choice(["English", "Hindi", "Regional"]),
                "customer_region": lead["state"],
                "status": "COMPLETED",
                "failure_reason": None,
                "attempts_count": 1,
                "avg_wait_time_sec": random.randint(10, 300),
                "call_duration_sec": random.randint(120, 600),
                "kyc_decision": "APPROVED",
                "decision_date": start_time + timedelta(hours=1, minutes=20)
            })
            
        # Customer
        acq_date = start_time.date()
        cust_data.append({
            "customer_id": cust_id,
            "crn_hash": fake.sha256()[:12],
            "mobile_hash": lead["mobile_hash"],
            "email_hash": fake.sha256()[:16],
            "gender": random.choice(["M", "F", "O"]),
            "age_band": random.choice(["18-25", "26-35", "36-45", "46-60", "60+"]),
            "occupation_type": random.choice(["Salaried", "Self-Employed", "Student"]),
            "income_band": random.choice(["0-5L", "5-10L", "10-20L", "20L+"]),
            "city": lead["city"],
            "state": lead["state"],
            "pincode": lead["pincode"],
            "region": "North", # simplifying
            "customer_segment": random.choice(["Mass", "Prime", "Elite"]),
            "acquisition_date": acq_date,
            "acquisition_channel": lead["lead_source"],
            "kyc_status": "FULL_KYC",
            "risk_category": random.choice(["Low", "Medium", "High"]),
            "active_flag": True,
            "last_active_date": acq_date + timedelta(days=random.randint(1, 30))
        })
        
        # Account
        is_funded = random.random() > 0.3
        acct_data.append({
            "account_id": acct_id,
            "customer_id": cust_id,
            "account_open_date": acq_date,
            "account_type": random.choice(["Savings", "Current"]),
            "account_status": "ACTIVE",
            "branch_code": lead["assigned_branch_code"],
            "region": "North",
            "opening_channel": "Digital",
            "initial_funding_amount": random.randint(1000, 50000) if is_funded else 0,
            "current_balance": random.randint(500, 100000) if is_funded else 0,
            "avg_monthly_balance": random.randint(500, 100000) if is_funded else 0,
            "debit_card_issued_flag": True,
            "virtual_card_active_flag": True,
            "physical_card_ordered": random.choice([True, False]),
            "upi_enabled_flag": random.choice([True, False]),
            "netbanking_active_flag": random.choice([True, False]),
            "mobile_banking_active": True,
            "first_funding_date": acq_date + timedelta(days=random.randint(1,5)) if is_funded else None,
            "first_transaction_date": acq_date + timedelta(days=random.randint(2,10)) if is_funded else None,
            "last_transaction_date": acq_date + timedelta(days=random.randint(10,30)) if is_funded else None
        })
        
        # Holdings
        if is_funded:
            holdings_data.append({
                "customer_id": cust_id,
                "account_id": acct_id,
                "product_code": "SAV_811",
                "product_name": "Kotak 811 Savings",
                "product_category": "LIABILITY",
                "opened_date": acq_date,
                "active_flag": True,
                "balance_or_limit": random.randint(500, 100000),
                "revenue_amount": random.randint(100, 5000),
                "source_channel": "Digital",
                "sales_user_id": lead["assigned_sales_user_id"],
                "region": "North"
            })
            
    return (
        pd.DataFrame(apps_data), 
        pd.DataFrame(vkyc_data), 
        pd.DataFrame(cust_data), 
        pd.DataFrame(acct_data),
        pd.DataFrame(holdings_data)
    )

def generate_transactions(accounts: pd.DataFrame, n_per_account=5):
    funded_accounts = accounts[accounts["first_funding_date"].notnull()]
    data = []
    for _, acct in funded_accounts.iterrows():
        num_tx = random.randint(1, n_per_account)
        for i in range(num_tx):
            tx_date = acct["first_funding_date"] + timedelta(days=random.randint(1, 30))
            data.append({
                "transaction_id": f"TX_{random.randint(1000000, 9999999)}",
                "account_id": acct["account_id"],
                "customer_id": acct["customer_id"],
                "transaction_time": tx_date,
                "transaction_date": tx_date,
                "transaction_type": random.choice(["CREDIT", "DEBIT"]),
                "transaction_channel": random.choice(["UPI", "NEFT", "IMPS", "POS", "ATM"]),
                "amount": random.randint(100, 20000),
                "merchant_category": random.choice(["Groceries", "Dining", "Utility", "E-commerce", None]),
                "merchant_name_masked": "MERCHANT_***",
                "transaction_status": random.choice(["SUCCESS", "SUCCESS", "FAILED"]),
                "failure_reason": None,
                "balance_after_txn": random.randint(5000, 100000),
                "city": fake.city(),
                "state": fake.state(),
                "region": "North",
                "is_salary_credit": random.choice([True, False]),
                "is_bill_payment": random.choice([True, False]),
                "is_upi_transaction": random.choice([True, False]),
                "is_card_transaction": random.choice([True, False])
            })
    return pd.DataFrame(data)

def generate_targets(sales: pd.DataFrame):
    data = []
    months = [datetime(2023, 1, 1), datetime(2023, 2, 1), datetime(2023, 3, 1)]
    for _, su in sales.iterrows():
        for m in months:
            t_acc = random.randint(10, 100)
            a_acc = random.randint(5, 110)
            data.append({
                "target_id": f"TGT_{random.randint(10000, 99999)}",
                "sales_user_id": su["sales_user_id"],
                "branch_code": su["branch_code"],
                "region": su["region"],
                "month": m,
                "target_accounts": t_acc,
                "achieved_accounts": a_acc,
                "target_funded_accounts": int(t_acc * 0.8),
                "achieved_funded_accounts": int(a_acc * 0.8),
                "target_balance": t_acc * 10000,
                "achieved_balance": a_acc * 9500,
                "target_cross_sell": int(t_acc * 0.2),
                "achieved_cross_sell": int(a_acc * 0.15),
                "achievement_percent": (a_acc / t_acc) * 100.0,
                "incentive_eligible_flag": a_acc >= t_acc
            })
    return pd.DataFrame(data)

def generate_complaints(customers: pd.DataFrame):
    data = []
    for _, cust in customers.sample(frac=0.1).iterrows():
        c_time = cust["acquisition_date"] + timedelta(days=random.randint(5, 60))
        data.append({
            "ticket_id": f"TKT_{random.randint(100000, 999999)}",
            "customer_id": cust["customer_id"],
            "account_id": None, # keeping it simple
            "created_time": c_time,
            "closed_time": c_time + timedelta(hours=random.randint(2, 48)),
            "issue_category": random.choice(["Login Issue", "Transaction Failure", "Card Not Received"]),
            "issue_subcategory": "General",
            "channel": random.choice(["App", "Call Center", "Branch"]),
            "status": "CLOSED",
            "resolution_time_hours": random.randint(2, 48),
            "escalation_flag": random.choice([True, False]),
            "customer_region": cust["region"],
            "branch_code": None,
            "satisfaction_score": random.randint(1, 5)
        })
    return pd.DataFrame(data)
    
def generate_events(customers: pd.DataFrame):
    data = []
    for _, cust in customers.sample(frac=0.3).iterrows():
        e_time = cust["acquisition_date"] + timedelta(days=random.randint(1, 30))
        data.append({
            "event_id": f"EVT_{random.randint(100000, 999999)}",
            "customer_id": cust["customer_id"],
            "session_id": fake.uuid4(),
            "event_time": e_time,
            "event_date": e_time,
            "platform": random.choice(["Android", "iOS"]),
            "app_version": "1.0.5",
            "device_type": "Mobile",
            "event_name": random.choice(["App Open", "Login", "Transfer Fund", "Check Balance"]),
            "screen_name": "Home",
            "previous_screen": "Login",
            "session_duration_sec": random.randint(30, 600),
            "error_code": None,
            "error_message": None,
            "city": cust["city"],
            "region": cust["region"]
        })
    return pd.DataFrame(data)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=10000) # smaller default for speed, can be overridden
    parser.add_argument("--output", type=str, default="data/")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    
    print("Generating Dimensions...")
    campaigns = generate_campaigns()
    campaigns.to_parquet(os.path.join(args.output, "campaign_master.parquet"), index=False)
    
    sales = generate_sales_hierarchy()
    sales.to_parquet(os.path.join(args.output, "sales_hierarchy.parquet"), index=False)
    
    targets = generate_targets(sales)
    targets.to_parquet(os.path.join(args.output, "sales_target_achievement.parquet"), index=False)
    
    print(f"Generating {args.rows} leads...")
    leads = generate_leads(args.rows, campaigns, sales)
    leads.to_parquet(os.path.join(args.output, "lead_master.parquet"), index=False)
    
    print("Generating funnel, vkyc, customers, accounts, holdings...")
    apps, vkyc, customers, accounts, holdings = generate_customers_and_accounts(leads, sales)
    apps.to_parquet(os.path.join(args.output, "account_application_funnel.parquet"), index=False)
    vkyc.to_parquet(os.path.join(args.output, "vkyc_session.parquet"), index=False)
    customers.to_parquet(os.path.join(args.output, "customer_master.parquet"), index=False)
    accounts.to_parquet(os.path.join(args.output, "account_master.parquet"), index=False)
    holdings.to_parquet(os.path.join(args.output, "customer_product_holding.parquet"), index=False)
    
    print("Generating transactions...")
    txns = generate_transactions(accounts)
    txns.to_parquet(os.path.join(args.output, "transaction_fact.parquet"), index=False)
    
    print("Generating complaints & events...")
    complaints = generate_complaints(customers)
    complaints.to_parquet(os.path.join(args.output, "service_request_complaint.parquet"), index=False)
    
    events = generate_events(customers)
    events.to_parquet(os.path.join(args.output, "app_event_log.parquet"), index=False)
    
    print("Synthetic Data Generation Complete!")

if __name__ == "__main__":
    main()
