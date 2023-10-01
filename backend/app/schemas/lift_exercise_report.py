from typing import List

from pydantic import BaseModel

from backend.app.schemas.exercise import Exercise
from backend.app.schemas.exercise_set import ExerciseSet


class LiftExerciseReport(BaseModel):
    exercise: Exercise
    sets: List[ExerciseSet]
    timestamp: int
