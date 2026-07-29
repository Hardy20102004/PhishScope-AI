# Enterprise Mobile Forensics - Architecture Guide

## Overview
The Mobile Forensics Platform (Phase X-043) bridges the gap between traditional endpoint investigations and mobile device usage. It handles the ingestion of logical acquisitions (e.g., iTunes Backups, ADB pulls) and extracts critical artifacts such as SMS threads, GPS locations, and third-party app data.

## Architecture Components

### 1. Device Manager (`device_manager.py`)
Responsible for tracking the lineage of the mobile acquisition, logging OS versions, and mapping the backup to specific Investigation IDs.

### 2. Communication Engine (`communication_engine.py`)
Parses mobile messaging SQLite databases (like `sms.db` for iOS). Crucially, this engine not only extracts active records but also scans the SQLite unallocated space/freelists to recover deleted messages, tagging them appropriately.

### 3. Location Engine (`location_engine.py`)
Extracts geospatial artifacts from various sources on the device:
- Cache databases (e.g., CoreLocation, Google Play Services).
- EXIF metadata embedded within camera roll media.
- Wi-Fi association logs.

### 4. Timeline Builder (`timeline_builder.py`)
A unified sequencing engine that merges asynchronous data streams (when a message was sent vs. where the phone physically was at the time) into a single chronological timeline for the investigator.

## Database Schema Highlights
- **`MobileDevice`**: The root acquisition entity.
- **`MobileCommunication`**: Represents individual threaded messages (SMS, WhatsApp, iMessage).
- **`MobileLocation`**: Geospatial waypoints linked back to the device.

## Frontend Modules
- **MobileDashboard**: High-level triage interface for tracking imported backups.
- **ConversationViewer**: An interactive, chat-like UI allowing analysts to read extracted SMS threads exactly as they appeared on the suspect's device, with deleted messages clearly highlighted.
- **LocationMap**: A geospatial mapping tool for visualizing the physical movement of the device leading up to an incident.
