import base64
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from backend.app.aws.cognito_provider import CognitoProvider
from backend.app.aws.secret_provider import SecretProvider
from datetime import datetime
from backend.app.global_settings import global_settings as g

class AccessController:
    def __init__(self):
        region = g.REGION
        stage = g.STAGE
        self._cognito_pool_data = SecretProvider(
            region,
            g.POOL_CLIENT_DATA_SECRET_NAME
        ).get_secret()
        self._cognito_provider = CognitoProvider(
            self._cognito_pool_data.get("COGNITO_POOL_CLIENT_ID"),
            self._cognito_pool_data.get("COGNITO_POOL_CLIENT_SECRET"))

    def sign_in(self, user):
        cognito_result = self._cognito_provider.sign_in(user)
        if cognito_result is not False:
            payload = {
                "accessToken": cognito_result["AuthenticationResult"]["AccessToken"],
            }
            response = JSONResponse(content={"payload": payload})
            response.set_cookie(key="refreshToken",
                                value=cognito_result["AuthenticationResult"]["RefreshToken"],
                                samesite="strict",
                                secure=True,
                                httponly=True,
                                domain=".api.grind-meter.com",
                                expires=int(datetime.now().timestamp() + g.REFRESH_TOKEN_EXP_MIN * 60))
            response.set_cookie(key="username",
                                value=base64.b64encode(user.get("username").encode()).decode(),
                                samesite="none",
                                secure=True,
                                domain=".grind-meter.com",
                                expires=int(datetime.now().timestamp() + g.REFRESH_TOKEN_EXP_MIN * 60))
            return response
        raise HTTPException(status_code=401)

    def refresh_token(self, refresh_token, username):
        response = self._cognito_provider.refresh_token(refresh_token, username)
        if response is not False:
            payload = {
                "accessToken": response["AuthenticationResult"]["AccessToken"]
            }
            return {"payload": payload}

        raise HTTPException(status_code=401)

    def create_account(self, new_user):
        result = self._cognito_provider.create_user(new_user)
        if result is True:
            return {"success": result}

        raise HTTPException(status_code=400)

    def verify_account(self, username, confirmation_code):
        result = self._cognito_provider.verify_account(username, confirmation_code)
        if result is True:
            return {"success": result}

        raise HTTPException(status_code=400)

    def sign_out(self, access_token):
        result = self._cognito_provider.sign_out(access_token)

        if result:
            return True

        raise HTTPException(status_code=500)
