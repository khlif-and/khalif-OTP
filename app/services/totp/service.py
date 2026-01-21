import pyotp
from typing import Dict
from .storage import TOTPStorage
from .qr import QRGenerator

class TOTPService:
    @staticmethod
    def generate_totp_secret(identifier: str) -> Dict[str, str]:
        secret = pyotp.random_base32()
        
        TOTPStorage.save_secret(identifier, secret)
        
        totp = pyotp.TOTP(secret)
        provisioning_uri = totp.provisioning_uri(name=identifier, issuer_name="khalif")
        
        qr_base64 = QRGenerator.generate_stylized_qr(provisioning_uri)
        
        return {
            "secret": secret,
            "provisioning_uri": provisioning_uri,
            "qr_code_base64": qr_base64
        }

    @staticmethod
    def verify_totp(identifier: str, token: str) -> bool:
        secret = TOTPStorage.get_secret(identifier)
        if not secret:
            return False
            
        is_valid = pyotp.TOTP(secret).verify(token)
        if is_valid:
            TOTPStorage.mark_verified(identifier)
            return True
            
        return False

    @staticmethod
    def is_totp_enabled(identifier: str) -> bool:
        return TOTPStorage.is_verified(identifier)
