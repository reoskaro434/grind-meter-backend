import os

from backend.app.aws.cognito_provider import CognitoProvider
from backend.app.aws.secret_provider import SecretProvider
from fastapi import HTTPException


def get_current_user(access_token: str):
    cognito_pool_data = SecretProvider(
        os.environ.get("REGION", "eu-central-1"),
        os.environ.get("STAGE", "dev")
    ).get_secret()
    cognito_provider = CognitoProvider(
        cognito_pool_data.get("COGNITO_POOL_CLIENT_ID"),
        cognito_pool_data.get("COGNITO_POOL_CLIENT_SECRET"))

    user = cognito_provider.get_user(access_token)
    if not user:
        raise HTTPException(status_code=403, detail="Cannot get current user")

    return user
