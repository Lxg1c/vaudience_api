from fastapi import APIRouter
from app.users.schemas import CreateUser
import crud

router = APIRouter(prefix="/users", tags=["Auth"])


@router.post("/register")
async def create_user(user: CreateUser):
    return crud.create_user(user)
