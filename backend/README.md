# re:Invent Community Planner — Backend

FastAPI backend for **Feature 11** (accounts + cloud plan), **Feature 12** (opt-in
location sharing) and **Feature 13** (findPepper). Deployed as a single AWS Lambda
(FastAPI via Mangum) behind an API Gateway HTTP API with a Cognito JWT authorizer,
persisting to a single DynamoDB table with TTL. See `../DESIGN.md` ADR-008–011.

## Privacy model (enforced server-side)

- Location sharing is **opt-in**; a user has no location record until they POST one.
- **Reciprocity**: `GET /api/v1/share` returns `403` unless the caller is *currently*
  sharing in the same scope. This is enforced in the API, not the client.
- Every location item carries `expiresAt` → DynamoDB **TTL** auto-expires it. GPS is
  capped at 4h, venue at 8h regardless of requested duration.
- `DELETE /api/v1/share` removes the record immediately (instant revoke).
- `DELETE /api/v1/account` wipes all plan + location data (right to erasure, F11.8).

## Local development

```bash
python3 -m venv .venv
./.venv/bin/pip install -e ".[dev]"

# Run tests (uses moto to mock DynamoDB — no AWS account needed)
./.venv/bin/pytest -q

# Run locally against DynamoDB Local (optional)
export TRIPEVENT_DEBUG=true
export TRIPEVENT_DYNAMODB_ENDPOINT_URL=http://localhost:8000
./.venv/bin/uvicorn app.main:app --reload
# Docs at http://localhost:8000/api/docs
```

In `DEBUG` mode only, auth accepts `Authorization: Bearer <sub>` where `<sub>` is
treated as the user id. In production the Cognito JWT authorizer supplies the verified
`sub` and this fallback is inactive.

## Deploy (AWS) — not run automatically

Infrastructure is defined as code in `infra/template.yaml` (AWS SAM). Deploying
creates real, billable resources, so it is intentionally a manual step:

```bash
sam validate --lint --template infra/template.yaml
sam build --template infra/template.yaml
sam deploy --guided --template infra/template.yaml
```

After deploy, use the `ApiUrl` output as `VITE_API_URL` and the Cognito outputs in the
frontend auth config.
