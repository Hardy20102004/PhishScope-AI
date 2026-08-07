import os

replacements = [
    ('CVCVOptimizationRecommendation', 'CVOptimizationRecommendation'),
    ('ForensicForensicBrowserExtension', 'ForensicBrowserExtension'),
    ('CSPMCSPMCloudAsset', 'CSPMCloudAsset'),
    ('CIEMCIEMCloudIdentity', 'CIEMCloudIdentity'),
    ('GovernanceGovernanceApprovalRecord', 'GovernanceApprovalRecord'),
    ('CDRCDRCloudInvestigation', 'CDRCloudInvestigation'),
]

for root, _, files in os.walk('backend/app'):
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()
                
            original_content = content
            for old, new in replacements:
                content = content.replace(old, new)
                
            if original_content != content:
                with open(filepath, 'w') as f:
                    f.write(content)
                print(f"Fixed double-replace in {filepath}")
