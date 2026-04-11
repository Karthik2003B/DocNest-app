from sqlalchemy.orm import Session
from database.connection import SessionLocal
from models.document import Document
from repositories.user_repository import UserRepository
from utils.email import send_email
from utils.email_template import build_email_template
from datetime import date


def send_alerts_for_all_users():
    db: Session = SessionLocal()

    try:
        users = db.query(Document.user_id).distinct().all()

        for (user_id,) in users:
            docs = db.query(Document).filter(Document.user_id == user_id).all()

            user_repo = UserRepository(db)
            user = user_repo.get_by_id(user_id)

            if not user:
                continue

            today = date.today()

            for doc in docs:
                if not doc.expiry_date:
                    continue

                days_left = (doc.expiry_date - today).days

                if doc.last_alert_sent == today:
                    continue

                subject = None
                html = None

                if days_left == 7:
                    subject = "📅 DocNest Reminder: 7 Days Left"
                    html = build_email_template(
                        title="📅 Reminder",
                        message=f'{doc.title} will expire in 7 days.',
                        highlight=f"Expiry Date: {doc.expiry_date}"
                    )

                elif days_left == 3:
                    subject = "⚠️ DocNest Alert: 3 Days Left"
                    html = build_email_template(
                        title="⚠️ Expiring Soon",
                        message=f'{doc.title} will expire in 3 days.',
                        highlight=f"Expiry Date: {doc.expiry_date}"
                    )

                elif days_left == 1:
                    subject = "🚨 Expires Tomorrow"
                    html = build_email_template(
                        title="🚨 Final Warning",
                        message=f'{doc.title} will expire tomorrow.',
                        highlight=f"Expiry Date: {doc.expiry_date}"
                    )

                elif days_left == 0:
                    subject = "❌ Expired Today"
                    html = build_email_template(
                        title="❌ Expired Today",
                        message=f'{doc.title} has expired today.',
                        highlight=f"Expiry Date: {doc.expiry_date}"
                    )

                elif days_left == -1:
                    subject = "⚠️ Expired Yesterday"
                    html = build_email_template(
                        title="⚠️ Recently Expired",
                        message=f'{doc.title} expired yesterday.',
                        highlight=f"Expiry Date: {doc.expiry_date}"
                    )

                elif days_left == -7:
                    subject = "📌 Still Expired"
                    html = build_email_template(
                        title="📌 Final Reminder",
                        message=f'{doc.title} is still expired.',
                        highlight=f"Expiry Date: {doc.expiry_date}"
                    )

                if subject:
                    try:
                        send_email(
                            to_email=user.email,
                            subject=subject,
                            html_content=html
                        )
                        doc.last_alert_sent = today
                    except Exception as e:
                        print("Email failed:", e)

        db.commit()

    finally:
        db.close()