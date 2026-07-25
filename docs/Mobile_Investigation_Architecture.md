# Enterprise Mobile Device Investigation Platform Architecture

## Overview
The Mobile Device Investigation Platform (PHOENIX Phase X-017) provides structured forensic analysis of lawfully acquired mobile data (e.g., Android/iOS backups, logical extractions, SQLite databases). It extracts device metadata, applications, communications, and locations, building a unified investigation timeline and correlating findings with the PHOENIX AI Brain.

## Architecture Components

### Backend (`app/mobile_investigation/`)
1. **ArtifactProcessingEngine**: Simulates the parsing of raw forensic exports (JSON, XML, SQLite dumps) into structured JSON objects.
2. **DeviceMetadataEngine**: Extracts the device manufacturer, model, OS version, and timezone.
3. **ApplicationAnalysisEngine**: Analyzes installed apps, focusing on requested permissions (e.g., SMS, Admin) to flag suspicious or sideloaded applications.
4. **CommunicationAnalysisEngine**: Parses SMS, MMS, and Call Logs to establish communication patterns.
5. **LocationAnalysisEngine**: Extracts GPS data, Wi-Fi networks, and Bluetooth pairings to reconstruct physical movements.
6. **TimelineEngine**: Merges communications, location updates, and app installations into a unified, chronologically sorted `MobileTimelineEvent` list.
7. **IOCExtractionEngine**: Uses Regex against SMS bodies and contact logs to extract actionable network and host indicators (URLs, IPs, Phone Numbers).
8. **RiskAssessmentEngine**: Normalizes the volume of suspicious apps and malicious communication links into a 0-100 severity score.
9. **MobileInvestigationManager**: Asynchronously orchestrates the extraction and timeline generation pipeline.
10. **MobileAIIntegration**: Generates a human-readable threat narrative summarizing the forensic anomalies on the device.

### Frontend (`frontend/src/features/mobile-investigation/`)
- **MobileInvestigationDashboard**: The main control center for simulating forensic data uploads and viewing the results.
- **DeviceOverview**: Displays the hardware profile and OS version.
- **TimelineViewer**: A chronological feed of all parsed events, making it easy to correlate a malicious SMS with a subsequent suspicious app installation.
- **ApplicationExplorer**: Tabular view of installed apps and their granted permissions.
- **CommunicationExplorer**: Displays SMS threads and call logs, highlighting extracted IOCs.
- **LocationMap**: Mock map component that visualizes extracted GPS coordinates and timestamps.
- **MobileAIFindings**: Renders the AI-generated forensic narrative.

## Data Models
Stored in `app/models/mobile_investigation.py`:
- `MobileInvestigation`: Central link to the PHOENIX investigation graph.
- `DeviceMetadata`: Hardware and OS details.
- `MobileApplication`: App package names and permissions.
- `MobileCommunication`: SMS bodies and Call metadata.
- `MobileLocation`: GPS coordinates and labels.
- `MobileTimelineEvent`: Unified chronological data model.
- `ExtractedMobileIOC`: Extracted URLs, phone numbers.

## Future Roadmap & Vision
- **True SQLite Parsing**: Directly ingest and parse common forensic artifacts like Android's `mmssms.db` or iOS's `sms.db`.
- **Live Maps Integration**: Integrate Leaflet.js to render actual map tiles based on the extracted GPS data.
- **Cloud Backup Analysis**: Integrate APIs to pull and analyze iCloud or Google Drive backups directly.
