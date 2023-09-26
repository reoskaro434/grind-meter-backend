# import io
# import json
# import os
#
# from flask import Response, g
#
# from backend.aws.dynamodb.projects_dynamodb_provider import ProjectsDynamodbProvider
# from backend.aws.dynamodb.saves_dynamodb_provider import SavedProjectsDynamodbProvider
# from backend.aws.dynamodb.scores_dynamodb_provider import ScoresDynamodbProvider
# from backend.aws.s3.s3_provider import S3Provider
#
#
# class ProjectController:
#     def __init__(self):
#         self._dynamodb = ProjectsDynamodbProvider(
#             os.environ.get("REGION", "eu-central-1"),
#             os.environ.get("STAGE", "dev"))
#         self._dynamodb_saved_projects = SavedProjectsDynamodbProvider(
#             os.environ.get("REGION", "eu-central-1"),
#             os.environ.get("STAGE", "dev"))
#         self._dynamodb_scores = ScoresDynamodbProvider(
#             os.environ.get("REGION", "eu-central-1"),
#             os.environ.get("STAGE", "dev"))
#         self._s3 = S3Provider(
#             os.environ.get("REGION", "eu-central-1"),
#             os.environ.get("STAGE", "dev"))
#
#     def get_project(self, project_id):
#         result = self._dynamodb.get_project(project_id)
#         if result:
#             item = result.get("Item")
#             if item.get("visible") is False:
#                 user = g.get("user")
#                 if user is not None:
#                     if item.get("user_id") != g.user.get("Username"):
#                         return Response(status=404, mimetype='application/json')
#                 else:
#                     return Response(status=404, mimetype='application/json')
#
#             item_description = self._s3.get_file(f"{project_id}/description").get("Body").read().decode("ascii")
#             item_picture = self._s3.get_file(f"{project_id}/picture").get("Body").read().decode("ascii")
#             project = {
#                 "id": item.get("id"),
#                 "title": item.get("title"),
#                 "description": item_description,
#                 "mainPicture": item_picture,
#                 "author": item.get("user_id"),
#                 "briefDescription": item.get("brief_description"),
#                 "visible": item.get("visible"),
#                 "timestamp": int(item.get("last_timestamp"))
#             }
#             return Response(json.dumps(project),
#                             status=200,
#                             mimetype='application/json')
#         return Response(status=404, mimetype='application/json')
#
#     def delete_project(self, project_id):
#         dynamodb_result = self._dynamodb.delete_project(project_id)
#         self._s3.delete_file(f"{project_id}/description")
#         self._s3.delete_file(f"{project_id}/picture")
#         s3_result = self._s3.delete_file(f"{project_id}/")
#
#         self._dynamodb_saved_projects.delete_all_project_saves(project_id)
#         self._dynamodb_scores.delete_all_project_scores(project_id)
#
#         if dynamodb_result and s3_result:
#             return Response(json.dumps({"success": True}),
#                             status=200,
#                             mimetype='application/json')
#
#         return Response(json.dumps({"success": False}),
#                         status=400,
#                         mimetype='application/json')
#
#     def add_project(self, project):
#         project_id = self._dynamodb.add_project(project)
#         if project_id:
#             description = project.get("description")
#             binary_description = io.BytesIO(description.encode("ascii"))
#             picture = project.get("mainPicture")
#             binary_picture = io.BytesIO(picture.encode("ascii"))
#             response_description = self._s3.upload_object_file(binary_description, f"{project_id}/description")
#             response_picture = self._s3.upload_object_file(binary_picture, f"{project_id}/picture")
#
#             return Response(json.dumps({"success": (response_picture and response_description)}),
#                             status=200,
#                             mimetype='application/json')
#         return Response(json.dumps({"success": False}),
#                         status=200,
#                         mimetype='application/json')
#
#     def get_projects_page(self, page):
#         items = self._dynamodb.get_projects(page)
#         if items:
#             projects = []
#             for item in items:
#                 if item.get("visible"):
#                     item_id = item.get("id")
#                     item_picture = self._s3.get_file(f"{item_id}/picture").get("Body").read().decode("ascii")
#                     projects.append({
#                         "id": item_id,
#                         "title": item.get("title"),
#                         "mainPicture": item_picture,
#                         "author": item.get("user_id"),
#                         "briefDescription": item.get("brief_description"),
#                         "visible": item.get("visible"),
#                         "timestamp": int(item.get("last_timestamp"))
#                     })
#             return Response(json.dumps({"projects": projects}),
#                             status=200,
#                             mimetype='application/json')
#         return Response(status=404, mimetype='application/json')
#
#     def update_project(self, project_data):
#         response = self._dynamodb.update_project(project_data)
#
#         project_id = project_data.get("id")
#         self._s3.delete_file(f"{project_id}/description")
#         self._s3.delete_file(f"{project_id}/picture")
#         self._s3.delete_file(f"{project_id}/")
#
#         description = project_data.get("description")
#         binary_description = io.BytesIO(description.encode("ascii"))
#         picture = project_data.get("mainPicture")
#         binary_picture = io.BytesIO(picture.encode("ascii"))
#         response_description = self._s3.upload_object_file(binary_description, f"{project_id}/description")
#         response_picture = self._s3.upload_object_file(binary_picture, f"{project_id}/picture")
#         if response and response_description and response_picture:
#             return Response(json.dumps({"success": True}),
#                             status=200,
#                             mimetype='application/json')
#
#         return Response(json.dumps({"success": False}),
#                         status=400,
#                         mimetype='application/json')
