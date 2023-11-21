from typing import List

from backend.app.schemas.camel_model import CamelModel


class SaveExercisesModel(CamelModel):
    exercise_id_list: List[str]
    plan_id: str
