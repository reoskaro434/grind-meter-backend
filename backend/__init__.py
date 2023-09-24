# import os
#
# from flask import Flask
# from flask_cors import CORS
#
# from backend.rest.access_endpoint import access
# from backend.rest.project_endpoint import project
# from backend.rest.saves_endpoint import saves
# from backend.rest.scores_endpoint import scores
# from backend.rest.user_profile_endpoint import user_profile
#
# app = Flask(__name__)
# stage = os.environ.get("STAGE", "dev")
# region = os.environ.get("REGION", "eu-central-1")
# url = f'https://{stage}-{region}.perfect-projects.link'
# www_url = f'https://www.{stage}-{region}.perfect-projects.link'
# local_url = "https://perfect-projects.link:4200"
# cors = CORS(app,
#             supports_credentials=True,
#             origins=[local_url, www_url, url])
#
# # Registered endpoints
# app.register_blueprint(access)
# app.register_blueprint(user_profile)
# app.register_blueprint(project)
# app.register_blueprint(scores)
# app.register_blueprint(saves)
