# Enterprise Disk Forensics - Architecture Guide

## Overview
The Disk Forensics Platform (Phase X-041) is designed to handle the deep analysis of raw evidence files (e.g., E01, DD). It provides the capabilities to map file systems, recover deleted artifacts from unallocated space, and generate chronologically ordered MAC timelines.

## Architecture Components

### 1. Image Manager (`image_manager.py`)
Responsible for the initial ingestion of evidence. Crucially, it manages cryptographic hash verification (MD5/SHA256) upon upload to maintain forensic chain of custody and ensure the image hasn't been tampered with.

### 2. File System Analysis Engine (`fs_analysis_engine.py`)
Acts as the parser for volume structures (e.g., NTFS MFT, EXT4 Inodes). It maps the hierarchical directory structure and logs active file artifacts to the database.

### 3. Recovery Engine (`recovery_engine.py`)
Executes signature-based file carving. It scans unallocated sectors (slack space) to recover deleted files that are no longer indexed by the MFT.

### 4. Timeline Builder (`timeline_builder.py`)
Synthesizes the MAC (Modified, Accessed, Created) timestamps from every extracted artifact, providing a unified chronological view of user activity leading up to an incident.

## Database Schema Highlights
- **`DiskImage`**: The top-level entity representing the physical/logical acquisition.
- **`DiskPartition`**: Represents a parsed volume.
- **`ForensicArtifact`**: An individual file (active or deleted). Stores flags (`is_deleted`, `is_carved`) to explicitly denote its forensic state.

## Frontend Modules
- **DiskDashboard**: High-level tracking of ingested images and their hash verification status.
- **FileExplorer**: A dual-pane interface featuring a navigable directory tree and a mock Hex Viewer for examining binary file headers.
- **ForensicTimeline**: A chronological feed of file system activity.
