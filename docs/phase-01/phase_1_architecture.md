# PHOENIX: AI-Powered Digital Scam Investigation Platform
## Phase 1 – System Architecture & Repository Foundation

---

## SECTION 1: System Architecture

The PHOENIX architecture is designed as an API-first, multi-layered system to support various client interfaces via a single, unified backend.

```mermaid
graph TD
    %% Presentation Layer
    subgraph Presentation Layer
        Web[Web Application]
        Mobile[Mobile Apps iOS/Android]
        Ext[Browser Extension]
        Desktop[Desktop Application]
        B2B[Enterprise Dashboard]
    end

    %% API Layer
    subgraph API Layer
        Gateway[API Gateway / Load Balancer]
        WAF[Web Application Firewall]
    end

    %% Business Logic Layer
    subgraph Business Logic Layer
        Auth[Auth & User Mgmt]
        Core[Core API Services]
        Billing[Subscription/Billing]
    end

    %% Investigation Engine
    subgraph Investigation Engine Layer
        Orchestrator[Investigation Orchestrator]
        WorkerPool[(Async Task Workers)]
        URL_Mod[URL Module]
        Email_Mod[Email Module]
        QR_Mod[QR Module]
    end

    %% AI & Threat Intel
    subgraph AI & Threat Intelligence Layer
        AI[AI Explanation Engine]
        Intel[External Threat Feeds VirusTotal, etc.]
    end

    %% Data Layer
    subgraph Database & Storage Layer
        DB[(Primary DB PostgreSQL)]
        Cache[(Cache Redis)]
        Ev_Storage[(Evidence Storage S3)]
    end

    %% Observability & Notifications
    subgraph Observability Layer
        LogSys[Logging System]
        Monitor[Monitoring & APM]
        Notify[Notification Engine]
    end

    %% Flow
    Presentation Layer --> WAF
    WAF --> Gateway
    Gateway --> Auth
    Gateway --> Core
    Gateway --> Orchestrator
    
    Orchestrator --> WorkerPool
    WorkerPool --> URL_Mod
    WorkerPool --> Email_Mod
    WorkerPool --> QR_Mod
    
    URL_Mod --> AI
    Email_Mod --> AI
    URL_Mod --> Intel
    Email_Mod --> Intel
    
    Core --> DB
    Core --> Cache
    Orchestrator --> DB
    WorkerPool --> Ev_Storage
    
    Core -.-> Notify
    WorkerPool -.-> Notify
    
    Gateway -.-> LogSys
    Core -.-> Monitor
```

### Layer Explanations
- **Presentation Layer:** The user-facing clients. All communicate strictly over HTTPS to REST/GraphQL APIs.
- **API Layer:** Handles routing, rate limiting, SSL termination, and basic WAF protections.
- **Business Logic Layer:** Manages users, organizations, API keys, and standard CRUD operations.
- **Investigation Engine:** The asynchronous core. Orchestrates complex, long-running investigations via message queues and worker pools.
- **AI Layer:** Interfaces with Large Language Models (LLMs) to generate natural language explanations of threats.
- **Threat Intelligence Layer:** Connects to third-party APIs (VirusTotal, URLScan) to gather external context.
- **Evidence Storage:** S3-compatible object storage for immutable artifacts (screenshots, PDF payloads, packet captures).
- **Database Layer:** Relational data for structured entities; caching for sessions and rate limiting.
- **Logging/Monitoring Layer:** Captures application metrics, audit trails, and errors (e.g., ELK Stack, Prometheus/Grafana).
- **Notification Layer:** Handles webhooks, email alerts, and in-app notifications.
- **Future Enterprise Layer:** Supports SAML SSO, SIEM integrations, and tenant-isolated deployments.

---

## SECTION 2: Architecture Style

**Recommendation:** **Modular Monolith** (Transitioning to Microservices).

### Why Modular Monolith?
- **Speed of Development:** In the early stages, a Modular Monolith allows the team to move fast without the DevOps overhead of managing 15+ separate microservices, networks, and distributed tracing.
- **Enforced Boundaries:** By strictly organizing code into independent domains (Modules) with well-defined interfaces, the system acts like microservices internally. 
- **Shared Infrastructure:** Single database instance (with schema separation), single deployment pipeline, making it highly cost-effective for V1.

### Migration Strategy for Future Scaling
When a specific module (e.g., the URL Investigation Module) requires scaling independently due to high compute/network load, it can be seamlessly extracted into its own Microservice. The use of an internal event bus (Message Queue) inside the Modular Monolith ensures that when the module becomes a separate service, the communication protocol (events) remains unchanged.

---

## SECTION 3: Module Planning

