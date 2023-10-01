from pydantic import BaseModel


class Exercise(BaseModel):
    id: str
    name: str
    type: str


