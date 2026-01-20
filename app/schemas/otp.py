from pydantic import BaseModel

class OTPRequest(BaseModel):
    phone_number: str

class OTPTelegramRequest(BaseModel):
    chat_id: str

class OTPVerifyRequest(BaseModel):
    phone_number: str
    otp_code: str
