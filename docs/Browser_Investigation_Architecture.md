# Enterprise Browser Investigation Platform Architecture

## Overview
The Browser Investigation Platform (PHOENIX Phase X-018) provides structured forensic analysis of lawfully acquired browser data (e.g., Chrome/Firefox profile exports, SQLite databases). It extracts browsing history, cookies, installed extensions, and downloads, building a unified investigation timeline and correlating findings with the PHOENIX AI Brain.

## Architecture Components

### Backend (`app/browser_investigation/`)
1. **ProfileParserEngine**: Simulates the parsing of raw browser exports (History SQLite, Cookies SQLite, Extensions JSON) into structured dictionaries.
2. **HistoryAnalysisEngine**: Extracts visited URLs, search queries, visit counts, and timestamps.
3. **CookieAnalysisEngine**: Parses cookie domains, names, and security flags (Secure, HttpOnly).
4. **ExtensionAnalysisEngine**: Analyzes installed extensions and their requested permissions to flag highly privileged or suspicious plugins.
5. **DownloadAnalysisEngine**: Tracks downloaded files, their origin URLs, and metadata.
6. **TimelineEngine**: Merges history visits, searches, downloads, and cookie creations into a unified, chronologically sorted `BrowserTimelineEvent` list.
7. **IOCExtractionEngine**: Extracts actionable network indicators (URLs, domains) and search keywords from browsing history and download logs.
8. **RiskAssessmentEngine**: Computes an overall risk score based on the presence of suspicious extensions and malicious downloads.
9. **BrowserInvestigationManager**: Asynchronously orchestrates the extraction, timeline generation, and correlation pipeline.
10. **BrowserAIIntegration**: Generates a human-readable threat narrative summarizing the forensic anomalies in the browser profile.

### Frontend (`frontend/src/features/browser-investigation/`)
- **BrowserInvestigationDashboard**: The main control center for simulating forensic data uploads and viewing the results.
- **HistoryExplorer**: Tabular view of browsing history and search queries.
- **CookieExplorer**: Displays cookie metadata and security flags.
- **ExtensionExplorer**: Displays installed extensions and highlights suspicious permissions (e.g., `<all_urls>`).
- **DownloadExplorer**: Displays downloaded files and source URLs.
- **TimelineViewer**: A unified chronological feed of all parsed events, enabling analysts to trace timelines (e.g., visiting a phishing link, followed by a malicious payload download).
- **BrowserAIFindings**: Renders the AI-generated forensic narrative.

## Data Models
Stored in `app/models/browser_investigation.py`:
- `BrowserInvestigation`: Central link to the PHOENIX investigation graph.
- `BrowserHistoryRecord`: URLs, titles, and search queries.
- `BrowserCookie`: Domains, creation times, and flags.
- `BrowserExtension`: Extension IDs and permissions.
- `BrowserDownload`: Filenames and source URLs.
- `BrowserTimelineEvent`: Unified chronological data model.
- `ExtractedBrowserIOC`: Extracted URLs and search keywords.

## Future Roadmap & Vision
- **True SQLite Parsing**: Directly ingest and parse actual `History` and `Cookies` SQLite databases from standard Chrome/Firefox/Edge endpoints.
- **Live Cache Extraction**: Integration with caching engines to recreate visited web pages visually.
- **Password Manager Metadata**: Extract metadata around auto-fill and saved credentials (without extracting the plaintext credentials themselves).
