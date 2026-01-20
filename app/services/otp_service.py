import secrets
import string
import logging
from typing import Dict
from datetime import datetime, timedelta
import requests
from app.core.config import settings
from app.core.messages import Messages

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

otp_storage: Dict[str, dict] = {}

class OTPService:
    @staticmethod
    def generate_otp(length: int = settings.otp_length) -> str:
        return ''.join(secrets.choice(string.digits) for _ in range(length))

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
    def send_otp_sms(phone_number: str) -> dict:
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
            status = OTPService._send_via_sms_gateway(phone_number, otp, counter)
            return {"status": "success", "message": status, "counter": counter}
        except Exception as e:
            logger.error(f"Failed to send SMS OTP: {e}")
            return {"status": "error", "message": str(e), "counter": counter}

    @staticmethod
    def send_otp_telegram(chat_id: str) -> dict:
        otp = OTPService.generate_otp()
        expiry = datetime.now() + timedelta(seconds=settings.otp_expiry_seconds)
        
        current_record = otp_storage.get(chat_id)
        counter = 1
        if current_record:
            counter = current_record.get("counter", 0) + 1
        
        otp_storage[chat_id] = {
            "otp": otp,
            "expires_at": expiry,
            "counter": counter
        }
        
        try:
            status = OTPService._send_via_telegram(chat_id, otp, counter)
            return {"status": "success", "message": status, "counter": counter}
        except Exception as e:
            logger.error(f"Failed to send Telegram OTP: {e}")
            return {"status": "error", "message": str(e), "counter": counter}

    @staticmethod
    def _send_via_telegram(chat_id: str, otp: str, counter: int):
        if not settings.telegram_bot_token:
            raise Exception("TELEGRAM_BOT_TOKEN is not configured")

        url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
        expiry_time = (datetime.now() + timedelta(seconds=settings.otp_expiry_seconds)).strftime("%H:%M")
        
        # Using the same template message but adapting formatting for Telegram (Markdown/HTML) if needed.
        # Messages.OTP_TEMPLATE uses *bold* which works in Telegram Markdown.
        message = Messages.OTP_TEMPLATE.format(otp=otp, expiry_time=expiry_time)
        
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        
        logger.info(f"Sending to Telegram: {payload}")
        
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        
        return "OTP sent via Telegram"

    @staticmethod
    def _send_via_gateway(phone_number: str, otp: str, counter: int):
        url = settings.wa_gateway_url
        
        expiry_time = (datetime.now() + timedelta(seconds=settings.otp_expiry_seconds)).strftime("%H:%M")
        
        message = Messages.OTP_TEMPLATE.format(otp=otp, expiry_time=expiry_time)
        
        payload = {
            "phone_number": phone_number,
            "message": message
        }
        
        logger.info(f"Sending to Gateway: {payload}")
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        return "OTP sent via WhatsApp"

    @staticmethod
    def _send_via_sms_gateway(phone_number: str, otp: str, counter: int):
        if not settings.sms_gateway_url:
            raise Exception("SMS_GATEWAY_URL is not configured")

        url = settings.sms_gateway_url
        expiry_time = (datetime.now() + timedelta(seconds=settings.otp_expiry_seconds)).strftime("%H:%M")
        
        message = f"Kode OTP: {otp}. Berlaku s/d {expiry_time}. Jgn kasih siapa2."
        
        payload = {
            "to": phone_number,
            "message": message
        }
        
        logger.info(f"Sending to SMS Gateway: {payload}")
        
        headers = {}
        if settings.sms_gateway_api_key:
            headers["Authorization"] = settings.sms_gateway_api_key

        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        
        return "OTP sent via SMS"

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
