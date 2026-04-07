from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.base import Base
from sqlalchemy import Boolean

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    otp = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False) 

    documents = relationship("Document", back_populates="owner")