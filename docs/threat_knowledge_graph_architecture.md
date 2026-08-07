# Enterprise IOC Knowledge Graph Architecture

## Overview
The Enterprise IOC Knowledge Graph acts as the central reasoning and relational mapping layer for all cyber intelligence operations in PHOENIX X. It extends the core graph architecture to specialize deeply in Threat Intelligence concepts.

## Core Components

### 1. Ontology Manager
Defines the strictly typed schema for nodes and edges.
- Supports 30+ entity types: `THREAT_ACTOR`, `MALWARE_FAMILY`, `YARA_RULE`, `IPV4`, etc.
- Supports STIX 2.1 aligned relationship types: `USES`, `TARGETS`, `COMMUNICATES_WITH`, `DROPS`.
- Validates logical triples to maintain data integrity.

### 2. Graph Database Strategy
Currently implemented as a Hybrid layer over PostgreSQL using `kg_entities` and `kg_relationships`.
- `is_inferred` boolean flag introduced to distinguish Analyst-confirmed edges from AI-deduced edges.
- Incorporates `observed_start` and `observed_end` for temporal queries and timelines.

### 3. Graph Inference Engine
A specialized rule engine that automatically deduces hidden relationships.
- Detects shared infrastructure automatically (e.g. Domains pointing to the same IP).
- Correlates threat actors sharing identical malware signatures.
- Automatically creates probabilistic edges with confidence scores.

### 4. Graph Analytics Engine
Uses NetworkX internally to compute advanced graph mathematics.
- **Degree Centrality**: Identifies critical nodes (e.g. core C2 servers).
- **Modularity Optimization**: Detects "Threat Clusters" representing coordinated campaigns.

### 5. Graph Query Engine
Supports traversal operations via REST APIs.
- Neighbor expansion up to N depth.
- Shortest-path detection between any two IOCs/Entities.
