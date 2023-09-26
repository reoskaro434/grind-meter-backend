# import json
#
# from flask import Blueprint, request
#
# from backend.controllers.saves_controller import SavedProjectsController
# from backend.decorators import require_authentication
#
# saves = Blueprint("saves", __name__)
#
#
# @saves.route("/saves/get-saves", methods=["GET"])
# def get_saves_endpoint():
#     project_id = request.args.get("projectId")
#     return SavedProjectsController().count_saves(project_id)
#
#
# @saves.route("/saves/save-project", methods=["POST"])
# @require_authentication
# def save_project_endpoint():
#     decoded_data = request.data.decode()
#     decoded_data = json.loads(decoded_data)
#     project_id = decoded_data.get("projectId")
#     return SavedProjectsController().save_project(project_id)
#
#
# @saves.route("/saves/delete-saved-project", methods=["DELETE"])
# @require_authentication
# def delete_saved_project_endpoint():
#     project_id = request.args.get("projectId")
#     return SavedProjectsController().delete_save(project_id)
#
#
# @saves.route("/saves/get-save-status", methods=["GET"])
# @require_authentication
# def get_save_status():
#     project_id = request.args.get("projectId")
#     return SavedProjectsController().get_saved_status(project_id)
