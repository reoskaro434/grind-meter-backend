from backend.app.schemas.camel_model import CamelModel


class Plan(CamelModel):
    id: str
    name: str
    state: str
