from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str
    otp_length: int
    otp_expiry_seconds: int
    debug_mode: bool
    wa_gateway_url: str
    sms_gateway_url: str = ""
    sms_gateway_api_key: str = ""
    telegram_bot_token: str = ""
    
    # SMTP Settings
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from_email: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
