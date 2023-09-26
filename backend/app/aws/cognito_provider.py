import base64
import hashlib
import hmac

import boto3
from botocore.exceptions import ClientError


class CognitoProvider:

    def __init__(self, app_client_id, app_client_secret):
        self.client = boto3.client("cognito-idp")
        self.app_client_id = app_client_id
        self.app_client_secret = app_client_secret

    def _create_secret_hash(self, username):
        message = bytes(username + self.app_client_id, "utf-8")
        key = bytes(self.app_client_secret, "utf-8")
        return base64.b64encode(hmac.new(key, message, digestmod=hashlib.sha256).digest()).decode()

    def create_user(self, new_user):
        username = new_user.get("username")
        email = new_user.get("email")
        password = new_user.get("password")

        secret_hash = self._create_secret_hash(username)

        try:
            self.client.sign_up(
                ClientId=self.app_client_id,
                SecretHash=secret_hash,
                Username=username,
                Password=password,
                UserAttributes=[{"Name": "email", "Value": email}])
        except ClientError as error:
            print(error)
            return False
        return True

    def sign_in(self, user):
        username = user.get("username")
        password = user.get("password")

        secret_hash = self._create_secret_hash(username)

        try:
            response = self.client.initiate_auth(
                AuthFlow="USER_PASSWORD_AUTH",
                AuthParameters={
                    "USERNAME": username,
                    "PASSWORD": password,
                    "SECRET_HASH": secret_hash
                },
                ClientMetadata={
                    "USERNAME": username,
                    "PASSWORD": password
                },
                ClientId=self.app_client_id)

        except ClientError as error:
            print(error)
            return False
        return response

    def verify_account(self, username, confirmation_code):
        secret_hash = self._create_secret_hash(username)

        try:
            self.client.confirm_sign_up(
                ClientId=self.app_client_id,
                SecretHash=secret_hash,
                Username=username,
                ConfirmationCode=confirmation_code,
                ForceAliasCreation=False, )
        except ClientError as error:
            print(error)
            return False
        return True

    def refresh_token(self, refresh_token, username):
        secret_hash = self._create_secret_hash(username)

        try:
            response = self.client.initiate_auth(
                AuthFlow="REFRESH_TOKEN_AUTH",
                AuthParameters={
                    "REFRESH_TOKEN": refresh_token,
                    "SECRET_HASH": secret_hash
                },
                ClientId=self.app_client_id)
        except ClientError as error:
            print(error)
            return False
        return response

    def get_user(self, access_token):
        try:
            response = self.client.get_user(
                AccessToken=access_token
            )
        except ClientError as error:
            print(error)
            return False
        return response

    def sign_out(self, access_token):
        try:
            self.client.global_sign_out(
                AccessToken=access_token
            )
        except ClientError as error:
            print(error)
            return False
        return True
