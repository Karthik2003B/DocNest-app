from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.connection import get_db
from backend.schemas.user import UserCreate, UserLogin, UserResponse
from backend.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


# ✅ FIXED (removed response_model)
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.register_user(user.name, user.email, user.password)


@router.post("/login", response_model=UserResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.login_user(user.email, user.password)


@router.post("/verify-otp")
def verify_otp(email: str, otp: str, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.verify_otp(email, otp)

@router.post("/forgot-password")
def forgot_password(email: str, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.forgot_password(email)


@router.post("/reset-password")
def reset_password(email: str, otp: str, new_password: str, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.reset_password(email, otp, new_password)