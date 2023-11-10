from typing import List, Optional

from pydantic import BaseModel

from backend.app.schemas.exercise import Exercise
from backend.app.schemas.exercise_set import ExerciseSet


class LiftExerciseReport(BaseModel):
    exercise: Optional[Exercise]
    sets: List[ExerciseSet]
    timestamp: Optional[int]
