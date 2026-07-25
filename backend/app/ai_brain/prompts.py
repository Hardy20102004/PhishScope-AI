import structlog
from typing import Dict, Any, Optional, List, Tuple
import string

logger = structlog.get_logger("phoenix.ai_brain.prompts")

class PromptManager:
    """
    Enterprise Prompt Management engine maintaining reusable SOC and incident response templates,
    enforcing dynamic schema validation, and defending against system prompt override attacks.
    """
    def __init__(self):
        self._templates: Dict[str, Dict[str, Any]] = {}
        self._seed_templates()

    def _seed_templates(self):
        templates = [
            {
                "name": "Executive Summary",
                "template_type": "Executive Summary",
                "description": "High-level risk, business impact, and strategic timeline summary for executive leadership and C-suite review.",
                "system_prompt": "You are PHOENIX AI Security Brain acting as Principal Cybersecurity & Risk Strategist. Provide clear, non-technical executive insights focused on financial and operational threat mitigation. Never hallucinate facts or unsupported indicators.",
                "user_template": "Analyze the following security investigation context and generate an Executive Summary report.\n\nContext:\n{{ context }}\n\nAnalyst Inquiry: {{ inquiry }}\n\nProvide an Overview, Key Risk Level (Low/Moderate/Elevated/Critical), Impacted Business Units, and Immediate Strategic Guidance.",
                "required_variables": ["context", "inquiry"],
                "version": "1.1.0"
            },
            {
                "name": "Technical Summary",
                "template_type": "Technical Summary",
                "description": "Detailed cryptographic, network, endpoint forensic, and payload analysis for SOC Tier 2/3 engineering review.",
                "system_prompt": "You are PHOENIX AI Security Brain acting as Principal Forensic Security Architect. Analyze technical telemetry, network PCAP markers, TLS cert metadata, and macro heuristics with strict factual adherence.",
                "user_template": "Review the attached forensic context and construct a comprehensive Technical Summary.\n\nContext:\n{{ context }}\n\nSpecific Focus Area: {{ inquiry }}\n\nList exact IOCs, observed TTPs (with MITRE ATT&CK codes), payload vector analysis, and precise technical containment actions.",
                "required_variables": ["context", "inquiry"],
                "version": "1.2.0"
            },
            {
                "name": "Threat Analysis",
                "template_type": "Threat Analysis",
                "description": "In-depth threat intelligence evaluation, attribution hypotheses, campaign profiling, and indicator correlation.",
                "system_prompt": "You are PHOENIX AI Security Brain acting as Chief Threat Intelligence Analyst. Evaluate domain reputations, autonomous detection engine results, and indicator feeds to determine threat actor intent and campaign alignment.",
                "user_template": "Conduct an exhaustive Threat Analysis on the provided investigation artifacts.\n\nContext:\n{{ context }}\n\nTarget Query: {{ inquiry }}\n\nEvaluate threat indicator confidence, correlate observed tactics against known digital scam campaigns, and provide defensive countermeasures.",
                "required_variables": ["context", "inquiry"],
                "version": "1.3.0"
            },
            {
                "name": "Case Summary",
                "template_type": "Case Summary",
                "description": "Comprehensive investigation dossier briefing aggregating timeline events, tasks, evidence logs, and analyst annotations.",
                "system_prompt": "You are PHOENIX AI Security Brain acting as Senior Incident Commander. Synthesize investigation case records into structured operational dossiers.",
                "user_template": "Summarize the following investigation case file into an authoritative Case Summary.\n\nCase Context:\n{{ context }}\n\nAnalyst Directive: {{ inquiry }}\n\nProvide Case Status Overview, Verified Evidentiary Timeline, Outstanding Action Items, and Containment Readiness Score.",
                "required_variables": ["context", "inquiry"],
                "version": "1.0.1"
            },
            {
                "name": "Evidence Explanation",
                "template_type": "Evidence Explanation",
                "description": "Plain-language and rigorous forensic explanation of specific URL strings, DNS anomalies, WHOIS records, or scripts.",
                "system_prompt": "You are PHOENIX AI Security Brain acting as Forensic Expert Witness and SOC Mentor. Break down complicated technical evidence into lucid, explainable summaries supported by empirical citations.",
                "user_template": "Examine and elucidate the following evidentiary artifacts.\n\nContext & Evidence Vault:\n{{ context }}\n\nItem to Explain: {{ inquiry }}\n\nExplain the anatomical structure of the evidence, why it was flagged by security filters, and what specific threat behaviors it facilitates.",
                "required_variables": ["context", "inquiry"],
                "version": "1.1.5"
            },
            {
                "name": "Risk Narrative",
                "template_type": "Risk Narrative",
                "description": "Structured quantitative and qualitative cyber risk calculation explaining probability of exploitation and institutional damage.",
                "system_prompt": "You are PHOENIX AI Security Brain acting as Enterprise Cyber Risk Analyst using NIST AI RMF and FAIR quantitative modeling principles.",
                "user_template": "Formulate an enterprise Risk Narrative based on the observed security events.\n\nContext:\n{{ context }}\n\nRisk Assessment Scope: {{ inquiry }}\n\nAssess Likelihood of Successful Exploitation, Potential Institutional Financial/Reputational Loss, Key Vulnerability Vectors, and Risk Treatment Strategies.",
                "required_variables": ["context", "inquiry"],
                "version": "1.0.0"
            },
            {
                "name": "Incident Report",
                "template_type": "Incident Report",
                "description": "Formal legal-grade and regulatory-ready digital security incident response report suitable for audit trail archiving.",
                "system_prompt": "You are PHOENIX AI Security Brain acting as Principal Compliance & Incident Investigator. Produce formal, structured regulatory incident disclosures.",
                "user_template": "Generate an official Incident Report from the finalized investigation records.\n\nContext:\n{{ context }}\n\nReporting Requirement: {{ inquiry }}\n\nInclude Incident Identification Timestamp, Vector of Compromise, Scope of Exposure, Containment & Remediation Log, and Post-Incident Review Findings.",
                "required_variables": ["context", "inquiry"],
                "version": "1.0.0"
            },
            {
                "name": "Threat Hunting",
                "template_type": "Threat Hunting",
                "description": "Proactive hypothesis generation, threat hunting query creation (Sigma, SPL, YARA), and lateral movement checks.",
                "system_prompt": "You are PHOENIX AI Security Brain acting as Lead Autonomous Threat Hunter. Design proactive detection workflows and telemetry hunting queries.",
                "user_template": "Develop an actionable Threat Hunting package targeting the tactics discovered in this investigation.\n\nContext:\n{{ context }}\n\nHunting Objective: {{ inquiry }}\n\nFormulate 2 distinct hunting hypotheses, generate draft detection rules (Sigma or SPL format), and identify log data sources required for proactive verification.",
                "required_variables": ["context", "inquiry"],
                "version": "1.2.1"
            },
            {
                "name": "Recommendation Report",
                "template_type": "Recommendation Report",
                "description": "Prioritized action checklist covering perimeter blocking, sinkholing, password resets, and user security training.",
                "system_prompt": "You are PHOENIX AI Security Brain acting as Principal SOC Remediation Architect. Deliver highly specific, prioritized, zero-trust remedial instructions.",
                "user_template": "Create a prioritized SOC Recommendation Report for containment and hardening.\n\nContext:\n{{ context }}\n\nTarget System / Department: {{ inquiry }}\n\nCategorize recommendations into Immediate Actions (0-2 hours), Near-Term Hardening (24-48 hours), and Long-Term Preventive Controls.",
                "required_variables": ["context", "inquiry"],
                "version": "1.1.0"
            }
        ]
        for t in templates:
            self.register_template(t["name"], t)

    def register_template(self, name: str, data: Dict[str, Any]):
        self._templates[name.lower()] = data

    def get_template(self, name: str) -> Optional[Dict[str, Any]]:
        return self._templates.get(name.lower())

    def list_templates(self) -> List[Dict[str, Any]]:
        return list(self._templates.values())

    def format_prompt(self, template_name: str, variables: Dict[str, Any]) -> Tuple[str, str]:
        """
        Retrieves template by name (or defaults to Threat Analysis) and dynamically interpolates using PromptComposer.
        Returns: (system_prompt, formatted_user_prompt)
        """
        from app.prompt_platform.composer import PromptComposer
        
        tpl_data = self.get_template(template_name) or self.get_template("Threat Analysis")
        system_prompt = tpl_data["system_prompt"]
        user_template = tpl_data["user_template"]
        
        # Normalize inquiry vs input_text
        if "inquiry" not in variables and "input_text" in variables:
            variables["inquiry"] = variables["input_text"]
            
        composer = PromptComposer()
        try:
            sys_out, user_out = composer.compose(system_prompt, user_template, variables)
            return sys_out, user_out
        except Exception as e:
            logger.error("prompt_composition_failed", error=str(e), template=template_name)
            return system_prompt, user_template
