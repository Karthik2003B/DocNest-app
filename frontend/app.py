import streamlit as st
from pathlib import Path
import base64
from frontend.utils import (check_and_send_alerts)
BASE_DIR = Path(__file__).resolve().parent
import requests
BASE_URL = "http://127.0.0.1:8000"

from frontend.utils import (
    register_user,
    login_user,
    create_document,
    get_documents,
    get_expiring_soon_documents,
    get_expired_documents,
    delete_document,
    build_file_url,
    fetch_file_bytes,
    verify_otp_api,
    get_password_strength,   # 🔥 ADD THIS
    validate_password_ui,
    forgot_password_api,
    reset_password_api
)
from styles import apply_custom_styles


def get_base64_image(filename):
    image_path = BASE_DIR / "assets" / filename
    if not image_path.exists():
        return ""
    return base64.b64encode(image_path.read_bytes()).decode()


def set_background(image_name=None, overlay_opacity=0.10):
    if image_name:
        encoded = get_base64_image(image_name)
        if encoded:
            st.markdown(
                f"""
                <style>
                [data-testid="stAppViewContainer"] {{
                    background:
                        linear-gradient(rgba(255,255,255,{overlay_opacity}), rgba(255,255,255,{overlay_opacity})),
                        url("data:image/png;base64,{encoded}");
                    background-size: cover;
                    background-position: center;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                }}

                [data-testid="stHeader"] {{
                    background: rgba(0,0,0,0);
                }}

                .stApp {{
                    background: transparent !important;
                }}

                .main .block-container {{
                    background: transparent !important;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )
            return

    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #eef7f7 0%, #f7fbfc 45%, #edf6fb 100%);
        }

        [data-testid="stHeader"] {
            background: rgba(0,0,0,0);
        }

        .stApp {
            background: transparent !important;
        }

        .main .block-container {
            background: transparent !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


st.set_page_config(
    page_title="DocNest",
    page_icon="📂",
    layout="wide"
)

st.markdown(apply_custom_styles(), unsafe_allow_html=True)

if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "show_auth" not in st.session_state:
    st.session_state.show_auth = False

if "sidebar_open" not in st.session_state:
    st.session_state.sidebar_open = False
    
if "success_msg" not in st.session_state:
    st.session_state.success_msg = None
    

# 🔥 ADD THIS BLOCK HERE
if st.session_state.get("success_msg"):
    st.toast(st.session_state.success_msg, icon="✅")
    st.session_state.success_msg = None
    


def safe_error_message(response, default_message):
    try:
        return response.json().get("detail", default_message)
    except Exception:
        return response.text if response.text else default_message

st.markdown("<style>pre {display:none !important;}</style>", unsafe_allow_html=True)
def landing_page():
    st.markdown(
        """
        <style>
        .hero-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 60px 40px;
            margin-top: 5vh;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 30px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            max-width: 850px;
            margin-left: auto;
            margin-right: auto;
        }
        .hero-title {
            font-size: 4.5rem;
            font-weight: 800;
            background: linear-gradient(to right, #ffffff, #a5f3fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0px;
        }
        .hero-tagline {
            color: #e2e8f0;
            font-size: 1.4rem;
            font-weight: 300;
            letter-spacing: 1px;
            margin-bottom: 30px;
            max-width: 600px;
        }
        .feature-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 40px;
            text-align: left;
        }
        .feature-item {
            color: #f1f5f9;
            font-size: 1rem;
            display: flex;
            align-items: center;
        }
        .feature-icon {
            margin-right: 10px;
            color: #22d3ee;
        }
        </style>

        <div class="hero-container">
            <h1 class="hero-title">DocNest</h1>
            <p class="hero-tagline">The Intelligent Vault for Your Digital Life</p>
            
            <div class="feature-grid">
                <div class="feature-item"><span class="feature-icon">✦</span> Bank-Grade Security Profile Access</div>
                <div class="feature-item"><span class="feature-icon">✦</span> Real-time Document Analytics</div>
                <div class="feature-item"><span class="feature-icon">✦</span> Smart Knowledge Base Search</div>
                <div class="feature-item"><span class="feature-icon">✦</span> Collaborative Team Folders</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns([1, 1.5, 0.2, 1.5, 1])
    
    with col2:
        if st.button("Login to Vault", use_container_width=True, type="primary"):
            st.session_state.show_auth = True
            st.session_state.auth_mode = "login"
            st.rerun()

    with col4:
        if st.button("Create Account", use_container_width=True):
            st.session_state.show_auth = True
            st.session_state.auth_mode = "register"
            st.rerun()
