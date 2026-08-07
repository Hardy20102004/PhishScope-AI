# Enterprise Data Security Posture Management (DSPM) Platform - Architecture Guide

## Overview
Phase X-066 introduces the DSPM platform to PHOENIX X, extending the ecosystem's protection down to the data layer itself. The platform continuously discovers data assets (S3, RDS, Blob Storage), classifies sensitive information, and evaluates complex exposure risks (like a public S3 bucket containing PII).

## Architecture Components

### 1. Data Discovery Engine (`data_discovery_engine.py`)
Scans multi-cloud environments to inventory all structured, semi-structured, and unstructured data stores. It abstracts the underlying storage technology into a unified `CloudDataAsset` model.

### 2. Data Classification Engine (`data_classification_engine.py`)
Evaluates the contents and metadata of discovered assets to assign sensitivity labels (PII, PHI, Financial, etc.). It generates a `confidence_score` and integrates with human-in-the-loop workflows if the AI context engine flags ambiguous, proprietary data below the confidence threshold.

### 3. Exposure Analysis Engine (`exposure_analysis_engine.py`)
Correlates the `CloudDataAsset` configuration with the `DataClassification` labels. This engine distinguishes between acceptable exposure (a public S3 bucket hosting website images) and critical risk (a public S3 bucket hosting PII backups).

### 4. Encryption Assessment Engine (`encryption_assessment_engine.py`)
Validates that sensitive data stores adhere to enterprise cryptography standards, checking for at-rest encryption, TLS in-transit enforcement, and KMS/CMK rotation hygiene.

### 5. DSPM Compliance Engine (`dspm_compliance_engine.py`)
Maps the specific exposure and encryption findings against frameworks like PCI DSS, ISO 27001, and privacy regulations (GDPR/CCPA via ISO 27701).

## Frontend Modules
- **DataInventoryDashboard**: A high-level view showing all discovered assets, their locations, and storage classes across AWS, Azure, and GCP.
- **ClassificationDashboard**: Analytics on data sensitivity distribution, explicitly highlighting low-confidence classifications awaiting human review.
- **ExposureDashboard**: The primary operational view for remediating data risk, highlighting exposures like cross-account sharing and public access.
- **EncryptionDashboard**: Posture view focused exclusively on key management (KMS/KeyVault) and at-rest encryption coverage.
