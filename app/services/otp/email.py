import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class EmailProvider:
    @staticmethod
    def send_email(email_to: str, otp: str) -> bool:
        if not settings.smtp_host:
            logger.error("SMTP config is missing")
            raise Exception("SMTP config is missing")
            
        expiry_time = (datetime.now() + timedelta(seconds=settings.otp_expiry_seconds)).strftime("%H:%M")
        
        msg = MIMEMultipart()
        msg['From'] = settings.smtp_from_email
        msg['To'] = email_to
        msg['Subject'] = f"Kode OTP Login: {otp}"
        
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #eee; border-radius: 10px;">
                    <h2 style="color: #333;">Verifikasi Login</h2>
                    <p>Halo,</p>
                    <p>Kode OTP Anda adalah:</p>
                    <h1 style="color: #4CAF50; font-size: 32px; letter-spacing: 5px;">{otp}</h1>
                    <p>Kode ini berlaku hingga pukul <strong>{expiry_time}</strong>.</p>
                    <p style="color: #888; font-size: 12px;">Jangan berikan kode ini kepada siapapun.</p>
                </div>
            </body>
        </html>
        """
        
        msg.attach(MIMEText(html_body, 'html'))
        
        try:
            with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
                server.starttls()
                server.login(settings.smtp_user, settings.smtp_password)
                server.send_message(msg)
            return True
        except Exception as e:
            logger.error(f"SMTP Error: {e}")
            raise e
