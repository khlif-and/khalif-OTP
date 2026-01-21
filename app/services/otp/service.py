import secrets
import string
import logging
from datetime import datetime, timedelta
from typing import Dict
from app.core.config import settings
from .storage import OTPStorage
from .email import EmailProvider
from .sms import SMSProvider
from .whatsapp import WhatsappProvider

logger = logging.getLogger(__name__)

class OTPService:
    @staticmethod
    def generate_otp(length: int = settings.otp_length) -> str:
        return ''.join(secrets.choice(string.digits) for _ in range(length))

    @staticmethod
    def send_otp_email(email: str) -> dict:
        otp = OTPService.generate_otp()
        expiry = datetime.now() + timedelta(seconds=settings.otp_expiry_seconds)
        
        # Determine counter
        current_record = OTPStorage.get_otp(email)
        counter = 1
        if current_record:
            counter = current_record.get("counter", 0) + 1
        
        OTPStorage.save_otp(email, otp, expiry, counter)
        
        try:
            EmailProvider.send_email(email, otp)
            return {"status": "success", "message": "OTP sent via Email", "counter": counter}
        except Exception as e:
            logger.error(f"Failed to send Email OTP: {e}")
            return {"status": "error", "message": str(e), "counter": counter}

    @staticmethod
    def send_otp(phone_number: str) -> dict:
        """Sends OTP via WhatsApp (Default)"""
        otp = OTPService.generate_otp()
        expiry = datetime.now() + timedelta(seconds=settings.otp_expiry_seconds)
        
        current_record = OTPStorage.get_otp(phone_number)
        counter = 1
        if current_record:
            counter = current_record.get("counter", 0) + 1
        
        OTPStorage.save_otp(phone_number, otp, expiry, counter)
        
        try:
            WhatsappProvider.send_whatsapp(phone_number, otp)
            return {"status": "success", "message": "OTP sent via WhatsApp", "counter": counter}
        except Exception as e:
            logger.error(f"Failed to send WA OTP: {e}")
            return {"status": "error", "message": "Gateway Error", "counter": counter}

    @staticmethod
    def send_otp_sms(phone_number: str) -> dict:
        otp = OTPService.generate_otp()
        expiry = datetime.now() + timedelta(seconds=settings.otp_expiry_seconds)
        
        current_record = OTPStorage.get_otp(phone_number)
        counter = 1
        if current_record:
            counter = current_record.get("counter", 0) + 1
        
        OTPStorage.save_otp(phone_number, otp, expiry, counter)
        
        try:
            SMSProvider.send_sms(phone_number, otp)
            return {"status": "success", "message": "OTP sent via SMS", "counter": counter}
        except Exception as e:
            logger.error(f"Failed to send SMS OTP: {e}")
            return {"status": "error", "message": str(e), "counter": counter}

    @staticmethod
    def verify_otp(identifier: str, otp_code: str) -> bool:
        record = OTPStorage.get_otp(identifier)
        
        if not record:
            return False
        
        if datetime.now() > record["expires_at"]:
            OTPStorage.delete_otp(identifier)
            return False
            
        if record["otp"] == otp_code:
            OTPStorage.delete_otp(identifier)
            return True
            
        return False
