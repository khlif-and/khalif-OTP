from typing import Dict, Optional

_totp_storage: Dict[str, dict] = {}

class TOTPStorage:
    @staticmethod
    def save_secret(identifier: str, secret: str):
        _totp_storage[identifier] = {
            "secret": secret,
            "verified": False
        }
        
    @staticmethod
    def get_secret(identifier: str) -> Optional[str]:
        record = _totp_storage.get(identifier)
        if record:
            return record.get("secret")
        return None
        
    @staticmethod
    def mark_verified(identifier: str):
        if identifier in _totp_storage:
            _totp_storage[identifier]["verified"] = True
            
    @staticmethod
    def is_verified(identifier: str) -> bool:
        record = _totp_storage.get(identifier)
        return record is not None and record.get("verified", False)
