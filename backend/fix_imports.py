import os

replacements = {
    'backend/app/api/routers/continuous_validation.py': [('OptimizationRecommendation', 'CVOptimizationRecommendation')],
    'backend/app/api/routers/mobile_forensics.py': [
        ('MobileDevice', 'ForensicMobileDevice'),
        ('MobileCommunication', 'ForensicMobileCommunication'),
        ('MobileLocation', 'ForensicMobileLocation')
    ],
    'backend/app/api/routers/browser_forensics.py': [('BrowserExtension', 'ForensicBrowserExtension')],
    'backend/app/api/routers/cspm.py': [('CloudAsset', 'CSPMCloudAsset')],
    'backend/app/api/routers/ciem.py': [('CloudIdentity', 'CIEMCloudIdentity')],
    'backend/app/api/routers/governance.py': [('ApprovalRecord', 'GovernanceApprovalRecord')],
    'backend/app/api/routers/cdr.py': [('CloudInvestigation', 'CDRCloudInvestigation')]
}

for filepath, reps in replacements.items():
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
        for old, new in reps:
            content = content.replace(old, new)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Fixed imports in {filepath}")