| Module | Responsibility |
| :--- | :--- |
| **Authentication** | Login, Registration, JWT issuing, Password resets, MFA, Session management. |
| **User Management** | Profile updates, roles, preferences, and organization mapping. |
| **Dashboard** | Aggregation of user statistics, recent scans, and high-level platform metrics. |
| **URL Investigation** | Parsing URLs, resolving DNS, capturing HTTP redirects, scraping DOM. |
| **Website Investigation** | Headless browser execution, capturing screenshots, TLS cert validation. |
| **Email Investigation** | Parsing EML files, analyzing headers (SPF/DKIM/DMARC), extracting attachments. |
| **QR/OCR/Voice/SMS/WhatsApp** | Future modules for processing specific scam vectors. |
| **AI Engine** | Prompt management, LLM API communication, caching AI responses. |
| **Threat Intelligence** | API client wrappers for external vendors; standardizing 3rd party threat scores. |
| **Evidence Manager** | Hashing files, uploading to S3, generating presigned URLs, chain-of-custody tracking. |
| **Case Management** | Grouping multiple investigations into a single incident, assigning analysts, tracking status. |
| **Reports** | Generating PDF/JSON reports from investigation data. |
| **Notification** | Dispatching emails (SendGrid/SES), pushing Webhooks to enterprise clients. |
| **Audit** | Immutable recording of "who did what and when" (critical for enterprise). |
| **Settings/Admin** | Platform configuration, API key generation, user suspension, global flags. |
| **Analytics** | Tracking platform usage, investigation volumes, and API consumption for billing. |

---

## SECTION 4: Repository Structure

**Recommendation:** Monorepo using a tool like Turborepo (for JS) or a standardized multi-root workspace.

```text
phoenix/
├── .github/                   # CI/CD workflows, issue templates, PR checks
├── docs/                      # Architecture Decisions (ADRs), API specs, onboarding
├── docker/                    # Dockerfiles, docker-compose.yml for local dev
├── infra/                     # Terraform code (AWS/GCP), Kubernetes manifests
├── scripts/                   # Local dev setup scripts, database seeders
│
├── frontend/                  # Web Application
│   ├── public/                # Static assets
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   ├── hooks/             # Custom React hooks
│   │   ├── layouts/           # Page layouts
│   │   ├── pages/             # Route components
│   │   ├── services/          # API client wrappers
│   │   ├── store/             # Global state management
│   │   └── utils/             # Helper functions
│   └── package.json
│
├── backend/                   # Python Backend (Modular Monolith)
│   ├── app/
│   │   ├── core/              # Config, Security, DB connection
│   │   ├── modules/           # Business domains (Auth, URL, Email, etc.)
│   │   │   ├── auth/          # Example module
│   │   │   │   ├── router.py  # API endpoints
│   │   │   │   ├── service.py # Business logic
│   │   │   │   ├── schema.py  # Pydantic models (DTOs)
│   │   │   │   └── models.py  # SQLAlchemy models
│   │   ├── shared/            # Common utilities used across modules
│   │   └── main.py            # FastAPI application entry point
│   ├── tests/                 # Pytest suite
│   ├── alembic/               # Database migrations
│   └── pyproject.toml
│
├── mobile/                    # React Native / Flutter (Future)
├── browser-extension/         # Manifest V3 extension (Future)
└── desktop/                   # Electron/Tauri app (Future)
```

---

## SECTION 5: Frontend Architecture

- **Framework:** **Next.js (React)**. Provides Server-Side Rendering (SSR) for fast initial loads, excellent SEO, and robust API routing if needed as a Backend-for-Frontend (BFF).
- **Routing:** Next.js App Router.
- **State Management:** **Zustand** for lightweight global state (user sessions, themes) and **React Query (TanStack Query)** for server state (caching API responses, loading states).
- **UI Components:** **Radix UI** or **Shadcn/UI** combined with **Tailwind CSS**. Provides unstyled, accessible primitives that we can completely customize for a premium feel.
- **Theme/Dark Mode:** Tailwind's built-in dark mode (`class` strategy). Controlled via next-themes.
- **Accessibility:** Radix UI primitives enforce WCAG compliance natively (ARIA attributes, keyboard navigation).
- **Internationalization:** `next-intl` or `i18next` for supporting multiple languages in the future.

---

## SECTION 6: Backend Architecture

