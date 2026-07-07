import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def kpi_card(title: str, value: str, icon: str = "") -> str:
    """Returns HTML for a Bootstrap KPI card."""
    return f"""
    <div class="card text-center mb-4 shadow-sm">
        <div class="card-body">
            <h6 class="card-subtitle mb-2 text-muted">{title}</h6>
            <h2 class="card-title mb-0">{icon} {value}</h2>
        </div>
    </div>
    """

def bar_chart(df: pd.DataFrame, x: str, y: str, title: str, color: str = None) -> str:
    if df is None or df.empty or x not in df.columns or y not in df.columns:
        return "<p>No data available for chart</p>"
    fig = px.bar(df, x=x, y=y, title=title, color=color, template="plotly_white")
    return fig.to_html(full_html=False, include_plotlyjs='cdn')

def line_chart(df: pd.DataFrame, x: str, y: str, title: str, color: str = None) -> str:
    if df is None or df.empty or x not in df.columns or y not in df.columns:
        return "<p>No data available for chart</p>"
    fig = px.line(df, x=x, y=y, title=title, color=color, template="plotly_white")
    return fig.to_html(full_html=False, include_plotlyjs='cdn')

def funnel_chart(df: pd.DataFrame, x: str, y: str, title: str) -> str:
    if df is None or df.empty or x not in df.columns or y not in df.columns:
        return "<p>No data available for chart</p>"
    fig = px.funnel(df, x=x, y=y, title=title, template="plotly_white")
    return fig.to_html(full_html=False, include_plotlyjs='cdn')

def pie_chart(df: pd.DataFrame, names: str, values: str, title: str) -> str:
    if df is None or df.empty or names not in df.columns or values not in df.columns:
        return "<p>No data available for chart</p>"
    fig = px.pie(df, names=names, values=values, title=title, template="plotly_white")
    return fig.to_html(full_html=False, include_plotlyjs='cdn')

def histogram_chart(df: pd.DataFrame, x: str, title: str) -> str:
    if df is None or df.empty or x not in df.columns:
        return "<p>No data available for chart</p>"
    fig = px.histogram(df, x=x, title=title, template="plotly_white")
    return fig.to_html(full_html=False, include_plotlyjs='cdn')

def correlation_heatmap(df: pd.DataFrame, title: str) -> str:
    if df is None or df.empty:
        return "<p>No data available for chart</p>"
    numeric_df = df.select_dtypes(include=['number'])
    if numeric_df.empty:
        return "<p>No numeric data available for correlation</p>"
    corr = numeric_df.corr()
    fig = px.imshow(corr, text_auto=True, title=title, template="plotly_white", aspect="auto")
    return fig.to_html(full_html=False, include_plotlyjs='cdn')

def missingness_chart(df: pd.DataFrame, title: str) -> str:
    if df is None or df.empty:
        return "<p>No data available</p>"
    missing = df.isnull().mean() * 100
    missing_df = missing.reset_index()
    missing_df.columns = ['Column', 'Missing Percentage']
    missing_df = missing_df[missing_df['Missing Percentage'] > 0].sort_values(by='Missing Percentage', ascending=False)
    
    if missing_df.empty:
        return "<p>No missing values found in the dataset.</p>"
    
    fig = px.bar(missing_df, x='Column', y='Missing Percentage', title=title, template="plotly_white")
    return fig.to_html(full_html=False, include_plotlyjs='cdn')

def top_n_bar_chart(df: pd.DataFrame, col: str, n: int = 10, title: str = None) -> str:
    if df is None or df.empty or col not in df.columns:
        return "<p>No data available for chart</p>"
    counts = df[col].value_counts().head(n).reset_index()
    counts.columns = [col, 'Count']
    title = title or f"Top {n} {col}"
    fig = px.bar(counts, x=col, y='Count', title=title, template="plotly_white")
    return fig.to_html(full_html=False, include_plotlyjs='cdn')
