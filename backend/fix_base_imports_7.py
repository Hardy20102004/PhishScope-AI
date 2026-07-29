import os

filepath = 'backend/app/db/base.py'
if os.path.exists(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    content = content.replace(
        'from app.models.soar import Playbook, ExecutionHistory, GovernanceApprovalRecord',
        'from app.models.soar import Playbook, ExecutionHistory, ApprovalRecord'
    )
    
    with open(filepath, 'w') as f:
        f.write(content)
