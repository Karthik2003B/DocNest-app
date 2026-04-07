from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from database.base import Base
from database.connection import engine

from models.user import User
from models.document import Document

from api.auth import router as auth_router
from api.documents import router as document_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="DocVault API")

app.include_router(auth_router)
app.include_router(document_router)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/")
def root():
    return {"message": "DocVault backend is running"}