import os

replacements = {
    'backend/tests/test_continuous_validation.py': [('OptimizationRecommendation', 'CVOptimizationRecommendation')],
    'backend/tests/test_mobile_forensics.py': [
        ('MobileDevice', 'ForensicMobileDevice'),
        ('MobileCommunication', 'ForensicMobileCommunication'),
        ('MobileLocation', 'ForensicMobileLocation')
    ],
    'backend/tests/test_browser_forensics.py': [('BrowserExtension', 'ForensicBrowserExtension')],
    'backend/tests/test_cspm.py': [('CloudAsset', 'CSPMCloudAsset')],
    'backend/tests/test_ciem.py': [('CloudIdentity', 'CIEMCloudIdentity')],
    'backend/tests/test_governance.py': [('ApprovalRecord', 'GovernanceApprovalRecord')],
    'backend/tests/test_cdr.py': [('CloudInvestigation', 'CDRCloudInvestigation')]
}

for filepath, reps in replacements.items():
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
        for old, new in reps:
            content = content.replace(old, new)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Fixed test imports in {filepath}")
