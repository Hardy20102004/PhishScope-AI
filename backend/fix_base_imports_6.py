import os

filepath = 'backend/app/db/base.py'
if os.path.exists(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    content = content.replace('RuleGovernanceApprovalRecord', 'RuleApprovalRecord')
    
    with open(filepath, 'w') as f:
        f.write(content)
