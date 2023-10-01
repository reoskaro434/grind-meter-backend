from pydantic import BaseModel

from backend.app.schemas.weight import Weight


class ExerciseSet(BaseModel):
    repetitions: int
    weight: Weight
    index: int

