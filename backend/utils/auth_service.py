from fastapi import HTTPException
from backend.repositories.user_repository import UserRepository
from backend.utils.security import hash_password, verify_password
import random


class AuthService:
    def __init__(self, db):
        self.user_repo = UserRepository(db)

    # ================= REGISTER =================
    def register_user(self, name: str, email: str, password: str):
        print("REGISTER FUNCTION CALLED")

        existing_user = self.user_repo.get_by_email(email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        password_hash = hash_password(password)
        return self.user_repo.create_user(name, email, password_hash)

    # ================= LOGIN =================
    def login_user(self, email: str, password: str):
        user = self.user_repo.get_by_email(email)

        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        return user

    # ================= FORGOT PASSWORD =================
    def forgot_password(self, email: str):
        user = self.user_repo.get_by_email(email)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        otp = str(random.randint(100000, 999999))

        # save OTP
        user.otp = otp
        self.user_repo.db.commit()

        # 🔥 TEMP: print instead of email
        print("RESET OTP:", otp)

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