from fastapi import APIRouter

from app.api.v1.endpoints import (
    ai_brain,
    ai_context,
    ai_memory,
    auth,
    automation,
    browser_investigation,
    cases,
    cloud_investigation,
    cyber_command,
    cyber_governance,
    cyber_os,
    dashboard,
    data_fabric,
    decision,
    email_intelligence,
    extension,
    health,
    investigations,
    knowledge_evolution,
    knowledge_graph,
    malware_intelligence,
    mobile,
    mobile_investigation,
    models,
    multi_agent,
    network_investigation,
    observability,
    prompt_platform,
    qr_intelligence,
    rag,
    reports,
    tenants,
    threat_intel,
    url_intelligence,
    users,
    version,
    website_investigation,
    xai,
)
from app.api.routers import ioc, ti_feed, threat_actor, campaign, attack_graph, reputation, cloud, timeline, predictive, alerts, detection, ai_triage, threat_hunting, incident_response, soar, collaboration, executive, soc_copilot, digital_twin, disk_forensics, memory_forensics, mobile_forensics, browser_forensics, email_forensics, malware_analysis, cloud_forensics, unified_timeline, reporting_engine, dfir_copilot, bas_platform, red_team, blue_team, continuous_validation, attack_path, detection_gap, cyber_resilience, executive_intelligence, strategic_defense, cspm, cwpp, k8s_security, ciem, cdr, dspm, multi_cloud, governance, ctem, command_center, aspm, devsecops, sbom, sast, dast, sca, secrets, iac, copilot, appsec_command_center, ispm, zta, pam, itdr, iga, nhi, authn, federation, identity_intel, identity_command_center, cyber_fusion, orchestration, digital_twin, predictive_risk

api_router = APIRouter()

