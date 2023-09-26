import json

import boto3
import base64
from botocore.exceptions import ClientError


class SecretProvider:

    def __init__(self, region, secret_name):
        self._region_name = region
        self._secret_name = secret_name

    def get_secret(self):
        session = boto3.session.Session()
        client = session.client(
            service_name="secretsmanager",
            region_name=self._region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=self._secret_name
            )
        except ClientError as error:
            print(error)
            return False

        if "SecretString" in get_secret_value_response:
            secret = get_secret_value_response["SecretString"]
            return json.loads(secret)
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response["SecretBinary"])
            return json.loads(decoded_binary_secret)
