import os

replacements = {
    'backend/tests/test_continuous_validation.py': [('CVOptimizationRecommendationCreate', 'OptimizationRecommendationCreate'), ('CVOptimizationRecommendationResponse', 'OptimizationRecommendationResponse')],
    'backend/tests/test_mobile_forensics.py': [
        ('ForensicMobileDeviceCreate', 'MobileDeviceCreate'),
        ('ForensicMobileDeviceResponse', 'MobileDeviceResponse'),
        ('ForensicMobileCommunicationCreate', 'MobileCommunicationCreate'),
        ('ForensicMobileCommunicationResponse', 'MobileCommunicationResponse'),
        ('ForensicMobileLocationCreate', 'MobileLocationCreate'),
        ('ForensicMobileLocationResponse', 'MobileLocationResponse')
    ],
    'backend/tests/test_browser_forensics.py': [('ForensicBrowserExtensionCreate', 'BrowserExtensionCreate'), ('ForensicBrowserExtensionResponse', 'BrowserExtensionResponse')],
    'backend/tests/test_cspm.py': [('CSPMCloudAssetCreate', 'CloudAssetCreate'), ('CSPMCloudAssetResponse', 'CloudAssetResponse')],
    'backend/tests/test_ciem.py': [('CIEMCloudIdentityCreate', 'CloudIdentityCreate'), ('CIEMCloudIdentityResponse', 'CloudIdentityResponse')],
    'backend/tests/test_governance.py': [('GovernanceApprovalRecordCreate', 'ApprovalRecordCreate'), ('GovernanceApprovalRecordResponse', 'ApprovalRecordResponse')],
    'backend/tests/test_cdr.py': [('CDRCloudInvestigationCreate', 'CloudInvestigationCreate'), ('CDRCloudInvestigationResponse', 'CloudInvestigationResponse')]
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
