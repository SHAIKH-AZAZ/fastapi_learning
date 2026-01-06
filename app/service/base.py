
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel
from typing import Generic, Type, TypeVar

ModelType = TypeVar("ModelType", bound=SQLModel)

class BaseService(Generic[ModelType]):
    def __init__(self , model : Type[ModelType] , session: AsyncSession) -> None:
        self.model = model
        self.session = session
        
    
    async def _get(self, id: UUID):
        return await self.session.get( self.model , id)
    
    async def _add(self , entity: ModelType):
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity
    
    async def _update(self , entity: ModelType):
        await self._add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity
    
    async def _delete(self , entity: ModelType):
        await self.session.delete(entity)
        await self.session.commit()