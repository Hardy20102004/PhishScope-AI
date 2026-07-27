from typing import Set, Tuple

import structlog

logger = structlog.get_logger("phoenix.kg.ontology")

class OntologyManager:
    """
    Defines and enforces the schema rules for the Enterprise IOC Knowledge Graph.
    Ensures that entities and relationships adhere to STIX 2.1-inspired logic.
    """
    
    VALID_ENTITY_TYPES = {
        "THREAT_ACTOR", "ALIAS", "CAMPAIGN", "MALWARE_FAMILY", "TOOL",
        "INFRASTRUCTURE", "DOMAIN", "SUBDOMAIN", "URL", "IPV4", "IPV6",
        "CERTIFICATE", "EMAIL_ADDRESS", "WALLET_ADDRESS", "CLOUD_RESOURCE",
        "VICTIM", "ORGANIZATION", "USER", "DEVICE", "APPLICATION", "APK",
        "FILE", "HASH", "YARA_RULE", "SIGMA_RULE", "MITRE_TECHNIQUE",
        "INVESTIGATION", "CASE", "EVIDENCE", "REPORT", "TI_SOURCE",
        "FEED_PROVIDER", "DETECTION_RULE", "CUSTOM_OBJECT"
    }

    VALID_RELATIONSHIP_TYPES = {
        "USES", "TARGETS", "HOSTED_ON", "COMMUNICATES_WITH", "PART_OF",
        "BELONGS_TO", "ASSOCIATED_WITH", "RELATED_TO", "LINKED_TO",
        "OBSERVED_IN", "DELIVERS", "DROPS", "EXECUTES", "DEPLOYS",
        "INDICATES", "INVESTIGATED_BY", "MITIGATED_BY", "DETECTED_BY",
        "REFERENCED_BY", "CUSTOM_RELATIONSHIP", "SHARED_INFRASTRUCTURE",
        "SHARED_CERTIFICATE", "SHARED_MALWARE", "SHARED_VICTIM"
    }

    # Allowed triples: (SourceType, RelationshipType, TargetType)
    # If a triple is not in this list, it may be flagged.
    VALID_TRIPLES: Set[Tuple[str, str, str]] = {
        ("THREAT_ACTOR", "USES", "MALWARE_FAMILY"),
        ("THREAT_ACTOR", "USES", "TOOL"),
        ("THREAT_ACTOR", "TARGETS", "VICTIM"),
        ("THREAT_ACTOR", "TARGETS", "ORGANIZATION"),
        ("CAMPAIGN", "ASSOCIATED_WITH", "THREAT_ACTOR"),
        ("CAMPAIGN", "TARGETS", "ORGANIZATION"),
        ("DOMAIN", "HOSTED_ON", "IPV4"),
        ("URL", "HOSTED_ON", "DOMAIN"),
        ("SUBDOMAIN", "PART_OF", "DOMAIN"),
        ("FILE", "HAS_HASH", "HASH"),
        ("FILE", "DROPS", "FILE"),
        ("MALWARE_FAMILY", "COMMUNICATES_WITH", "DOMAIN"),
        ("MALWARE_FAMILY", "COMMUNICATES_WITH", "IPV4"),
        ("YARA_RULE", "DETECTED_BY", "MALWARE_FAMILY"),
        ("MITRE_TECHNIQUE", "USED_BY", "THREAT_ACTOR")
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
