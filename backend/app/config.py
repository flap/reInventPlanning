from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "re:Invent Community Planner API"
    debug: bool = False

    # CORS — origins allowed to call the API (GitHub Pages front-end).
    cors_origins: list[str] = [
        "http://localhost:5173",
        "https://flap.github.io",
    ]

    # DynamoDB
    table_name: str = "tripevent-app"
    aws_region: str = "us-east-1"
    # For local dev against DynamoDB Local (e.g. http://localhost:8000). Empty = real AWS.
    dynamodb_endpoint_url: str = ""

    # Cognito (used by the API Gateway JWT authorizer; kept here for reference/local validation)
    cognito_user_pool_id: str = ""
    cognito_app_client_id: str = ""

    # Location sharing limits (seconds)
    gps_max_ttl_seconds: int = 4 * 60 * 60  # precise GPS: max 4h
    venue_max_ttl_seconds: int = 8 * 60 * 60  # coarse venue: max 8h

    # Special "pepper" highlight: this user is flagged (isPepper) in peer lists.
    # Compared server-side against the profile email so the email itself is never
    # exposed to other users (privacy: ADR-011 minimization).
    pepper_email: str = "flaviopimenta@gmail.com"

    model_config = {"env_file": ".env", "env_prefix": "TRIPEVENT_"}


settings = Settings()
