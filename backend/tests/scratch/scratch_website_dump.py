import sys
import os
sys.path.append(os.getcwd())
from backend.app.services.investigations.website_engine import WebsiteEngine

engine = WebsiteEngine(target="youtube.com")
success = engine.run_pipeline()
print("Success:", success)
print("Findings:", [f.model_dump() for f in engine.findings])
