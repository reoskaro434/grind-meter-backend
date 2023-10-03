from backend.app.schemas.camel_model import CamelModel


class Exercise(CamelModel):
    id: str
    name: str
    type: str
    is_active: bool
