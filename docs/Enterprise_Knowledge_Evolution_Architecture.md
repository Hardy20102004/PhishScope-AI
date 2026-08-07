# Enterprise Knowledge Evolution Architecture

## 1. Overview
The Enterprise Autonomous Knowledge Graph Evolution, AI Learning & Continuous Cyber Intelligence Platform (Phase X-097) provides a robust foundation for continuously enriching the enterprise knowledge graph using observed telemetry, investigation findings, and historical analytics.

It includes AI-assisted semantic enrichment, ontology recommendations, relationship discovery, and knowledge quality evaluation with explicit human-governed approval mechanisms.

## 2. Core Components

### Knowledge Evolution Manager
Central orchestrator (`KnowledgeEvolutionManager`) coordinating the lifecycle of graph evolution.

### Ontology Management Engine
Manages structural schemas, entity types, relationship types, and their taxonomy. Maintains versioning and status tracking for changes.

### Relationship Discovery Engine
Analyzes underlying patterns from the Security Data Fabric to discover and propose new connections (e.g. Asset-Threat mappings). Identifies inferred relationships and assigns confidence scores.

### Semantic Enrichment Engine
Normalizes knowledge entities to business glossary standards using AI-driven context alignment.

### Knowledge Quality Engine
Calculates multidimensional quality metrics covering:
- **Coverage**: Extent to which entities are documented.
- **Consistency**: Adherence to schema constraints.
- **Freshness**: Up-to-date validity of the information.
- **Confidence**: Reliability score of the data source.
- **Relationship Quality**: Integrity of graph connections.

### Schema Recommendation Engine
Generates actionable recommendations (e.g., adding properties, merging redundant entity definitions).

### AI Knowledge Evolution Assistant
A conversational interface integrated with the `AI Security Brain` providing summaries, ontology mapping suggestions, and insights into graph health.

## 3. Database Models

Implemented in `backend/app/models/knowledge_evolution.py`:
- `OntologyNode`: Core structural definitions tracking `ApprovalStatus`.
- `SchemaRecommendation`: Proposed schema changes with supporting evidence.
- `EvolutionQualityMetric`: Snapshot metric evaluations over time.

## 4. API Endpoints

- `GET /api/v1/knowledge-evolution/overview` - Retrieves current platform metrics.
- `GET /api/v1/knowledge-evolution/ontology` - Lists ontology nodes.
- `POST /api/v1/knowledge-evolution/ontology` - Submits a new node.
- `POST /api/v1/knowledge-evolution/ontology/{id}/approve` - Approves a pending node.
- `GET /api/v1/knowledge-evolution/relationships/discover` - Retrieves newly inferred relationships.
- `GET /api/v1/knowledge-evolution/recommendations` - Lists pending schema recommendations.

## 5. Frontend Interfaces

Module path: `frontend/src/features/knowledgeEvolution/`
- **KnowledgeEvolutionDashboard**: Main entry with tab-based navigation.
- **OntologyDashboard**: Interface for schema/entity governance.
- **RelationshipExplorer**: Visualization of observed vs inferred knowledge links.
- **KnowledgeQualityDashboard**: Visual charts and metric trackers for graph health.
- **SchemaRecommendationDashboard**: UI to review, accept, or reject AI proposed updates.
- **AIKnowledgeEvolutionAssistant**: AI chat interface for evolution queries.

## 6. Security & Governance
All critical schema and ontology changes strictly mandate `PENDING` states requiring human (`APPROVED` / `REJECTED`) interactions ensuring a Human-in-the-Loop governance model.
