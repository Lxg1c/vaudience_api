from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from sqlalchemy import String, Text

from .mixins import UserRelationMixin

if TYPE_CHECKING:
    from .user import User


class Post(UserRelationMixin, Base):
    # _user_id_nullable = False
    # _user_id_unique = False
    _user_back_populates = "posts"
    title: Mapped[str] = mapped_column(
        String(100),
        unique=False,
    )
    body: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )

    user: Mapped["User"] = relationship(back_populates="posts")
