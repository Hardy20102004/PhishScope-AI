import os
import re

replacements = {
    'backend/app/models/continuous_validation.py': [('class OptimizationRecommendation', 'class CVOptimizationRecommendation')],
    'backend/app/models/digital_twin.py': [('relationship("OptimizationRecommendation"', 'relationship("OptimizationRecommendation"')], # keep one as is
    'backend/app/models/mobile_forensics.py': [
        ('class MobileDevice', 'class ForensicMobileDevice'),
        ('class MobileCommunication', 'class ForensicMobileCommunication'),
        ('class MobileLocation', 'class ForensicMobileLocation'),
        ('relationship("MobileCommunication"', 'relationship("ForensicMobileCommunication"'),
        ('relationship("MobileLocation"', 'relationship("ForensicMobileLocation"'),
        ('relationship("MobileDevice"', 'relationship("ForensicMobileDevice"')
    ],
    'backend/app/models/browser_forensics.py': [
        ('class BrowserExtension', 'class ForensicBrowserExtension'),
        ('relationship("BrowserExtension"', 'relationship("ForensicBrowserExtension"')
    ],
    'backend/app/models/cspm.py': [
        ('class CloudAsset', 'class CSPMCloudAsset'),
        ('relationship("CloudAsset"', 'relationship("CSPMCloudAsset"')
    ],
    'backend/app/models/ciem.py': [
        ('class CloudIdentity', 'class CIEMCloudIdentity'),
        ('relationship("CloudIdentity"', 'relationship("CIEMCloudIdentity"')
    ],
    'backend/app/models/governance.py': [
        ('class ApprovalRecord', 'class GovernanceApprovalRecord'),
        ('relationship("ApprovalRecord"', 'relationship("GovernanceApprovalRecord"')
    ],
    'backend/app/models/cdr.py': [
        ('class CloudInvestigation', 'class CDRCloudInvestigation'),
        ('relationship("CloudInvestigation"', 'relationship("CDRCloudInvestigation"')
    ]
}

for filepath, reps in replacements.items():
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
        for old, new in reps:
            content = content.replace(old, new)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Fixed {filepath}")
