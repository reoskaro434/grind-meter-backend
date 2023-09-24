# import json
# import os
#
# from flask import Response, g
#
# from backend.aws.dynamodb.projects_dynamodb_provider import ProjectsDynamodbProvider
# from backend.aws.dynamodb.saves_dynamodb_provider import SavedProjectsDynamodbProvider
# from backend.aws.s3.s3_provider import S3Provider
#
#
# class UserProfileController:
#     def __init__(self):
#         self._dynamodb = ProjectsDynamodbProvider(
#             os.environ.get("REGION", "eu-central-1"),
#             os.environ.get("STAGE", "dev"))
#         self._s3 = S3Provider(
#             os.environ.get("REGION", "eu-central-1"),
#             os.environ.get("STAGE", "dev"))
#         self._user_id = g.user.get("Username")
#         self._dynamodb_saved_projects = SavedProjectsDynamodbProvider(
#             os.environ.get("REGION", "eu-central-1"),
#             os.environ.get("STAGE", "dev"))
#
#     def get_all_projects(self):
#         dynamo_result = self._dynamodb.get_all_user_projects(self._user_id)
#         items = dynamo_result.get("Items")
#         projects = []
#         for item in items:
#             item_id = item.get("id")
#             item_picture = self._s3.get_file(f"{item_id}/picture")
#
#             if item_picture:
#                 item_picture = item_picture.get("Body").read().decode("ascii")
#             else:
#                 item_picture = ""
#
#             projects.append({
#                 "id": item_id,
#                 "title": item.get("title"),
#                 "mainPicture": item_picture,
#                 "author": item.get("user_id"),
#                 "briefDescription": item.get("brief_description"),
#                 "visible": item.get("visible"),
#                 "timestamp": int(item.get("last_timestamp"))
#             })
#         return Response(json.dumps({"projects": projects}),
#                         status=200,
#                         mimetype='application/json')
#
#     def update_visibility(self, project_id, visible):
#         dynamo_result = self._dynamodb.update_visibility(project_id, visible)
#
#         if dynamo_result:
#             return Response(json.dumps({"success": True}),
#                             status=200,
#                             mimetype='application/json')
#         return Response(json.dumps({"success": False}),
#                         status=400,
#                         mimetype='application/json')
#
#     def get_saved_projects(self):
#         result = self._dynamodb_saved_projects.get_saved_projects(self._user_id)
#         if result is False:
#             return Response(status=400, mimetype='application/json')
#
#         items = result.get("Items")
#         projects = []
#         for item in items:
#             item_id = item.get("project_id")
#             project_data = self._dynamodb.get_project(item_id)
#             project = project_data.get("Item")
#             project_picture = self._s3.get_file(f"{item_id}/picture")
#             if project_picture:
#                 project_picture = project_picture.get("Body").read().decode("ascii")
#             else:
#                 project_picture = ""
#
#             projects.append({
#                 "id": item_id,
#                 "title": project.get("title"),
#                 "mainPicture": project_picture,
#                 "author": project.get("user_id"),
#                 "briefDescription": project.get("brief_description"),
#                 "visible": project.get("visible"),
#                 "timestamp": int(project.get("last_timestamp"))
#             })
#         return Response(json.dumps({"projects": projects}),
#                         status=200,
#                         mimetype='application/json')
