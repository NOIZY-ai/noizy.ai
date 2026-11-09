#!/bin/bash
# PASTE THIS ENTIRE BLOCK INTO TERMINAL ON GOD - ONE COMMAND INSTALL

cat > ~/api_token_vault.py << 'VAULT_EOF'
#!/usr/bin/env python3
"""
API TOKEN VAULT v2.0 - GORUNFREE EDITION
Secure • Encrypted • Cloud-Synced • Voice-Ready
"""

import os, sys, json, base64, hashlib, subprocess, requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List
from dataclasses import dataclass, asdict

CF_ACCOUNT_ID = "2446d788cc4280f5ea22a9948410c355"
CF_KV_NAMESPACE = "c453c1b2d5e84a17bf7282cf427f8301"

SERVICE_VALIDATORS = {
    "anthropic": {
        "url": "https://api.anthropic.com/v1/messages",
        "method": "POST",
        "headers": lambda token: {"x-api-key": token, "anthropic-version": "2023-06-01", "content-type": "application/json"},
        "body": {"model": "claude-3-haiku-20240307", "max_tokens": 1, "messages": [{"role": "user", "content": "hi"}]},
        "success_codes": [200, 400, 429]
    },
    "openai": {
        "url": "https://api.openai.com/v1/models",
        "method": "GET",
        "headers": lambda token: {"Authorization": f"Bearer {token}"},
        "success_codes": [200, 429]
    },
    "cloudflare": {
        "url": "https://api.cloudflare.com/client/v4/user/tokens/verify",
        "method": "GET",
        "headers": lambda token: {"Authorization": f"Bearer {token}"},
        "success_codes": [200]
    },
    "github": {
        "url": "https://api.github.com/user",
        "method": "GET",
        "headers": lambda token: {"Authorization": f"Bearer {token}"},
        "success_codes": [200]
    },
    "elevenlabs": {
        "url": "https://api.elevenlabs.io/v1/user",
        "method": "GET",
        "headers": lambda token: {"xi-api-key": token},
        "success_codes": [200]
    },
    "stripe": {
        "url": "https://api.stripe.com/v1/balance",
        "method": "GET",
        "headers": lambda token: {"Authorization": f"Bearer {token}"},
        "success_codes": [200]
    }
}

@dataclass
class TokenRecord:
    name: str
    token_encrypted: str
    service: str = ""
    description: str = ""
    tags: List[str] = None
    created_at: str = ""
    updated_at: str = ""
    expires_at: Optional[str] = None
    last_used: Optional[str] = None
    last_checked: Optional[str] = None
    last_check_status: str = "unknown"
    use_count: int = 0
    
    def __post_init__(self):
        if self.tags is None: self.tags = []
        if not self.created_at: self.created_at = datetime.now().isoformat()
        if not self.updated_at: self.updated_at = datetime.now().isoformat()

