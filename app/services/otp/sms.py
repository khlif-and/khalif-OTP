import requests
from datetime import datetime, timedelta
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class SMSProvider:
    @staticmethod
    def send_sms(phone_number: str, otp: str) -> bool:
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

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"SMS Gateway Error: {e}")
            raise e
