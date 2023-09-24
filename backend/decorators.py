# import os
# from functools import wraps
#
# import flask
# from flask import g, request
#
# from backend.aws.cognito_provider import CognitoProvider
# from backend.aws.secret_provider import SecretProvider
#
#
# def require_authentication(f):
#     @wraps(f)
#     def is_signed_in(*args, **kwargs):
#         cognito_pool_data = SecretProvider(
#             os.environ.get("REGION", "eu-central-1"),
#             os.environ.get("STAGE", "dev")
#         ).get_secret()
#         cognito_provider = CognitoProvider(
#             cognito_pool_data.get("COGNITO_POOL_CLIENT_ID"),
#             cognito_pool_data.get("COGNITO_POOL_CLIENT_SECRET"))
#         g.user = cognito_provider.get_user(request.headers.get("accessToken"))
#         if g.user:
#             return f(*args, **kwargs)
#         return flask.Response(status=401)
#
#     return is_signed_in
#
#
# def possible_authentication(f):
#     @wraps(f)
#     def set_user_if_possible(*args, **kwargs):
#         access_token = request.headers.get("accessToken")
#         if access_token is not None:
#             cognito_pool_data = SecretProvider(
#                 os.environ.get("REGION", "eu-central-1"),
#                 os.environ.get("STAGE", "dev")
#             ).get_secret()
#             cognito_provider = CognitoProvider(
#                 cognito_pool_data.get("COGNITO_POOL_CLIENT_ID"),
#                 cognito_pool_data.get("COGNITO_POOL_CLIENT_SECRET"))
#             g.user = cognito_provider.get_user(access_token)
#         return f(*args, **kwargs)
#
#     return set_user_if_possible
