from typing import List

from fastapi import HTTPException

from backend.app.aws.dynamodb.pynamodb_model.user_exercise import UserExercise
from backend.app.aws.dynamodb.pynamodb_model.user_plan import UserPlan
from backend.app.schemas.exercise import Exercise
from backend.app.schemas.exercise_id import ExerciseId
from backend.app.schemas.plan import Plan
from backend.app.schemas.user import User


class UserPlanController:
    MAX_PLANS_PER_ACCOUNT = 5

    def add_plan(self, user_plan: Plan, user: User):
        item_len = len([item for item in UserPlan.user_id_index.query(user.email, limit=self.MAX_PLANS_PER_ACCOUNT)])

        if item_len >= self.MAX_PLANS_PER_ACCOUNT:
            raise HTTPException(status_code=403, detail=f"Max plans per account reached ({self.MAX_PLANS_PER_ACCOUNT})")

        pynamodb_exercise = UserPlan(
            plan_id=user_plan.id,
            user_id=user.email,
            name=user_plan.name,
            plan_state=user_plan.state
        )

        pynamodb_exercise.save()

        return True

    def get_plan_page(self, user_id: str, page: int): # TODO fix pagination
        plan_list = []
        for item in UserPlan.user_id_index.query(user_id, limit=self.MAX_PLANS_PER_ACCOUNT):
            plan_list.append({
                "id": item.plan_id,
                "name": item.name,
                "state": item.plan_state
            })

        if not plan_list:
            raise HTTPException(status_code=404, detail="No plans found")

        return plan_list

    def save_exercises(self, user_id: str, plan_id: str, exercises_list: List[str]):
        print(user_id)
        print(plan_id)
        print(exercises_list)

    # def get_exercise(self, user_id: str, exercise_id: str):
    #     try:
    #         exercise = UserExercise.get(exercise_id, user_id)
    #         return Exercise(
    #             id=exercise.exercise_id,
    #             name=exercise.name,
    #             type=exercise.type,
    #             state=exercise.exercise_state
    #         )
    #     except:
    #         raise HTTPException(status_code=404, detail="No exercises found")
    #
    # def set_exercise_active(self, exercise_id: ExerciseId, user: User):
    #     pynamodb_exercise = UserExercise(
    #         exercise_id=exercise_id.id,
    #         user_id=user.email
    #     )
    #
    #     pynamodb_exercise.update(actions=[UserExercise.exercise_state.set("ACTIVE")])
    #
    #     return True
    #
    # def set_exercise_inactive(self, exercise_id: ExerciseId, user: User):
    #     pynamodb_exercise = UserExercise(
    #         exercise_id=exercise_id.id,
    #         user_id=user.email
    #     )
    #
    #     pynamodb_exercise.update(actions=[UserExercise.exercise_state.set("INACTIVE")])
    #
    #     return True
    #
    # def get_active_exercises(self, user_id, page):
    #     exercise_list = []
    #     for item in UserExercise.user_id_index.query(user_id):
    #         state = item.exercise_state
    #         if state == "ACTIVE":
    #             exercise_list.append({
    #                 "id": item.exercise_id,
    #                 "name": item.name,
    #                 "type": item.type,
    #                 "state": state
    #             })
    #
    #     if not exercise_list:
    #         raise HTTPException(status_code=404, detail="No exercises found")
    #
    #     return exercise_list