def top_bar():
    col1, col2 = st.columns([1, 10])

    with col1:
        if st.button("☰"):
            st.session_state.sidebar_open = not st.session_state.sidebar_open
            st.rerun()

    with col2:
        st.markdown("### Dashboard")
            
def auth_page():
    st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)

    # 🔥 INIT STATES
    if "show_otp" not in st.session_state:
        st.session_state.show_otp = False

    if "temp_email" not in st.session_state:
        st.session_state.temp_email = ""

    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"

    # ================= LOGIN =================
    if st.session_state.auth_mode == "login":

        st.markdown('<div class="auth-title">Login</div>', unsafe_allow_html=True)

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login", use_container_width=True):
            response = login_user(email, password)

            if response.status_code == 200:
                data = response.json()

                st.session_state.logged_in = True
                st.session_state.user_id = data["id"]
                st.session_state.user_name = data["name"]
                st.session_state.user_email = data["email"]

                st.success("Login successful")
                st.rerun()
            else:
                st.error("Login failed")

        # ✅ FIXED POSITION
        if st.button("Forgot Password?"):
            st.session_state.auth_mode = "forgot"
            st.rerun()

        # if st.button("Create an account"):
        #     st.session_state.auth_mode = "register"
        #     st.rerun()

        # 🔥 SWITCH TO REGISTER
        st.markdown('<div class="switch-text">Don’t have an account?</div>', unsafe_allow_html=True)

        if st.button("Create an account", use_container_width=True):
            st.session_state.auth_mode = "register"
            st.rerun()

    # ================= REGISTER =================
    elif st.session_state.auth_mode == "register":

        # 🔥 OTP SCREEN
        if st.session_state.show_otp:

            st.markdown('<div class="auth-title">Verify Email</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="auth-subtitle">Enter OTP sent to {st.session_state.temp_email}</div>',
                unsafe_allow_html=True
            )

            otp = st.text_input("Enter OTP", max_chars=6)

            if otp and not otp.isdigit():
                st.warning("Only digits allowed")

            is_valid = otp.isdigit() and len(otp) == 6

            if st.button("Verify OTP", use_container_width=True, disabled=not is_valid):

                response = verify_otp_api(st.session_state.temp_email, otp)

                if response.status_code == 200:
                    st.success("Email verified successfully!")
                    st.session_state.show_otp = False
                    st.session_state.auth_mode = "login"
                    st.rerun()
                else:
                    st.error("Invalid OTP")

            return
        
        elif st.session_state.auth_mode == "forgot":

            st.markdown('<div class="auth-title">Forgot Password</div>', unsafe_allow_html=True)

            email = st.text_input("Enter your email")

            if st.button("Send OTP", use_container_width=True):
                response = forgot_password_api(email)

                if response.status_code == 200:
                    st.session_state.temp_email = email
                    st.session_state.show_reset = True
                    st.success("OTP sent!")
                    st.rerun()
                else:
                    st.error("User not found")

            if st.session_state.get("show_reset"):

                otp = st.text_input("Enter OTP")
                new_password = st.text_input("New Password", type="password")

                if st.button("Reset Password", use_container_width=True):
                    response = reset_password_api(email, otp, new_password)

                    if response.status_code == 200:
                        st.success("Password reset successful!")
                        st.session_state.auth_mode = "login"
                        st.rerun()
                    else:
                        st.error("Invalid OTP")

            if st.button("← Back"):
                st.session_state.auth_mode = "login"
                st.rerun()
                
        


        # 🔥 REGISTER FORM
        st.markdown('<div class="auth-title">Register</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="auth-subtitle">Create your DocNest account.</div>',
            unsafe_allow_html=True
        )

        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        # 🔥 PASSWORD RULES
        rules = {
            "8+ characters": len(password) >= 8,
            "Uppercase letter": any(c.isupper() for c in password),
            "Lowercase letter": any(c.islower() for c in password),
            "Number": any(c.isdigit() for c in password),
            "Special character": any(c in "!@#$%^&*()" for c in password),
        }

        strength = get_password_strength(password)

        # 🔥 COLOR
        if strength <= 2:
            color = "#ef4444"
            label = "Weak"
        elif strength <= 4:
            color = "#f59e0b"
            label = "Medium"
        else:
            color = "#22c55e"
            label = "Strong"

        if password:

            # 🔥 STRENGTH BAR
            st.markdown(f"""
            <div style="height:8px;background:#e5e7eb;border-radius:5px;">
                <div style="width:{(strength/5)*100}%;background:{color};height:100%;border-radius:5px;"></div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"<span style='color:{color}; font-weight:600;'>{label}</span>", unsafe_allow_html=True)

            st.markdown("##### Password must contain:")
            for rule, ok in rules.items():
                st.markdown(
                    f"<span style='color:{'#22c55e' if ok else '#ef4444'}; font-weight:500;'>"
                    f"{'✔' if ok else '✖'} {rule}</span>",
                    unsafe_allow_html=True
                )

        is_password_valid = all(rules.values())

        if st.button("Register", use_container_width=True, disabled=not is_password_valid):

            if not name or not email:
                st.warning("All fields required")
                return

            response = register_user(name, email, password)

            if response.status_code == 200:
                st.session_state.temp_email = email
                st.session_state.show_otp = True
                st.success("OTP sent to your email")
                st.rerun()
            else:
                st.error(response.text)

        st.markdown('<div class="switch-text">Already have an account?</div>', unsafe_allow_html=True)

        if st.button("Go to Login", use_container_width=True):
            st.session_state.auth_mode = "login"
            st.rerun()
            
        # ================= FORGOT PASSWORD =================
    elif st.session_state.auth_mode == "forgot":

        st.markdown("### Forgot Password")

        # ✅ store email in session
        if "reset_email" not in st.session_state:
            st.session_state.reset_email = ""

        st.session_state.reset_email = st.text_input(
            "Enter your email",
            value=st.session_state.reset_email
        )

        if st.button("Send OTP"):

            if not st.session_state.reset_email:
                st.warning("Please enter email")
                return

            response = forgot_password_api(st.session_state.reset_email)

            if response.status_code == 200:
                st.success("OTP sent!")
                st.session_state.auth_mode = "reset"
                st.rerun()
            else:
                st.error("User not found")

        # if st.button("← Back"):
        #     st.session_state.auth_mode = "login"
        #     st.rerun()

    elif st.session_state.auth_mode == "reset":

        st.markdown("### Reset Password")

        otp = st.text_input("OTP")
        new_password = st.text_input("New Password", type="password")

        # 🔥 PASSWORD RULES
        rules = {
            "8+ characters": len(new_password) >= 8,
            "Uppercase": any(c.isupper() for c in new_password),
            "Lowercase": any(c.islower() for c in new_password),
            "Number": any(c.isdigit() for c in new_password),
            "Special char": any(c in "!@#$%^&*" for c in new_password),
        }

        strength = sum(rules.values())

        # 🔥 PASSWORD STRENGTH COLOR (STANDARDIZED)
        if strength <= 2:
            color = "#ef4444"   # Red
            label = "Weak"
        elif strength <= 4:
            color = "#f59e0b"   # Amber
            label = "Medium"
        else:
            color = "#22c55e"   # Green
            label = "Strong"

        if new_password:

            st.markdown(f"""
            <div style="height:8px;background:#eee;border-radius:5px;">
                <div style="width:{(strength/5)*100}%;background:{color};height:100%;border-radius:5px;"></div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"<span style='color:{color}'>{label}</span>", unsafe_allow_html=True)

            st.markdown("##### Password must contain:")

            for rule, ok in rules.items():
                st.markdown(
                    f"<span style='color:{'#22c55e' if ok else '#ef4444'}; font-weight:500;'>"
                    f"{'✔' if ok else '✖'} {rule}</span>",
                    unsafe_allow_html=True
                )

        is_valid = all(rules.values())

        if st.button("Reset Password", disabled=not is_valid):

            response = reset_password_api(
                st.session_state.reset_email,
                otp,
                new_password
            )

            if response.status_code == 200:
                st.success("Password reset successful")
                st.session_state.auth_mode = "login"
                st.rerun()
            else:
                st.error("Invalid OTP")

        # if st.button("← Back"):
        #     st.session_state.auth_mode = "login"
        #     st.rerun()

    # ================= BACK =================
    if st.button("← Back", use_container_width=True):
        st.session_state.show_auth = False
        st.session_state.show_otp = False
        st.session_state.auth_mode = "login"
        st.rerun()

