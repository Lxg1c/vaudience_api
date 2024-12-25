from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, EmailStr
from typing_extensions import Annotated


class CreateUser(BaseModel):
    username: Annotated[str, MaxLen(30), MinLen(6)]
    email: EmailStr
