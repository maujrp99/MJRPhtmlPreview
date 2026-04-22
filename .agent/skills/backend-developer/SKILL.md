---
name: Backend Developer
description: >
  Use when IMPLEMENTING backend code: API design (REST and GraphQL), data
  modeling and migrations, authentication/authorization patterns, error handling
  and structured logging, caching strategies, security fundamentals (OWASP top
  10), writing backend tests (unit, integration, contract), and API documentation.
  This skill owns server-side implementation — not test strategy (see QA Engineer)
  or architecture assessment (see Code Quality).
---

# Skill: Backend Developer

**Purpose**: Teach an AI agent backend development best practices — from API design to security, ensuring the server layer is robust, secure, and well-documented.

**Related Workflows**: `sdd_task_protocol.md`, `code_quality_assessment_protocol.md`, `regression_protocol.md`

---

## 1. API Design

### REST Principles

**Resource-oriented URLs**:
```
✅ GET    /api/books          → List books
✅ GET    /api/books/:id      → Get one book
✅ POST   /api/books          → Create a book
✅ PUT    /api/books/:id      → Replace a book
✅ PATCH  /api/books/:id      → Partially update a book
✅ DELETE /api/books/:id      → Delete a book

❌ GET    /api/getBooks
❌ POST   /api/deleteBook
❌ GET    /api/books/getByAuthor
```

**HTTP Status Codes**:

| Code | When to Use |
|------|-------------|
| 200 | Success with body |
| 201 | Created (POST success) |
| 204 | Success, no body (DELETE) |
| 400 | Client error (bad input, validation failed) |
| 401 | Not authenticated (no valid token) |
| 403 | Not authorized (valid token, insufficient permissions) |
| 404 | Resource not found |
| 409 | Conflict (duplicate, version mismatch) |
| 422 | Unprocessable entity (valid JSON, invalid semantics) |
| 429 | Rate limited |
| 500 | Server error (unexpected, log it) |

**Pagination**:
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 142,
    "total_pages": 8
  }
}
```

**Filtering and Sorting**:
```
GET /api/books?status=reading&sort=-updated_at&page=2&per_page=20
```

### GraphQL Guidelines (when applicable)
- Schema-first design: write the schema before resolvers
- Avoid N+1 queries: use DataLoader or equivalent batching
- Limit query depth and complexity to prevent abuse
- Paginate with cursor-based pagination (Relay spec) for large datasets
- Separate queries (reads) from mutations (writes) clearly

---

## 2. Data Modeling

### Design Process
1. **Identify entities**: What are the nouns? (Book, User, Tag, Session)
2. **Define relationships**: One-to-many, many-to-many, one-to-one
3. **Choose IDs**: UUIDs for distributed systems, auto-increment for simple apps
4. **Add timestamps**: `created_at`, `updated_at` on every table/collection
5. **Soft delete**: Add `deleted_at` instead of hard deletes (data recovery, audit trail)

### Schema Conventions
```
Tables:       plural, snake_case (books, user_sessions)
Columns:      snake_case (garden_status, created_at)
Foreign keys: <singular_table>_id (author_id, category_id)
Booleans:     is_<adjective> or has_<noun> (is_published, has_cover)
Enums:        Define as constrained types, not free strings
```

### Migration Rules
- Every schema change is a **migration** (never edit production DB manually)
- Migrations are versioned and reversible
- Add columns as nullable first, then backfill, then add constraints
- Never rename columns in production without a deprecation period

---

## 3. Authentication & Authorization

### Authentication Patterns

| Pattern | Best For |
|---------|----------|
| **JWT (stateless)** | SPAs, mobile apps, microservices |
| **Session cookies** | Traditional web apps, SSR |
| **OAuth 2.0 / OIDC** | Third-party login (Google, GitHub) |
| **API keys** | Machine-to-machine, simple integrations |

### JWT Best Practices
- Short expiration (15-30 min) + refresh tokens
- Store refresh tokens server-side (DB or Redis), not in localStorage
- Include minimal claims: `sub`, `iat`, `exp`, `role` — not full user profile
- Use `httpOnly`, `secure`, `sameSite` cookies for web transport
- Rotate signing keys periodically

### Authorization Patterns
- **RBAC** (Role-Based): User has role → role has permissions
- **ABAC** (Attribute-Based): Rules based on user + resource + context attributes
- **Check at the API layer**: Never trust the frontend to enforce permissions
- **Principle of least privilege**: Start with no access, grant explicitly

---

## 4. Error Handling & Logging

### Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Book title is required",
    "details": [
      { "field": "title", "issue": "cannot be empty" }
    ],
    "request_id": "req_abc123"
  }
}
```

### Error Handling Rules
- **Catch at boundaries**: Route handlers, middleware, queue processors
- **Classify errors**: Client errors (4xx) vs Server errors (5xx) — different handling
- **Never expose internals**: Stack traces, SQL queries, file paths → only in dev/logs
- **Request ID**: Generate a unique ID per request, include in response and logs
- **Graceful degradation**: If a non-critical service fails, degrade, don't crash

### Logging Levels
```
ERROR:  Something broke, needs attention (failed transactions, unhandled errors)
WARN:   Something unexpected but handled (retry succeeded, deprecation used)
INFO:   Business events (user registered, order placed, sync completed)
DEBUG:  Technical details (SQL queries, API call timings) — dev/staging only
```

