from fastapi import APIRouter
from fastapi.responses import HTMLResponse

html_router = APIRouter()

@html_router.get("/demo/totp", response_class=HTMLResponse)
async def get_totp_demo_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>OTP Demo</title>
        <script>
            // --- TOTP Functions ---
            async function generate_totp() {
                const id = document.getElementById("totp-id").value;
                if(!id) return alert("Identifier required");
                const response = await fetch("/totp/enable", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({identifier: id})
                });
                const data = await response.json();
                document.getElementById("secret").innerText = "Secret: " + data.secret;
                document.getElementById("qr").src = "data:image/png;base64," + data.qr_code_base64;
                document.getElementById("totp-verify-section").style.display = "block";
            }
            
            async function verify_totp() {
                const id = document.getElementById("totp-id").value;
                const code = document.getElementById("totp-code").value;
                const response = await fetch("/totp/verify", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({identifier: id, totp_code: code})
                });
                result_alert(response);
            }

            // --- Standard OTP Functions ---
            async function send_otp(type) {
                const id = document.getElementById("std-id").value;
                if(!id) return alert("Identifier required");
                
                let endpoint = "/send-otp"; // default WA
                let body = {phone_number: id};

                if(type === 'email') {
                    endpoint = "/send-email-otp";
                    body = {email: id};
                } else if (type === 'sms') {
                    endpoint = "/send-sms-otp";
                    body = {phone_number: id};
                }

                try {
                    const res = await fetch(endpoint, {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify(body)
                    });
                    const data = await res.json();
                    if(res.ok) {
                        alert("OTP Sent! Counter: " + data.counter);
                        document.getElementById("std-verify-section").style.display = "block";
                    } else {
                        alert("Error: " + data.detail);
                    }
                } catch(e) { alert(e); }
            }

            async function verify_std_otp() {
                const id = document.getElementById("std-id").value;
                const code = document.getElementById("std-code").value;
                
                try {
                    const res = await fetch("/verify-otp", {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify({identifier: id, otp_code: code})
                    });
                    const data = await res.json();
                    if(res.ok) alert("✅ SUCCESS: " + data.message);
                    else alert("❌ ERROR: " + data.detail);
                } catch(e) { alert(e); }
            }

            async function result_alert(response) {
                const data = await response.json();
                if(response.ok) alert("✅ SUCCESS: " + data.message);
                else alert("❌ ERROR: " + data.detail);
            }
        </script>
        <style>
            body { font-family: sans-serif; padding: 20px; max-width: 800px; margin: 0 auto; display: flex; gap: 20px; }
            .col { flex: 1; }
            input, button { padding: 10px; margin: 5px 0; width: 100%; box-sizing: border-box; }
            #qr { display: block; margin: 20px auto; max-width: 200px; }
            .section { margin-bottom: 30px; border: 1px solid #ccc; padding: 20px; border-radius: 8px; }
            h2, h3 { margin-top: 0; }
            .btn-group { display: flex; gap: 5px; }
        </style>
    </head>
    <body>
        <div class="col">
            <div class="section">
                <h2>📱 Standard OTP</h2>
                <p>Email, SMS, WhatsApp</p>
                <input type="text" id="std-id" placeholder="Email or Phone Number">
                <div class="btn-group">
                    <button onclick="send_otp('email')">Send Email</button>
                    <button onclick="send_otp('sms')">Send SMS</button>
                    <button onclick="send_otp('wa')">Send WA</button>
                </div>

                <div id="std-verify-section" style="display:none; margin-top: 20px; border-top: 1px dashed #ccc; padding-top: 10px;">
                    <h3>Verify Code</h3>
                    <input type="text" id="std-code" placeholder="Enter Code">
                    <button onclick="verify_std_otp()">Verify Standard OTP</button>
                </div>
            </div>
        </div>

        <div class="col">
            <div class="section">
                <h2>🔐 TOTP (Auth App)</h2>
                <p>Google Authenticator</p>
                <h3>1. Setup</h3>
                <input type="text" id="totp-id" placeholder="Username / ID">
                <button onclick="generate_totp()">Generate Secret & QR</button>
                <p id="secret" style="word-break: break-all; color: #666; font-size: 12px;"></p>
                <img id="qr" src="" />
        
                <div id="totp-verify-section" style="display:none;">
                    <h3>2. Verify</h3>
                    <input type="text" id="totp-code" placeholder="6-digit Authenticator Code">
                    <button onclick="verify_totp()">Verify TOTP</button>
                </div>
            </div>
        </div>
        
        <script>
            // Compatibility Wrapper for the raw script tags above which python might handle poorly if I don't treat them right
            // Re-declaring functions properly in JS context
            
            async function generate_totp() {
                const id = document.getElementById("totp-id").value;
                if(!id) return alert("Identifier required");
                try {
                     const response = await fetch("/totp/enable", {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify({identifier: id})
                    });
                    const data = await response.json();
                    document.getElementById("secret").innerText = "Secret: " + data.secret;
                    document.getElementById("qr").src = "data:image/png;base64," + data.qr_code_base64;
                    document.getElementById("totp-verify-section").style.display = "block";
                } catch(e) { alert(e); }
            }
            
            async function verify_totp() {
                const id = document.getElementById("totp-id").value;
                const code = document.getElementById("totp-code").value;
                try {
                    const response = await fetch("/totp/verify", {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify({identifier: id, totp_code: code})
                    });
                    const data = await response.json();
                    if(response.ok) alert("✅ SUCCESS: " + data.message);
                    else alert("❌ ERROR: " + data.detail);
                } catch(e) { alert(e); }
            }
        </script>
    </body>
    </html>
    """
