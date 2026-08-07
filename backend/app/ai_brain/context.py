import json
from typing import Any, Dict, List, Optional

import structlog

from app.ai_brain.optimization import ContextCompressor

logger = structlog.get_logger("phoenix.ai_brain.context")

class EvidenceAggregator:
    """
    Aggregates and formats multi-source cryptographic findings, network traces,
    threat feed ratings, and case artifacts into structured evidence bundles.
    """
    @staticmethod
    def aggregate_evidence(evidence_items: List[Dict[str, Any]]) -> str:
        if not evidence_items:
            return "No explicit evidentiary artifacts provided for this interaction."

        lines = ["### Verified Evidentiary Record (PHOENIX Evidence Vault):"]
        for idx, item in enumerate(evidence_items, 1):
            f_id = item.get("id") or item.get("finding_id", f"EVID-{idx:04d}")
            f_type = item.get("type", "General Artifact")
            value = item.get("value") or item.get("url") or item.get("ioc", "N/A")
            reputation = item.get("reputation_score", item.get("risk", "Unknown"))
            source = item.get("source", "PHOENIX Detection Engine")
            
            lines.append(f"[{idx}] Finding ID: {f_id} | Type: {f_type} | Target: {value} | Risk Rating: {reputation} | Source: {source}")
            if item.get("details"):
                lines.append(f"    Details: {str(item.get('details')).strip()}")
        
        deduped = ContextCompressor.deduplicate_evidence_lines(lines)
        return "\n".join(deduped)


class ContextBuilder:
    """
    Assembles optimized AI context bundles from Investigation Results, Threat Intelligence,
    Evidence, Case Information, Timeline events, Previous AI responses, User Notes, and Organization Policies.
    """
    @staticmethod
    def build_context(
        investigation_results: Optional[Dict[str, Any]] = None,
        threat_intelligence: Optional[List[Dict[str, Any]]] = None,
        evidence: Optional[List[Dict[str, Any]]] = None,
        case_info: Optional[Dict[str, Any]] = None,
        timeline: Optional[List[Dict[str, Any]]] = None,
        previous_ai_responses: Optional[List[str]] = None,
        user_notes: Optional[List[str]] = None,
        organization_policies: Optional[List[str]] = None,
        max_context_chars: int = 16000
    ) -> str:
        sections: List[str] = []

        # 1. Organization Policies (Highest operational precedence)
        if organization_policies:
            sec_policy = "### Mandatory Organization Security & AI Policies:\n" + "\n".join([f"- {p}" for p in organization_policies])
            sections.append(sec_policy)
        else:
            sections.append("### Mandatory Organization Security & AI Policies:\n- Enforce strict factual compliance and cite verified evidence IDs only.")

        # 2. Case Information
        if case_info:
            case_str = f"### Active Investigation Case Overview:\n- Case ID: {case_info.get('id', 'N/A')}\n- Title: {case_info.get('title', 'Untitled Security Case')}\n- Severity: {case_info.get('severity', 'MODERATE')}\n- Status: {case_info.get('status', 'OPEN')}\n- Description: {case_info.get('description', 'No detailed synopsis provided.')}"
            sections.append(case_str)

        # 3. Aggregated Evidence Vault
        if evidence:
            sections.append(EvidenceAggregator.aggregate_evidence(evidence))

        # 4. Threat Intelligence Feeds & IOC Correlations
        if threat_intelligence:
            ti_lines = ["### Threat Intelligence Indicator Feeds:"]
            for ti in threat_intelligence:
                ti_lines.append(f"- Indicator: {ti.get('indicator')} ({ti.get('type', 'IOC')}) | Threat Feed: {ti.get('feed', 'Global SOC Feed')} | Threat Score: {ti.get('score', 0)}/100")
            sections.append("\n".join(ti_lines))

        # 5. Investigation Automated Telemetry
        if investigation_results:
            inv_lines = ["### Automated Engine Investigation Results:"]
            for key, val in investigation_results.items():
                if isinstance(val, (dict, list)):
                    inv_lines.append(f"- {key.replace('_', ' ').title()}: {json.dumps(val, default=str)}")
                else:
                    inv_lines.append(f"- {key.replace('_', ' ').title()}: {val}")
            sections.append("\n".join(inv_lines))

        # 6. Chronological Incident Timeline
        if timeline:
            tl_lines = ["### Chronological Incident Event Timeline:"]
            for evt in sorted(timeline, key=lambda x: str(x.get("timestamp", ""))):
                tl_lines.append(f"- [{evt.get('timestamp', 'Time Unknown')}] {evt.get('event_type', 'EVENT')}: {evt.get('description', '')}")
            sections.append("\n".join(tl_lines))

        # 7. Analyst Notes & Manual Annotations
        if user_notes:
            notes_str = "### Security Analyst Working Notes:\n" + "\n".join([f"- {note}" for note in user_notes])
            sections.append(notes_str)

        # 8. Previous AI Response Memory
        if previous_ai_responses:
            prev_str = "### Prior AI Security Brain Synthese Memory:\n" + "\n---\n".join(previous_ai_responses[-2:])
            sections.append(prev_str)

        raw_context = "\n\n".join(sections)
        optimized_context = ContextCompressor.compress_by_truncation(raw_context, max_context_chars)
        logger.info("context_bundle_assembled", raw_len=len(raw_context), optimized_len=len(optimized_context), sections_count=len(sections))
        return optimized_context
