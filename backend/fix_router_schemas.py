import os

replacements = {
    'backend/app/api/routers/continuous_validation.py': [('CVOptimizationRecommendationCreate', 'OptimizationRecommendationCreate'), ('CVOptimizationRecommendationResponse', 'OptimizationRecommendationResponse')],
    'backend/app/api/routers/mobile_forensics.py': [
        ('ForensicMobileDeviceCreate', 'MobileDeviceCreate'),
        ('ForensicMobileDeviceResponse', 'MobileDeviceResponse'),
        ('ForensicMobileCommunicationCreate', 'MobileCommunicationCreate'),
        ('ForensicMobileCommunicationResponse', 'MobileCommunicationResponse'),
        ('ForensicMobileLocationCreate', 'MobileLocationCreate'),
        ('ForensicMobileLocationResponse', 'MobileLocationResponse')
    ],
    'backend/app/api/routers/browser_forensics.py': [('ForensicBrowserExtensionCreate', 'BrowserExtensionCreate'), ('ForensicBrowserExtensionResponse', 'BrowserExtensionResponse')],
    'backend/app/api/routers/cspm.py': [('CSPMCloudAssetCreate', 'CloudAssetCreate'), ('CSPMCloudAssetResponse', 'CloudAssetResponse')],
    'backend/app/api/routers/ciem.py': [('CIEMCloudIdentityCreate', 'CloudIdentityCreate'), ('CIEMCloudIdentityResponse', 'CloudIdentityResponse')],
    'backend/app/api/routers/governance.py': [('GovernanceApprovalRecordCreate', 'ApprovalRecordCreate'), ('GovernanceApprovalRecordResponse', 'ApprovalRecordResponse')],
    'backend/app/api/routers/cdr.py': [('CDRCloudInvestigationCreate', 'CloudInvestigationCreate'), ('CDRCloudInvestigationResponse', 'CloudInvestigationResponse')]
}

for filepath, reps in replacements.items():
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
        for old, new in reps:
            content = content.replace(old, new)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Fixed schema names in {filepath}")
