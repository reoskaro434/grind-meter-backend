from typing import List, Optional

from pydantic import BaseModel

from backend.app.schemas.camel_model import CamelModel
from backend.app.schemas.exercise import Exercise
from backend.app.schemas.exercise_set import ExerciseSet


class LiftExerciseReport(CamelModel):
    exercise_id: str
    report_id: Optional[str]
    sets: List[ExerciseSet]
    timestamp: Optional[int]
