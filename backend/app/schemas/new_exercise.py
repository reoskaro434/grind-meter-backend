from pydantic import BaseModel


class NewExercise(BaseModel):
    name: str
    type: str
