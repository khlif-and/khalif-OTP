from fastapi.testclient import TestClient
from main import app
import pyotp

client = TestClient(app)

def test_totp_flow():
    print("Starting TOTP Flow Test...")
    phone = "08123456789"
    
    # 1. Enable
    print("1. Testing Enable TOTP...")
    response = client.post("/totp/enable", json={"phone_number": phone})
    if response.status_code != 200:
        print(f"FAILED: Enable endpoint returned {response.status_code}")
        print(response.text)
        exit(1)
        
    data = response.json()
    secret = data["secret"]
    uri = data["provisioning_uri"]
    print(f"   Success! Secret: {secret}")
    print(f"   URI: {uri}")
    
    # 2. Verify Valid
    print("2. Testing Valid Verification...")
    totp = pyotp.TOTP(secret)
    code = totp.now()
    verify_response = client.post("/totp/verify", json={"phone_number": phone, "totp_code": code})
    
    if verify_response.status_code != 200:
        print(f"FAILED: Verify endpoint returned {verify_response.status_code}")
        print(verify_response.text)
        exit(1)
        
    print("   Success! verification response:", verify_response.json())
    
    # 3. Verify Invalid
    print("3. Testing Invalid Code Verification...")
    fail_response = client.post("/totp/verify", json={"phone_number": phone, "totp_code": "000000"})
    
    if fail_response.status_code == 400:
        print("   Success! Invalid code was rejected as expected.")
    else:
        print(f"FAILED: Expected 400 for invalid code, got {fail_response.status_code}")
        exit(1)

    print("\nALL TESTS PASSED ✅")

if __name__ == "__main__":
    test_totp_flow()
