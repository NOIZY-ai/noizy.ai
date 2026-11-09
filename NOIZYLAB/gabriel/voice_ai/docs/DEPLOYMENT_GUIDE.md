# 🚀 GABRIEL DEPLOYMENT GUIDE - 100% PERFECT
**Complete Deployment Instructions**
GORUNFREE Protocol

---

## 📋 PREREQUISITES

### **Required:**
- Docker & docker-compose
- PostgreSQL 16+
- Redis 7+
- Python 3.12+
- Git

### **Optional:**
- Kubernetes cluster
- Cloudflare R2 or AWS S3
- Stripe account
- SMTP server

---

## 🐳 DOCKER DEPLOYMENT

### **1. Clone Repository:**
```bash
git clone <repository-url>
cd GABRIEL
```

### **2. Set Environment Variables:**
```bash
cp .env.example .env
# Edit .env with your values
```

### **3. Start Services:**
```bash
docker-compose up -d
```

### **4. Run Migrations:**
```bash
docker-compose exec api alembic upgrade head
```

### **5. Verify:**
```bash
curl http://localhost:8000/health
```

---

## ☸️ KUBERNETES DEPLOYMENT

### **1. Create Namespace:**
```bash
kubectl create namespace gabriel
```

### **2. Create Secrets:**
```bash
kubectl create secret generic gabriel-secrets \
  --from-literal=database-url=postgresql://... \
  --from-literal=jwt-secret-key=... \
  --from-literal=redis-url=redis://... \
  -n gabriel
```

### **3. Apply Configs:**
```bash
kubectl apply -f k8s/ -n gabriel
```

### **4. Check Status:**
```bash
kubectl get pods -n gabriel
kubectl get services -n gabriel
```

---

## 🔧 MANUAL DEPLOYMENT

### **1. Install Dependencies:**
```bash
pip install -r infrastructure/requirements.txt
```

### **2. Set Environment Variables:**
```bash
export DATABASE_URL="postgresql://user:pass@localhost/gabriel"
export REDIS_URL="redis://localhost:6379/0"
export JWT_SECRET_KEY="your-secret-key"
```

### **3. Initialize Database:**
```bash
alembic upgrade head
```

### **4. Start Services:**
```bash
# Start Redis
redis-server

# Start PostgreSQL
# (system dependent)

# Start API
uvicorn api.voice_ai_api_server_perfect:app --host 0.0.0.0 --port 8000

# Start Celery workers
celery -A infrastructure.queue.celery_tasks worker --loglevel=info
```

---

## 🔐 SECURITY SETUP

### **1. Generate Secrets:**
```bash
# JWT Secret
openssl rand -hex 32

# Database Password
openssl rand -base64 32
```

### **2. Configure HTTPS:**
- Use reverse proxy (nginx/traefik)
- Configure SSL certificates
- Enable HSTS

### **3. Firewall Rules:**
- Only expose necessary ports
- Restrict database access
- Use VPN for admin access

---

## 📊 MONITORING SETUP

### **1. Prometheus:**
```bash
docker run -d -p 9090:9090 prom/prometheus
```

### **2. Grafana:**
```bash
docker run -d -p 3000:3000 grafana/grafana
```

### **3. Configure:**
- Add Prometheus data source
- Import GABRIEL dashboards
- Set up alerts

---

## ✅ VERIFICATION

### **Health Checks:**
```bash
# Liveness
curl http://localhost:8000/health

# Readiness
curl http://localhost:8000/health/ready

# Metrics
curl http://localhost:8000/metrics
```

### **API Test:**
```bash
# Get token
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test"}' \
  | jq -r '.access_token')

# Test endpoint
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/services
```

---

## 🔄 UPDATES & MAINTENANCE

### **Update Application:**
```bash
git pull
docker-compose build
docker-compose up -d
alembic upgrade head
```

### **Backup Database:**
```bash
pg_dump -h localhost -U gabriel gabriel > backup.sql
```

### **Restore Database:**
```bash
psql -h localhost -U gabriel gabriel < backup.sql
```

---

## 🐛 TROUBLESHOOTING

### **Database Connection Issues:**
- Check DATABASE_URL
- Verify PostgreSQL is running
- Check firewall rules

### **Redis Connection Issues:**
- Check REDIS_URL
- Verify Redis is running
- Check network connectivity

### **API Not Starting:**
- Check logs: `docker-compose logs api`
- Verify environment variables
- Check port availability

---

**GORUNFREE!** 🚀

---

**Last Updated:** December 24, 2025

