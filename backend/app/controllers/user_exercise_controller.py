from fastapi import HTTPException

from backend.app.aws.dynamodb.pynamodb_model.user_exercise import UserExercise
from backend.app.schemas.exercise import Exercise
from backend.app.schemas.exercise_id import ExerciseId
from backend.app.schemas.user import User


class UserExerciseController:

    def add_exercise(self, user_exercise: Exercise, user: User):
        pynamodb_exercise = UserExercise(
            exercise_id=user_exercise.id,
            user_id=user.email,
            name=user_exercise.name,
            type=user_exercise.type,
            exercise_state=user_exercise.state
        )

        pynamodb_exercise.save()

        return True

    def get_exercise_page(self, user_id: str, page: int): # TODO fix pagination
        exercise_list = []
        for item in UserExercise.user_id_index.query(user_id, limit=25):
            exercise_list.append({
                "id": item.exercise_id,
                "name": item.name,
                "type": item.type,
                "state": item.exercise_state
            })

        if not exercise_list:
            raise HTTPException(status_code=404, detail="No exercises found")

        return exercise_list

    def get_exercise(self, user_id: str, exercise_id: str):
        try:
            exercise = UserExercise.get(exercise_id, user_id)
            return Exercise(
                id=exercise.exercise_id,
                name=exercise.name,
                type=exercise.type,
                state=exercise.exercise_state
            )
        except:
            raise HTTPException(status_code=404, detail="No exercises found")

    def set_exercise_active(self, exercise_id: ExerciseId, user: User):
        pynamodb_exercise = UserExercise(
            exercise_id=exercise_id.id,
            user_id=user.email
        )

        pynamodb_exercise.update(actions=[UserExercise.exercise_state.set("ACTIVE")])

        return True

    def set_exercise_inactive(self, exercise_id: ExerciseId, user: User):
        pynamodb_exercise = UserExercise(
            exercise_id=exercise_id.id,
            user_id=user.email
        )

        pynamodb_exercise.update(actions=[UserExercise.exercise_state.set("INACTIVE")])

        return True

    def get_active_exercises(self, user_id, page):
        exercise_list = []
        for item in UserExercise.user_id_index.query(user_id):
            state = item.exercise_state
            if state == "ACTIVE":
                exercise_list.append({
                    "id": item.exercise_id,
                    "name": item.name,
                    "type": item.type,
                    "state": state
                })

        if not exercise_list:
            raise HTTPException(status_code=404, detail="No exercises found")

        return exercise_list
