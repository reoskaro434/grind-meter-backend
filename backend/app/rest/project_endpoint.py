# import json
#
# from flask import Blueprint, request
#
# from backend.controllers.project_controller import ProjectController
# from backend.decorators import require_authentication, possible_authentication
#
# project = Blueprint("project", __name__)
#
#
# @project.route("/project", methods=["GET"])
# @possible_authentication
# def project_endpoint():
#     project_id = request.args.get("id")
#     return ProjectController().get_project(project_id)
#
#
# @project.route('/project', methods=["POST"])
# @require_authentication
# def add_project_endpoint():
#     decoded_data = request.data.decode()
#     decoded_data = json.loads(decoded_data)
#     project_data = decoded_data.get("projectData")
#     return ProjectController().add_project(project_data)
#
#
# @project.route('/project', methods=["DELETE"])
# @require_authentication
# def delete_project_endpoint():
#     decoded_data = request.data.decode()
#     decoded_data = json.loads(decoded_data)
#     project_id = decoded_data.get("projectId")
#     return ProjectController().delete_project(project_id)
#
#
# @project.route('/projects', methods=["GET"])
# def get_project_page():
#     page = request.args.get("page")
#     return ProjectController().get_projects_page(int(page))
#
#
# @project.route('/project/update', methods=["POST"])
# @require_authentication
# def update_project():
#     decoded_data = request.data.decode()
#     decoded_data = json.loads(decoded_data)
#     project_data = decoded_data.get("projectData")
#     return ProjectController().update_project(project_data)
