import sys
import os
sys.path.append(os.getcwd())
from backend.app.services.investigations.email_engine import EmailEngine

eml = """From: attacker@evil.com
To: victim@company.com
Subject: URGENT: Invoice Payment Required

Please see the attached invoice and pay immediately.
"""

engine = EmailEngine(target="test", raw_content=eml)
engine.run_pipeline()
print("Score:", engine.risk_score)
print("Findings:", [f.title for f in engine.findings])