# Mount all v1 routes here
api_router.include_router(health.router, prefix="/health", tags=["system"])
api_router.include_router(version.router, prefix="/version", tags=["system"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(data_fabric.router, prefix="/data-fabric", tags=["Enterprise Security Data Fabric"])
api_router.include_router(investigations.router, prefix="/investigations", tags=["investigations"])
api_router.include_router(threat_intel.router, prefix="/threat-intel", tags=["threat-intel"])
api_router.include_router(url_intelligence.router, prefix="/url-intelligence", tags=["url-intelligence"])
api_router.include_router(website_investigation.router, prefix="/website-investigation", tags=["website-investigation"])
api_router.include_router(email_intelligence.router, prefix="/email-intelligence", tags=["email-intelligence"])
api_router.include_router(qr_intelligence.router, prefix="/qr-intelligence", tags=["qr-intelligence"])
api_router.include_router(malware_intelligence.router, prefix="/malware-intelligence", tags=["malware-intelligence"])
api_router.include_router(mobile_investigation.router, prefix="/mobile-investigation", tags=["mobile-investigation"])
api_router.include_router(browser_investigation.router, prefix="/browser-investigation", tags=["browser-investigation"])
api_router.include_router(network_investigation.router, prefix="/network-investigation", tags=["network-investigation"])
api_router.include_router(cloud_investigation.router, prefix="/cloud-investigation", tags=["cloud-investigation"])
api_router.include_router(cases.router, prefix="/cases", tags=["cases"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(automation.router, prefix="/automation", tags=["automation"])
api_router.include_router(extension.router, prefix="/extension", tags=["extension"])
api_router.include_router(mobile.router, prefix="/mobile", tags=["mobile"])
api_router.include_router(tenants.router, prefix="/tenants", tags=["tenants"])
api_router.include_router(observability.router, prefix="/observability", tags=["observability"])
api_router.include_router(ai_brain.router, prefix="/ai-brain", tags=["ai-security-brain"])
api_router.include_router(multi_agent.router, prefix="/multi-agent", tags=["multi-agent"])
api_router.include_router(ai_memory.router, prefix="/ai-memory", tags=["AI Memory Engine"])
api_router.include_router(ai_context.router, prefix="/ai-context", tags=["AI Context Engine"])
api_router.include_router(prompt_platform.router, prefix="/prompt-platform", tags=["Prompt Engineering Platform"])
api_router.include_router(rag.router, prefix="/rag", tags=["Enterprise RAG Platform"])
api_router.include_router(knowledge_graph.router, prefix="/knowledge-graph", tags=["Enterprise Knowledge Graph"])
api_router.include_router(decision.router, prefix="/decision", tags=["AI Decision Engine"])
api_router.include_router(xai.router, prefix="/xai", tags=["Explainable AI"])
api_router.include_router(models.router, prefix="/models", tags=["AI Model Manager"])
api_router.include_router(ioc.router, prefix="/ioc", tags=["Enterprise IOC Correlation Engine"])
api_router.include_router(ti_feed.router, prefix="/ti-feed", tags=["Enterprise Threat Intelligence Feed Platform"])
api_router.include_router(threat_actor.router, prefix="/threat-actor", tags=["Enterprise Threat Actor Intelligence Platform"])
api_router.include_router(campaign.router, prefix="/campaign", tags=["Enterprise Campaign Detection Engine"])
api_router.include_router(attack_graph.router, prefix="/attack-graph", tags=["Enterprise Attack Graph Generator"])
api_router.include_router(reputation.router, prefix="/reputation", tags=["Enterprise Reputation Intelligence Platform"])
api_router.include_router(cloud.router, prefix="/cloud", tags=["Enterprise Threat Intelligence Cloud"])
api_router.include_router(timeline.router, prefix="/timeline", tags=["Enterprise Threat Timeline Intelligence"])
api_router.include_router(predictive.router, prefix="/predictive", tags=["Enterprise Predictive Threat Intelligence"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["Enterprise Security Alert Management"])
api_router.include_router(detection.router, prefix="/detection", tags=["Enterprise Detection Rule Engine"])
api_router.include_router(ai_triage.router, prefix="/ai-triage", tags=["Enterprise AI Alert Triage"])
api_router.include_router(threat_hunting.router, prefix="/threat-hunting", tags=["Enterprise AI Threat Hunting Workspace"])
api_router.include_router(incident_response.router, prefix="/incident-response", tags=["Enterprise Incident Response & Case Management"])
api_router.include_router(soar.router, prefix="/soar", tags=["Enterprise SOAR Playbooks & Automation"])
api_router.include_router(collaboration.router, prefix="/collaboration", tags=["Enterprise SOC Collaboration Workspace"])
api_router.include_router(executive.router, prefix="/executive", tags=["Enterprise SOC Executive Dashboard"])
api_router.include_router(soc_copilot.router, prefix="/soc-copilot", tags=["Enterprise AI SOC Copilot"])
api_router.include_router(digital_twin.router, prefix="/digital-twin", tags=["Enterprise SOC Digital Twin"])
api_router.include_router(disk_forensics.router, prefix="/disk-forensics", tags=["Enterprise Disk Forensics"])
api_router.include_router(memory_forensics.router, prefix="/memory-forensics", tags=["Enterprise Memory Forensics"])
api_router.include_router(mobile_forensics.router, prefix="/mobile-forensics", tags=["Enterprise Mobile Forensics"])
api_router.include_router(browser_forensics.router, prefix="/browser-forensics", tags=["Enterprise Browser Forensics"])
api_router.include_router(email_forensics.router, prefix="/email-forensics", tags=["Enterprise Email Forensics"])
api_router.include_router(malware_analysis.router, prefix="/malware-analysis", tags=["Enterprise Malware Laboratory"])
api_router.include_router(cloud_forensics.router, prefix="/cloud-forensics", tags=["Enterprise Cloud Forensics"])
api_router.include_router(unified_timeline.router, prefix="/unified-timeline", tags=["Enterprise Unified Timeline"])
api_router.include_router(reporting_engine.router, prefix="/reporting-engine", tags=["Enterprise Forensic Reporting"])
api_router.include_router(dfir_copilot.router, prefix="/dfir-copilot", tags=["Enterprise AI DFIR Copilot"])
api_router.include_router(bas_platform.router, prefix="/bas-platform", tags=["Enterprise BAS Platform"])
api_router.include_router(red_team.router, prefix="/red-team", tags=["Enterprise Red Team Platform"])
api_router.include_router(blue_team.router, prefix="/blue-team", tags=["Enterprise Blue Team Readiness"])
api_router.include_router(continuous_validation.router, prefix="/continuous-validation", tags=["Enterprise Continuous Validation"])
api_router.include_router(attack_path.router, prefix="/attack-path", tags=["Enterprise Attack Path Simulation"])
api_router.include_router(detection_gap.router, prefix="/detection-gap", tags=["Enterprise Detection Gap Analysis"])
api_router.include_router(cyber_resilience.router, prefix="/cyber-resilience", tags=["Enterprise Cyber Resilience Platform"])
api_router.include_router(executive_intelligence.router, prefix="/executive-intelligence", tags=["Enterprise Executive Decision Intelligence"])
api_router.include_router(strategic_defense.router, prefix="/strategic-defense", tags=["Enterprise AI Strategic Cyber Defense"])
api_router.include_router(cspm.router, prefix="/cspm", tags=["Enterprise Cloud Security Posture Management"])
api_router.include_router(cwpp.router, prefix="/cwpp", tags=["Enterprise Cloud Workload Protection Platform"])
api_router.include_router(k8s_security.router, prefix="/k8s-security", tags=["Enterprise Kubernetes Security Platform"])
api_router.include_router(ciem.router, prefix="/ciem", tags=["Enterprise Cloud Identity & Entitlement Management"])
api_router.include_router(cdr.router, prefix="/cdr", tags=["Enterprise Cloud Detection & Response"])
api_router.include_router(dspm.router, prefix="/dspm", tags=["Enterprise Data Security Posture Management"])
api_router.include_router(multi_cloud.router, prefix="/multi-cloud", tags=["Enterprise Multi-Cloud Security Intelligence"])
api_router.include_router(governance.router, prefix="/governance", tags=["Enterprise Cloud Security Governance"])
api_router.include_router(ctem.router, prefix="/ctem", tags=["Enterprise Cloud Threat Exposure Management"])
api_router.include_router(command_center.router, prefix="/command-center", tags=["Enterprise AI Cloud Security Command Center"])
api_router.include_router(aspm.router, prefix="/aspm", tags=["Enterprise Application Security Posture Management"])
api_router.include_router(devsecops.router, prefix="/devsecops", tags=["Enterprise Secure SDLC & DevSecOps"])
api_router.include_router(sbom.router, prefix="/sbom", tags=["Enterprise Software Bill of Materials (SBOM)"])
api_router.include_router(sast.router, prefix="/sast", tags=["Enterprise Static Application Security Testing (SAST)"])
api_router.include_router(dast.router, prefix="/dast", tags=["Enterprise Dynamic Application Security Testing (DAST)"])
api_router.include_router(sca.router, prefix="/sca", tags=["Enterprise Software Composition Analysis (SCA)"])
api_router.include_router(secrets.router, prefix="/secrets", tags=["Enterprise Secrets Security"])
api_router.include_router(iac.router, prefix="/iac", tags=["Enterprise IaC Security"])
api_router.include_router(copilot.router, prefix="/copilot", tags=["Enterprise AI Developer Copilot"])
api_router.include_router(appsec_command_center.router, prefix="/appsec-command-center", tags=["Enterprise AppSec Command Center"])
api_router.include_router(ispm.router, prefix="/ispm", tags=["Enterprise Identity Security Posture Management (ISPM)"])
api_router.include_router(zta.router, prefix="/zta", tags=["ZTA"])
api_router.include_router(pam.router, prefix="/pam", tags=["Enterprise Privileged Access Management (PAM)"])
api_router.include_router(itdr.router, prefix="/itdr", tags=["Identity Threat Detection & Response (ITDR)"])
api_router.include_router(iga.router, prefix="/iga", tags=["Identity Governance & Administration (IGA)"])
api_router.include_router(nhi.router, prefix="/nhi", tags=["Machine & Non-Human Identity (NHI)"])
api_router.include_router(authn.router, prefix="/authn", tags=["Passwordless Authentication (AUTHN)"])
api_router.include_router(federation.router, prefix="/federation", tags=["Federated Identity & SSO (FEDERATION)"])
api_router.include_router(identity_intel.router, prefix="/identity-intel", tags=["Identity Intelligence & Trust (IDENTITY_INTEL)"])
api_router.include_router(identity_command_center.router, prefix="/identity-cc", tags=["Unified Identity Command Center"])
api_router.include_router(cyber_fusion.router, prefix="/cyber-fusion", tags=["Cyber Fusion Center (CYBER_FUSION)"])
api_router.include_router(orchestration.router, prefix="/orchestration", tags=["AI Security Orchestration (ORCHESTRATION)"])
api_router.include_router(digital_twin.router, prefix="/digital-twin", tags=["Cyber Digital Twin (DIGITAL_TWIN)"])
api_router.include_router(predictive_risk.router, prefix="/predictive-risk", tags=["Predictive Cyber Risk (PREDICTIVE_RISK)"])
api_router.include_router(cyber_resilience.router, prefix="/cyber-resilience", tags=["Cyber Resilience & BCP (CYBER_RESILIENCE)"])
api_router.include_router(knowledge_evolution.router, prefix="/knowledge-evolution", tags=["Enterprise Knowledge Evolution"])
api_router.include_router(cyber_governance.router, prefix="/cyber-governance", tags=["Cyber Governance & Executive Strategy"])
api_router.include_router(cyber_command.router, prefix="/cyber-command", tags=["Enterprise Cyber Command"])
api_router.include_router(cyber_os.router, prefix="/cyber-os", tags=["CyberOS Kernel"])

