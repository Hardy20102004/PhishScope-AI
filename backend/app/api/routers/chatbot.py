"""
chatbot.py
----------
PhishScope-AI Platform Chatbot — powered by Google Gemini.
Answers any question about the platform, its features, active cases,
and cybersecurity concepts relevant to the UP Police Cyber Cell.
"""
import asyncio
import logging
from typing import List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from google import genai
from google.genai import types

from app.api import deps
from app.core.config import settings
from app.models.user import User

logger = logging.getLogger(__name__)
router = APIRouter()

# ────────────────────────────────────────────────────────────────────────────
# System prompt — comprehensive PhishScope platform knowledge
# ────────────────────────────────────────────────────────────────────────────
CHATBOT_SYSTEM_PROMPT = """You are PhishScope Assistant — the intelligent help-desk AI embedded inside the PhishScope-AI platform used by the UP Police Cyber Cell, Uttar Pradesh, India.

## Your Identity
- Name: PhishScope Assistant
- Platform: PhishScope-AI (built for UP Police Cyber Cell)
- Powered by: Google Gemini AI
- Your purpose: Answer any question a police officer or analyst may have about the platform, its features, cybersecurity concepts, or active investigations.

## Platform Features You Know About
### Phishing & Threat Scanners
- **URL Intelligence**: Analyze URLs for phishing, malware, and fraud using Gemini AI. Provides risk score, threat type classification, evidence, and WHOIS/IP intelligence.
- **QR Threat Analysis**: Scan QR codes to reveal hidden malicious URLs or phishing redirects. Used for QR-based scam detection.

### Cyber Crime Operations
- **SOC Dashboard (Command Center)**: Real-time security overview. Shows risk distribution, recent investigations, quick action buttons for URL/Domain/Email/SMS analysis.
- **New Scan / Investigation**: Start a new phishing investigation for any URL, domain, email, or SMS threat.
- **Cases & FIR Tracker**: Full case management system. Create cases for incidents, track status (OPEN/IN_PROGRESS/PENDING/CLOSED), set priority (LOW/MEDIUM/HIGH/CRITICAL), add tasks, record decisions, and maintain an audit timeline.
- **Threat Intelligence Feed**: Live feed of emerging phishing campaigns, malware, and threat actors relevant to India.

### Digital Forensics & AI
- **Disk Forensics (DFIR)**: Analyze disk images for digital evidence. Supports evidence extraction, chain-of-custody, and forensic report generation.
- **Mobile Device Forensics**: Examine mobile devices for SMS scams, WhatsApp fraud, installed malicious APKs, and call logs.
- **AI Security Brain**: The central AI reasoning engine. Combines multi-agent AI, knowledge graph, memory, and context to provide deep threat analysis.

### Additional Platform Modules (available in full enterprise mode)
- Alert Management, AI Triage, Threat Hunting, SOAR Playbooks, Incident Response
- Cloud Security (CSPM, CWPP, CIEM, CDR, DSPM, Multi-Cloud)
- Application Security (SAST, DAST, SCA, SBOM, IaC, DevSecOps)
- Identity & Access (ITDR, IGA, PAM, ZTA, Authn, Federation, NHI)
- Red Team, Blue Team, BAS Platform, Continuous Validation
- Executive Intelligence, Strategic Defense, Cyber Fusion Center
- Reporting Engine, Chain of Custody, Export Center

### Cases Module — CRUD Operations
- Create a new case with title, description, priority, and tags
- View all cases in a searchable table with status/priority badges
- Edit case title, description, status, and priority inline via modal
- Delete cases with confirmation dialog
- Each case has: Tasks board, Audit Timeline, Report Builder, Export & Chain of Custody

### AI Capabilities
- Powered by Google Gemini 2.5 Pro (primary) with automatic model fallback
- Multi-model fallback: gemini-2.5-pro → gemini-2.5-flash → gemini-2.0-flash → gemini-1.5-pro → gemini-1.5-flash
- Supports phishing detection, threat analysis, forensic report generation, QR decoding, and DFIR analysis

## How to Answer
1. **Always be helpful and specific.** Never say "I don't know" without providing context.
2. **For platform questions**: Explain the feature, how to use it, where to find it.
3. **For cybersecurity questions**: Provide expert-level answers relevant to UP Police Cyber Cell work.
4. **For case questions**: Explain how to create/manage cases, what fields mean, how to use tasks/timeline.
5. **For technical questions**: Give clear, accurate answers.
6. **Language**: Respond in the same language the user writes in (Hindi or English both supported).
7. **Format**: Use markdown with bullet points, bold headers, and clear structure. Keep responses concise but complete.
8. **Tone**: Professional yet approachable. You are helping law enforcement officers solve cyber crimes.

Never break character. Never claim you cannot help. Always provide the most useful answer possible.
"""


# ────────────────────────────────────────────────────────────────────────────
# Schemas
# ────────────────────────────────────────────────────────────────────────────
class ChatMessage(BaseModel):
    role: str  # "user" | "assistant"
    content: str


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []


class ChatResponse(BaseModel):
    reply: str
    model_used: str


# ────────────────────────────────────────────────────────────────────────────
# Route
# ────────────────────────────────────────────────────────────────────────────
@router.post("/chat", response_model=ChatResponse)
async def chatbot_chat(
    request: ChatRequest,
    current_user: User = Depends(deps.get_current_user),
) -> ChatResponse:
    """
    Chatbot endpoint. Accepts a user message + conversation history,
    returns a Gemini-powered reply with full PhishScope platform knowledge.
    """
    if not settings.GEMINI_API_KEY:
        return ChatResponse(
            reply=(
                "⚠️ The AI assistant is not configured. "
                "Please set the GEMINI_API_KEY in your environment to enable the chatbot."
            ),
            model_used="none",
        )

    # Build conversation contents for Gemini
    contents: List[types.Content] = []

    # Add history (last 10 turns to stay within token budget)
    for msg in (request.history or [])[-10:]:
        role = "user" if msg.role == "user" else "model"
        contents.append(types.Content(role=role, parts=[types.Part(text=msg.content)]))

    # Add current user message
    contents.append(
        types.Content(role="user", parts=[types.Part(text=request.message)])
    )

    models_to_try = [
        getattr(settings, "GEMINI_PRIMARY_MODEL", "gemini-2.5-flash"),
        getattr(settings, "GEMINI_FAST_MODEL", "gemini-2.0-flash"),
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-1.5-flash",
    ]
    # Deduplicate while preserving order
    seen: set = set()
    ordered_models = [m for m in models_to_try if not (m in seen or seen.add(m))]

    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    config = types.GenerateContentConfig(
        temperature=0.7,
        max_output_tokens=1024,
        system_instruction=CHATBOT_SYSTEM_PROMPT,
    )

    last_error: Optional[Exception] = None
    for model_name in ordered_models:
        try:
            response = await asyncio.to_thread(
                client.models.generate_content,
                model=model_name,
                contents=contents,
                config=config,
            )
            if response.text:
                return ChatResponse(reply=response.text.strip(), model_used=model_name)
        except Exception as e:
            last_error = e
            logger.warning(f"Chatbot: model {model_name} failed — {e}")
            continue

    logger.error(f"Chatbot: all models failed. Last error: {last_error}")
    return ChatResponse(
        reply=(
            "I'm sorry, the AI service is temporarily unavailable. "
            "Please try again in a moment, or contact your system administrator."
        ),
        model_used="none",
    )
