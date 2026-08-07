# API Reference Guidelines

The PHOENIX backend exposes a RESTful JSON API at `https://api.phoenix-platform.com/api/v1/`.

## 1. Authentication
All endpoints (except `/auth/login`) require a Bearer JWT Token.
Provide the token in the `Authorization` header:
`Authorization: Bearer <your_jwt_token>`

## 2. Global Response Envelope
To ensure predictable parsing for frontend clients and SDKs, all successful API responses are wrapped in a standard generic envelope defined in `app.schemas.base.APIResponse`:
```json
{
  "status": "success",
  "data": { ... payload ... }
}
```

## 3. Error Handling
Errors are returned as standard HTTP status codes alongside a structured JSON payload:
- `400 Bad Request`: General validation failure.
- `401 Unauthorized`: Missing, expired, or invalid JWT token.
- `403 Forbidden`: Authenticated, but lacking sufficient RBAC permissions.
- `404 Not Found`: Resource does not exist or belongs to another tenant.
- `422 Unprocessable Entity`: Pydantic schema validation failure (e.g., missing required field).

## 4. Pagination
Collection endpoints (e.g., `GET /investigations`) support cursor-based or offset-based pagination via query parameters:
- `skip` (default 0): Number of records to skip.
- `limit` (default 50, max 100): Maximum number of records to return.
