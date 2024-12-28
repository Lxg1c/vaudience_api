import asyncio

from sqlalchemy.engine import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.products.crud import get_products
from core.models import db_helper, User, Profile, Post
from sqlalchemy.orm import joinedload, selectinload


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    statement = select(User).where(User.username == username)
    # result: Result = await session.execute(statement)
    # user: User | None = result.scalar_one_or_none()
    # user: User | None = result.scalar_one()
    user: User | None = await session.scalar(statement)
    print("Found user", username, user)
    return user


async def create_user_profile(
    session: AsyncSession,
    user_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
) -> Profile:
    profile = Profile(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
    )
    session.add(profile)
    await session.commit()
    return profile


async def show_users_with_profiles(session: AsyncSession):
    # Создаем запрос с загрузкой профиля
    statement = select(User).options(joinedload(User.profile)).order_by(User.id)

    # Выполняем запрос и получаем результаты
    users = await session.scalars(statement)

    # Обрабатываем каждого пользователя
    for user in users:
        print(user)
        if user.profile is not None:  # Проверяем, существует ли профиль
            print(user.profile.first_name)
        else:
            print("Имя не определено")


async def create_posts(
    session: AsyncSession,
    user_id: int,
    posts_titles: list[str],
) -> list[Post]:
    posts = [Post(title=title, user_id=user_id) for title in posts_titles]
    session.add_all(posts)
    await session.commit()
    print(posts)
    return posts


async def get_users_with_posts(session: AsyncSession):
    # Лучший вариант
    stmnt = select(User).options(selectinload(User.posts)).order_by(User.id)
    result: Result = await session.execute(stmnt)
    users = result.scalars()

    for user in users:
        print("**" * 10)
        print(user)
        for post in user.posts:
            print("-", post)

    # Еще один способ
    # stmt = select(User).options(joinedload(User.posts)).order_by(User.id)
    # result: Result = await session.execute(stmt)
    # users = result.unique().scalars()
    #
    # for user in users:
    #     print("**" * 10)
    #     print(user)
    #     for post in user.posts:
    #         print("-", post)

    # Другой способ
    # stmt = select(User).options(joinedload(User.posts)).order_by(User.id)
    # users = await session.scalars(stmt)
    #
    # for user in users.unique():
    #     print("**" * 10)
    #     print(user)
    #     for post in user.posts:
    #         print("-", post)


async def get_users_with_posts_and_profiles(session: AsyncSession):
    # Лучший вариант
    stmnt = (
        select(User)
        .options(joinedload(User.profile), selectinload(User.posts))
        .order_by(User.id)
    )

    users = await session.scalars(stmnt)

    for user in users:
        print("**" * 10)
        print(user)
        print("--" * 10)
        print(user.profile and user.profile.first_name)
        for post in user.posts:
            print("-", post)


async def get_posts_with_authors(session: AsyncSession):
    stmnt = select(Post).options(joinedload(Post.user)).order_by(Post.id)
    posts = await session.scalars(stmnt)

    for post in posts:
        print("Post: ", post, "***Author: ", post.user_id)


async def get_profiles_with_users_and_users_with_posts(
    session: AsyncSession,
):
    stmnt = (
        select(Profile)
        .options(joinedload(Profile.user).selectinload(User.posts))
        .order_by(Profile.id)
    )

    profiles = await session.scalars(stmnt)

    for profile in profiles:
        print(profile.first_name, profile.user)
        print(profile.user.posts)


async def main():
    async with db_helper.session_factory() as session:
        # await create_user(session=session, username="Nick")
        # await create_user(session=session, username="John")
        user_nick = await get_user_by_username(session=session, username="Nick")
        # await get_user_by_username(session=session, username="Bob")
        # await create_user_profile(
        #     session=session, user_id=user_nick.id, first_name="John", last_name="Doe"
        # )
        # await show_users_with_profiles(session=session)
        # await create_posts(
        #     session=session,
        #     user_id=user_nick.id,
        #     posts_titles=["FastApi for Beginners", "FastApi Advanced", "FastApi Pro"],
        # )

        # await get_users_with_posts(session=session)

        # await get_posts_with_authors(session=session)

        # await get_users_with_posts_and_profiles(session=session)

        await get_profiles_with_users_and_users_with_posts(session=session)


if __name__ == "__main__":
    asyncio.run(main())
