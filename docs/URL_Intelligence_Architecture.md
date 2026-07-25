# Advanced URL Intelligence Platform Architecture

## Overview
The Advanced URL Intelligence Platform (PHOENIX Phase X-011) provides deep, evidence-backed investigations of URLs. It transcends simple reputation checking by analyzing infrastructure, URL structure, and brand relationships, ultimately integrating with the PHOENIX AI Brain to generate explainable risk narratives.

## Architecture Components

### Backend (`app/url_intelligence/`)
1. **URLParser & Normalizer**: Parses URLs strictly to RFC standards. Implements deduplication, lowercase normalization, and path resolution to create Canonical URLs.
2. **URLIntelligenceEngine**: Analyzes URL length, entropy, encoded characters, and identifies suspicious keywords (e.g., "login", "verify") often used in phishing.
3. **RedirectAnalysisEngine**: Resolves HTTP redirect chains asynchronously, tracking status codes, final landing pages, and detecting potential open redirect patterns.
4. **InfrastructureCorrelationEngine**: Gathers Domain Intelligence via DNS (A, NS, MX, TXT). Connects to raw sockets to retrieve TLS Certificates (Issuer, Validity, Subject Alt Names).
5. **BrandProtectionEngine**: Detects typosquatting using Levenshtein distance heuristics against a database of known highly targeted brands (e.g., Microsoft, Apple). Detects homograph attacks (e.g., IDN/Punycode).
6. **RiskScoringEngine**: Aggregates the intelligence data to compute an overall risk score (0-100), assigning Threat Severity (LOW, MEDIUM, HIGH, CRITICAL) and Confidence levels.
7. **InvestigationOrchestrator**: Acts as the central coordinator. Handles parallel execution of asynchronous network lookups to ensure the system is performant and responsive.
8. **URLAIIntegration**: Interfaces with the AI Security Brain to generate human-readable, explainable narratives synthesizing the disparate evidence points into a single Threat Summary.

### Frontend (`frontend/src/features/url-intelligence/`)
- **URLInvestigationDashboard**: Main entry point for analysts.
- **EvidenceTimeline**: Visualizes the step-by-step redirect chain and response latency.
- **InfrastructureMap**: Details the correlated IP addresses, Name Servers, MX records, and TLS Certificate validity.
- **RelationshipGraph**: A structural view of the target domain and its connections.
- **AIFindingsPanel**: Renders the AI-generated risk narrative and recommended actions.
- **RiskDashboard**: A quantitative visualization of the Risk Score, Confidence, and sub-scores (Brand Risk, Infrastructure Risk).

## Data Models
New models added to `app/models/url_intelligence.py`:
- `URLInvestigationDetails`: Central evidence store linked to the base `Investigation`.
- `ParsedURL`: Structured URI components.
- `RedirectChain`: Line-item storage for each hop in a redirect sequence.
- `DomainInfrastructure`: IP and DNS correlations.
- `CertificateData`: Parsed X.509 certificate data.
- `BrandIntelligence`: Typosquatting and impersonation metrics.

## Performance & Security
- **Asynchronous Execution**: Network-bound tasks (DNS, TLS, Redirects) are executed in parallel via `asyncio`.
- **Tenant Isolation**: Integrates with the existing PHOENIX `tenants` structure (pending).
- **Scalability**: The modular engine design allows individual components to be scaled or replaced with advanced third-party API integrations (e.g., VirusTotal, URLScan) in the future.
