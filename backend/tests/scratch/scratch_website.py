import sys
import os
sys.path.append(os.getcwd())
from backend.app.services.investigations.website_engine import WebsiteEngine

engine = WebsiteEngine(target="youtube.com")
success = engine.run_pipeline()
print("Success:", success)
print("Error:", engine.error_message)
print("Score:", engine.risk_score)
