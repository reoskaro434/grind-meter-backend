from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str


class UserAuthorized(User):
    access_token: str

