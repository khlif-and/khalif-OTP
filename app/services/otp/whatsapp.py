import requests
from datetime import datetime, timedelta
from app.core.config import settings
from app.core.messages import Messages
import logging

logger = logging.getLogger(__name__)

class WhatsappProvider:
    @staticmethod
    def send_whatsapp(phone_number: str, otp: str) -> bool:
        url = settings.wa_gateway_url
        
        expiry_time = (datetime.now() + timedelta(seconds=settings.otp_expiry_seconds)).strftime("%H:%M")
        
        message = Messages.OTP_TEMPLATE.format(otp=otp, expiry_time=expiry_time)
        
        payload = {
            "phone_number": phone_number,
            "message": message
        }
        
        logger.info(f"Sending to WA Gateway: {payload}")
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"WA Gateway Error: {e}")
            raise e
