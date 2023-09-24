# import json
#
# from flask import Blueprint, request
#
# from backend.controllers.user_profile_controller import UserProfileController
# from backend.decorators import require_authentication
#
# user_profile = Blueprint('user_profile', __name__)
#
#
# @user_profile.route('/user-profile', methods=["GET"])
# @require_authentication
# def user_profile_endpoint():
#     return UserProfileController().get_all_projects()
#
#
# @user_profile.route('/user-profile/update-visibility', methods=["POST"])
# @require_authentication
# def update_visibility():
#     decoded_data = request.data.decode()
#     decoded_data = json.loads(decoded_data)
#     project_id = decoded_data.get("projectId")
#     visible = decoded_data.get("visible")
#     return UserProfileController().update_visibility(project_id, visible)
#
#
# @user_profile.route("/user-profile/get-saved-projects", methods=["GET"])
# @require_authentication
# def get_saved_projects():
#     return UserProfileController().get_saved_projects()
