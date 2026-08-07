import sys
import os
sys.path.append(os.getcwd())
from backend.app.services.investigations.url_engine import URLEngine

engine = URLEngine(target="http://example.com")
engine.run_pipeline()
print("Score:", engine.risk_score)
print("Findings:", [f.title for f in engine.findings])
