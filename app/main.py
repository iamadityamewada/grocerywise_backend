from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1.api import api_router


# Create database tables if they don't exist (for development/simple setups)
# For production, prefer using Alembic migrations
# Base.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
# In production, restrict this to your frontend's domain

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # <-- should be a list, not a function!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}

# Include the API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# You might want to add global exception handlers here later
