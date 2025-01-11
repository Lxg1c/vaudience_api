from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, EmailStr, ConfigDict
from typing_extensions import Annotated


class CreateUser(BaseModel):
    username: Annotated[str, MaxLen(30), MinLen(6)]
    email: EmailStr

class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    password: bytes
    active: bool = True
    email: EmailStr | None = None