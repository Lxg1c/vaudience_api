import secrets
import uuid
from time import time
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Header, Response, Cookie
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from starlette import status

router = APIRouter(prefix="/demo-auth", tags=["Demo-Auth"])

security = HTTPBasic()


@router.get("/basic-auth")
def demo_basic_auth_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    return {
        "message": "Hi",
        "username": credentials.username,
        "password": credentials.password,
    }


usernames_to_passwords = {
    "admin": "admin",
    "nick": "password",
}

static_auth_token_to_username = {
    "de884cf9e1188b64c6e3d89667d4bd78": "admin",
    "cee6e2f0aaf817ffeb21f0edc8b4afe7": "john",
}


def get_username_by_static_token(
    static_token: str = Header(alias="static-auth-token"),
) -> str:
    # Вариант 1
    if username := static_auth_token_to_username.get(static_token):
        return username
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid static auth token",
    )

    # Вариант 2
    # if static_token not in static_auth_token_to_username:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid static token",
    #     )
    #
    # return static_auth_token_to_username[static_token]


def get_auth_user_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    unauth_exp = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Basic"},
    )

    correct_password = usernames_to_passwords.get(credentials.username)
    if not correct_password:
        raise unauth_exp

    if credentials.username not in usernames_to_passwords:
        raise unauth_exp

    if not secrets.compare_digest(
        credentials.password.encode("utf-8"),
        correct_password.encode("utf-8"),
    ):
        raise unauth_exp

    return credentials.username


@router.get("/basic-auth-username")
def demo_basic_auth_username(
    auth_username: str = Depends(get_auth_user_username),
):
    return {
        "message": "Hi",
        "username": auth_username,
    }


@router.get("/some-https-header-auth")
def demo_auth_some_http_header(username: str = Depends(get_username_by_static_token)):
    return {
        "message": f"Hi, {username}!",
        "username": username,
    }


COOKIES: dict[str, dict[str, any]] = {}

COOKIE_SESSION_ID_KEY = "web-app-session-id"


def generate_session_id():
    return uuid.uuid4().hex


def get_session_data(session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY)):
    if session_id not in COOKIES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    return COOKIES[session_id]


@router.post("/login/cookie")
def demo_auth_login_cookie(
    response: Response,
    auth_username: str = Depends(get_auth_user_username),
    # username: str = Depends(get_username_by_static_token)
):

    session_id = generate_session_id()
    COOKIES[session_id] = {
        "username": auth_username,
        "login_at": int(time()),
    }
    response.set_cookie(COOKIE_SESSION_ID_KEY, session_id)
    return {"message": "ok"}


@router.get("/check-cookie")
def demo_auth_check_cookie(
    user_session_data: dict = Depends(get_session_data),
):
    username = user_session_data["username"]
    return {
        "message": f"Hi, {username}!",
        "username": username,
    }


@router.get("/logout-cookie")
def demo_auth_check_cookie(
    response: Response,
    session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
    user_session_data: dict = Depends(get_session_data),
):
    COOKIES.pop(session_id)
    response.delete_cookie(COOKIE_SESSION_ID_KEY)
    username = user_session_data["username"]
    return {
        "message": f"Bye, {username}!",
    }
