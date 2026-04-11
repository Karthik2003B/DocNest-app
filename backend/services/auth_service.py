from fastapi import HTTPException
from backend.repositories.user_repository import UserRepository
from backend.utils.security import hash_password, verify_password
from backend.utils.email import send_email
import random
from backend.utils.email_template import build_email_template

class AuthService:
    def __init__(self, db):
        self.user_repo = UserRepository(db)

    # ================= REGISTER =================
    def register_user(self, name: str, email: str, password: str):

        existing_user = self.user_repo.get_by_email(email)

        # 🔥 IF USER EXISTS
        if existing_user:

            # ❌ Already verified → block
            if getattr(existing_user, "is_verified", False):
                raise HTTPException(status_code=400, detail="Email already registered")

            # 🔁 Not verified → resend OTP
            otp = str(random.randint(100000, 999999))

            existing_user.otp = otp
            existing_user.password_hash = hash_password(password)
            self.user_repo.db.commit()

            html = build_email_template(
            title="🔐 Verify Your Email",
            message="Use the OTP below to verify your DocNest account.",
            highlight=f"OTP: {otp}"
            )

            send_email(
                to_email=email,
                subject="🔐 DocNest Verification Code",
                html_content=html
            )

            return {"message": "OTP resent to your email"}

        # 🔥 NEW USER
        otp = str(random.randint(100000, 999999))

        password_hash = hash_password(password)

        user = self.user_repo.create_user(name, email, password_hash)

        user.otp = otp
        user.is_verified = False
        self.user_repo.db.commit()

        html = build_email_template(
        title="🔐 Verify Your Email",
        message="Use the OTP below to verify your DocNest account.",
        highlight=f"OTP: {otp}"
        )

        send_email(
            to_email=email,
            subject="🔐 DocNest Verification Code",
            html_content=html
        )

        return {"message": "OTP sent to your email"}

    # ================= LOGIN =================
    def login_user(self, email: str, password: str):
        user = self.user_repo.get_by_email(email)

        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        # ❌ Block unverified users
        if not getattr(user, "is_verified", False):
            raise HTTPException(status_code=403, detail="Please verify your email first")

        return user

    # ================= VERIFY OTP =================
    def verify_otp(self, email: str, otp: str):
        user = self.user_repo.get_by_email(email)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.otp != otp:
            raise HTTPException(status_code=400, detail="Invalid OTP")

        user.is_verified = True
        user.otp = None
        self.user_repo.db.commit()

        return {"message": "Email verified successfully"}
    
    # ================= FORGOT PASSWORD =================
    def forgot_password(self, email: str):
        email = email.strip().lower()

        user = self.user_repo.get_by_email(email)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        otp = str(random.randint(100000, 999999))

        user.otp = otp
        self.user_repo.db.commit()

        # ✅ SEND EMAIL USING SENDGRID
        html = build_email_template(
        title="🔐 Verify Your Email",
        message="Use the OTP below to verify your DocNest account.",
        highlight=f"OTP: {otp}"
        )

        send_email(
            to_email=email,
            subject="🔐 DocNest Verification Code",
            html_content=html
        )

        return {"message": "OTP sent to your email"}

    # ================= RESET PASSWORD =================
    def reset_password(self, email: str, otp: str, new_password: str):
        user = self.user_repo.get_by_email(email)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.otp != otp:
            raise HTTPException(status_code=400, detail="Invalid OTP")

        user.password_hash = hash_password(new_password)
        user.otp = None
        self.user_repo.db.commit()

        return {"message": "Password reset successful"}