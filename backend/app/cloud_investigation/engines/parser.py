import json
from typing import Any, Dict


class CloudArtifactParserEngine:
    """
    Simulates parsing JSON cloud exports into structured data (Assets, Identities, Configurations, Audit Logs).
    """
    
    @staticmethod
    def parse(payload: str) -> Dict[str, Any]:
        try:
            data = json.loads(payload)
            return data
        except:
            # Fallback mock for testing
            return {
                "assets": [
                    {"asset_type": "EC2 Instance", "asset_id": "i-1234567890abcdef0", "name": "Web-Server-1", "region": "us-east-1", "is_public": True, "metadata_json": {"public_ip": "1.2.3.4"}},
                    {"asset_type": "S3 Bucket", "asset_id": "s3://sensitive-customer-data-001", "name": "sensitive-customer-data-001", "region": "us-east-1", "is_public": False, "metadata_json": {}}
                ],
                "identities": [
                    {"identity_type": "User", "identity_id": "AIDACKCEVSQ6C2EXAMPLE", "name": "alice.smith", "permissions": ["S3:GetObject", "EC2:DescribeInstances"], "is_highly_privileged": False},
                    {"identity_type": "Role", "identity_id": "AROACKCEVSQ6C2EXAMPLE", "name": "EmergencyAdminRole", "permissions": ["*"], "is_highly_privileged": True}
                ],
                "configurations": [
                    {"config_type": "IAM Policy", "resource_id": "EmergencyAdminRole", "details": {"Statement": [{"Effect": "Allow", "Action": "*", "Resource": "*"}]}, "is_misconfigured": True}
                ],
                "audit_logs": [
                    {"timestamp": "2024-01-01T10:00:00Z", "event_name": "AssumeRole", "event_source": "sts.amazonaws.com", "actor": "alice.smith", "source_ip": "192.168.1.1", "user_agent": "aws-cli/2.0.0", "is_anomalous": False},
                    {"timestamp": "2024-01-01T10:05:00Z", "event_name": "StopLogging", "event_source": "cloudtrail.amazonaws.com", "actor": "EmergencyAdminRole", "source_ip": "45.33.1.2", "user_agent": "python-requests/2.25.1", "is_anomalous": True}
                ]
            }
