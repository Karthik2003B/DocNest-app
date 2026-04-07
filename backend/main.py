from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.database.base import Base
from backend.database.connection import engine

from backend.models.user import User
from backend.models.document import Document

from backend.api.auth import router as auth_router
from backend.api.documents import router as document_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="DocVault API")

app.include_router(auth_router)
app.include_router(document_router)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/")
def root():
    return {"message": "DocVault backend is running"}