- **Python Framework:** **FastAPI**. Chosen for its extreme performance (ASGI), native async support, and automatic generation of OpenAPI documentation.
- **Project Structure:** Domain-Driven Design (DDD) inspired Modular structure (see Section 4).
- **Service Layer Pattern:** API routers (`router.py`) must never contain business logic. They call `service.py`, keeping HTTP concerns separate from business rules.
- **Repository Pattern:** `service.py` calls standard database abstractions (e.g., `repo.py` or direct SQLAlchemy 2.0 ORM interactions). This allows swapping the DB layer without touching business logic.
- **Dependency Injection:** Use FastAPI's native `Depends()` system to inject database sessions, external API clients, and configuration.
- **Configuration:** **Pydantic BaseSettings**. Reads from `.env` files locally and environment variables in production, enforcing strict type-checking on config values.
- **Secrets Management:** Environment variables in development. AWS Secrets Manager or HashiCorp Vault in production, injected into containers at runtime.
- **Background Tasks:** **Celery** with **Redis** as the broker. Crucial for long-running investigations (e.g., headless browser scraping) that would otherwise block the HTTP thread.
- **Validation:** **Pydantic v2**. Provides lightning-fast (Rust-based) schema validation for all incoming API payloads and outgoing responses.
- **Logging:** **Structlog** for structured JSON logging, enabling easy ingestion into tools like Datadog or ELK.
- **Error Handling:** Centralized exception handlers in FastAPI (`@app.exception_handler`). Never expose raw stack traces to the client; always return standardized API error models (e.g., `{ "error": "NOT_FOUND", "message": "..." }`).

---

## SECTION 7: Infrastructure Planning

- **Docker:** Everything is containerized. `backend` runs as a Python/Uvicorn container. `frontend` runs as a Node/Next.js container. Workers run as Celery containers.
- **Reverse Proxy:** **Nginx** or **Traefik**. Traefik is highly recommended for modern containerized stacks due to auto-discovery.
- **HTTPS:** Let's Encrypt / Certbot for automated TLS certificates. SSL termination happens at the Load Balancer/Proxy.
- **Environment Management:** 
  - `Development`: Local machines (docker-compose).
  - `Staging`: Cloud environment mirroring production (for QA and client demos).
  - `Production`: High-availability cluster.
- **Cloud Readiness:** Agnostic by design, but optimized for AWS (EKS/ECS, RDS for Postgres, ElastiCache for Redis, S3 for Evidence).
- **Scaling Strategy:** Horizontal Pod Autoscaling (HPA) in Kubernetes based on CPU and custom metrics (e.g., Celery queue length).
- **CI/CD Readiness:** GitHub Actions.
  - *CI:* On Push -> Run tests, lint, security scan (Bandit/Safety).
  - *CD:* On Tag -> Build Docker images, push to registry (ECR), deploy to Staging/Prod.

---

## SECTION 8: Security Architecture

- **Authentication:** JWT (JSON Web Tokens). Short-lived Access Tokens (15 mins) and HTTP-Only, Secure, SameSite=Strict Refresh Tokens (7 days).
- **Authorization/RBAC:** Role-Based Access Control managed via the database. Roles: `Viewer`, `Analyst`, `Admin`, `SuperAdmin`. Enforced via FastAPI dependencies.
- **Secrets & Encryption:** AES-256 for sensitive data at rest (e.g., user API keys for 3rd party tools). TLS 1.3 for data in transit.
- **Rate Limiting:** Redis-based token bucket algorithm. Strict limits on unauthenticated endpoints (e.g., login, password reset) and quota-based limits for API consumers.
- **Input Validation:** Pydantic strictly validates all incoming JSON. Sanitize all HTML/String inputs to prevent XSS.
- **Secure Headers:** Implement standard security headers (Helmet in JS equivalents): HSTS, CSP (Content Security Policy), X-Frame-Options, X-Content-Type-Options.
- **Audit Logs:** A dedicated `audit_logs` table tracking `user_id`, `action`, `resource`, `timestamp`, and `ip_address` for every mutating action (POST/PUT/DELETE).

---

## SECTION 9: Logging Strategy

- **Application Logs:** Structured JSON logging (Structlog). Output to stdout, captured by container orchestrator (e.g., FluentBit).
- **Security Logs:** Distinct log tags for login failures, suspicious IPs, and unauthorized access attempts. Routed to SIEM.
- **Investigation Logs:** Debug-level logs specific to a module's execution (e.g., "URL resolved to IP X", "Timeout during DOM load").
- **AI Logs:** Logging LLM prompts (sanitized) and responses to track AI token usage, latency, and hallucination rates.
- **System Logs:** OS and database level logs.
- **Audit Logs:** Stored immutably in the primary database for user-facing compliance.
- **Retention Strategy:** Hot storage (30 days in Elasticsearch/Datadog), Cold storage (1 year in S3/Glacier).

---

## SECTION 10: Monitoring Strategy

- **Health Checks:** `/health` endpoints on all services checking DB connectivity, Cache connectivity, and external API status.
- **Performance Metrics:** 
  - API: Latency, Request Rate, Error Rate (HTTP 5xx).
  - Workers: Queue length, Task processing time, Task failure rate.
- **System Metrics:** CPU, Memory, Network I/O of containers.
- **Alerting:** PagerDuty/Slack alerts triggered by Prometheus/Datadog monitors (e.g., "API Error Rate > 2% for 5 mins").
- **Error Tracking:** **Sentry** integration in both Frontend and Backend for real-time capture of unhandled exceptions and stack traces.

