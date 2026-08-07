# Enterprise Security Data Fabric Architecture

## 1. Overview
The Enterprise Security Data Fabric is the foundational layer of PHOENIX X, unifying security telemetry, metadata, knowledge assets, analytics, reports, simulations, governance information, and executive metrics into a single governed enterprise data ecosystem.

It provides semantic relationships, metadata catalogs, lineage tracking, data quality monitoring, policy-aware access, and AI-assisted knowledge discovery while preserving existing security controls and governance.

## 2. Core Components

### Security Data Fabric Manager
Central orchestrator for the data fabric, coordinating between metadata catalogs, lineage tracking, quality monitoring, and knowledge graph integration.

### Metadata Catalog Engine
Registers and catalogs data sources, schemas, business glossaries, asset metadata, identity metadata, risk metadata, and governance policies. Uses `MetadataNode` entity.

### Knowledge Mesh Engine
Represents semantic relationships across Security Domains, Business Domains, Identity, Application, Cloud, Threat, and Operational relationships. Acts as an abstraction layer for Graph Database integration.

### Data Lineage Engine
Tracks data origins, transformation history, processing pipelines, and analytics dependencies. Maintains directed graphs of data flows using `LineageEdge`.

### Data Quality Engine
Evaluates data completeness, consistency, freshness, and accuracy. Computes confidence scores and overall quality status using `QualityMetric`.

### Governance Engine
Enforces governance policies, ownership information, retention rules, and classification labels across all registered metadata nodes.

### AI Data Fabric Assistant
Uses the AI Security Brain to analyze data fabric connectivity, identify data quality gaps, generate governance roadmaps, and summarize lineage relationships.

## 3. Database Schema

The architecture introduces the following core models:
- **`MetadataNode`**: Represents any cataloged entity (e.g., Schema, Data Source, Asset).
- **`LineageEdge`**: Represents data transformations or flows between MetadataNodes.
- **`QualityMetric`**: Represents a quality evaluation of a MetadataNode at a specific point in time.

## 4. API Endpoints

- `GET /api/v1/data-fabric/overview` - Retrieves high-level statistics and AI summaries.
- `GET /api/v1/data-fabric/metadata` - Lists metadata catalog nodes.
- `POST /api/v1/data-fabric/metadata` - Registers a new metadata node.
- `POST /api/v1/data-fabric/lineage` - Creates a new lineage relationship.
- `POST /api/v1/data-fabric/quality` - Records a new quality evaluation.

## 5. Frontend Integration
The Data Fabric includes a comprehensive React-based UI in the `frontend/src/features/dataFabric` feature module:
- **Security Data Fabric Dashboard**: Unified entry point.
- **Metadata Catalog Dashboard**: Browsing and managing catalog nodes.
- **Knowledge Mesh Dashboard**: Visualizing graph relationships.
- **Data Lineage Dashboard**: Tracing data origins and dependencies.
- **Data Quality Dashboard**: Monitoring completeness and accuracy metrics.
- **Governance Dashboard**: Reviewing active policies and compliance.
- **AI Data Fabric Assistant**: Conversational agent providing data insights.
