"""Authentication dependency.

In production, an API Gateway (HTTP API) JWT authorizer backed by Amazon Cognito
validates the access token BEFORE the request reaches Lambda, and injects the
verified claims into the request context. We simply read the `sub` claim from
there — the Lambda never sees or trusts a raw token.

For local development / tests (no API Gateway in front), we fall back to reading
the user id from the `Authorization: Bearer <sub>` header. This fallback is only
active when `debug` is enabled, so it can never be used against a real deployment.
"""

from fastapi import Depends, Header, HTTPException, Request, status

from app.config import settings


def _sub_from_gateway_context(request: Request) -> str | None:
    """Read the Cognito `sub` injected by the API Gateway JWT authorizer."""
    scope = request.scope.get("aws.event") or {}
    try:
        claims = (
            scope.get("requestContext", {})
            .get("authorizer", {})
            .get("jwt", {})
            .get("claims", {})
        )
        sub = claims.get("sub")
        return sub or None
    except AttributeError:
        return None


def get_current_user_sub(
    request: Request,
    authorization: str | None = Header(default=None),
) -> str:
    """Return the authenticated user's Cognito `sub`, or raise 401."""
    sub = _sub_from_gateway_context(request)
    if sub:
        return sub

    # Local/dev fallback only — never trusted in a real deployment.
    if settings.debug and authorization and authorization.lower().startswith("bearer "):
        candidate = authorization[7:].strip()
        if candidate:
            return candidate

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
    )


CurrentUser = Depends(get_current_user_sub)
