# Enterprise QR Intelligence & Visual Scam Detection Platform Architecture

## Overview
The QR Intelligence Platform (PHOENIX Phase X-014) extends PHOENIX X into physical-to-digital attack vectors (e.g., Quishing). It processes QR code images, decodes their embedded payloads, performs visual analysis to detect physical tampering (such as malicious stickers placed over legitimate codes), and deeply analyzes specialized payment infrastructure indicators (like UPI and EMVCo).

## Architecture Components

### Backend (`app/qr_intelligence/`)
1. **QRDecoderEngine**: Wraps Computer Vision libraries to extract raw payload data (URLs, Text, Wi-Fi configs, Payment strings) from image bytes.
2. **ImageProcessingEngine**: Pre-processes the image, applying perspective correction and contrast enhancement to ensure reliable decoding, while logging image metadata.
3. **VisualAnalysisEngine & BrandDetectionEngine**: Analyzes the structural composition of the QR code and identifies central logos to ensure brand consistency.
4. **TamperingDetectionEngine**: Evaluates image heuristics (contrast anomalies, misaligned finder patterns) to detect physical overlay stickers or digital manipulation.
5. **PaymentQRAnalyzer**: Parses complex financial payloads (UPI URIs, EMVCo TLV structures) to extract merchant identifiers, transaction amounts, and determine payload mutability (static vs. dynamic).
6. **QRRiskScoringEngine**: Aggregates risks based on visual tampering, payload type, and downstream URL intelligence scores.
7. **QRInvestigationOrchestrator**: Manages the asynchronous flow of decoding, analysis, and cross-platform correlation (triggering X-011 for embedded URLs).
8. **QRAIIntegration**: Interfaces with PHOENIX AI Brain to synthesize the detected indicators into an actionable Threat Narrative.

### Frontend (`frontend/src/features/qr-intelligence/`)
- **QRInvestigationDashboard**: Central submission and investigation hub for analysts.
- **QRViewer**: Displays the original image with bounding boxes around detected QR regions and metadata overlays.
- **PayloadViewer**: Highlights the extracted raw data and flags risky URL indicators.
- **TamperingViewer**: Visualizes confidence levels for physical and digital image tampering.
- **PaymentAnalysisPanel**: Extracts and formats specialized financial metadata for fraud analysts.
- **QRAIFindings**: Renders the AI-generated Executive Summary and Threat Narrative.

## Data Models
New models added to `app/models/qr_intelligence.py`:
- `QRInvestigation`: Central link to the PHOENIX investigation graph.
- `DecodedQRPayload`: Raw strings and extracted URLs.
- `QRImageMetadata`: Resolution, format, file size.
- `VisualTamperingData`: Anomaly confidence scores and sticker detection flags.
- `QRPaymentMetadata`: Merchant IDs, Networks, and Transaction details.

## Future Roadmap & Vision
The architecture is designed to support:
- Live camera feeds (streaming extraction).
- Cross-channel scam correlation (linking a Quishing attack to identical infrastructure found via Email Intelligence).
- Real-time video frame analysis.
