# API Contract Architecture
**Project:** PHOENIX AI-Powered Digital Scam Investigation Platform
**Layer:** Backend to Frontend Communication
**Protocol:** REST over HTTP/1.1 (HTTP/2 ready)
**Format:** JSON (`application/json`)

---

## 1. API Philosophy

The PHOENIX API is designed strictly around an **API-First** and **Contract-Driven** methodology. 

- **Consistency:** Every endpoint must adhere to the exact same response envelope. 
- **Idempotency:** `PUT` and `DELETE` requests are strictly idempotent. Replaying them safely results in the same resource state. `POST` requests for sensitive transactions utilize `Idempotency-Key` headers.
- **Versioning:** URI Versioning is mandatory (`/api/v1/`). Major breaking changes require `/api/v2/`. Minor additive changes are pushed directly to `v1`.
- **Filtering & Sorting:** Executed via URL queries (e.g., `?sort=-created_at&status=active`).
- **Pagination:** Dual-strategy. 
  - *Offset-based:* `?page=1&size=20` for shallow, non-realtime tables.
  - *Cursor-based:* `?cursor=eyJpZCI...&limit=50` for infinite scroll and high-velocity audit logs.

---

## 2. API Folder Structure (FastAPI)

The backend code enforces this contract via the following structure inside `app/`:

- `api/v1/endpoints/` : The actual router controllers (FastAPI endpoints).
- `schemas/` : Pydantic V2 models defining the exact JSON shape (Requests/Responses).
- `schemas/base.py` : The generic universal response envelope definition.
- `validators/` : Complex cross-field validation logic.
- `common/responses.py` : Utility wrappers ensuring endpoints correctly format output.

---

## 3. Standard Response Format

All responses, regardless of success or failure, are wrapped in a standard JSend-inspired envelope enhanced with enterprise metadata.

### Success Envelope
```json
{
  "status": "success",
  "data": { ... },
  "meta": {
    "request_id": "req_5f8a9b2",
    "timestamp": "2026-07-24T12:00:00.000Z",
    "version": "v1.0"
  }
}
```

### Error Envelope
```json
{
  "status": "error",
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Input validation failed",
    "details": [
      { "field": "email", "issue": "Invalid email format" }
    ]
  },
  "meta": {
    "request_id": "req_5f8a9b2",
    "timestamp": "2026-07-24T12:00:00.000Z",
    "version": "v1.0"
  }
}
```

---

## 4. Endpoint Design Standards

- **Resource Naming:** Strictly plural nouns in kebab-case (e.g., `/api/v1/investigations`). No verbs in URLs except for specific RPC actions (`/api/v1/users/123/suspend`).
- **HTTP Methods:**
  - `GET`: Read resources. Safe, Cacheable.
  - `POST`: Create a new resource.
  - `PUT`: Full replacement of a resource.
  - `PATCH`: Partial update.
  - `DELETE`: Soft or hard delete.
- **Status Codes:**
  - `200 OK` (Standard success)
  - `201 Created` (Resource created)
  - `202 Accepted` (Background job enqueued)
  - `400 Bad Request` (Validation errors)
  - `401 Unauthorized` (Missing/invalid JWT)
  - `403 Forbidden` (RBAC failure)
  - `404 Not Found`
  - `429 Too Many Requests`
  - `500 Internal Server Error`

---

## 5. Authentication Integration

Authentication operates statelessly via short-lived JWT Access Tokens and long-lived HTTP-Only Refresh Tokens.

- `POST /api/v1/auth/login` : Accepts credentials, returns Access Token in body, sets Refresh Token in `Secure; HttpOnly` cookie.
- `POST /api/v1/auth/refresh` : Exchanges valid cookie for a new Access Token.
- `POST /api/v1/auth/logout` : Revokes Refresh Token in database, clears cookie.
- `GET /api/v1/auth/me` : Returns current user profile and RBAC permissions based on JWT validation.

---

## 6. Investigation API Blueprint

The core feature of PHOENIX is the AI Investigation engine. Endpoint group:

- `POST /api/v1/investigations/url` - Submit a URL for phishing analysis.
- `POST /api/v1/investigations/email` - Upload an `.eml` file for header/payload analysis.
- `GET /api/v1/investigations/{id}` - Retrieve active status (Pending, Processing, Completed) and final report.
- `GET /api/v1/investigations/{id}/threat-map` - Return graph nodes for visualization.
- `GET /api/v1/investigations/{id}/pcap` - (Future) Download associated network traffic.

---

## 7. OpenAPI & Documentation Standards

- Swagger UI is automatically generated at `/api/v1/docs`.
- Every Pydantic model field must include `title`, `description`, and `example` attributes.
- Every FastAPI endpoint must include `summary`, `response_description`, and declare all possible `responses={400: ..., 403: ...}` models.

---

## 8. Frontend Integration Conventions

The React Frontend must adhere to:
- **Axios Interceptors:** Automatically attaching the `Authorization: Bearer <JWT>` header to all requests.
- **Retry Strategy:** Implement transparent retry logic (e.g., `tanstack/query` retry set to 1) for `502/503/504` errors only. `4xx` errors must never be automatically retried.
- **Stale Cache:** Utilize aggressive caching (`staleTime: 5m`) for static resources to minimize backend traffic.

---

## 9. Observability & Security

- **Request ID Injection:** The frontend should ideally send an `X-Request-ID` header. If absent, the backend Middleware generates one. This UUID is logged in all systems and returned in the `meta` response envelope to easily trace crashes in Sentry/Datadog.
- **CSRF:** Required only for endpoints accepting cookie-based auth. API relies entirely on Authorization headers, largely mitigating CSRF.
- **Rate Limiting:** Enforced at the API Gateway / Nginx level, with `X-RateLimit-Remaining` headers returned to the frontend.
