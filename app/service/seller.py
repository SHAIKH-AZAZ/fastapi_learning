from sqlalchemy.ext.asyncio import AsyncSession

from passlib.context import CryptContext
from app.Database.models import Seller
from app.api.schema.seller import SellerCreate
from app.service.user import UserService

password_context = CryptContext(schemes=["argon2"], deprecated="auto")


class SellerService(UserService):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Seller, session)

    async def add(self, seller_create: SellerCreate) -> Seller:
        # TODO: Debugging statements to inspect password details
        print("PASSWORD VALUE:", seller_create.password)
        print("PASSWORD TYPE:", type(seller_create.password))
        print("PASSWORD BYTES:", seller_create.password.encode())
        print("PASSWORD BYTE LEN:", len(seller_create.password.encode()))

        return await self._add_user(
            seller_create.model_dump(),
        )

    async def token(self, email, password) -> str :
        return await self._generate_token(email , password)
