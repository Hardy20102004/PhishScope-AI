# Architecture Reference

PHOENIX is built upon **Clean Architecture** and **SOLID** principles to ensure enterprise-grade maintainability, testability, and scalability.

## 1. High-Level Architecture
- **Frontend**: React 18, TypeScript, TailwindCSS, Vite. Uses a feature-sliced design. State is managed locally within features to prevent global state bloat.
- **Backend**: Python 3.11, FastAPI, SQLAlchemy 2.0, PostgreSQL 15, Redis 7. 
- **Infrastructure**: Dockerized microservices deployed via Kubernetes on AWS EKS.

## 2. Backend Design Patterns
We strictly enforce the **Repository Pattern** and **Service Layer** separation.
- `app/api/v1/endpoints/`: Handles HTTP routing, Pydantic validation, and dependency injection (FastAPI Routers). **No business logic lives here.**
- `app/services/`: Contains the core business logic (e.g., `UnifiedInvestigationEngine`, `AICopilot`).
- `app/crud/`: The Data Access Layer. Implements the Repository Pattern via `CRUDBase` to abstract SQLAlchemy ORM calls away from the services.
- `app/models/`: SQLAlchemy declarative Base models defining the physical database schema.
- `app/schemas/`: Pydantic models used for input validation and output serialization.

## 3. Multi-Tenancy Architecture
PHOENIX uses a **Logical Multi-Tenancy** model (Shared Infrastructure).
- All sensitive database tables (`investigations`, `cases`, `users`) contain a foreign key to `organizations.id`.
- Tenant isolation is enforced programmatically in the Service and CRUD layers. Endpoints use `Depends(get_current_user)` to derive the active `organization_id` and explicitly scope all SQLAlchemy queries to that ID, preventing Broken Object Level Authorization (BOLA).
