# 💻 GABRIEL CODE EXAMPLES - 100% PERFECT
**Complete Code Examples**
GORUNFREE Protocol

---

## 🎤 VOICE AI EXAMPLES

### **Basic Voice Generation:**
```python
from GABRIEL.core.voice_ai_universal_improved import UniversalVoiceAI

# Initialize
voice_ai = UniversalVoiceAI()

# Generate voice
result = voice_ai.generate(
    text="Hello, world!",
    service="gtts",
    language="en"
)
print(f"Generated: {result}")
```

### **Batch Generation:**
```python
texts = [
    "First text",
    "Second text",
    "Third text"
]

results = []
for text in texts:
    result = voice_ai.generate(text, service="edge")
    results.append(result)
```

### **With Error Handling:**
```python
from GABRIEL.infrastructure.errors.exceptions import VoiceGenerationError

try:
    result = voice_ai.generate(
        text="Hello!",
        service="elevenlabs",
        voice="voice_id_123"
    )
except VoiceGenerationError as e:
    print(f"Error: {e.message}")
```

---

## 🔐 AUTHENTICATION EXAMPLES

### **Create Token:**
```python
from GABRIEL.infrastructure.auth.jwt_auth import create_access_token

data = {
    "sub": 1,
    "email": "user@example.com",
    "role": "user"
}
token = create_access_token(data)
```

### **Verify Token:**
```python
from GABRIEL.infrastructure.auth.jwt_auth import verify_token

payload = verify_token(token)
if payload:
    user_id = payload["sub"]
    email = payload["email"]
```

### **Hash Password:**
```python
from GABRIEL.infrastructure.auth.password import hash_password, verify_password

# Hash
hashed = hash_password("my_password")

# Verify
is_valid = verify_password("my_password", hashed)
```

---

## 💾 DATABASE EXAMPLES

### **Create User:**
```python
from GABRIEL.infrastructure.database.schema import User, UserRole
from sqlalchemy.orm import Session

user = User(
    email="user@example.com",
    username="user",
    hashed_password=hash_password("password"),
    role=UserRole.CLIENT
)
db_session.add(user)
db_session.commit()
```

### **Query Users:**
```python
from GABRIEL.infrastructure.database.schema import User

# Get user by email
user = db_session.query(User).filter(User.email == "user@example.com").first()

# Get all voice actors
actors = db_session.query(VoiceActor).all()
```

---

## 📦 STORAGE EXAMPLES

### **Upload File:**
```python
from GABRIEL.infrastructure.storage import get_storage

storage = get_storage()
url = storage.upload_file(
    file_path="local_file.mp3",
    key="voices/user123/voice.mp3",
    content_type="audio/mpeg"
)
```

### **Download File:**
```python
storage.download_file(
    key="voices/user123/voice.mp3",
    file_path="downloaded.mp3"
)
```

---

## 💳 PAYMENT EXAMPLES

### **Create Payment Intent:**
```python
from GABRIEL.infrastructure.payments.stripe_integration import StripePayment

stripe = StripePayment()
intent = stripe.create_payment_intent(
    amount=10.00,
    currency="usd",
    customer_id="cus_123",
    metadata={"license_id": "123"}
)
```

### **Handle Webhook:**
```python
event = stripe.handle_webhook(payload, signature)

if event["type"] == "payment_intent.succeeded":
    payment_id = event["data"]["object"]["id"]
    # Process payment
```

---

## 📧 EMAIL EXAMPLES

### **Send Email:**
```python
from GABRIEL.infrastructure.email import send_email

send_email(
    to_email="user@example.com",
    subject="Welcome!",
    body="Welcome to GABRIEL!",
    html_body="<h1>Welcome!</h1>"
)
```

### **Send Welcome Email:**
```python
from GABRIEL.infrastructure.email import send_welcome_email

send_welcome_email(
    to_email="user@example.com",
    name="John Doe"
)
```

---

## 📬 TASK QUEUE EXAMPLES

### **Queue Voice Generation:**
```python
from GABRIEL.infrastructure.queue import generate_voice_task

# Queue task
task = generate_voice_task.delay(
    text="Hello, world!",
    service="gtts",
    language="en"
)

# Get result
result = task.get(timeout=30)
```

### **Queue Voice Training:**
```python
from GABRIEL.infrastructure.queue import process_voice_training

task = process_voice_training.delay(
    actor_id=1,
    audio_file_path="/path/to/audio.mp3",
    voice_name="My Voice"
)
```

---

## 🌐 API EXAMPLES

### **Python Requests:**
```python
import requests

# Get token
response = requests.post(
    "http://localhost:8000/api/auth/login",
    json={"email": "user@example.com", "password": "password"}
)
token = response.json()["access_token"]

# Generate voice
response = requests.post(
    "http://localhost:8000/api/generate",
    headers={"Authorization": f"Bearer {token}"},
    json={"text": "Hello!", "service": "gtts"}
)
```

### **JavaScript Fetch:**
```javascript
// Get token
const loginResponse = await fetch('http://localhost:8000/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email: 'user@example.com', password: 'password' })
});
const { access_token } = await loginResponse.json();

// Generate voice
const generateResponse = await fetch('http://localhost:8000/api/generate', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${access_token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ text: 'Hello!', service: 'gtts' })
});
const audioBlob = await generateResponse.blob();
```

---

## 🔍 MONITORING EXAMPLES

### **Log Performance:**
```python
from GABRIEL.infrastructure.logging import get_logger

logger = get_logger("my_module")
logger.info("operation_completed", duration_ms=150, operation="voice_generation")
```

### **Record Metrics:**
```python
from GABRIEL.infrastructure.monitoring.metrics import record_voice_generation

record_voice_generation(
    service="gtts",
    status="success",
    duration=0.5
)
```

---

## 🧪 TESTING EXAMPLES

### **Unit Test:**
```python
import pytest
from GABRIEL.core.voice_ai_universal_improved import UniversalVoiceAI

def test_generate_voice():
    voice_ai = UniversalVoiceAI()
    result = voice_ai.generate("Hello!", service="gtts")
    assert result is not None
```

### **Integration Test:**
```python
from fastapi.testclient import TestClient
from GABRIEL.api.voice_ai_api_server_perfect import app

client = TestClient(app)

def test_api_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
```

---

**GORUNFREE!** 🚀

---

**Last Updated:** December 24, 2025

