import os

from fastapi import HTTPException

from backend.app.aws.dynamodb.user_exercise_dynamodb_provider import UserExerciseDynamodbProvider
from backend.app.schemas.exercise import Exercise
from backend.app.schemas.exercise_id import ExerciseId
from backend.app.schemas.user import User


class UserExerciseController:
    def __init__(self):
        self.__user_exercise_db = UserExerciseDynamodbProvider(
            os.environ.get("REGION", "eu-central-1"),
            os.environ.get("STAGE", "dev"))

    def add_exercise(self, user_exercise: Exercise, user: User):
        return self.__user_exercise_db.add(user.email, user_exercise)

    def get_exercise_page(self, user_id, page):
        items = self.__user_exercise_db.get_exercise_page(user_id, page)
        if items:
            exercise_list = []
            for item in items:
                exercise_list.append({
                    "id": item.get("exercise_id"),
                    "name": item.get("name"),
                    "type": item.get("type"),
                    "state": item.get("exercise_state")
                })
            return exercise_list

        raise HTTPException(status_code=404, detail="No exercises found")

    def set_exercise_active(self, exercise_id: ExerciseId, user: User):
        return self.__user_exercise_db.update_visibility(exercise_id.id, user.email, 'ACTIVE')

    def set_exercise_inactive(self, exercise_id: ExerciseId, user: User):
        return self.__user_exercise_db.update_visibility(exercise_id.id, user.email, 'INACTIVE')

    def get_active_exercises(self, user_id, page):
        items = self.__user_exercise_db.get_exercise_page(user_id, page)
        if items:
            exercise_list = []
            for item in items:
                state = item.get("exercise_state")
                if state == "ACTIVE":
                    exercise_list.append({
                        "id": item.get("exercise_id"),
                        "name": item.get("name"),
                        "type": item.get("type"),
                        "state": state
                    })
            return exercise_list

        raise HTTPException(status_code=404, detail="No exercises found")

    # def get_project(self, project_id):
    #     result = self._dynamodb.get_project(project_id)
    #     if result:
    #         item = result.get("Item")
    #         if item.get("visible") is False:
    #             user = g.get("user")
    #             if user is not None:
    #                 if item.get("user_id") != g.user.get("Username"):
    #                     return Response(status=404, mimetype='application/json')
    #             else:
    #                 return Response(status=404, mimetype='application/json')
    #
    #         item_description = self._s3.get_file(f"{project_id}/description").get("Body").read().decode("ascii")
    #         item_picture = self._s3.get_file(f"{project_id}/picture").get("Body").read().decode("ascii")
    #         project = {
    #             "id": item.get("id"),
    #             "title": item.get("title"),
    #             "description": item_description,
    #             "mainPicture": item_picture,
    #             "author": item.get("user_id"),
    #             "briefDescription": item.get("brief_description"),
    #             "visible": item.get("visible"),
    #             "timestamp": int(item.get("last_timestamp"))
    #         }
    #         return Response(json.dumps(project),
    #                         status=200,
    #                         mimetype='application/json')
    #     return Response(status=404, mimetype='application/json')
    #
    # def delete_project(self, project_id):
    #     dynamodb_result = self._dynamodb.delete_project(project_id)
    #     self._s3.delete_file(f"{project_id}/description")
    #     self._s3.delete_file(f"{project_id}/picture")
    #     s3_result = self._s3.delete_file(f"{project_id}/")
    #
    #     self._dynamodb_saved_projects.delete_all_project_saves(project_id)
    #     self._dynamodb_scores.delete_all_project_scores(project_id)
    #
    #     if dynamodb_result and s3_result:
    #         return Response(json.dumps({"success": True}),
    #                         status=200,
    #                         mimetype='application/json')
    #
    #     return Response(json.dumps({"success": False}),
    #                     status=400,
    #                     mimetype='application/json')




    # def update_project(self, project_data):
    #     response = self._dynamodb.update_project(project_data)
    #
    #     project_id = project_data.get("id")
    #     self._s3.delete_file(f"{project_id}/description")
    #     self._s3.delete_file(f"{project_id}/picture")
    #     self._s3.delete_file(f"{project_id}/")
    #
    #     description = project_data.get("description")
    #     binary_description = io.BytesIO(description.encode("ascii"))
    #     picture = project_data.get("mainPicture")
    #     binary_picture = io.BytesIO(picture.encode("ascii"))
    #     response_description = self._s3.upload_object_file(binary_description, f"{project_id}/description")
    #     response_picture = self._s3.upload_object_file(binary_picture, f"{project_id}/picture")
    #     if response and response_description and response_picture:
    #         return Response(json.dumps({"success": True}),
    #                         status=200,
    #                         mimetype='application/json')
    #
    #     return Response(json.dumps({"success": False}),
    #                     status=400,
    #                     mimetype='application/json')
