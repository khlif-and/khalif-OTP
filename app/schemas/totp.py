from pydantic import BaseModel
from typing import Optional

class TOTPEnableRequest(BaseModel):
    identifier: str

class TOTPVerifyRequest(BaseModel):
    identifier: str
    totp_code: str

class TOTPResponse(BaseModel):
    secret: str
    provisioning_uri: str
    qr_code_base64: str
