from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str
    otp_length: int
    otp_expiry_seconds: int
    debug_mode: bool
    wa_gateway_url: str

    class Config:
        env_file = ".env"

settings = Settings()
