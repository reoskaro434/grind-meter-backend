from fastapi import HTTPException
from fastapi.responses import JSONResponse

from backend.app.aws.cognito_provider import CognitoProvider
from backend.app.aws.secret_provider import SecretProvider
from datetime import datetime, timedelta
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

    def __get_expiry(self, minutes):
        expiry = datetime.utcnow()
        expiry += timedelta(minutes=minutes)
        return expiry.strftime('%a, %d-%b-%Y %T GMT')

    def __get_domain(self, username):
        return ".gm.perfect-projects.link" if username == "cmVzYW50ZXI=" or username == "resanter" else ".grind-meter.com" # TODO fix this after buying normal domain

    def sign_in(self, user):
        cognito_result = self._cognito_provider.sign_in(user)
        if cognito_result is not False:
            username = user.get("username")
            payload = {
                "status": True,
            }
            response = JSONResponse(content={"payload": payload})
            response.set_cookie(key="accessToken",
                                value=cognito_result["AuthenticationResult"]["AccessToken"],
                                samesite="strict",
                                secure=True,
                                httponly=True,
                                domain=self.__get_domain(username),
                                expires=self.__get_expiry(g.ACCESS_TOKEN_EXP_MIN))
            response.set_cookie(key="refreshToken",
                                value=cognito_result["AuthenticationResult"]["RefreshToken"],
                                samesite="strict",
                                secure=True,
                                httponly=True,
                                domain=self.__get_domain(username),
                                expires=self.__get_expiry(g.REFRESH_TOKEN_EXP_MIN))
            response.set_cookie(key="username",
                                value=username,
                                samesite="none",
                                secure=True, # "cmVzYW50ZXI=" == "resanter"
                                domain=self.__get_domain(username),
                                expires=self.__get_expiry(g.REFRESH_TOKEN_EXP_MIN))
            return response
        raise HTTPException(status_code=401)

    def refresh_token(self, refresh_token, username):
        cognito_response = self._cognito_provider.refresh_token(refresh_token, username)
        if cognito_response is not False:
            response_body = {
                "payload": {
                    "status": True,
                }
            }

            response = JSONResponse(content=response_body)

            response.set_cookie(key="accessToken",
                                value=cognito_response["AuthenticationResult"]["AccessToken"],
                                samesite="strict",
                                secure=True,
                                httponly=True,
                                domain=self.__get_domain(username),
                                expires=self.__get_expiry(g.ACCESS_TOKEN_EXP_MIN))
            return response

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
