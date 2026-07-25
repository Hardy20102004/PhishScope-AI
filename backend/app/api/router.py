from fastapi import APIRouter
from app.api.v1.endpoints import (
    health,
    version,
    auth,
    users,
    dashboard,
    investigations,
    threat_intel,
    copilot,
    cases,
    reports,
    automation,
    extension,
    mobile,
    tenants,
    observability,
    ai_brain,
    multi_agent,
    ai_memory,
    ai_context,
    prompt_platform,
    rag,
    knowledge_graph,
    decision,
    xai,
    models,
    url_intelligence,
    website_investigation,
    email_intelligence,
    qr_intelligence,
    malware_intelligence,
    mobile_investigation,
    browser_investigation,
    network_investigation,
    cloud_investigation
)

api_router = APIRouter()

# Mount all v1 routes here
api_router.include_router(health.router, prefix="/health", tags=["system"])
api_router.include_router(version.router, prefix="/version", tags=["system"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
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
api_router.include_router(copilot.router, prefix="/copilot", tags=["copilot"])
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
