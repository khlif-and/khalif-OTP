from fastapi import APIRouter, HTTPException
from app.schemas.otp import OTPRequest, OTPVerifyRequest, OTPTelegramRequest
from app.services.otp_service import OTPService
from app.services.telegram_service import TelegramService
from pydantic import BaseModel

router = APIRouter()

@router.post("/send-otp")
async def send_otp(request: OTPRequest):
    result = OTPService.send_otp(request.phone_number)
    return {
        "message": result["message"], 
        "counter": result["counter"],
        "phone_number": request.phone_number
    }

@router.post("/send-sms-otp")
async def send_sms_otp(request: OTPRequest):
    result = OTPService.send_otp_sms(request.phone_number)
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])

    return {
        "message": result["message"], 
        "counter": result["counter"],
        "phone_number": request.phone_number
    }

@router.post("/send-telegram-otp")
async def send_telegram_otp(request: OTPTelegramRequest):
    result = OTPService.send_otp_telegram(request.chat_id)
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])

    return {
        "message": result["message"], 
        "counter": result["counter"],
        "chat_id": request.chat_id
    }

# --- Telegram Linking Features ---

@router.post("/telegram/link")
async def create_telegram_link():
    """Generates a unique link for user to connect Telegram."""
    token = TelegramService.generate_link_token()
    link = TelegramService.get_bot_link(token)
    return {
        "token": token,
        "link": link,
        "instructions": "Click the link and press Start to connect."
    }

@router.get("/telegram/status/{token}")
async def check_telegram_status(token: str):
    """Check if a token has been linked to a chat_id."""
    chat_id = TelegramService.get_chat_id_by_token(token)
    if chat_id:
        return {"linked": True, "chat_id": chat_id}
    return {"linked": False}

class OTPLinkedRequest(BaseModel):
    token: str

@router.post("/send-telegram-otp-linked")
async def send_telegram_otp_linked(request: OTPLinkedRequest):
    """Send OTP using the linked token instead of raw chat_id."""
    chat_id = TelegramService.get_chat_id_by_token(request.token)
    if not chat_id:
        raise HTTPException(status_code=400, detail="Token not linked or invalid")
        
    result = OTPService.send_otp_telegram(chat_id)
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])

    return {
        "message": result["message"], 
        "counter": result["counter"],
        "token": request.token
    }

@router.post("/verify-otp")
async def verify_otp(request: OTPVerifyRequest):
    is_valid = OTPService.verify_otp(request.phone_number, request.otp_code)
    
    if is_valid:
        return {"message": "OTP verified successfully"}
    else:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
