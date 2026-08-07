import re

with open("frontend/src/router/index.tsx", "r") as f:
    content = f.read()

# 1
content = content.replace(
    'import { CredentialGovernanceDashboard } from "@/pages/secrets/CredentialGovernanceDashboard";',
    'import { CredentialGovernanceDashboard as SecretsCredentialGovernanceDashboard } from "@/pages/secrets/CredentialGovernanceDashboard";'
)
content = content.replace(
    'import CredentialGovernanceDashboard from "@/pages/pam/CredentialGovernanceDashboard";',
    'import PAMCredentialGovernanceDashboard from "@/pages/pam/CredentialGovernanceDashboard";'
)
content = re.sub(r'path: "secrets/credentials",\s*element: <CredentialGovernanceDashboard />', r'path: "secrets/credentials",\n            element: <SecretsCredentialGovernanceDashboard />', content)
content = re.sub(r'path: "pam/credentials",\s*element: <CredentialGovernanceDashboard />', r'path: "pam/credentials",\n            element: <PAMCredentialGovernanceDashboard />', content)

# 2
content = content.replace(
    'import { CertificateDashboard } from "@/pages/secrets/CertificateDashboard";',
    'import { CertificateDashboard as SecretsCertificateDashboard } from "@/pages/secrets/CertificateDashboard";'
)
content = content.replace(
    'import CertificateDashboard from "@/pages/nhi/CertificateDashboard";',
    'import NHICertificateDashboard from "@/pages/nhi/CertificateDashboard";'
)
content = re.sub(r'path: "secrets/certificates",\s*element: <CertificateDashboard />', r'path: "secrets/certificates",\n            element: <SecretsCertificateDashboard />', content)
content = re.sub(r'path: "nhi/certificates",\s*element: <CertificateDashboard />', r'path: "nhi/certificates",\n            element: <NHICertificateDashboard />', content)

# 3
content = content.replace(
    'import IdentityRiskDashboard from "@/pages/ispm/IdentityRiskDashboard";',
    'import ISPMIdentityRiskDashboard from "@/pages/ispm/IdentityRiskDashboard";'
)
content = content.replace(
    'import IdentityRiskDashboard from "@/pages/itdr/IdentityRiskDashboard";',
    'import ITDRIdentityRiskDashboard from "@/pages/itdr/IdentityRiskDashboard";'
)
content = content.replace(
    'import IdentityRiskDashboard from "@/pages/identity_intel/IdentityRiskDashboard";',
    'import IntelIdentityRiskDashboard from "@/pages/identity_intel/IdentityRiskDashboard";'
)
content = re.sub(r'path: "ispm/risk",\s*element: <IdentityRiskDashboard />', r'path: "ispm/risk",\n            element: <ISPMIdentityRiskDashboard />', content)
content = re.sub(r'path: "itdr/risk",\s*element: <IdentityRiskDashboard />', r'path: "itdr/risk",\n            element: <ITDRIdentityRiskDashboard />', content)
content = re.sub(r'path: "identity-intel/risk",\s*element: <IdentityRiskDashboard />', r'path: "identity-intel/risk",\n            element: <IntelIdentityRiskDashboard />', content)

# 4
content = content.replace(
    'import { DecisionDashboard } from "@/features/decision/pages/DecisionDashboard";',
    'import { DecisionDashboard as FeaturesDecisionDashboard } from "@/features/decision/pages/DecisionDashboard";'
)
content = content.replace(
    'import DecisionDashboard from "@/pages/orchestration/DecisionDashboard";',
    'import OrchestrationDecisionDashboard from "@/pages/orchestration/DecisionDashboard";'
)
content = re.sub(r'path: "decision",\s*element: <DecisionDashboard />', r'path: "decision",\n            element: <FeaturesDecisionDashboard />', content)
content = re.sub(r'path: "orchestration/decision",\s*element: <DecisionDashboard />', r'path: "orchestration/decision",\n            element: <OrchestrationDecisionDashboard />', content)

with open("frontend/src/router/index.tsx", "w") as f:
    f.write(content)
