from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class AadhaarForm(Base):
    __tablename__ = "aadhaar_forms"

    id = Column(Integer, primary_key=True, index=True)
    vid = Column(String(20), nullable=True, index=True)
    aadhaar_number = Column(String(15), nullable=False, unique=True, index=True)
    name_tamil = Column(Text, nullable=True)
    name = Column(String(255), nullable=False)
    guardian_name = Column(String(255), nullable=True)
    dob = Column(String(20), nullable=True)
    gender = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    vtc = Column(String(255), nullable=True)
    po = Column(String(255), nullable=True)
    sub_district = Column(String(255), nullable=True)
    district = Column(String(255), nullable=True)
    state = Column(String(255), nullable=True)
    pincode = Column(String(10), nullable=True)
    phone = Column(String(15), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<AadhaarForm(aadhaar_number='{self.aadhaar_number}', name='{self.name}')>"
