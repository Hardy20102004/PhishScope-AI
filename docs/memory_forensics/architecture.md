# Enterprise Memory Forensics - Architecture Guide

## Overview
The Memory Forensics Platform (Phase X-042) provides deep Volatility-style analysis capabilities. It maps kernel data structures from raw RAM dumps (vmem, raw, dmp) to uncover rootkits, injected DLLs, Direct Kernel Object Manipulation (DKOM), and active network sockets that are entirely invisible to disk-based forensics.

## Architecture Components

### 1. Image Manager (`image_manager.py`)
Handles ingestion and OS profile identification. Accurate memory parsing relies entirely on identifying the exact kernel symbols (e.g., `Win10x64_19041`) to correctly read offsets for the EPROCESS blocks.

### 2. Process Analysis Engine (`process_engine.py`)
Simulates the core functionality of Volatility's `pslist` and `psxview` plugins.
- **pslist**: Follows the active process linked list in the kernel.
- **psxview**: Scans the memory space for thread dispatcher tables to find processes that have unlinked themselves from the main `pslist` (a classic DKOM rootkit technique).

### 3. Network Artifact Engine (`network_engine.py`)
Simulates the `netscan` plugin, hunting through memory to find `TCPT_OBJECT` and `UDPC_ENDPOINT` structures. This reconstructs active and listening sockets, including those owned by hidden processes.

## Database Schema Highlights
- **`MemoryImage`**: The top-level volatile acquisition.
- **`MemoryProcess`**: Maps parent/child relationships (PPID to PID). Uses `is_hidden` and `is_injected` flags to mark DKOM/Hollowing anomalies.
- **`MemoryNetworkConnection`**: Links an active socket to the specific `MemoryProcess` that opened it, facilitating direct threat intelligence correlation.

## Frontend Modules
- **MemoryDashboard**: High-level tracker for RAM ingestion and automated AI analysis.
- **ProcessTreeViewer**: A hierarchical visualizer for nesting PPID/PID relationships, immediately highlighting suspicious anomalies like `cmd.exe` running under a hollowed `svchost.exe`.
- **NetworkSockets**: A data grid showing active memory network connections, automatically cross-referenced with PHOENIX X's Threat Intelligence platform.