class Encryptor:
    def __init__(self, password: str = None):
        if password is None:
            machine_id = self._get_machine_id()
            password = f"vault:{machine_id}:{os.getenv('USER', 'default')}"
        self.key = hashlib.pbkdf2_hmac('sha256', password.encode(), b'api-token-vault-salt-v2', 100000)
    
    def _get_machine_id(self) -> str:
        try:
            result = subprocess.run(["ioreg", "-rd1", "-c", "IOPlatformExpertDevice"], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if 'IOPlatformUUID' in line: return line.split('"')[-2]
        except: pass
        return hashlib.sha256(f"{os.getenv('HOME', '')}{os.getenv('USER', '')}".encode()).hexdigest()[:32]
    
    def encrypt(self, plaintext: str) -> str:
        data = plaintext.encode()
        key_stream = (self.key * ((len(data) // len(self.key)) + 1))[:len(data)]
        encrypted = bytes(a ^ b for a, b in zip(data, key_stream))
        return f"v2:{base64.b64encode(encrypted).decode()}"
    
    def decrypt(self, ciphertext: str) -> str:
        if ciphertext.startswith("v2:"):
            encrypted = base64.b64decode(ciphertext[3:])
            key_stream = (self.key * ((len(encrypted) // len(self.key)) + 1))[:len(encrypted)]
            return bytes(a ^ b for a, b in zip(encrypted, key_stream)).decode()
        elif ciphertext.startswith("v1:"): return base64.b64decode(ciphertext[3:]).decode()
        return ciphertext

class CloudflareKV:
    def __init__(self):
        self.token = self._get_token()
        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/storage/kv/namespaces/{CF_KV_NAMESPACE}"
        self.headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
    
    def _get_token(self) -> str:
        token = os.environ.get("CLOUDFLARE_API_TOKEN")
        if token: return token
        for path in [Path.home() / ".config" / "cloudflare" / "token", Path.home() / ".cloudflare_token"]:
            if path.exists(): return path.read_text().strip()
        env_path = Path.home() / ".env"
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                if line.startswith("CLOUDFLARE_API_TOKEN="): return line.split("=", 1)[1].strip().strip('"\'')
        return None
    
    def put(self, key: str, value: dict) -> bool:
        r = requests.put(f"{self.base_url}/values/{key}", headers=self.headers, data=json.dumps(value))
        return r.status_code == 200
    
    def get(self, key: str) -> Optional[dict]:
        r = requests.get(f"{self.base_url}/values/{key}", headers=self.headers)
        if r.status_code == 200:
            try: return r.json()
            except: return {"raw": r.text}
        return None
    
    def delete(self, key: str) -> bool:
        return requests.delete(f"{self.base_url}/values/{key}", headers=self.headers).status_code == 200
    
    def list_keys(self, prefix: str = "") -> List[str]:
        url = f"{self.base_url}/keys" + (f"?prefix={prefix}" if prefix else "")
        r = requests.get(url, headers=self.headers)
        if r.status_code == 200: return [k["name"] for k in r.json().get("result", [])]
        return []

class TokenVault:
    def __init__(self):
        self.kv = CloudflareKV()
        self.encryptor = Encryptor()
        if not self.kv.token:
            print("⚠️  CLOUDFLARE_API_TOKEN not set"); print("   echo 'YOUR_TOKEN' > ~/.config/cloudflare/token"); sys.exit(1)
    
    def _detect_service(self, name: str, token: str) -> str:
        name_lower = name.lower()
        for svc in SERVICE_VALIDATORS.keys():
            if svc in name_lower: return svc
        if token.startswith("sk-ant-"): return "anthropic"
        elif token.startswith("sk-"): return "openai"
        elif token.startswith("ghp_") or token.startswith("gho_"): return "github"
        elif token.startswith("sk_live_") or token.startswith("sk_test_"): return "stripe"
        return ""
    
    def add(self, name: str, token: str, description: str = "", expires: str = None, tags: List[str] = None) -> bool:
        service = self._detect_service(name, token)
        record = TokenRecord(name=name, token_encrypted=self.encryptor.encrypt(token), service=service, description=description, tags=tags or [], expires_at=expires)
        key = f"token:{name.lower()}"
        success = self.kv.put(key, asdict(record))
        if success:
            masked = f"{token[:8]}...{token[-4:]}" if len(token) > 12 else token[:4] + "..."
            print(f"✅ Stored: {name}"); print(f"   Service: {service or 'unknown'}"); print(f"   Preview: {masked}")
        else: print(f"❌ Failed: {name}")
        return success
    
    def get(self, name: str, full: bool = False) -> Optional[str]:
        key = f"token:{name.lower()}"
        data = self.kv.get(key)
        if not data: print(f"❌ Token '{name}' not found"); return None
        token = self.encryptor.decrypt(data.get("token_encrypted", ""))
        data["last_used"] = datetime.now().isoformat(); data["use_count"] = data.get("use_count", 0) + 1
        self.kv.put(key, data)
        if full: return token
        return f"{token[:8]}...{token[-4:]}" if len(token) > 12 else token[:4] + "..."
    
    def copy(self, name: str) -> bool:
        token = self.get(name, full=True)
        if not token: return False
        try: subprocess.run(["pbcopy"], input=token.encode(), check=True); print(f"✅ {name} → clipboard"); return True
        except: print(f"❌ Clipboard failed"); return False
    
    def list_all(self, tag: str = None, expiring: bool = False) -> List[dict]:
        keys = self.kv.list_keys("token:")
        tokens = []
        now = datetime.now()
        for key in keys:
            data = self.kv.get(key)
            if not data: continue
            name = data.get("name", key.replace("token:", ""))
            if tag and tag not in data.get("tags", []): continue
            status = "active"
            exp = data.get("expires_at")
            if exp:
                try:
                    exp_date = datetime.fromisoformat(exp)
                    if exp_date < now: status = "expired"
                    elif exp_date < now + timedelta(days=14): status = "expiring_soon"
                except: pass
            if expiring and status not in ["expiring_soon", "expired"]: continue
            tokens.append({"name": name, "service": data.get("service", ""), "status": status, "tags": data.get("tags", []), "expires_at": exp, "last_used": data.get("last_used"), "use_count": data.get("use_count", 0), "last_check_status": data.get("last_check_status", "unknown")})
        return sorted(tokens, key=lambda x: x["name"])
    
    def delete(self, name: str) -> bool:
        success = self.kv.delete(f"token:{name.lower()}")
        print(f"{'✅ Deleted' if success else '❌ Failed'}: {name}"); return success
    
    def check(self, name: str) -> str:
        key = f"token:{name.lower()}"
        data = self.kv.get(key)
        if not data: print(f"❌ Token '{name}' not found"); return "not_found"
        service = data.get("service", "")
        if service not in SERVICE_VALIDATORS: print(f"⚠️  No validator: {service or 'unknown'}"); return "no_validator"
        token = self.encryptor.decrypt(data.get("token_encrypted", ""))
        validator = SERVICE_VALIDATORS[service]
        print(f"🔍 Checking {name} ({service})...", end=" ", flush=True)
        try:
            headers = validator["headers"](token)
            if validator["method"] == "GET": r = requests.get(validator["url"], headers=headers, timeout=10)
            else: r = requests.post(validator["url"], headers=headers, json=validator.get("body", {}), timeout=10)
            status = "valid" if r.status_code in validator["success_codes"] else "invalid"
        except Exception as e: status = "error"; print(f"Error: {e}")
        data["last_checked"] = datetime.now().isoformat(); data["last_check_status"] = status
        self.kv.put(key, data)
        print(f"{'✅' if status=='valid' else '❌' if status=='invalid' else '⚠️'} {status.upper()}")
        return status
    
    def check_all(self) -> dict:
        tokens = self.list_all()
        results = {"valid": 0, "invalid": 0, "error": 0, "skipped": 0}
        print(f"\n🔍 Checking {len(tokens)} tokens...\n")
        for t in tokens:
            if not t["service"] or t["service"] not in SERVICE_VALIDATORS:
                print(f"⏭️  Skipping {t['name']}"); results["skipped"] += 1; continue
            status = self.check(t["name"])
            if status in results: results[status] += 1
        print(f"\n📊 {results['valid']} valid, {results['invalid']} invalid, {results['error']} errors, {results['skipped']} skipped")
        return results
    
    def rotate(self, name: str, new_token: str) -> bool:
        key = f"token:{name.lower()}"
        data = self.kv.get(key)
        if not data: print(f"❌ Token '{name}' not found"); return False
        data["token_encrypted"] = self.encryptor.encrypt(new_token)
        data["updated_at"] = datetime.now().isoformat(); data["last_check_status"] = "unknown"
        success = self.kv.put(key, data)
        if success:
            masked = f"{new_token[:8]}...{new_token[-4:]}" if len(new_token) > 12 else new_token[:4] + "..."
            print(f"🔄 Rotated: {name}"); print(f"   New: {masked}")
        return success
    
    def inject(self, shell: bool = False) -> str:
        tokens = self.list_all()
        lines = []
        for t in tokens:
            token = self.get(t["name"], full=True)
            if not token: continue
            env_name = f"API_{t['name'].upper().replace('-', '_')}"
            lines.append(f'export {env_name}="{token}"' if shell else f"{env_name}={token}")
        output = "\n".join(lines)
        if shell: print("# eval $(vault inject --shell)")
        print(output); return output
    
    def backup(self, filepath: str = None) -> str:
        if not filepath: filepath = f"token_vault_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json.enc"
        keys = self.kv.list_keys("token:")
        backup_data = [self.kv.get(k) for k in keys if self.kv.get(k)]
        encrypted = self.encryptor.encrypt(json.dumps(backup_data, indent=2))
        Path(filepath).write_text(encrypted)
        print(f"✅ Backup: {filepath} ({len(backup_data)} tokens)"); return filepath
    
    def restore(self, filepath: str) -> int:
        if not Path(filepath).exists(): print(f"❌ Not found: {filepath}"); return 0
        try:
            backup_data = json.loads(self.encryptor.decrypt(Path(filepath).read_text()))
        except Exception as e: print(f"❌ Decrypt failed: {e}"); return 0
        restored = sum(1 for r in backup_data if r.get("name") and self.kv.put(f"token:{r['name'].lower()}", r) and print(f"✅ Restored: {r['name']}") is None)
        print(f"\n📊 Restored {restored}/{len(backup_data)}"); return restored

def print_table(tokens):
    if not tokens: print("No tokens"); return
    print(f"\n{'NAME':<20} {'SERVICE':<12} {'STATUS':<10} {'USES':<6} {'LAST USED':<12}"); print("─" * 70)
    icons = {"active": "🟢", "expiring_soon": "🟡", "expired": "🔴", "invalid": "❌", "unknown": "⚪"}
    for t in tokens:
        lu = t["last_used"][:10] if t["last_used"] else "never"
        print(f"{t['name']:<20} {t['service'] or '-':<12} {icons.get(t['status'], '⚪')} {t['status']:<8} {t['use_count']:<6} {lu:<12}")
    print(f"\nTotal: {len(tokens)}")

def main():
    import argparse
    p = argparse.ArgumentParser(description="API Token Vault")
    sp = p.add_subparsers(dest="cmd")
    a = sp.add_parser("add"); a.add_argument("name"); a.add_argument("token"); a.add_argument("--desc", "-d", default=""); a.add_argument("--expires", "-e"); a.add_argument("--tags", "-t")
    g = sp.add_parser("get"); g.add_argument("name"); g.add_argument("--full", "-f", action="store_true"); g.add_argument("--copy", "-c", action="store_true")
    l = sp.add_parser("list"); l.add_argument("--tag"); l.add_argument("--expiring", action="store_true")
    d = sp.add_parser("delete"); d.add_argument("name")
    c = sp.add_parser("check"); c.add_argument("name", nargs="?")
    r = sp.add_parser("rotate"); r.add_argument("name"); r.add_argument("new_token")
    i = sp.add_parser("inject"); i.add_argument("--shell", action="store_true")
    b = sp.add_parser("backup"); b.add_argument("--file", "-f")
    rs = sp.add_parser("restore"); rs.add_argument("file")
    args = p.parse_args()
    if not args.cmd: p.print_help(); sys.exit(0)
    v = TokenVault()
    if args.cmd == "add": v.add(args.name, args.token, args.desc, args.expires, args.tags.split(",") if args.tags else [])
    elif args.cmd == "get": v.copy(args.name) if args.copy else print(v.get(args.name, args.full) or "")
    elif args.cmd == "list": print_table(v.list_all(args.tag, args.expiring))
    elif args.cmd == "delete": v.delete(args.name)
    elif args.cmd == "check": v.check(args.name) if args.name else v.check_all()
    elif args.cmd == "rotate": v.rotate(args.name, args.new_token)
    elif args.cmd == "inject": v.inject(args.shell)
    elif args.cmd == "backup": v.backup(args.file)
    elif args.cmd == "restore": v.restore(args.file)

if __name__ == "__main__": main()
VAULT_EOF

chmod +x ~/api_token_vault.py

cat > ~/vault_shortcuts.sh << 'SHORTCUTS_EOF'
#!/bin/bash
VAULT_SCRIPT="${HOME}/api_token_vault.py"
alias vault="python3 ${VAULT_SCRIPT}"
alias v="python3 ${VAULT_SCRIPT}"
alias vadd="python3 ${VAULT_SCRIPT} add"
alias vget="python3 ${VAULT_SCRIPT} get"
alias vlist="python3 ${VAULT_SCRIPT} list"
alias vdel="python3 ${VAULT_SCRIPT} delete"
alias vcheck="python3 ${VAULT_SCRIPT} check"
alias vcopy="python3 ${VAULT_SCRIPT} get --copy"
anthropic-key() { python3 ${VAULT_SCRIPT} get anthropic --copy; }
openai-key() { python3 ${VAULT_SCRIPT} get openai --copy; }
cf-key() { python3 ${VAULT_SCRIPT} get cloudflare --copy; }
gh-key() { python3 ${VAULT_SCRIPT} get github --copy; }
vault-load() { eval "$(python3 ${VAULT_SCRIPT} inject --shell)"; echo "✅ Loaded"; }
vault-health() { python3 ${VAULT_SCRIPT} check; }
vault-backup() { python3 ${VAULT_SCRIPT} backup; }
echo "🔐 Vault Ready: vault list | vadd | vcopy | vcheck"
SHORTCUTS_EOF

mkdir -p ~/.config/cloudflare

grep -q "vault_shortcuts.sh" ~/.zshrc 2>/dev/null || echo -e "\n# Token Vault\nsource ~/vault_shortcuts.sh" >> ~/.zshrc

echo ""
echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║              ✅ TOKEN VAULT v2 INSTALLED                          ║"
echo "╠═══════════════════════════════════════════════════════════════════╣"
echo "║  source ~/.zshrc                                                  ║"
echo "║  vault add anthropic YOUR-API-KEY                                 ║"
echo "║  vcopy anthropic                                                  ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
