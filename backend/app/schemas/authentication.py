from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    client_id: int
