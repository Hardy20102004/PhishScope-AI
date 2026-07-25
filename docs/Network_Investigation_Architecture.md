# Enterprise Network Investigation Platform Architecture

## Overview
The Network Investigation Platform (PHOENIX Phase X-019) provides structured forensic analysis of lawfully acquired network evidence (e.g., PCAP exports, Zeek logs, JSON/CSV dumps). It extracts flows, DNS requests, HTTP sessions, and TLS handshakes to build a unified chronological timeline, and leverages the AI Brain for threat correlation.

## Architecture Components

### Backend (`app/network_investigation/`)
1. **PCAPProcessingEngine**: Simulates the parsing of raw network logs (Zeek JSON format) into structured dictionaries for Flows, DNS, HTTP, and TLS.
2. **FlowAnalysisEngine**: Analyzes NetFlow/Connection logs (Source IP, Dest IP, Ports, Bytes transferred).
3. **DNSAnalysisEngine**: Parses DNS queries and responses, identifying lookups to known suspicious domains.
4. **HTTPAnalysisEngine**: Analyzes HTTP methods, Host headers, URIs, and User Agents.
5. **TLSAnalysisEngine**: Analyzes TLS metadata including Server Name Indication (SNI) and versions.
6. **TimelineEngine**: Merges connections, DNS requests, HTTP requests, and TLS handshakes into a unified, chronologically sorted `NetworkTimelineEvent` list.
7. **IOCExtractionEngine**: Extracts actionable network indicators (IPs, domains, URLs) from the network logs.
8. **RiskAssessmentEngine**: Computes an overall risk score based on anomalous flows, malicious DNS queries, and anomalous HTTP User Agents.
9. **NetworkInvestigationManager**: Asynchronously orchestrates the extraction, timeline generation, and correlation pipeline.
10. **NetworkAIIntegration**: Generates a human-readable threat narrative summarizing the forensic anomalies in the network capture.

### Frontend (`frontend/src/features/network-investigation/`)
- **NetworkInvestigationDashboard**: The main control center for simulating forensic data uploads and viewing the results.
- **FlowExplorer**: Tabular view of connection logs.
- **DNSExplorer**: Tabular view of DNS queries and responses, highlighting malicious lookups.
- **HTTPExplorer**: Displays HTTP requests, methods, and User Agents.
- **TLSExplorer**: Displays TLS handshakes and SNI data.
- **TimelineViewer**: A unified chronological feed of all parsed events, enabling analysts to trace timelines (e.g., DNS lookup for a malicious domain followed by an HTTP POST beacon).
- **NetworkAIFindings**: Renders the AI-generated forensic narrative.

## Data Models
Stored in `app/models/network_investigation.py`:
- `NetworkInvestigation`: Central link to the PHOENIX investigation graph.
- `NetworkFlowRecord`: Connection metadata.
- `DNSRecord`: Queries, record types, and answers.
- `HTTPMetadata`: Methods, URIs, Status codes, User Agents.
- `TLSMetadata`: SNI, Versions, Ciphers.
- `NetworkTimelineEvent`: Unified chronological data model.
- `ExtractedNetworkIOC`: Extracted IPs, Domains, and URLs.

## Future Roadmap & Vision
- **True PCAP Parsing**: Directly ingest and parse `.pcap` and `.pcapng` files.
- **Cloud Network Logs**: Integrate with AWS VPC Flow Logs, Azure NSG Flow Logs, and GCP VPC Flow Logs.
- **Graph Visualization**: Visual mapping of Top Talkers and lateral movement pathways.
