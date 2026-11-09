# 📚 GABRIEL API DOCUMENTATION - 100% PERFECT
**Complete API Reference**
GORUNFREE Protocol

---

## 🌐 BASE URL

```
Production: https://api.gabriel.noizylab.com
Development: http://localhost:8000
```

---

## 🔐 AUTHENTICATION

### **JWT Authentication**

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <token>
```

### **Get Token**

```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

---

## 🎤 VOICE AI ENDPOINTS

### **List Services**

```http
GET /api/services
```

**Response:**
```json
{
  "services": [
    {
      "id": "gtts",
      "name": "Google TTS (gTTS)",
      "available": true
    },
    {
      "id": "edge",
      "name": "Microsoft Edge TTS",
      "available": true
    }
  ]
}
```

### **Generate Voice**

```http
POST /api/generate
Authorization: Bearer <token>
Content-Type: application/json

{
  "text": "Hello, world!",
  "service": "gtts",
  "voice": null,
  "language": "en",
  "apply_effects": true
}
```

**Response:**
- Content-Type: `audio/mpeg`
- File download with generated audio

### **Batch Generate**

```http
POST /api/batch
Authorization: Bearer <token>
Content-Type: application/json

{
  "texts": [
    "First text",
    "Second text",
    "Third text"
  ],
  "service": "gtts",
  "language": "en"
}
```

**Response:**
```json
{
  "success": true,
  "generated": 3,
  "total": 3,
  "files": [
    {
      "index": 0,
      "text": "First text",
      "file": "/path/to/voice_000.mp3"
    }
  ]
}
```

---

## 🏥 HEALTH ENDPOINTS

### **Health Check**

```http
GET /health
```

**Response:**
```json
{
  "status": "alive",
  "version": "2.0.0",
  "timestamp": "2025-12-24T17:00:00Z"
}
```

### **Readiness Check**

```http
GET /health/ready
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-24T17:00:00Z",
  "version": "2.0.0",
  "checks": {
    "database": {
      "status": "healthy",
      "latency_ms": 5
    },
    "redis": {
      "status": "healthy",
      "latency_ms": 2
    }
  }
}
```

---

## 📊 MONITORING ENDPOINTS

### **Prometheus Metrics**

```http
GET /metrics
```

**Response:**
```
# Prometheus format
voice_generations_total{service="gtts",status="success"} 100
api_requests_total{method="POST",endpoint="/api/generate",status="200"} 50
```

---

## ⚠️ ERROR RESPONSES

### **Validation Error (400)**

```json
{
  "error": true,
  "code": "VALIDATION_ERROR",
  "message": "Validation failed",
  "details": {
    "errors": [
      {
        "field": "text",
        "message": "Text cannot be empty",
        "type": "value_error"
      }
    ]
  }
}
```

### **Authentication Error (401)**

```json
{
  "error": true,
  "code": "AUTHENTICATION_ERROR",
  "message": "Authentication failed",
  "details": {}
}
```

### **Rate Limit Error (429)**

```json
{
  "error": true,
  "code": "RATE_LIMIT_EXCEEDED",
  "message": "Rate limit exceeded",
  "details": {
    "retry_after": 60
  }
}
```

---

## 🔗 OPENAPI DOCUMENTATION

Interactive API documentation available at:
- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI JSON: `/openapi.json`

---

**GORUNFREE!** 🚀

