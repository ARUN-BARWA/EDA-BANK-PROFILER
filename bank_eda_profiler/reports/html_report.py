import os
from jinja2 import Environment, FileSystemLoader
from . import charts, insights

def generate_html_reports(reports: dict, output_dir: str):
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    
    os.makedirs(output_dir, exist_ok=True)
    
    report_links = []
    
    # 1. Process specific reports
    for report_name, df in reports.items():
        if df is None:
            continue
            
        template_name = f"{report_name}.html"
        
        # Fallback to base or profile if specific template doesn't exist yet
        if not os.path.exists(os.path.join(template_dir, template_name)):
            if report_name == "profiles":
                template_name = "profile.html"
            else:
                template_name = "generic_report.html"
                
        # Skip privacy warnings from here, handled separately if needed
        if report_name == "privacy_warnings":
            continue
            
        try:
            template = env.get_template(template_name)
        except Exception:
            # Fallback inline if missing generic
            template = env.from_string("{% extends 'base.html' %}{% block content %}<h1>{{ report_name }}</h1>{{ df.to_html() | safe }}{% endblock %}")
            
        # Pass charts and insights modules so the template can call them
        output = template.render(
            report_name=report_name,
            df=df,
            charts=charts,
            insights=insights,
            reports=reports
        )
        
        filename = f"{report_name}.html"
        with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as f:
            f.write(output)
            
        report_links.append({
            "name": report_name.replace("_", " ").title(),
            "url": filename
        })
        
    # 2. Generate Index
    index_template = env.get_template('index.html')
    index_output = index_template.render(links=report_links)
    
    with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_output)
