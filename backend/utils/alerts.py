import requests
import os
from datetime import date
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

BASE_URL = "https://docnest-app.onrender.com"
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))# loads .env file

# ================= EMAIL FUNCTION =================
def send_email(to_email, subject, html_content):
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

def verify_otp_api(email, otp):
    return requests.post(
        f"{BASE_URL}/auth/verify-otp",
        json={"email": email, "otp": otp}
    )
    
# ================= ALERT LOGIC =================
def check_and_send_alerts(docs, user_email):
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
                html_content = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
    @media only screen and (max-width: 600px) {{
        .inner-body {{ width: 100% !important; }}
        .footer {{ width: 100% !important; }}
    }}
</style>
</head>
<body style="margin:0; padding:0; background-color:#f4f7fa; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; -webkit-font-smoothing:antialiased;">

<table width="100%" border="0" cellpadding="0" cellspacing="0" style="background-color:#f4f7fa; padding: 40px 0;">
    <tr>
        <td align="center">
            
            <table class="inner-body" width="600" border="0" cellpadding="0" cellspacing="0" style="background-color:#ffffff; border-radius:12px; overflow:hidden; border: 1px solid #e1e8f0;">
                
                <tr>
                    <td style="background-color:#0f172a; padding: 40px 20px; text-align: center;">
                        <span style="font-size: 24px; font-weight: 800; color: #ffffff; letter-spacing: -0.5px; display: inline-block;">
                           📂 DocNest
                        </span>
                    </td>
                </tr>

                <tr>
                    <td style="padding: 40px 50px;">
                        <h1 style="color:#1e293b; font-size:22px; font-weight:700; margin:0 0 20px; text-align:left;">
                            Document Expiry Alert
                        </h1>
                        
                        <p style="color:#475569; font-size:16px; line-height:1.6; margin:0 0 30px;">
                            Hello, <br><br>
                            This is a courtesy notification from your <strong>DocNest Vault</strong>. Our system has identified a document that requires your immediate attention to maintain compliance and access.
                        </p>

                        <table width="100%" border="0" cellpadding="0" cellspacing="0" style="background-color:#f8fafc; border-radius:10px; border: 1px solid #cbd5e1; margin-bottom: 30px;">
                            <tr>
                                <td style="padding: 25px;">
                                    <table width="100%" border="0" cellpadding="0" cellspacing="0">
                                        <tr>
                                            <td style="color:#64748b; font-size:12px; text-transform:uppercase; font-weight:700; letter-spacing:1px; padding-bottom:5px;">Document Name</td>
                                        </tr>
                                        <tr>
                                            <td style="color:#1e293b; font-size:18px; font-weight:600;">{doc['title']}</td>
                                        </tr>
                                        <tr>
                                            <td style="padding-top:15px; color:#64748b; font-size:12px; text-transform:uppercase; font-weight:700; letter-spacing:1px; padding-bottom:5px;">Status</td>
                                        </tr>
                                        <tr>
                                            <td style="color:#ef4444; font-size:16px; font-weight:700;">Expired on {doc['expiry_date']}</td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>

                        <table width="100%" border="0" cellpadding="0" cellspacing="0">
                            <tr>
                                <td align="center" style="padding-bottom: 30px;">
                                    <a href="https://docnest.me/dashboard" style="background-color:#3b82f6; color:#ffffff; padding:16px 32px; border-radius:8px; font-weight:700; text-decoration:none; font-size:15px; display:inline-block; box-shadow: 0 4px 6px rgba(59, 130, 246, 0.2);">
                                        Renew in Dashboard
                                    </a>
                                </td>
                            </tr>
                        </table>

                        <p style="color:#94a3b8; font-size:13px; line-height:1.5; text-align:center;">
                            If you have already renewed this document, please update the details in your vault to dismiss this alert.
                        </p>
                    </td>
                </tr>

                <tr>
                    <td style="background-color:#f8fafc; padding: 30px 50px; border-top: 1px solid #e2e8f0; text-align: center;">
                        <p style="color:#64748b; font-size:12px; margin:0;">
                            &copy; 2026 DocNest | Secure Document Intelligence<br>
                            You received this because you enabled expiry tracking.
                        </p>
                    </td>
                </tr>
            </table>

        </td>
    </tr>
</table>

</body>
</html>
"""

                send_email(
                    user_email,
                    " DocNest Alert: Document Expired",
                    html_content
                )


# ================= FILE HANDLING =================
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


# ================= AUTH =================
def register_user(name, email, password):
    return requests.post(
        f"{BASE_URL}/auth/register",
        json={"name": name, "email": email, "password": password},
    )


def login_user(email, password):
    return requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": email, "password": password},
    )


# ================= DOCUMENT APIs =================
def create_document(data, file_obj=None):
    files = None
    if file_obj:
        files = {"file": (file_obj.name, file_obj, file_obj.type)}

    return requests.post(
        f"{BASE_URL}/documents/",
        data=data,
        files=files
    )


def get_documents(user_id):
    return requests.get(f"{BASE_URL}/documents/{user_id}")


def get_expiring_soon_documents(user_id):
    return requests.get(f"{BASE_URL}/documents/expiring-soon/{user_id}")


def get_expired_documents(user_id):
    return requests.get(f"{BASE_URL}/documents/expired/{user_id}")


def delete_document(document_id):
    return requests.delete(f"{BASE_URL}/documents/{document_id}")
