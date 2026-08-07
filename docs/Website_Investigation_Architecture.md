# Advanced Website Investigation Platform Architecture

## Overview
The Advanced Website Investigation Platform (PHOENIX Phase X-012) conducts deep, structural investigations of website content, expanding beyond network-level URL intelligence. It inspects HTML DOM, executes and analyzes JavaScript, checks security headers, and visually inspects screenshots using AI to detect sophisticated phishing and impersonation attacks.

## Architecture Components

### Backend (`app/website_investigation/`)
1. **PageFetchEngine**: Simulates headless browser interaction. Extracts HTML, rendered DOM, tracking cookies, HTTP security headers, and visual layout captures (screenshots).
2. **HTMLAnalysisEngine & DOMAnalysisEngine**: Evaluates HTML structure. Identifies hidden elements (e.g., `display: none`), meta refreshes, iframes, embedded credentials in source code, and suspicious tags.
3. **JavaScriptAnalysisEngine**: Scans both inline and external scripts for obfuscation techniques, excessive `eval()` usage, tracking libraries, API misuse (e.g., Clipboard manipulation), and background AJAX requests.
4. **FormAnalysisEngine & CookieAnalysisEngine**: Identifies login, password, and PII collection forms. Validates cookie security flags (Secure, HttpOnly, SameSite).
5. **SecurityHeaderAnalyzer**: Assesses defensive posture by parsing Content-Security-Policy (CSP), Strict-Transport-Security (HSTS), X-Frame-Options, and Referrer-Policy.
6. **VisualAnalysisEngine & BrandDetectionEngine**: Integrates with Vision AI models to compare rendered screenshots against known brand templates (e.g., Microsoft, Chase), identifying highly-similar visual phishing indicators.
7. **WebsiteRiskScoringEngine**: Normalizes collected data into specific risk vectors (Code Risk, Form Risk, Infrastructure Risk, Visual Risk) to produce an Overall Risk Score and Threat Severity.
8. **WebsiteInvestigationOrchestrator**: Asynchronously coordinates the fetcher and analysis engines to ensure rapid processing of heavy DOM payloads.
9. **WebsiteAIIntegration**: Interfaces with PHOENIX AI Brain to synthesize technical findings into an explainable Threat Narrative.

### Frontend (`frontend/src/features/website-investigation/`)
- **WebsiteInvestigationDashboard**: Main entry point for deep scanning.
- **CodeExplorer**: Visualizes HTML and JS analysis results, highlighting obfuscated scripts and hidden DOM elements.
- **DataViewer**: Provides a clear view of targeted forms (Login, PII) and insecure cookie configurations.
- **SecurityDashboard**: Displays parsed HTTP security headers and their absence.
- **VisualInvestigationPanel**: Renders the captured screenshot and AI visual comparison metrics.
- **WebsiteAIFindings**: Renders the AI Threat Narrative and contextual recommendations.

## Data Models
New models added to `app/models/website_investigation.py`:
- `WebsiteInvestigation`: Links to the base `Investigation`.
- `PageSnapshot`: Stores metadata about the HTML response.
- `JavaScriptMetadata`: Tracks individual scripts and obfuscation flags.
- `FormMetadata`: Details inputs and targets.
- `SecurityHeaderData`: Parsed HTTP headers.
- `VisualAnalysisData`: Brand impersonation metrics and screenshot paths.

## Scalability & Performance
The architecture isolates the DOM fetching layer from the analytical layers. In production, `PageFetchEngine` communicates with a distributed Headless Browser Cluster, streaming the rendered DOM back to the analysis engines asynchronously, ensuring the FastAPI application remains responsive under heavy load.
