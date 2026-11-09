# ☸️ KUBERNETES DEPLOYMENT - 100% PERFECT
**Complete Kubernetes Setup**
GORUNFREE Protocol

---

## 📋 FILES

- `deployment.yaml` - API deployment
- `celery-worker.yaml` - Worker deployment
- `postgres.yaml` - PostgreSQL StatefulSet
- `redis.yaml` - Redis deployment
- `ingress.yaml` - Ingress configuration

---

## 🚀 QUICK START

### **1. Create Namespace:**
```bash
kubectl create namespace gabriel
```

### **2. Create Secrets:**
```bash
kubectl create secret generic gabriel-secrets \
  --from-literal=database-url=postgresql://... \
  --from-literal=postgres-password=... \
  --from-literal=redis-url=redis://... \
  --from-literal=jwt-secret-key=... \
  -n gabriel
```

### **3. Deploy:**
```bash
kubectl apply -f postgres.yaml
kubectl apply -f redis.yaml
kubectl apply -f deployment.yaml
kubectl apply -f celery-worker.yaml
kubectl apply -f ingress.yaml
```

### **4. Check Status:**
```bash
kubectl get all -n gabriel
```

---

## 🔧 CONFIGURATION

### **Scaling:**
```bash
kubectl scale deployment gabriel-api --replicas=5 -n gabriel
kubectl scale deployment gabriel-worker --replicas=3 -n gabriel
```

### **Updates:**
```bash
kubectl set image deployment/gabriel-api \
  api=gabriel:new-version \
  -n gabriel
```

---

**GORUNFREE!** 🚀

