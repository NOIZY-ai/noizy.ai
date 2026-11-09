# 🔧 GABRIEL TROUBLESHOOTING GUIDE - 100% PERFECT
**Complete Troubleshooting Reference**
GORUNFREE Protocol

---

## 🐛 COMMON ISSUES

### **1. Database Connection Failed**

**Symptoms:**
- `OperationalError: could not connect to server`
- `Connection refused`

**Solutions:**
```bash
# Check PostgreSQL is running
pg_isready

# Check connection string
echo $DATABASE_URL

# Test connection
psql $DATABASE_URL -c "SELECT 1"

# Restart PostgreSQL
sudo systemctl restart postgresql
```

---

### **2. Redis Connection Failed**

**Symptoms:**
- `ConnectionError: Error connecting to Redis`
- `Connection refused`

**Solutions:**
```bash
# Check Redis is running
redis-cli ping

# Check connection string
echo $REDIS_URL

# Test connection
redis-cli -u $REDIS_URL ping

# Restart Redis
sudo systemctl restart redis
```

---

### **3. Authentication Errors**

**Symptoms:**
- `401 Unauthorized`
- `Could not validate credentials`

**Solutions:**
```bash
# Check JWT secret key
echo $JWT_SECRET_KEY

# Verify token
python3 -c "from infrastructure.auth.jwt_auth import verify_token; print(verify_token('your_token'))"

# Check token expiration
# Tokens expire after 30 minutes by default
```

---

### **4. Voice Generation Fails**

**Symptoms:**
- `VoiceGenerationError`
- `Service not available`

**Solutions:**
```bash
# Check service availability
python3 -c "from core.voice_ai_universal_improved import UniversalVoiceAI; ai = UniversalVoiceAI(); print(ai.list_services())"

# Check API keys
echo $ELEVENLABS_API_KEY
echo $AZURE_SPEECH_KEY

# Test service directly
python3 core/voice_ai_universal_improved.py --generate "test" --service gtts
```

---

### **5. Rate Limit Exceeded**

**Symptoms:**
- `429 Too Many Requests`
- `Rate limit exceeded`

**Solutions:**
```bash
# Check rate limit settings
grep RATE_LIMIT infrastructure/config.py

# Increase limits (if needed)
export RATE_LIMIT_PER_MINUTE=120

# Wait for reset (default: 60 seconds)
```

---

### **6. File Storage Errors**

**Symptoms:**
- `Upload failed`
- `Storage not configured`

**Solutions:**
```bash
# Check storage type
echo $STORAGE_TYPE

# Check R2 credentials
echo $CLOUDFLARE_R2_ACCOUNT_ID
echo $CLOUDFLARE_R2_ACCESS_KEY_ID

# Test storage
python3 -c "from infrastructure.storage import get_storage; s = get_storage(); print(s)"
```

---

### **7. Docker Issues**

**Symptoms:**
- `Cannot connect to Docker daemon`
- `Container failed to start`

**Solutions:**
```bash
# Check Docker is running
docker ps

# Check logs
docker-compose logs api

# Restart services
docker-compose restart

# Rebuild images
docker-compose build --no-cache
```

---

### **8. Kubernetes Issues**

**Symptoms:**
- `Pod not starting`
- `ImagePullBackOff`

**Solutions:**
```bash
# Check pod status
kubectl get pods -n gabriel

# Check logs
kubectl logs -n gabriel deployment/gabriel-api

# Check events
kubectl get events -n gabriel

# Restart deployment
kubectl rollout restart deployment/gabriel-api -n gabriel
```

---

## 🔍 DEBUGGING

### **Enable Debug Mode:**
```bash
export DEBUG=true
export ENVIRONMENT=development
```

### **Check Logs:**
```bash
# Application logs
tail -f logs/gabriel.log

# Docker logs
docker-compose logs -f api

# Kubernetes logs
kubectl logs -f deployment/gabriel-api -n gabriel
```

### **Test Components:**
```bash
# Test database
python3 -c "from infrastructure.database.schema import User; print('DB OK')"

# Test Redis
python3 -c "from infrastructure.cache.redis_cache import get_redis_client; r = get_redis_client(); print(r.ping())"

# Test authentication
python3 -c "from infrastructure.auth.jwt_auth import create_access_token; print(create_access_token({'sub': 1}))"
```

---

## 📊 HEALTH CHECKS

### **Check All Services:**
```bash
# Health endpoint
curl http://localhost:8000/health

# Readiness endpoint
curl http://localhost:8000/health/ready

# Metrics endpoint
curl http://localhost:8000/metrics
```

---

## 🔐 SECURITY ISSUES

### **CORS Errors:**
```bash
# Check CORS configuration
grep CORS_ORIGINS infrastructure/config.py

# Add origin to allowed list
export CORS_ORIGINS='["http://localhost:3000","https://yourdomain.com"]'
```

### **SSL/TLS Issues:**
```bash
# Check certificate
openssl s_client -connect api.gabriel.noizylab.com:443

# Verify HTTPS redirect
curl -I http://api.gabriel.noizylab.com
```

---

## 🚀 PERFORMANCE ISSUES

### **Slow API Responses:**
```bash
# Check metrics
curl http://localhost:8000/metrics | grep api_request_duration

# Check database queries
# Enable query logging in SQLAlchemy

# Check cache hit rate
curl http://localhost:8000/metrics | grep cache
```

### **High Memory Usage:**
```bash
# Check container resources
docker stats

# Check Kubernetes resources
kubectl top pods -n gabriel

# Scale up if needed
kubectl scale deployment gabriel-api --replicas=5 -n gabriel
```

---

## 📞 SUPPORT

### **Get Help:**
1. Check logs first
2. Review documentation
3. Check GitHub issues
4. Contact support

### **Report Issues:**
- Include error messages
- Include logs
- Include configuration (sanitized)
- Include steps to reproduce

---

**GORUNFREE!** 🚀

---

**Last Updated:** December 24, 2025

