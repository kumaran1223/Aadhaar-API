from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
import re

class AadhaarDataBase(BaseModel):
    vid: Optional[str] = Field(None, description="Virtual ID")
    aadhaar_number: str = Field(..., description="Aadhaar number in format XXXX XXXX XXXX")
    name_tamil: Optional[str] = Field(None, description="Name in Tamil")
    name: str = Field(..., description="Name in English")
    guardian_name: Optional[str] = Field(None, description="Guardian's name")
    dob: Optional[str] = Field(None, description="Date of birth")
    gender: Optional[str] = Field(None, description="Gender")
    address: Optional[str] = Field(None, description="Address")
    vtc: Optional[str] = Field(None, description="Village/Town/City")
    po: Optional[str] = Field(None, description="Post Office")
    sub_district: Optional[str] = Field(None, description="Sub District")
    district: Optional[str] = Field(None, description="District")
    state: Optional[str] = Field(None, description="State")
    pincode: Optional[str] = Field(None, description="PIN code")
    phone: Optional[str] = Field(None, description="Phone number")

    @validator('aadhaar_number')
    def validate_aadhaar_number(cls, v):
        if v:
            # Remove spaces and check if it's 12 digits
            clean_aadhaar = re.sub(r'\s+', '', v)
            if not re.match(r'^\d{12}$', clean_aadhaar):
                raise ValueError('Aadhaar number must be 12 digits')
            # Return formatted version
            return f"{clean_aadhaar[:4]} {clean_aadhaar[4:8]} {clean_aadhaar[8:]}"
        return v

    @validator('pincode')
    def validate_pincode(cls, v):
        if v and not re.match(r'^\d{6}$', v):
            raise ValueError('PIN code must be 6 digits')
        return v

    @validator('phone')
    def validate_phone(cls, v):
        if v and not re.match(r'^\d{10}$', v):
            raise ValueError('Phone number must be 10 digits')
        return v

class AadhaarDataCreate(AadhaarDataBase):
    pass

class AadhaarDataUpdate(AadhaarDataBase):
    aadhaar_number: Optional[str] = None
    name: Optional[str] = None

class AadhaarDataInDBBase(AadhaarDataBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class AadhaarData(AadhaarDataInDBBase):
    pass

class AadhaarDataInDB(AadhaarDataInDBBase):
    pass

class AadhaarSubmissionResponse(BaseModel):
    success: bool
    message: str
    data: Optional[AadhaarData] = None
    aadhaar_number: Optional[str] = None

class AadhaarRetrievalResponse(BaseModel):
    success: bool
    message: str
    data: Optional[AadhaarData] = None

class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    detail: Optional[str] = None