---

## SECTION 11: Configuration Management

- **Development:** Local `.env` files (never committed to git).
- **Testing:** CI pipeline injects testing environment variables.
- **Production:** Infrastructure as Code (Terraform) provisions AWS Parameter Store or HashiCorp Vault. The application fetches config at startup.
- **Environment Variables:** Strictly typed via Pydantic BaseSettings. System crashes on boot if a required variable is missing.
- **Feature Flags:** Use a system like LaunchDarkly or a simple database table to toggle beta features (e.g., `enable_voice_module=false`) without redeploying.

---

## SECTION 12: Naming Standards

- **Folders/Directories:** `kebab-case` (e.g., `user-management`, `api-gateway`).
- **Files (Python):** `snake_case.py` (e.g., `investigation_service.py`).
- **Files (React):** `PascalCase.tsx` for components, `camelCase.ts` for utilities.
- **Variables/Functions (Python):** `snake_case`.
- **Variables/Functions (JS/TS):** `camelCase`.
- **Classes:** `PascalCase` across all languages.
- **Database Tables:** `snake_case`, plural (e.g., `users`, `investigations`).
- **API Endpoints:** `kebab-case`, plural nouns (e.g., `GET /api/v1/investigations/`, `POST /api/v1/users/`).
- **Git Branches:** `<type>/<issue-id>-<short-desc>` (e.g., `feat/PHX-123-url-module`, `fix/PHX-456-login-bug`).
- **Commit Messages:** Conventional Commits (e.g., `feat(auth): implement JWT refresh`, `fix(ui): resolve button misalignment`).

---

## SECTION 13: Git Strategy

**Recommendation:** **GitHub Flow** (simpler, leaner alternative to strict GitFlow, suitable for SaaS Continuous Deployment).

- **Main Branch:** `main`. Always deployable. Represents production state.
- **Development Branch:** Feature branches branch off `main` and merge directly back into `main` (if CD is robust) or a `staging` branch depending on QA needs.
- **Feature Branches:** `feat/*`.
- **Release Branches:** Optional. Used if doing scheduled releases (e.g., `release/v1.2.0`).
- **Hotfix Branches:** `hotfix/*`. Branched from `main`, merged back into `main` (and deployed immediately).
- **Versioning:** Semantic Versioning (SemVer) - `MAJOR.MINOR.PATCH`.
- **Pull Request Workflow:** 
  1. Draft PR opened.
  2. CI runs tests and linters.
  3. At least 1 code review approval required.
  4. Squash and merge (keeps history clean).

---

## SECTION 14: Documentation Standards

- **README.md:** Root level. Explains what the project is, local setup instructions, and architecture overview.
- **Architecture Docs (ADRs):** Stored in `docs/architecture/`. Used to document major technical decisions (e.g., "Why we chose Celery over RQ").
- **API Docs:** Automatically generated via FastAPI (Swagger UI at `/docs` and ReDoc at `/redoc`).
- **Developer Guide:** `docs/development.md`. Code style, how to run migrations, how to add a new module.
- **Deployment Guide:** `docs/deployment.md`. Infrastructure topology, scaling runbooks.
- **Security Guide:** `docs/security.md`. Threat models, incident response plan, vulnerability disclosure policy.
- **Contribution Guide:** `CONTRIBUTING.md`. Branch naming, PR process.
- **Coding Standards:** Enforced via automated tools (Ruff/Black for Python, ESLint/Prettier for JS), minimizing manual arguments over style.

---

## SECTION 15: Development Roadmap

- **Phase 1: Foundation (Weeks 1-4)**
  - Repository setup, CI/CD pipelines.
  - Database provisioning and base schema (Users, Orgs).
  - Auth module implementation (JWT).
  - API Gateway and basic Web Dashboard skeleton.
- **Phase 2: Core Investigation Engine (Weeks 5-8)**
  - Implementation of Celery background workers.
  - URL Module (DNS resolution, simple scraping).
  - AI Engine integration (Prompting, Evidence structuring).
  - Evidence Storage (S3 uploads).
- **Phase 3: Expansion & Reporting (Weeks 9-12)**
  - Email Module implementation.
  - Threat Intelligence API integrations.
  - PDF Report generation module.
  - Notification Engine (Email/Webhooks).
- **Phase 4: Client Ecosystem (Weeks 13-16)**
  - Browser Extension MVP.
  - Public REST API finalization and documentation.
  - API Key management in the Dashboard.
- **Phase 5: Enterprise Readiness (Weeks 17+)**
  - Advanced RBAC and Audit Logging implementation.
  - Case Management module.
  - SAML/SSO integrations.
  - Load testing and performance tuning for production launch.
