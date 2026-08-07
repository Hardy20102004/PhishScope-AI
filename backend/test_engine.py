import asyncio
from app.services.investigations.website_engine import WebsiteEngine
engine = WebsiteEngine(target="google.com")
engine.run_pipeline()
print(f"Risk Score: {engine.risk_score}")
print(f"Findings: {engine.findings}")
