import pandas as pd
from typing import List, Dict, Any

def generate_activation_insights(df: pd.DataFrame) -> List[str]:
    insights = []
    if df is None or df.empty:
        return ["No data available to generate insights."]
    
    if 'region' in df.columns and 'upi_activation_percent' in df.columns:
        best_region = df.loc[df['upi_activation_percent'].idxmax()]
        worst_region = df.loc[df['upi_activation_percent'].idxmin()]
        insights.append(f"Region <b>{best_region['region']}</b> has the highest UPI activation rate ({best_region['upi_activation_percent']:.1f}%).")
        insights.append(f"Region <b>{worst_region['region']}</b> has the lowest UPI activation rate ({worst_region['upi_activation_percent']:.1f}%).")
    
    if 'branch_id' in df.columns and 'accounts_opened' in df.columns and 'funded_account_percent' in df.columns:
        high_accounts = df[df['accounts_opened'] > df['accounts_opened'].median()]
        if not high_accounts.empty:
            low_funding = high_accounts.sort_values('funded_account_percent').head(3)
            branches = ", ".join(low_funding['branch_id'].astype(str).tolist())
            if branches:
                insights.append(f"Branches with high account opening but low funding: <b>{branches}</b>.")

    return insights

def generate_kyc_insights(df: pd.DataFrame) -> List[str]:
    insights = []
    if df is None or df.empty:
        return ["No data available to generate insights."]
        
    if 'dropoff_stage' in df.columns and 'count' in df.columns:
        top_dropoff = df.sort_values('count', ascending=False).iloc[0]
        insights.append(f"The highest drop-off occurs at the <b>{top_dropoff['dropoff_stage']}</b> stage.")
        
    return insights

def generate_sales_insights(df: pd.DataFrame) -> List[str]:
    insights = []
    if df is None or df.empty:
        return ["No data available to generate insights."]
        
    if 'salesperson_id' in df.columns and 'target_achievement_percent' in df.columns:
        top_performers = df[df['target_achievement_percent'] >= 100]
        insights.append(f"<b>{len(top_performers)}</b> salespersons achieved or exceeded their targets.")
        
    return insights

def generate_dormancy_insights(df: pd.DataFrame) -> List[str]:
    insights = []
    if df is None or df.empty:
        return ["No data available to generate insights."]
        
    if 'days_since_last_tx' in df.columns:
        dormant_count = len(df[df['days_since_last_tx'] > 180])
        total_count = len(df)
        pct = (dormant_count / total_count) * 100 if total_count > 0 else 0
        insights.append(f"<b>{pct:.1f}%</b> ({dormant_count}) of accounts have been dormant for over 180 days.")
        
    return insights

def generate_campaign_insights(df: pd.DataFrame) -> List[str]:
    insights = []
    if df is None or df.empty:
        return ["No data available to generate insights."]
        
    if 'campaign_name' in df.columns and 'roi' in df.columns:
        best_campaign = df.loc[df['roi'].idxmax()]
        insights.append(f"The best performing campaign by ROI is <b>{best_campaign['campaign_name']}</b> with an ROI of {best_campaign['roi']:.2f}.")
        
    return insights

def generate_profile_insights(df: pd.DataFrame) -> List[str]:
    insights = []
    if df is None or df.empty:
        return ["No data available to generate insights."]
    
    insights.append(f"The dataset contains <b>{len(df)}</b> rows and <b>{len(df.columns)}</b> columns.")
    
    missing_pct = df.isnull().mean().mean() * 100
    insights.append(f"Overall missingness across the dataset is <b>{missing_pct:.2f}%</b>.")
    
    numeric_cols = df.select_dtypes(include='number').columns
    if len(numeric_cols) > 0:
        insights.append(f"Found <b>{len(numeric_cols)}</b> numeric columns suitable for correlation analysis.")
        
    return insights
