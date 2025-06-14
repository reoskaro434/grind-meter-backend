from backend.app.schemas.camel_model import CamelModel


class Plan(CamelModel):
    id: str
    name: str
    exercise_id_list: list[str]
    user_id: str
