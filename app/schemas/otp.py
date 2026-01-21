from pydantic import BaseModel

class OTPRequest(BaseModel):
    phone_number: str

class OTPTelegramRequest(BaseModel):
    chat_id: str

class OTPEmailRequest(BaseModel):
    email: str

class OTPVerifyRequest(BaseModel):
    identifier: str
    otp_code: str