def show_header():
    st.markdown(
        """
        <div class="hero-box">
            <div class="hero-title">DocNest</div>
            <div class="hero-subtitle">
                Store important documents, organize them neatly, and access them whenever you need.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def metric_cards(all_docs, expiring_docs, expired_docs):
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Total Documents</div>
                <div class="metric-value">{len(all_docs)}</div>
                <div class="metric-note">All documents stored in your vault</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Expiring Soon</div>
                <div class="metric-value">{len(expiring_docs)}</div>
                <div class="metric-note">Documents needing attention soon</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Expired</div>
                <div class="metric-value">{len(expired_docs)}</div>
                <div class="metric-note">Documents that may need renewal</div>
            </div>
            """,
            unsafe_allow_html=True
        )


def dashboard_page():
    show_header()

    # ================= USER INFO =================
    user_name = st.session_state.get("user_name", "User")
    user_id = st.session_state.get("user_id")
    user_email = st.session_state.get("user_email")

    st.write(f"Welcome, **{user_name}**")

    if not user_id:
        st.error("❌ User not logged in properly")
        return

    # ================= FETCH DATA =================
    all_docs_resp = get_documents(user_id)
    expiring_resp = get_expiring_soon_documents(user_id)
    expired_resp = get_expired_documents(user_id)
    
    if "alerts_sent" not in st.session_state:
        requests.post(f"{BASE_URL}/documents/send-alerts/{user_id}")
        st.session_state.alerts_sent = True

    all_docs = all_docs_resp.json() if all_docs_resp.status_code == 200 else []
    expiring_docs = expiring_resp.json() if expiring_resp.status_code == 200 else []
    expired_docs = expired_resp.json() if expired_resp.status_code == 200 else []

    print("📄 ALL DOCS:", all_docs)
    print("📧 USER EMAIL:", user_email)

    # ================= EMAIL ALERT TRIGGER =================
    # if user_email:
    #     check_and_send_alerts(all_docs, user_email)
    # else:
    #     print("❌ user_email missing — email not sent")

    # ================= METRICS =================
    metric_cards(all_docs, expiring_docs, expired_docs)

    # ================= ALERT UI =================
    if expiring_docs:
        count = len(expiring_docs)
        st.warning(
            f"⚠️ {count} document{'s' if count > 1 else ''} "
            f"{'are' if count > 1 else 'is'} expiring soon!"
        )

        if st.button("View Expiring Documents", key="exp_btn"):
            st.session_state.page = "Expiring Soon"
            st.rerun()

    if expired_docs:
        count = len(expired_docs)
        st.error(
            f"🚨 {count} document{'s' if count > 1 else ''} "
            f"{'have' if count > 1 else 'has'} expired!"
        )

        if st.button("View Expired Documents", key="expd_btn"):
            st.session_state.page = "Expired Documents"
            st.rerun()

    # ================= ACTION BUTTONS =================
    st.markdown('<div class="section-title">Quick Actions</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Add New Document", use_container_width=True):
            st.session_state.page = "Add Document"
            st.rerun()

    with col2:
        if st.button("Refresh Dashboard", use_container_width=True):
            st.rerun()

    # ================= RECENT DOCUMENTS =================
    st.markdown('<div class="section-title">Recent Documents</div>', unsafe_allow_html=True)

    if all_docs:
        for doc in all_docs[:5]:
            st.markdown(f"""
            <div class="doc-card">
                <div class="doc-title">{doc.get('title', 'No Title')}</div>
                <div class="doc-chip">{doc.get('category', 'No Category')}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No documents added yet.")

def add_document_page():
    show_header()
    
    st.markdown('<div class="section-title">Add a Document</div>', unsafe_allow_html=True)

    category = st.selectbox(
        "Category",
        ["Identity", "Vehicle", "Insurance", "Education", "Medical", "Travel", "Finance", "Other"]
    )

    has_expiry = st.checkbox("This document has an expiry date")

    with st.form("add_document_form"):

        title = st.text_input("Document Title")

        # 🔥 SMART SUGGESTION
        if "license" in title.lower():
            st.info("Suggested Category: Identity")
        elif "rc" in title.lower():
            st.info("Suggested Category: Vehicle")

        uploaded_file = st.file_uploader("Upload Document", type=["pdf", "jpg", "jpeg", "png"])

        expiry_date = None
        reminder_days_before = 30

        if has_expiry:
            expiry_date = st.date_input("Expiry Date")
            reminder_days_before = st.selectbox("Remind Me Before", [7, 15, 30, 60, 90])

        notes = st.text_area("Notes")

        submitted = st.form_submit_button("Save Document", use_container_width=True)

        if submitted:

            if not title.strip():
                st.error("Document title is required")
                return

            if has_expiry and not expiry_date:
                st.error("Please select an expiry date")
                return

            payload = {
                "title": title,
                "category": category,
                "expiry_date": str(expiry_date) if has_expiry else "",
                "reminder_days_before": str(reminder_days_before) if has_expiry else "0",
                "notes": notes,
                "user_id": str(st.session_state.user_id),
            }

            # 🔥 LOADING SPINNER
            with st.spinner("Saving document..."):
                response = create_document(payload, uploaded_file)

            if response.status_code == 200:
                st.session_state.success_msg = "✅ Document added successfully"
                st.rerun()
            else:
                st.error(safe_error_message(response, "Failed to add document"))
                
def documents_page():
    show_header()
    st.markdown('<div class="section-title">My Documents</div>', unsafe_allow_html=True)

    response = get_documents(st.session_state.user_id)
    if response.status_code != 200:
        st.error("Could not load documents")
        return

    docs = response.json()
    if not docs:
        st.info("No documents found.")
        return

    search = st.text_input("Search documents by title")
    filtered_docs = docs

    if search:
        filtered_docs = [doc for doc in docs if search.lower() in doc["title"].lower()]

    # 🔥 SORT BY PRIORITY
    from datetime import date, timedelta
    today = date.today()

    def get_priority(doc):
        if not doc.get("expiry_date"):
            return 3
        expiry = date.fromisoformat(doc["expiry_date"])
        if expiry < today:
            return 0
        elif expiry <= today + timedelta(days=7):
            return 1
        else:
            return 2

    filtered_docs = sorted(filtered_docs, key=get_priority)

    for doc in filtered_docs:
        file_url = build_file_url(doc.get("file_url"))

        color = "white"
        status = ""

        if doc.get("expiry_date"):
            expiry = date.fromisoformat(doc["expiry_date"])
            days_left = (expiry - today).days

            if expiry < today:
                color = "#ffe5e5"
                status = f"❌ Expired {-days_left} days ago"
            elif expiry <= today + timedelta(days=7):
                color = "#fff5cc"
                status = f"⚠️ {days_left} days left"
            else:
                status = f"⏳ {days_left} days left"

        # ✅ FIXED HTML (NO DOUBLE DIV BUG)
        details_html = f"""
        <div class="doc-card" style="background:{color};">
            <div class="doc-title">{doc['title']}</div>
            <div class="doc-chip">{doc['category']}</div>
        """

        if doc.get("expiry_date"):
            details_html += f"""<div class="doc-meta">Expiry: {doc['expiry_date']}</div>"""
            details_html += f"""<div class="doc-meta">{status}</div>"""

        if doc.get("notes"):
            details_html += f"""<div class="doc-meta">Notes: {doc['notes']}</div>"""

        details_html += "</div>"

        st.markdown(details_html, unsafe_allow_html=True)

        c1, c2, c3 = st.columns([1.2, 1.2, 1])

        with c1:
            if file_url:
                st.link_button("View Document", file_url, use_container_width=True)

        with c2:
            if doc.get("file_url"):
                file_bytes, filename = fetch_file_bytes(doc["file_url"])
                if file_bytes:
                    st.download_button(
                        label="Download",
                        data=file_bytes,
                        file_name=filename,
                        use_container_width=True,
                        key=f"download_{doc['id']}"
                    )

        with c3:
            if st.button("Delete", key=f"delete_{doc['id']}", use_container_width=True):
                delete_document(doc["id"])
                st.session_state.success_msg = "🗑️ Document deleted"
                st.rerun()

def expiring_page():
    show_header()
    st.markdown('<div class="section-title">Expiring Soon</div>', unsafe_allow_html=True)

    response = get_expiring_soon_documents(st.session_state.user_id)
    docs = response.json() if response.status_code == 200 else []

    if not docs:
        st.success("No documents expiring soon.")
        return

    for doc in docs:
        st.markdown(
            f"""
            <div class="doc-card">
                <div class="doc-title">{doc['title']}</div>
                <div class="doc-chip">{doc['category']}</div>
                <div class="doc-meta">Expiry Date: {doc['expiry_date']}</div>
                <div class="doc-meta">Reminder: {doc['reminder_days_before']} days before</div>
            </div>
            """,
            unsafe_allow_html=True
        )


def expired_page():
    show_header()
    st.markdown('<div class="section-title">Expired Documents</div>', unsafe_allow_html=True)

    response = get_expired_documents(st.session_state.user_id)
    docs = response.json() if response.status_code == 200 else []

    if not docs:
        st.success("No expired documents.")
        return

    for doc in docs:
        st.markdown(
            f"""
            <div class="doc-card">
                <div class="doc-title">{doc['title']}</div>
                <div class="doc-chip">{doc['category']}</div>
                <div class="doc-meta">Expired On: {doc['expiry_date']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

def sidebar():

    if not st.session_state.sidebar_open:
        # ❌ HIDE sidebar completely
        st.markdown("""
        <style>
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        </style>
        """, unsafe_allow_html=True)
        return

    # ✅ SHOW sidebar when toggled
    with st.sidebar:

        st.markdown("## 📂 DocNest")

        st.markdown(
            f"<div style='color:#c9d1d9;'>Welcome, <b>{st.session_state.user_name}</b></div>",
            unsafe_allow_html=True
        )

        st.markdown("---")

        menu = {
            "🏠 Dashboard": "Dashboard",
            "➕ Add Document": "Add Document",
            "📄 My Documents": "My Documents",
            "⏰ Expiring Soon": "Expiring Soon",
            "❌ Expired Documents": "Expired Documents",
        }

        for label, page in menu.items():
            if st.button(label, use_container_width=True):
                st.session_state.page = page

        st.markdown("---")

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
                
                
# ✅ GLOBAL POPUP (MUST BE AT TOP)
if st.session_state.get("success_msg"):
    st.toast(st.session_state.success_msg)
    st.session_state.success_msg = None


if not st.session_state.logged_in:
    set_background("hero.png", overlay_opacity=0.08)

    if st.session_state.show_auth:
        auth_page()
    else:
        landing_page()

else:
    set_background("hero.png")

    top_bar()
    sidebar()

    page = st.session_state.get("page", "Dashboard")

    if page == "Dashboard":
        dashboard_page()
    elif page == "Add Document":
        add_document_page()
    elif page == "My Documents":
        documents_page()
    elif page == "Expiring Soon":
        expiring_page()
    elif page == "Expired Documents":
        expired_page()