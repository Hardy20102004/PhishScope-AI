import os

filepath = 'backend/app/db/base.py'
if os.path.exists(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    replacements = [
        ('OptimizationRecommendation', 'CVOptimizationRecommendation'),
        ('MobileDevice', 'ForensicMobileDevice'),
        ('MobileCommunication', 'ForensicMobileCommunication'),
        ('MobileLocation', 'ForensicMobileLocation'),
        ('BrowserExtension', 'ForensicBrowserExtension'),
        ('CloudAsset', 'CSPMCloudAsset'),
        ('CloudIdentity', 'CIEMCloudIdentity'),
        ('ApprovalRecord', 'GovernanceApprovalRecord'),
        ('CloudInvestigation', 'CDRCloudInvestigation')
    ]
    
    for old, new in replacements:
        content = content.replace(old, new)
        
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Fixed imports in {filepath}")
