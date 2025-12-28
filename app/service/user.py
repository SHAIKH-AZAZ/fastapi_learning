from typing import Type
from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.Database.models import User
from app.service.base import BaseService
from app.utils import generate_access_token


password_context = CryptContext(schemes=["argon2"], deprecated="auto")


class UserService(BaseService):
    def __init__(self, model: Type[User], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def _get_by_email(self, email) -> User | None:
        return await self.session.scalar(
            select(self.model).where(self.model.email == email)
        )

    async def _add_user(self , data: dict):
        user = self.model(
            **data,
            password_hash=password_context.hash(data["password"]),
        )
        return await self._add(user)

    async def _generate_token(self, email, password):
        # validate the credentials
        user = await self._get_by_email(email)

        if user is None or not password_context.verify(
            password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        return generate_access_token(
            data={
                "user": {
                    "name": user.name,
                    "id": str(user.id),
                }
            }
        )
        