### Structured Logging
```json
{
  "level": "error",
  "message": "Failed to fetch book cover",
  "request_id": "req_abc123",
  "book_id": "book_456",
  "error": "TimeoutError: 5000ms exceeded",
  "timestamp": "2026-02-17T14:30:00Z"
}
```

---

## 5. Caching

### Caching Layers

| Layer | Tool | TTL | Use Case |
|-------|------|-----|----------|
| **Browser** | HTTP headers (Cache-Control, ETag) | Varies | Static assets, API responses |
| **CDN** | Cloudflare, Vercel Edge | Minutes-hours | Public pages, images |
| **Application** | Redis, in-memory (LRU) | Seconds-minutes | API responses, computed values |
| **Database** | Query cache, materialized views | Varies | Expensive aggregations |

### Cache Invalidation Strategies
- **Time-based (TTL)**: Simple, predictable, may serve stale data
- **Event-based**: Invalidate on write/update — more complex, always fresh
- **Stale-while-revalidate**: Serve stale, refresh in background — best UX

### Rules
- Cache the **result**, not the query (avoid re-computing on every request)
- Always have a cache-busting mechanism (manual purge, version key)
- Monitor cache hit rates — if < 80%, reconsider your strategy
- Never cache user-specific data in shared caches (security risk)

---

## 6. Security (OWASP Top 10 Essentials)

| Vulnerability | Prevention |
|---------------|------------|
| **Injection** (SQL, NoSQL, OS) | Parameterized queries, ORMs, input validation |
| **Broken Authentication** | Strong password policies, MFA, secure session management |
| **Sensitive Data Exposure** | Encrypt at rest and in transit (TLS), hash passwords (bcrypt/argon2) |
| **Broken Access Control** | Check permissions server-side on every request, deny by default |
| **Security Misconfiguration** | Disable debug in production, remove default credentials, CORS whitelist |
| **XSS** | Escape output, Content-Security-Policy header, sanitize HTML input |
| **CSRF** | CSRF tokens for state-changing requests, SameSite cookies |
| **Rate Limiting** | Limit requests per IP/user, especially on auth endpoints |

### Security Checklist
```
[ ] All passwords hashed with bcrypt/argon2 (never MD5/SHA)
[ ] HTTPS enforced everywhere
[ ] CORS configured with explicit origins (not *)
[ ] Rate limiting on /login, /register, /forgot-password
[ ] SQL injection prevented (parameterized queries)
[ ] Input validation on all endpoints (type, length, format)
[ ] Secrets in environment variables, never in code
[ ] Dependencies scanned for vulnerabilities (npm audit, Snyk)
```

---

## 7. Testing

### Backend Testing Pyramid

```
         ╱╲
        ╱ E2E ╲         Few: Full API flow tests
       ╱────────╲
      ╱Integration╲     Some: API routes + DB + external services
     ╱──────────────╲
    ╱   Unit Tests    ╲  Many: Services, validators, utils
   ╱____________________╲
```

### What to Test

| Layer | What | How |
|-------|------|-----|
| **Unit** | Business logic, validators, transformers | Mock dependencies, test pure functions |
| **Integration** | API endpoints, DB operations | Test DB (in-memory or test container), real HTTP |
| **Contract** | API shape stability | Snapshot API responses, OpenAPI schema validation |

### Testing Rules
- Every API endpoint has at least one happy path and one error path test
- Test auth: unauthenticated, wrong role, correct role
- Use factories/fixtures for test data (not hardcoded IDs)
- Test database migrations: up and down
- Mock external services (payment, email) — never call real ones in tests

---

## 8. API Documentation

### Minimum Documentation
- **OpenAPI/Swagger spec** or equivalent: auto-generated from code or maintained manually
- Every endpoint: method, path, params, request body, response body, error codes
- Authentication requirements per endpoint
- Example requests and responses

### Living Documentation
- Generate docs from code annotations when possible
- Test that docs match reality (contract tests)
- Include in onboarding: new developer should be able to call any endpoint using only the docs

---

---

## Scope & Boundaries

This skill owns backend **implementation patterns**. Other skills own adjacent concerns:

```
"How do I design this API endpoint?"      → Backend Developer (this skill)
"What should the test plan cover?"        → QA Engineer
"How do I write this integration test?"   → Backend Developer (this skill)
"Is the architecture well-structured?"    → Code Quality & Architecture Assessment
"How do I deploy this?"                   → (out of scope — infrastructure/DevOps)
```

### Decision Tree

```
Need to design API routes, data models, or auth?
  └─ YES → Backend Developer
Need to decide what to test or write acceptance criteria?
  └─ YES → QA Engineer
Need to write actual backend test code?
  └─ YES → Backend Developer
Need to assess overall code architecture health?
  └─ YES → Code Quality & Architecture Assessment
Building a mobile app that calls this API?
  └─ YES → Mobile Developer (client side) + Backend Developer (server side)
```

---

## When to Apply This Skill

- During **Specify** phase: Define API contracts, data models, auth requirements in spec.md
- During **Plan** phase: Design endpoints, choose caching strategy, plan migrations
- During **Tasks** phase: Decompose into data layer → API routes → business logic → tests
- During **Implementation**: Follow security checklist, write integration tests, document APIs
- During **Review**: Validate against OWASP checklist, check error handling, review SQL queries
