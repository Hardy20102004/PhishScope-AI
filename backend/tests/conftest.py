import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.main import app
from app.api.deps import get_db

from sqlalchemy.pool import StaticPool
# Create an in-memory database for tests
test_engine = create_engine(
    "sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Override get_db dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

class AwaitableProxy:
    def __init__(self, value):
        self.value = value
    def __await__(self):
        yield
        return self.value
    def __getattr__(self, name):
        return getattr(self.value, name)

class AsyncMockSession:
    def __init__(self, sync_session):
        self._sync = sync_session
        
    def add(self, *args, **kwargs):
        return self._sync.add(*args, **kwargs)
        
    def add_all(self, *args, **kwargs):
        return self._sync.add_all(*args, **kwargs)
        
    def commit(self):
        self._sync.commit()
        return AwaitableProxy(None)
        
    def refresh(self, *args, **kwargs):
        self._sync.refresh(*args, **kwargs)
        return AwaitableProxy(None)
        
    def flush(self):
        self._sync.flush()
        return AwaitableProxy(None)
        
    def execute(self, *args, **kwargs):
        res = self._sync.execute(*args, **kwargs)
        return AwaitableProxy(res)
        
    def query(self, *args, **kwargs):
        return self._sync.query(*args, **kwargs)

    def scalar(self, *args, **kwargs):
        res = self._sync.scalar(*args, **kwargs)
        return AwaitableProxy(res)
        
    def scalars(self, *args, **kwargs):
        res = self._sync.scalars(*args, **kwargs)
        return AwaitableProxy(res)
        
    def delete(self, *args, **kwargs):
        self._sync.delete(*args, **kwargs)
        return AwaitableProxy(None)
        
    def get(self, *args, **kwargs):
        res = self._sync.get(*args, **kwargs)
        return AwaitableProxy(res)
        
    def expire_all(self):
        self._sync.expire_all()
        return AwaitableProxy(None)

@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield AsyncMockSession(db)
    finally:
        db.close()

@pytest.fixture
async def async_client():
    """
    Provides an asynchronous HTTPX client for testing FastAPI endpoints.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
