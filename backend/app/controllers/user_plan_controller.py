from typing import List

from fastapi import HTTPException
from pynamodb.exceptions import DoesNotExist

from backend.app.aws.dynamodb.pynamodb_model.user_exercise import UserExercise
from backend.app.aws.dynamodb.pynamodb_model.user_plan import UserPlan
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
            name=user_plan.name
        )

        pynamodb_exercise.save()

        return True

    def get_plans_for_account(self, user_id: str):
        plan_list = []
        for item in UserPlan.user_id_index.query(user_id, limit=self.MAX_PLANS_PER_ACCOUNT):
            plan_list.append({
                "id": item.plan_id,
                "name": item.name
            })

        if not plan_list:
            raise HTTPException(status_code=404, detail="No plans found")

        return plan_list

    def save_exercises(self, user_id: str, plan_id: str, exercise_id_list: List[str]):
        plan = UserPlan(plan_id, user_id)

        plan.update(actions=[UserPlan.exercise_id_list.set(exercise_id_list)])

        return True

    def get_exercises(self, user_id: str, plan_id: str):
        plan = UserPlan.get(plan_id, user_id)
        exercises = []
        exercise_id_list = plan.exercise_id_list

        for exercise_id in exercise_id_list:
            try:
                item = UserExercise.get(exercise_id, user_id)

                exercises.append({
                    "id": item.exercise_id,
                    "name": item.name,
                    "type": item.type
                })
            except DoesNotExist:  # Might be raised when user deleted exercise
                print("Item does not exists", exercise_id, user_id)

        return exercises

    def get_exercises_id(self, user_id: str, plan_id: str):
        plan = UserPlan.get(plan_id, user_id)

        return plan.exercise_id_list

    def rename(self, plan_id, email, name):
        plan = UserPlan(plan_id, email)

        plan.update(actions=[UserPlan.name.set(name)])

        return True

    def delete(self, plan_id, email):
        UserPlan.get(plan_id, email).delete()

        return True

    def get_plan(self, email, plan_id):
        plan = UserPlan.get(plan_id, email)

        if plan:
            return {
                "planId": plan.plan_id,
                "name": plan.name,
                "exerciseIdList": plan.exercise_id_list,
                "userId": plan.user_id
            }

        return None
