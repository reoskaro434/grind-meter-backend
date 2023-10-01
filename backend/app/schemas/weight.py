from pydantic import BaseModel


class Weight(BaseModel):
    mass: float | int
    unit: str
