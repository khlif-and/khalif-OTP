from fastapi import APIRouter, HTTPException
from app.schemas.otp import OTPRequest, OTPVerifyRequest
from app.services.otp_service import OTPService

router = APIRouter()

@router.post("/send-otp")
async def send_otp(request: OTPRequest):
    result = OTPService.send_otp(request.phone_number)
    return {
        "message": result["message"], 
        "counter": result["counter"],
        "phone_number": request.phone_number
    }

@router.post("/verify-otp")
async def verify_otp(request: OTPVerifyRequest):
    is_valid = OTPService.verify_otp(request.phone_number, request.otp_code)
    
    if is_valid:
        return {"message": "OTP verified successfully"}
    else:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
