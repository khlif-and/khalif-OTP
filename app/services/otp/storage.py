from typing import Dict, Optional
from datetime import datetime

# In-memory storage for OTPs.
# Format: {identifier: {"otp": "123456", "expires_at": datetime, "counter": int}}
_otp_storage: Dict[str, dict] = {}

class OTPStorage:
    @staticmethod
    def save_otp(identifier: str, otp: str, expiry: datetime, counter: int):
        _otp_storage[identifier] = {
            "otp": otp,
            "expires_at": expiry,
            "counter": counter
        }

    @staticmethod
    def get_otp(identifier: str) -> Optional[dict]:
        return _otp_storage.get(identifier)

    @staticmethod
    def delete_otp(identifier: str):
        if identifier in _otp_storage:
            del _otp_storage[identifier]
