from fastapi import APIRouter
from users.schemas import CreateUser
import users.crud as crud

router = APIRouter(prefix="/users", tags=["Auth"])


@router.post("/register")
async def create_user(user: CreateUser):
    return crud.create_user(user)
