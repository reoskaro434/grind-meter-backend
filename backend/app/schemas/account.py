from backend.app.schemas.camel_model import CamelModel


class Account(CamelModel):
    user_id: str
    monday: str
    tuesday: str
    wednesday: str
    thursday: str
    friday: str
    saturday: str
    sunday: str
