import datetime
from fastapi import HTTPException, status
import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import security_settings
from passlib.context import CryptContext
from app.Database.models import Seller
from app.api.schema.seller import SellerCreate
from app.utils import generate_access_token

password_context = CryptContext(schemes=["argon2"], deprecated="auto")


class SellerService:
    def __init__(self, session: AsyncSession) -> None:
        # get database session to perform database operations
        self.session = session

    async def add(self, credentials: SellerCreate) -> Seller:
        print("PASSWORD VALUE:", credentials.password)
        print("PASSWORD TYPE:", type(credentials.password))
        print("PASSWORD BYTES:", credentials.password.encode())
        print("PASSWORD BYTE LEN:", len(credentials.password.encode()))

        seller = Seller(
            **credentials.model_dump(),
            password_hash=password_context.hash(credentials.password)
        )
        self.session.add(seller)
        await self.session.commit()
        await self.session.refresh(seller)

        return seller

    async def token(self, email, password) -> str | HTTPException:
        # validate credentials \
        result = await self.session.execute(select(Seller).where(Seller.email == email))
        
        
        seller = result.scalar()
        
        if seller is None or not password_context.verify(
            password, seller.password_hash
        ):
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Seller Email or Password is Incorrect",
            )

        token = generate_access_token(
            data={
                "user": {
                    "name": seller.name,
                    "id": str(seller.id),
                }
            }
        )

        return token
