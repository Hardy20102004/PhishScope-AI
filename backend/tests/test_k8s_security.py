import pytest
import uuid
from app.k8s_security.cluster_discovery_engine import ClusterDiscoveryEngine
from app.k8s_security.rbac_analysis_engine import RBACAnalysisEngine
from app.k8s_security.k8s_risk_engine import K8sRiskEngine

pytestmark = pytest.mark.asyncio

async def test_k8s_security_workflows(db_session):
    tenant_id = uuid.uuid4()
    
    # 1. Test Cluster Discovery
    cde = ClusterDiscoveryEngine(db_session)
    cluster = await cde.register_cluster(tenant_id, "prod-eks-1", "EKS", "1.28", "us-east-1")
    
    assert cluster.cluster_name == "prod-eks-1"
    assert cluster.status == "ACTIVE"
    
    # 2. Test RBAC Analysis (Normal)
    rae = RBACAnalysisEngine(db_session)
    normal_perms = {"verbs": ["get", "list"], "resources": ["pods"]}
    policy1 = await rae.analyze_subject(tenant_id, cluster.id, "viewer", "ServiceAccount", "default", normal_perms)
    
    assert policy1.is_overprivileged is False
    
    # 3. Test RBAC Analysis (Overprivileged)
    admin_perms = {"verbs": ["*"], "resources": ["*"]}
    policy2 = await rae.analyze_subject(tenant_id, cluster.id, "jenkins", "ServiceAccount", "ci-cd", admin_perms)
    
    assert policy2.is_overprivileged is True
    
    # 4. Test Risk Aggregation
    kre = K8sRiskEngine(db_session)
    risk_score = await kre.update_cluster_risk(tenant_id, cluster.id)
    
    # We have 1 overprivileged account, risk should be 20.0
    assert risk_score.risk_score == 20.0
    assert risk_score.rbac_issues_count == 1
