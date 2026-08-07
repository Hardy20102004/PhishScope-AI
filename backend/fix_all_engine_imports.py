import os

replacements = {
    'backend/app/browser_forensics/extension_engine.py': [('BrowserExtension', 'ForensicBrowserExtension')],
    'backend/app/cspm/asset_discovery_engine.py': [('CloudAsset', 'CSPMCloudAsset')],
    'backend/app/cspm/risk_assessment_engine.py': [('CloudAsset', 'CSPMCloudAsset')],
    'backend/app/ciem/identity_manager.py': [('CloudIdentity', 'CIEMCloudIdentity')],
    'backend/app/governance/workflow_engine.py': [('ApprovalRecord', 'GovernanceApprovalRecord')],
    'backend/app/cdr/telemetry_engine.py': [('CloudInvestigation', 'CDRCloudInvestigation')],
    'backend/app/cdr/response_engine.py': [('CloudInvestigation', 'CDRCloudInvestigation')]
}

for root, _, files in os.walk('backend/app'):
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()
                
            original_content = content
            if 'app.models.continuous_validation' in content:
                content = content.replace('OptimizationRecommendation', 'CVOptimizationRecommendation')
            if 'app.models.browser_forensics' in content:
                content = content.replace('BrowserExtension', 'ForensicBrowserExtension')
            if 'app.models.cspm' in content:
                content = content.replace('CloudAsset', 'CSPMCloudAsset')
            if 'app.models.ciem' in content:
                content = content.replace('CloudIdentity', 'CIEMCloudIdentity')
            if 'app.models.governance' in content:
                content = content.replace('ApprovalRecord', 'GovernanceApprovalRecord')
            if 'app.models.cdr' in content:
                content = content.replace('CloudInvestigation', 'CDRCloudInvestigation')
                
            if original_content != content:
                with open(filepath, 'w') as f:
                    f.write(content)
                print(f"Auto-fixed {filepath}")
