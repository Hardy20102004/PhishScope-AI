import pytest
from app.ai_context.builder import ContextManager
from app.schemas.ai_context import ContextRequest
from app.models.ai_context import ContextPolicy, ContextPolicyType

def test_context_compression():
    # We can test compression logic independently or via manager
    pass

def test_policy_engine_redaction(db_session):
    # Create active PII Redaction policy
    policy = ContextPolicy(
        policy_type=ContextPolicyType.REDACT_PII.value,
        name="Global PII Redaction",
        is_active=True
    )
    db_session.add(policy)
    db_session.commit()
    
    manager = ContextManager(db_session)
    
    # We mock the builder's raw fetch to return something with an SSN
    # to test if policy applies correctly.
    original_fetch = manager.builder.fetch_raw_context
    def mock_fetch(request):
        return "The user's SSN is 123-45-6789."
    manager.builder.fetch_raw_context = mock_fetch
    
    import uuid
    req = ContextRequest(query=f"test_redaction_{uuid.uuid4()}", max_tokens=100)
    res = manager.build_context(req)
    
    assert "[REDACTED_SSN]" in res.assembled_context
    assert "123-45-6789" not in res.assembled_context
    assert any("PII" in w for w in res.validation.warnings)
    
    # Restore mock
    manager.builder.fetch_raw_context = original_fetch

def test_context_caching(db_session):
    manager = ContextManager(db_session)
    
    import uuid
    unique_query = f"cache_test_{uuid.uuid4()}"
    req = ContextRequest(query=unique_query)
    
    # First build (cache miss)
    res1 = manager.build_context(req)
    assert res1.metrics.cache_hit is False
    
    # Second build (cache hit)
    res2 = manager.build_context(req)
    assert res2.metrics.cache_hit is True
