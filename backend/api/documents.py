from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pathlib import Path
import shutil
import uuid
from datetime import date
from backend.models.document import Document
from backend.database.connection import get_db
from backend.schemas.document import DocumentResponse
from backend.services.document_service import DocumentService
from datetime import date
from backend.utils.email import send_email
from backend.repositories.user_repository import UserRepository
from backend.utils.email_template import build_email_template
router = APIRouter(prefix="/documents", tags=["Documents"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png"}


@router.post("/", response_model=DocumentResponse)
def create_document(
    title: str = Form(...),
    category: str = Form(...),
    expiry_date: Optional[date] = Form(None),
    reminder_days_before: int = Form(30),
    notes: Optional[str] = Form(None),
    user_id: int = Form(...),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    file_url = None

    if file:
        ext = Path(file.filename).suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Only PDF, JPG, JPEG, and PNG files are allowed",
            )

        unique_filename = f"{uuid.uuid4()}{ext}"
        file_path = UPLOAD_DIR / unique_filename

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_url = str(file_path)

    service = DocumentService(db)
    document_data = {
        "title": title,
        "category": category,
        "expiry_date": expiry_date,
        "reminder_days_before": reminder_days_before,
        "file_url": file_url,
        "notes": notes,
        "user_id": user_id,
    }

    doc = service.create_document(document_data)

    return {
        "id": doc.id,
        "title": doc.title,
        "category": doc.category,
        "expiry_date": doc.expiry_date,
        "reminder_days_before": doc.reminder_days_before,
        "file_url": doc.file_url,
        "notes": doc.notes,
        "user_id": doc.user_id,
    }

@router.get("/expired/{user_id}", response_model=List[DocumentResponse])
def get_expired_documents(user_id: int, db: Session = Depends(get_db)):
    service = DocumentService(db)
    return service.get_expired_documents(user_id)


@router.get("/expiring-soon/{user_id}", response_model=List[DocumentResponse])
def get_expiring_soon_documents(user_id: int, db: Session = Depends(get_db)):
    service = DocumentService(db)
    return service.get_expiring_soon_documents(user_id)


@router.delete("/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db)):
    service = DocumentService(db)
    return service.delete_document(document_id)

@router.get("/{user_id}", response_model=List[DocumentResponse])
def get_documents(user_id: int, db: Session = Depends(get_db)):
    return db.query(Document).filter(Document.user_id == user_id).all()

@router.post("/send-alerts/{user_id}")
def send_alerts(user_id: int, db: Session = Depends(get_db)):

    docs = db.query(Document).filter(Document.user_id == user_id).all()

    user_repo = UserRepository(db)
    user = user_repo.get_by_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    today = date.today()

    for doc in docs:
        if not doc.expiry_date:
            continue

        days_left = (doc.expiry_date - today).days

        # 🚫 PREVENT DUPLICATE EMAILS
        if doc.last_alert_sent == today:
            continue

        subject = None
        html = None

        # 📅 ALERT RULES
        if days_left == 7:
            subject = "📅 DocNest Reminder: 7 Days Left"
            html = build_email_template(
                title="📅 Reminder",
                message=f'Your document "<b>{doc.title}</b>" will expire in 7 days.',
                highlight=f"Expiry Date: {doc.expiry_date}"
            )

        elif days_left == 3:
            subject = "⚠️ DocNest Alert: 3 Days Left"
            html = build_email_template(
                title="⚠️ Expiring Soon",
                message=f'Your document "<b>{doc.title}</b>" will expire in 3 days.',
                highlight=f"Expiry Date: {doc.expiry_date}"
            )

        elif days_left == 1:
            subject = "🚨 DocNest Alert: Expires Tomorrow"
            html = build_email_template(
                title="🚨 Final Warning",
                message=f'Your document "<b>{doc.title}</b>" will expire tomorrow.',
                highlight=f"Expiry Date: {doc.expiry_date}"
            )

        elif days_left == 0:
            subject = "❌ DocNest Alert: Expired Today"
            html = build_email_template(
                title="❌ Expired Today",
                message=f'Your document "<b>{doc.title}</b>" has expired today.',
                highlight=f"Expiry Date: {doc.expiry_date}"
            )

        elif days_left == -1:
            subject = "⚠️ DocNest Alert: Expired Yesterday"
            html = build_email_template(
                title="⚠️ Recently Expired",
                message=f'Your document "<b>{doc.title}</b>" expired yesterday.',
                highlight=f"Expiry Date: {doc.expiry_date}"
            )

        elif days_left == -7:
            subject = "📌 DocNest Final Reminder"
            html = build_email_template(
                title="📌 Still Expired",
                message=f'Your document "<b>{doc.title}</b>" is still expired.',
                highlight=f"Expiry Date: {doc.expiry_date}"
            )

        # 📧 SEND EMAIL
        if subject:
            try:
                print(f"📧 Sending alert for {doc.title}")

                send_email(
                    to_email=user.email,
                    subject=subject,
                    html_content=html
                )

                doc.last_alert_sent = today  # ✅ mark sent

            except Exception as e:
                print("Email failed:", e)

    db.commit()

    return {"message": "Alerts checked"}

@router.put("/update/{doc_id}")
def update_document(doc_id: int, data: dict, db: Session = Depends(get_db)):

    doc = db.query(Document).filter(Document.id == doc_id).first()

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    # update fields
    doc.title = data.get("title", doc.title)
    doc.category = data.get("category", doc.category)
    doc.expiry_date = data.get("expiry_date", doc.expiry_date)
    doc.notes = data.get("notes", doc.notes)

    db.commit()
    db.refresh(doc)

    return {"message": "Document updated successfully"}