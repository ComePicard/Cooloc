from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    email: str | None = None
    adress: str | None = None
    phone_number: str | None = None
