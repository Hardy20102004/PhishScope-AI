# Enterprise Browser Forensics - Architecture Guide

## Overview
The Browser Forensics Platform (Phase X-044) is designed to parse and analyze the complex web of artifacts left behind by modern web browsers (Chrome, Firefox, Edge). It transforms raw SQLite databases (`History`, `Web Data`, `Preferences`) and JSON manifests into actionable threat intelligence.

## Architecture Components

### 1. Profile Manager (`profile_manager.py`)
Handles the ingestion of the browser profile directory, identifying the browser type (Chromium-based vs. Gecko-based) to apply the correct extraction schemas.

### 2. History Engine (`history_engine.py`)
Extracts URLs, page titles, and visit timestamps. Crucially, it passes every extracted domain through the PHOENIX X Threat Intelligence feed, instantly flagging known malicious URLs (e.g., Credential Phishing, C2 nodes) that the user navigated to.

### 3. Extension Engine (`extension_engine.py`)
A highly specialized engine that parses extension manifests (`manifest.json`) and local storage. It identifies side-loaded or malicious extensions by analyzing the requested permissions (e.g., flagging a "PDF Converter" that requests `<all_urls>` and `webRequestBlocking`).

### 4. Timeline Builder (`timeline_builder.py`)
Merges web history, file downloads, and extension installation events into a single, unified chronological view. This allows analysts to determine if a malicious extension was installed immediately following a visit to a specific phishing domain.

## Frontend Modules
- **BrowserDashboard**: High-level tracker for ingested profiles and total threat hits.
- **HistoryExplorer**: A searchable interface for browsing history, with malicious domains highlighted in red and enriched with threat categories.
- **ExtensionAnalyzer**: A purpose-built view for auditing installed extensions. It highlights suspicious permissions and provides AI-driven rationales for why an extension is considered high-risk.
