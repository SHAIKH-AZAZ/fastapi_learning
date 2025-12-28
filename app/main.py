from contextlib import asynccontextmanager
from doctest import master


from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from app.Database.session import create_db_tables  
from app.api import router
from app.api.master_router import master_router 

@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    await create_db_tables()
    yield


app = FastAPI(
    lifespan=lifespan_handler,
)



app.include_router(master_router)

# scaler API documentations
@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )  