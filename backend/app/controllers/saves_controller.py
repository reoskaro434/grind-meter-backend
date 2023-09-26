# import json
# import os
#
# from flask import Response, g
#
# from backend.aws.dynamodb.saves_dynamodb_provider import SavedProjectsDynamodbProvider
# from backend.aws.dynamodb.scores_dynamodb_provider import ScoresDynamodbProvider
#
#
# class SavedProjectsController:
#     def __init__(self):
#         self._dynamodb_saved_projects = SavedProjectsDynamodbProvider(
#             os.environ.get("REGION", "eu-central-1"),
#             os.environ.get("STAGE", "dev"))
#
#     def save_project(self, project_id):
#         user_id = g.user.get("Username")
#         result = self._dynamodb_saved_projects.save_project(user_id, project_id)
#         if result:
#             return Response(json.dumps({"success": result}), status=200, mimetype='application/json')
#         return Response(status=400, mimetype='application/json')
#
#     def delete_save(self, project_id):
#         user_id = g.user.get("Username")
#         result = self._dynamodb_saved_projects.delete_save(user_id, project_id)
#         if result:
#             return Response(json.dumps({"success": result}), status=200, mimetype='application/json')
#         return Response(status=400, mimetype='application/json')
#
#     def count_saves(self, project_id):
#         scores = self._dynamodb_saved_projects.count_saves(project_id)
#         if scores is not False:
#             return Response(json.dumps({"saves": scores}),
#                             status=200,
#                             mimetype='application/json')
#         return Response(status=404, mimetype='application/json')
#
#     def get_saved_status(self, project_id):
#         user_id = g.user.get("Username")
#         result = self._dynamodb_saved_projects.is_saved(user_id, project_id)
#         return Response(json.dumps({"saved": result}),
#                         status=200,
#                         mimetype='application/json')
