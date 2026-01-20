import secrets
import string
import logging
from typing import Dict
from datetime import datetime, timedelta
import requests
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

otp_storage: Dict[str, dict] = {}

class OTPService:
    @staticmethod
    def generate_otp(length: int = settings.otp_length) -> str:
        return ''.join(secrets.choice(string.digits) for _ in range(length))

    @staticmethod
    @staticmethod
    def send_otp(phone_number: str) -> dict:
        otp = OTPService.generate_otp()
        expiry = datetime.now() + timedelta(seconds=settings.otp_expiry_seconds)
        
        current_record = otp_storage.get(phone_number)
        counter = 1
        if current_record:
            counter = current_record.get("counter", 0) + 1
        
        otp_storage[phone_number] = {
            "otp": otp,
            "expires_at": expiry,
            "counter": counter
        }
        
        try:
            status = OTPService._send_via_gateway(phone_number, otp, counter)
            return {"status": "success", "message": status, "counter": counter}
        except Exception as e:
            logger.error(f"Failed to send OTP: {e}")
            return {"status": "error", "message": "Gateway Error", "counter": counter}

    @staticmethod
    def _send_via_gateway(phone_number: str, otp: str, counter: int):
        url = settings.wa_gateway_url
        
        # Calculate expiry time string (e.g. 20:30)
        expiry_time = (datetime.now() + timedelta(seconds=settings.otp_expiry_seconds)).strftime("%H:%M")
        
        message = f"Your Verification Code is: {otp}\n\nValid until: {expiry_time} (5 minutes).\nDo not share this code with anyone."
        
        payload = {
            "phone_number": phone_number,
            "message": message
        }
        
        logger.info(f"Sending to Gateway: {payload}")
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        return "OTP sent via WhatsApp"

    @staticmethod
    def verify_otp(phone_number: str, otp_code: str) -> bool:
        record = otp_storage.get(phone_number)
        
        if not record:
            return False
        
        if datetime.now() > record["expires_at"]:
            del otp_storage[phone_number]
            return False
            
        if record["otp"] == otp_code:
            del otp_storage[phone_number]
            return True
            
        return False
