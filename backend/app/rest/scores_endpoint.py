# import json
#
# from flask import Blueprint, request
#
# from backend.controllers.scores_controller import ScoresController
# from backend.decorators import require_authentication
#
# scores = Blueprint("scores", __name__)
#
#
# @scores.route("/scores/get-scores", methods=["GET"])
# def get_scores_endpoint():
#     project_id = request.args.get("projectId")
#     return ScoresController().get_scores(project_id)
#
#
# @scores.route("/scores/add-score", methods=["POST"])
# @require_authentication
# def add_scores_endpoint():
#     decoded_data = request.data.decode()
#     decoded_data = json.loads(decoded_data)
#     project_id = decoded_data.get("projectId")
#     return ScoresController().add_score(project_id)
#
#
# @scores.route("/scores/delete-score", methods=["DELETE"])
# @require_authentication
# def delete_scores_endpoint():
#     project_id = request.args.get("projectId")
#     return ScoresController().delete_score(project_id)
#
#
# @scores.route("/scores/get-scored-status", methods=["GET"])  # is scoreD not scorE
# @require_authentication
# def get_scored_status():
#     project_id = request.args.get("projectId")
#     return ScoresController().get_scored_status(project_id)
