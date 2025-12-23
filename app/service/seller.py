from warnings import deprecated
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from passlib.context import CryptContext
from app.Database.models import Seller
from app.api.schema.seller import SellerCreate

password_context = CryptContext(schemes=["argon2"], deprecated="auto")

class SellerService:
    def __init__(self , session : AsyncSession) -> None:
        # get database session to perform database operations 
        self.session = session
    
    async def add(self , credentials : SellerCreate)-> Seller:
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
    
    async def token(self , email , password):
        # validate credentials \
        result  = await self.session.execute(
            select(Seller).where(Seller.email == email)
        )
        seller = result.scalar()
        if seller is None or password_context.verify(password , seller.password_hash):
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Seller Email or Password is Incorrect")
        # verified seller 
        
        