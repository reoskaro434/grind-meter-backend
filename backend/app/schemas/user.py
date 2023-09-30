from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserAuthorized(UserBase):
    access_token: str

