from fastapi import HTTPException

from backend.app.aws.dynamodb.pynamodb_model.user_exercise import UserExercise
from backend.app.schemas.exercise import Exercise
from backend.app.schemas.exercise_id import ExerciseId
from backend.app.schemas.user import User


class UserExerciseController:
    MAX_EXERCISES_PER_ACCOUNT = 50

    def add_exercise(self, user_exercise: Exercise, user: User):
        item_len = len(
            [item for item in UserExercise.user_id_index.query(user.email, limit=self.MAX_EXERCISES_PER_ACCOUNT)])

        if item_len >= self.MAX_EXERCISES_PER_ACCOUNT:
            raise HTTPException(status_code=403,
                                detail=f"Max exercises per account reached ({self.MAX_EXERCISES_PER_ACCOUNT})")

        pynamodb_exercise = UserExercise(
            exercise_id=user_exercise.id,
            user_id=user.email,
            name=user_exercise.name,
            type=user_exercise.type
        )

        pynamodb_exercise.save()

        return True

    def get_exercise_page(self, user_id: str):
        exercise_list = []
        for item in UserExercise.user_id_index.query(user_id, limit=self.MAX_EXERCISES_PER_ACCOUNT):
            exercise_list.append({
                "id": item.exercise_id,
                "name": item.name,
                "type": item.type
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

    def rename(self, exercise_id: str, email: str, name: str):
        pynamodb_exercise = UserExercise(
            exercise_id=exercise_id,
            user_id=email
        )

        pynamodb_exercise.update(actions=[UserExercise.name.set(name)])

        return True
