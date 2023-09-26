# import json
# import os
#
# from flask import Response, g
#
# from backend.aws.dynamodb.scores_dynamodb_provider import ScoresDynamodbProvider
#
#
# class ScoresController:
#     def __init__(self):
#         self._dynamodb_scores = ScoresDynamodbProvider(
#             os.environ.get("REGION", "eu-central-1"),
#             os.environ.get("STAGE", "dev"))
#
#     def get_scores(self, project_id):
#         scores = self._dynamodb_scores.count_scores(project_id)
#         if scores is not False:
#             return Response(json.dumps({"scores": scores}),
#                             status=200,
#                             mimetype='application/json')
#         return Response(status=404, mimetype='application/json')
#
#     def add_score(self, project_id):
#         user_id = g.user.get("Username")
#         result = self._dynamodb_scores.add_score(user_id, project_id)
#         if result:
#             return Response(json.dumps({"success": result}), status=200, mimetype='application/json')
#         return Response(status=400, mimetype='application/json')
#
#     def delete_score(self, project_id):
#         user_id = g.user.get("Username")
#         result = self._dynamodb_scores.delete_score(user_id, project_id)
#         if result:
#             return Response(json.dumps({"success": result}), status=200, mimetype='application/json')
#         return Response(status=400, mimetype='application/json')
#
#     def get_scored_status(self, project_id):
#         user_id = g.user.get("Username")
#         result = self._dynamodb_scores.is_scored(user_id, project_id)
#         return Response(json.dumps({"scored": result}),
#                         status=200,
#                         mimetype='application/json')
