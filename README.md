# AymGprek OTP Service 🔐

A comprehensive Multi-Channel OTP (One-Time Password) Service built with **FastAPI** (Python) and **Node.js**.

## 🚀 Features

1.  **Email OTP**:  Sends HTML-formatted OTPs via SMTP (Gmail, etc.).
2.  **WhatsApp OTP**: Sends OTPs via WhatsApp Web using a local gateway (Baileys/Whatsapp-Web.js).
3.  **SMS OTP**: Hardware-based SMS sending (via connected modem/gateway endpoint).
4.  **TOTP (Google Authenticator)**: Generates 2FA secrets and Stylized QR Codes (Instagram-style) for authenticator apps.

---

## 🛠️ Prerequisites

-   **Python 3.10+** (for Backend)
-   **Node.js & NPM** (for WhatsApp Gateway)
    -   *Windows Users*: Must install Node.js inside **WSL** (`sudo apt install nodejs npm`) to avoid path errors.

---

## 📦 Installation

### 1. Backend (Python/FastAPI)

```bash
# Navigate to project root
cd backend/OTP

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. WhatsApp Gateway (Node.js)

```bash
# Navigate to gateway folder
cd backend/OTP/wa-gateway

# Install dependencies (do this inside WSL!)
npm install
```

---

## ⚙️ Configuration (.env)

Create a `.env` file in the `backend/OTP` directory:

```env
APP_NAME="AymGprek OTP"
OTP_LENGTH=6
OTP_EXPIRY_SECONDS=300
DEBUG_MODE=True

# --- WhatsApp Gateway ---
WA_GATEWAY_URL="http://localhost:3000/send"

# --- SMS Gateway (Hardware) ---
SMS_GATEWAY_URL="http://192.168.100.47:8082"
SMS_GATEWAY_API_KEY="your-api-key"

# --- Email OTP (SMTP) ---
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=emailmu@gmail.com
SMTP_PASSWORD="app-password-16-digit"
SMTP_FROM_EMAIL=emailmu@gmail.com
```

---

## ▶️ Running the Service

You need to run **both** the Backend and the WA Gateway (if using WhatsApp).

### 1. Start WhatsApp Gateway (Port 3000)
```bash
cd backend/OTP/wa-gateway
npm start
```
*Scan the QR code that appears in the terminal with your WhatsApp.*

### 2. Start Backend Server (Port 8000)
Open a new terminal tab:
```bash
cd backend/OTP
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🎮 Demo & Testing

Access the **Unified Demo Dashboard** to test all OTP methods:

👉 **http://localhost:8000/demo/totp**

-   **Standard OTP**: Test sending via Email, SMS, or WhatsApp.
-   **TOTP Setup**: Generate QR Code for Google Authenticator.
-   **TOTP Verify**: Verify the 6-digit code from the app.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/send-email-otp` | Send OTP via Email |
| `POST` | `/send-otp` | Send OTP via WhatsApp (Default) |
| `POST` | `/send-sms-otp` | Send OTP via SMS |
| `POST` | `/verify-otp` | Verify Email/SMS/WA OTP |
| `POST` | `/totp/enable` | Generate TOTP Secret & QR |
| `POST` | `/totp/verify` | Verify Time-based OTP |
