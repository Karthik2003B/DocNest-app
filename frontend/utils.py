import requests
import os
from datetime import date
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
load_dotenv()

BASE_URL = "http://127.0.0.1:8000"

# ================= EMAIL FUNCTION =================
def send_email(to_email, subject, html_content):
    print("📨 send_email CALLED")
    print("TO:", to_email)
    print("SUBJECT:", subject)
    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))

        message = Mail(
            from_email="DocNest Alerts <alerts@docnest.me>",
            to_emails=to_email,
            subject=subject,
            html_content=html_content,
            plain_text_content="Please check your document status in DocNest."
        )

        response = sg.send(message)

        print("STATUS:", response.status_code)

        if response.status_code == 202:
            print("✅ Email sent successfully")
        else:
            print("❌ Email failed")

    except Exception as e:
        print("❌ Error:", e)

# ================= ALERT LOGIC =================
def check_and_send_alerts(docs, user_email):
    print("🔥 ALERT FUNCTION CALLED")
    today = date.today()

    for doc in docs:
        if doc.get("expiry_date"):
            expiry = date.fromisoformat(doc["expiry_date"])
            days_left = (expiry - today).days

            # 🔔 Expiring soon
            if days_left == 3:
                send_email(
                    user_email,
                    "⚠️ DocNest Alert: Expiring Soon",
                    f"<p>{doc['title']} will expire in 3 days.</p>"
                )

            # 🚨 Already expired
            if days_left < 0:
                html_message = f"""
                <html>
                <body style="font-family: Arial; background:#f4f6f8; padding:20px;">
                    <div style="max-width:600px; margin:auto; background:white; padding:20px; border-radius:10px;">
                        <h2 style="color:#0f2740;">📂 DocNest Alert</h2>

                        <p>Hello,</p>

                        <p style="color:#d32f2f; font-weight:bold;">
                            🚨 Your document "<b>{doc['title']}</b>" has expired.
                        </p>

                        <p>📅 Expiry Date: <b>{doc['expiry_date']}</b></p>

                        <p>Please renew it as soon as possible.</p>

                        <hr>

                        <p style="font-size:12px; color:gray;">
                            This is an automated message from DocNest.
                        </p>
                    </div>
                </body>
                </html>
                """

                send_email(
                    user_email,
                    "🚨 DocNest Alert: Document Expired",
                    html_message
                )

def build_file_url(file_path):
    if not file_path:
        return None

    normalized = file_path.replace("\\", "/")

    if normalized.startswith("uploads/"):
        return f"{BASE_URL}/{normalized}"

    filename = os.path.basename(normalized)
    return f"{BASE_URL}/uploads/{filename}"


def fetch_file_bytes(file_path):
    file_url = build_file_url(file_path)
    if not file_url:
        return None, None

    response = requests.get(file_url)
    if response.status_code != 200:
        return None, None

    filename = os.path.basename(file_path.replace("\\", "/"))
    return response.content, filename

def register_user(name, email, password):
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json={"name": name, "email": email, "password": password},
    )
    return response


def login_user(email, password):
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": email, "password": password},
    )
    return response


def create_document(data, file_obj=None):
    files = None
    if file_obj is not None:
        files = {
            "file": (file_obj.name, file_obj, file_obj.type)
        }

    response = requests.post(
        f"{BASE_URL}/documents/",
        data=data,
        files=files
    )
    return response


def get_documents(user_id):
    response = requests.get(f"{BASE_URL}/documents/{user_id}")
    return response


def get_expiring_soon_documents(user_id):
    response = requests.get(f"{BASE_URL}/documents/expiring-soon/{user_id}")
    return response


def get_expired_documents(user_id):
    response = requests.get(f"{BASE_URL}/documents/expired/{user_id}")
    return response


def delete_document(document_id):
    response = requests.delete(f"{BASE_URL}/documents/{document_id}")
    return response

# ================= OTP =================
def verify_otp_api(email, otp):
    return requests.post(
        f"{BASE_URL}/auth/verify-otp",
        params={
            "email": email,
            "otp": otp
        }
    )


# ================= FORGOT PASSWORD =================
def forgot_password_api(email):
    return requests.post(
        f"{BASE_URL}/auth/forgot-password",
        params={"email": email}
    )


def reset_password_api(email, otp, new_password):
    return requests.post(
        f"{BASE_URL}/auth/reset-password",
        params={
            "email": email,
            "otp": otp,
            "new_password": new_password
        }
    )
    
# ================= PASSWORD VALIDATION =================
def get_password_strength(password):
    strength = 0

    if len(password) >= 8:
        strength += 1
    if any(c.isupper() for c in password):
        strength += 1
    if any(c.islower() for c in password):
        strength += 1
    if any(c.isdigit() for c in password):
        strength += 1
    if any(c in "!@#$%^&*()" for c in password):
        strength += 1

    return strength


def validate_password_ui(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not any(c.isupper() for c in password):
        return False, "Must contain uppercase letter"
    if not any(c.islower() for c in password):
        return False, "Must contain lowercase letter"
    if not any(c.isdigit() for c in password):
        return False, "Must contain a number"
    if not any(c in "!@#$%^&*()" for c in password):
        return False, "Must contain special character"

    return True, "Strong password"