from typing import Set, Tuple

import structlog

logger = structlog.get_logger("phoenix.kg.ontology")

class OntologyManager:
    """
    Defines and enforces the schema rules for the Enterprise Knowledge Graph.
    Ensures that entities and relationships adhere to STIX 2.1-inspired logic.
    """
    
    VALID_ENTITY_TYPES = {
        "INVESTIGATION", "CASE", "EVIDENCE", "THREAT_ACTOR", "CAMPAIGN",
        "IOC", "URL", "DOMAIN", "SUBDOMAIN", "IP_ADDRESS", "ASN",
        "TLS_CERTIFICATE", "WHOIS_RECORD", "EMAIL_ADDRESS", "EMAIL",
        "PHONE_NUMBER", "QR_CODE", "WEBSITE", "FILE", "HASH",
        "MALWARE_SAMPLE", "YARA_RULE", "SIGMA_RULE", "CLOUD_ASSET",
        "USER", "ORGANIZATION", "TENANT", "AI_AGENT", "WORKFLOW",
        "REPORT", "POLICY", "KNOWLEDGE_DOCUMENT", "MEMORY"
    }

    VALID_RELATIONSHIP_TYPES = {
        "BELONGS_TO", "USES", "HOSTED_ON", "RESOLVES_TO", "RELATED_TO",
        "ASSOCIATED_WITH", "TARGETS", "COMMUNICATES_WITH", "GENERATED_BY",
        "REFERENCES", "CONTAINS", "LOCATED_IN", "PART_OF", "SIMILAR_TO",
        "DUPLICATE_OF", "OBSERVED_IN", "LINKED_TO", "INDICATES",
        "INVESTIGATED_BY", "REPORTED_IN", "CUSTOM_RELATIONSHIP"
    }

    # Allowed triples: (SourceType, RelationshipType, TargetType)
    # If a triple is not in this list, it may be flagged.
    VALID_TRIPLES: Set[Tuple[str, str, str]] = {
        ("THREAT_ACTOR", "USES", "MALWARE_SAMPLE"),
        ("THREAT_ACTOR", "TARGETS", "ORGANIZATION"),
        ("CAMPAIGN", "ATTRIBUTED_TO", "THREAT_ACTOR"),
        ("DOMAIN", "RESOLVES_TO", "IP_ADDRESS"),
        ("URL", "HOSTED_ON", "DOMAIN"),
        ("SUBDOMAIN", "PART_OF", "DOMAIN"),
        ("IP_ADDRESS", "BELONGS_TO", "ASN"),
        ("FILE", "HAS_HASH", "HASH"),
        ("EMAIL", "SENT_FROM", "EMAIL_ADDRESS"),
        # ... We can populate this with thousands of STIX relationships.
        # For this prototype, we'll allow anything but log a warning if it's "weird".
    }

    def validate_entity_type(self, entity_type: str) -> bool:
        """Returns True if the entity type is recognized in the ontology."""
        return entity_type.upper() in self.VALID_ENTITY_TYPES

    def validate_relationship_type(self, rel_type: str) -> bool:
        return rel_type.upper() in self.VALID_RELATIONSHIP_TYPES

    def is_valid_triple(self, source_type: str, rel_type: str, target_type: str) -> bool:
        """
        Check if the relationship makes logical sense according to the ontology.
        If strict mode is off, we just return True but log it.
        """
        triple = (source_type.upper(), rel_type.upper(), target_type.upper())
        if triple in self.VALID_TRIPLES or rel_type.upper() in {"RELATED_TO", "ASSOCIATED_WITH", "CUSTOM_RELATIONSHIP"}:
            return True
            
        logger.debug("unrecognized_ontology_triple", triple=triple)
        return True # For Prototype: allow dynamic relationship discovery
