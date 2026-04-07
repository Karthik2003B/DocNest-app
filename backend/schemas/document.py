from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class DocumentCreate(BaseModel):
    title: str
    category: str
    expiry_date: Optional[date] = None
    reminder_days_before: int = 30
    file_url: Optional[str] = None
    notes: Optional[str] = None
    user_id: int


class DocumentResponse(BaseModel):
    id: int
    title: str
    category: str
    expiry_date: Optional[date] = None
    reminder_days_before: int
    file_url: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True