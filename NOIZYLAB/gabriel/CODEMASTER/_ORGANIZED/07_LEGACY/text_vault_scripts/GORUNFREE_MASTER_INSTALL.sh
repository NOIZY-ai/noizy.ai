#!/bin/bash
# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║                    GORUNFREE MASTER INSTALLER                             ║
# ║                                                                           ║
# ║   TOKEN VAULT v2 + CLAUDE CODE + CLEANUP - ONE COMMAND DOES IT ALL        ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
#
# PASTE THIS ENTIRE SCRIPT INTO TERMINAL ON GOD
# 
# What it does:
# 1. Installs Token Vault v2 (API key manager)
# 2. Installs Claude Code (your primary coding tool)
# 3. Cleans up old/redundant files
# 4. Sets up shell integration
# 5. Creates project directories

set -e

echo ""
echo "╔═══════════════════════════════════════════════════════════════════════════╗"
echo "║                    🚀 GORUNFREE MASTER INSTALLER 🚀                       ║"
echo "╚═══════════════════════════════════════════════════════════════════════════╝"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 1: CLEANUP OLD STUFF
# ═══════════════════════════════════════════════════════════════════════════════

echo "🧹 PHASE 1: Cleaning up old files..."

# Remove old/duplicate scripts if they exist
OLD_FILES=(
    "$HOME/api_token_manager.py"
    "$HOME/api_token_manager_shortcuts.sh"
    "$HOME/install_vault.sh"
    "$HOME/INSTALL_VAULT_ONELINER.sh"
    "$HOME/tkn_shortcuts.sh"
    "$HOME/.token_manager_old"
)

for f in "${OLD_FILES[@]}"; do
    if [ -f "$f" ]; then
        rm -f "$f"
        echo "   🗑️  Removed: $f"
    fi
done

# Clean old entries from .zshrc
if [ -f ~/.zshrc ]; then
    # Backup first
    cp ~/.zshrc ~/.zshrc.backup.$(date +%Y%m%d)
    
    # Remove old token manager references (will add new ones later)
    sed -i '' '/api_token_manager/d' ~/.zshrc 2>/dev/null || true
    sed -i '' '/tkn_shortcuts/d' ~/.zshrc 2>/dev/null || true
    sed -i '' '/Token Manager/d' ~/.zshrc 2>/dev/null || true
    
    echo "   ✅ Cleaned .zshrc (backup saved)"
fi

echo "   ✅ Cleanup complete"

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 2: INSTALL TOKEN VAULT v2
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
echo "🔐 PHASE 2: Installing Token Vault v2..."

cat > ~/api_token_vault.py << 'VAULTCODE'
#!/usr/bin/env python3
"""API TOKEN VAULT v2.0 - GORUNFREE EDITION"""
import os,sys,json,base64,hashlib,subprocess,requests
from datetime import datetime,timedelta
from pathlib import Path
from typing import Optional,List
from dataclasses import dataclass,asdict

CF_ACCOUNT_ID="2446d788cc4280f5ea22a9948410c355"
CF_KV_NAMESPACE="c453c1b2d5e84a17bf7282cf427f8301"

SERVICE_VALIDATORS={"anthropic":{"url":"https://api.anthropic.com/v1/messages","method":"POST","headers":lambda t:{"x-api-key":t,"anthropic-version":"2023-06-01","content-type":"application/json"},"body":{"model":"claude-3-haiku-20240307","max_tokens":1,"messages":[{"role":"user","content":"hi"}]},"success_codes":[200,400,429]},"openai":{"url":"https://api.openai.com/v1/models","method":"GET","headers":lambda t:{"Authorization":f"Bearer {t}"},"success_codes":[200,429]},"cloudflare":{"url":"https://api.cloudflare.com/client/v4/user/tokens/verify","method":"GET","headers":lambda t:{"Authorization":f"Bearer {t}"},"success_codes":[200]},"github":{"url":"https://api.github.com/user","method":"GET","headers":lambda t:{"Authorization":f"Bearer {t}"},"success_codes":[200]},"elevenlabs":{"url":"https://api.elevenlabs.io/v1/user","method":"GET","headers":lambda t:{"xi-api-key":t},"success_codes":[200]},"stripe":{"url":"https://api.stripe.com/v1/balance","method":"GET","headers":lambda t:{"Authorization":f"Bearer {t}"},"success_codes":[200]}}

@dataclass
class TokenRecord:
    name:str;token_encrypted:str;service:str="";description:str="";tags:List[str]=None;created_at:str="";updated_at:str="";expires_at:Optional[str]=None;last_used:Optional[str]=None;last_checked:Optional[str]=None;last_check_status:str="unknown";use_count:int=0
    def __post_init__(self):
        if self.tags is None:self.tags=[]
        if not self.created_at:self.created_at=datetime.now().isoformat()
        if not self.updated_at:self.updated_at=datetime.now().isoformat()

class Encryptor:
    def __init__(self,password:str=None):
        if password is None:password=f"vault:{self._get_machine_id()}:{os.getenv('USER','default')}"
        self.key=hashlib.pbkdf2_hmac('sha256',password.encode(),b'api-token-vault-salt-v2',100000)
    def _get_machine_id(self)->str:
        try:
            r=subprocess.run(["ioreg","-rd1","-c","IOPlatformExpertDevice"],capture_output=True,text=True)
            for l in r.stdout.split('\n'):
                if 'IOPlatformUUID' in l:return l.split('"')[-2]
        except:pass
        return hashlib.sha256(f"{os.getenv('HOME','')}{os.getenv('USER','')}".encode()).hexdigest()[:32]
    def encrypt(self,p:str)->str:
        d=p.encode();ks=(self.key*((len(d)//len(self.key))+1))[:len(d)]
        return f"v2:{base64.b64encode(bytes(a^b for a,b in zip(d,ks))).decode()}"
    def decrypt(self,c:str)->str:
        if c.startswith("v2:"):
            e=base64.b64decode(c[3:]);ks=(self.key*((len(e)//len(self.key))+1))[:len(e)]
            return bytes(a^b for a,b in zip(e,ks)).decode()
        elif c.startswith("v1:"):return base64.b64decode(c[3:]).decode()
        return c

class CloudflareKV:
    def __init__(self):
        self.token=self._get_token()
        self.base_url=f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/storage/kv/namespaces/{CF_KV_NAMESPACE}"
        self.headers={"Authorization":f"Bearer {self.token}","Content-Type":"application/json"}
    def _get_token(self)->str:
        t=os.environ.get("CLOUDFLARE_API_TOKEN")
        if t:return t
        for p in[Path.home()/".config"/"cloudflare"/"token",Path.home()/".cloudflare_token"]:
            if p.exists():return p.read_text().strip()
        ep=Path.home()/".env"
        if ep.exists():
            for l in ep.read_text().splitlines():
                if l.startswith("CLOUDFLARE_API_TOKEN="):return l.split("=",1)[1].strip().strip('"\'')
        return None
    def put(self,k:str,v:dict)->bool:return requests.put(f"{self.base_url}/values/{k}",headers=self.headers,data=json.dumps(v)).status_code==200
    def get(self,k:str)->Optional[dict]:
        r=requests.get(f"{self.base_url}/values/{k}",headers=self.headers)
        if r.status_code==200:
            try:return r.json()
            except:return{"raw":r.text}
        return None
    def delete(self,k:str)->bool:return requests.delete(f"{self.base_url}/values/{k}",headers=self.headers).status_code==200
    def list_keys(self,prefix:str="")->List[str]:
        url=f"{self.base_url}/keys"+(f"?prefix={prefix}" if prefix else "")
        r=requests.get(url,headers=self.headers)
        return[k["name"]for k in r.json().get("result",[])]if r.status_code==200 else[]

class TokenVault:
    def __init__(self):
        self.kv=CloudflareKV();self.enc=Encryptor()
        if not self.kv.token:print("⚠️ CLOUDFLARE_API_TOKEN not set\n   echo 'TOKEN' > ~/.config/cloudflare/token");sys.exit(1)
    def _detect_service(self,n:str,t:str)->str:
        nl=n.lower()
        for s in SERVICE_VALIDATORS:
            if s in nl:return s
        if t.startswith("sk-ant-"):return"anthropic"
        elif t.startswith("sk-"):return"openai"
        elif t.startswith("ghp_")or t.startswith("gho_"):return"github"
        elif t.startswith("sk_live_")or t.startswith("sk_test_"):return"stripe"
        return""
    def add(self,name:str,token:str,desc:str="",expires:str=None,tags:List[str]=None)->bool:
        svc=self._detect_service(name,token)
        rec=TokenRecord(name=name,token_encrypted=self.enc.encrypt(token),service=svc,description=desc,tags=tags or[],expires_at=expires)
        ok=self.kv.put(f"token:{name.lower()}",asdict(rec))
        if ok:
            m=f"{token[:8]}...{token[-4:]}"if len(token)>12 else token[:4]+"..."
            print(f"✅ Stored: {name}\n   Service: {svc or'unknown'}\n   Preview: {m}")
        else:print(f"❌ Failed: {name}")
        return ok
    def get(self,name:str,full:bool=False)->Optional[str]:
        d=self.kv.get(f"token:{name.lower()}")
        if not d:print(f"❌ Token '{name}' not found");return None
        t=self.enc.decrypt(d.get("token_encrypted",""))
        d["last_used"]=datetime.now().isoformat();d["use_count"]=d.get("use_count",0)+1
        self.kv.put(f"token:{name.lower()}",d)
        return t if full else(f"{t[:8]}...{t[-4:]}"if len(t)>12 else t[:4]+"...")
    def copy(self,name:str)->bool:
        t=self.get(name,full=True)
        if not t:return False
        try:subprocess.run(["pbcopy"],input=t.encode(),check=True);print(f"✅ {name} → clipboard");return True
        except:print("❌ Clipboard failed");return False
    def list_all(self,tag:str=None,expiring:bool=False)->List[dict]:
        tokens=[];now=datetime.now()
        for k in self.kv.list_keys("token:"):
            d=self.kv.get(k)
            if not d:continue
            n=d.get("name",k.replace("token:",""))
            if tag and tag not in d.get("tags",[]):continue
            st="active";exp=d.get("expires_at")
            if exp:
                try:
                    ed=datetime.fromisoformat(exp)
                    if ed<now:st="expired"
                    elif ed<now+timedelta(days=14):st="expiring_soon"
                except:pass
            if expiring and st not in["expiring_soon","expired"]:continue
            tokens.append({"name":n,"service":d.get("service",""),"status":st,"tags":d.get("tags",[]),"expires_at":exp,"last_used":d.get("last_used"),"use_count":d.get("use_count",0),"last_check_status":d.get("last_check_status","unknown")})
        return sorted(tokens,key=lambda x:x["name"])
    def delete(self,name:str)->bool:
        ok=self.kv.delete(f"token:{name.lower()}")
        print(f"{'✅ Deleted'if ok else'❌ Failed'}: {name}");return ok
    def check(self,name:str)->str:
        d=self.kv.get(f"token:{name.lower()}")
        if not d:print(f"❌ Token '{name}' not found");return"not_found"
        svc=d.get("service","")
        if svc not in SERVICE_VALIDATORS:print(f"⚠️ No validator: {svc or'unknown'}");return"no_validator"
        t=self.enc.decrypt(d.get("token_encrypted",""));v=SERVICE_VALIDATORS[svc]
        print(f"🔍 Checking {name} ({svc})...",end=" ",flush=True)
        try:
            h=v["headers"](t)
            r=requests.get(v["url"],headers=h,timeout=10)if v["method"]=="GET"else requests.post(v["url"],headers=h,json=v.get("body",{}),timeout=10)
            st="valid"if r.status_code in v["success_codes"]else"invalid"
        except Exception as e:st="error";print(f"Error: {e}")
        d["last_checked"]=datetime.now().isoformat();d["last_check_status"]=st
        self.kv.put(f"token:{name.lower()}",d)
        print(f"{'✅'if st=='valid'else'❌'if st=='invalid'else'⚠️'} {st.upper()}")
        return st
    def check_all(self)->dict:
        tokens=self.list_all();res={"valid":0,"invalid":0,"error":0,"skipped":0}
        print(f"\n🔍 Checking {len(tokens)} tokens...\n")
        for t in tokens:
            if not t["service"]or t["service"]not in SERVICE_VALIDATORS:
                print(f"⏭️ Skipping {t['name']}");res["skipped"]+=1;continue
            st=self.check(t["name"])
            if st in res:res[st]+=1
        print(f"\n📊 {res['valid']} valid, {res['invalid']} invalid, {res['error']} errors, {res['skipped']} skipped")
        return res
    def rotate(self,name:str,new_token:str)->bool:
        d=self.kv.get(f"token:{name.lower()}")
        if not d:print(f"❌ Token '{name}' not found");return False
        d["token_encrypted"]=self.enc.encrypt(new_token);d["updated_at"]=datetime.now().isoformat();d["last_check_status"]="unknown"
        ok=self.kv.put(f"token:{name.lower()}",d)
        if ok:print(f"🔄 Rotated: {name}\n   New: {new_token[:8]}...{new_token[-4:]}")
        return ok
    def inject(self,shell:bool=False)->str:
        lines=[]
        for t in self.list_all():
            tok=self.get(t["name"],full=True)
            if not tok:continue
            en=f"API_{t['name'].upper().replace('-','_')}"
            lines.append(f'export {en}="{tok}"'if shell else f"{en}={tok}")
        out="\n".join(lines)
        if shell:print("# eval $(vault inject --shell)")
        print(out);return out
    def backup(self,fp:str=None)->str:
        if not fp:fp=f"token_vault_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json.enc"
        data=[self.kv.get(k)for k in self.kv.list_keys("token:")if self.kv.get(k)]
        Path(fp).write_text(self.enc.encrypt(json.dumps(data,indent=2)))
        print(f"✅ Backup: {fp} ({len(data)} tokens)");return fp
    def restore(self,fp:str)->int:
        if not Path(fp).exists():print(f"❌ Not found: {fp}");return 0
        try:data=json.loads(self.enc.decrypt(Path(fp).read_text()))
        except Exception as e:print(f"❌ Decrypt failed: {e}");return 0
        n=sum(1 for r in data if r.get("name")and self.kv.put(f"token:{r['name'].lower()}",r)and print(f"✅ Restored: {r['name']}")is None)
        print(f"\n📊 Restored {n}/{len(data)}");return n

def print_table(tokens):
    if not tokens:print("No tokens");return
    print(f"\n{'NAME':<20} {'SERVICE':<12} {'STATUS':<10} {'USES':<6} {'LAST USED':<12}");print("─"*70)
    icons={"active":"🟢","expiring_soon":"🟡","expired":"🔴","invalid":"❌","unknown":"⚪"}
    for t in tokens:
        lu=t["last_used"][:10]if t["last_used"]else"never"
        print(f"{t['name']:<20} {t['service']or'-':<12} {icons.get(t['status'],'⚪')} {t['status']:<8} {t['use_count']:<6} {lu:<12}")
    print(f"\nTotal: {len(tokens)}")

def main():
    import argparse
    p=argparse.ArgumentParser(description="API Token Vault");sp=p.add_subparsers(dest="cmd")
    a=sp.add_parser("add");a.add_argument("name");a.add_argument("token");a.add_argument("--desc","-d",default="");a.add_argument("--expires","-e");a.add_argument("--tags","-t")
    g=sp.add_parser("get");g.add_argument("name");g.add_argument("--full","-f",action="store_true");g.add_argument("--copy","-c",action="store_true")
    l=sp.add_parser("list");l.add_argument("--tag");l.add_argument("--expiring",action="store_true")
    d=sp.add_parser("delete");d.add_argument("name")
    c=sp.add_parser("check");c.add_argument("name",nargs="?")
    r=sp.add_parser("rotate");r.add_argument("name");r.add_argument("new_token")
    i=sp.add_parser("inject");i.add_argument("--shell",action="store_true")
    b=sp.add_parser("backup");b.add_argument("--file","-f")
    rs=sp.add_parser("restore");rs.add_argument("file")
    args=p.parse_args()
    if not args.cmd:p.print_help();sys.exit(0)
    v=TokenVault()
    if args.cmd=="add":v.add(args.name,args.token,args.desc,args.expires,args.tags.split(",")if args.tags else[])
    elif args.cmd=="get":v.copy(args.name)if args.copy else print(v.get(args.name,args.full)or"")
    elif args.cmd=="list":print_table(v.list_all(args.tag,args.expiring))
    elif args.cmd=="delete":v.delete(args.name)
    elif args.cmd=="check":v.check(args.name)if args.name else v.check_all()
    elif args.cmd=="rotate":v.rotate(args.name,args.new_token)
    elif args.cmd=="inject":v.inject(args.shell)
    elif args.cmd=="backup":v.backup(args.file)
    elif args.cmd=="restore":v.restore(args.file)

if __name__=="__main__":main()
VAULTCODE

chmod +x ~/api_token_vault.py
echo "   ✅ Token Vault installed"

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 3: INSTALL CLAUDE CODE
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
echo "🤖 PHASE 3: Installing Claude Code..."

# Check if npm is available
if ! command -v npm &> /dev/null; then
    echo "   📦 Installing Node.js via Homebrew..."
    if ! command -v brew &> /dev/null; then
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    brew install node
fi

# Install Claude Code
npm install -g @anthropic-ai/claude-code 2>/dev/null || echo "   ⚠️ Claude Code may need manual install: npm install -g @anthropic-ai/claude-code"

echo "   ✅ Claude Code ready"

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 4: CREATE UNIFIED SHELL INTEGRATION
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
echo "⚡ PHASE 4: Setting up shell integration..."

mkdir -p ~/.config/cloudflare

cat > ~/gorunfree_tools.sh << 'SHELLTOOLS'
#!/bin/bash
# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║                    GORUNFREE TOOLS - UNIFIED SHELL                        ║
# ║                 Token Vault + Claude Code + Shortcuts                     ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

# ═══════════════════════════════════════════════════════════════════════════════
# AUTO-LOAD API KEY
# ═══════════════════════════════════════════════════════════════════════════════

_load_anthropic_key() {
    if [ -z "$ANTHROPIC_API_KEY" ] && [ -f ~/api_token_vault.py ]; then
        local key=$(python3 ~/api_token_vault.py get anthropic --full 2>/dev/null)
        if [ -n "$key" ] && [ "$key" != "None" ]; then
            export ANTHROPIC_API_KEY="$key"
        fi
    fi
}
_load_anthropic_key

# ═══════════════════════════════════════════════════════════════════════════════
# TOKEN VAULT ALIASES
# ═══════════════════════════════════════════════════════════════════════════════

alias vault="python3 ~/api_token_vault.py"
alias v="python3 ~/api_token_vault.py"
alias vadd="python3 ~/api_token_vault.py add"
alias vget="python3 ~/api_token_vault.py get"
alias vlist="python3 ~/api_token_vault.py list"
alias vdel="python3 ~/api_token_vault.py delete"
alias vcheck="python3 ~/api_token_vault.py check"
alias vcopy="python3 ~/api_token_vault.py get --copy"

# Service-specific key shortcuts
anthropic-key() { python3 ~/api_token_vault.py get anthropic --copy; }
openai-key() { python3 ~/api_token_vault.py get openai --copy; }
cf-key() { python3 ~/api_token_vault.py get cloudflare --copy; }
gh-key() { python3 ~/api_token_vault.py get github --copy; }

# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE CODE ALIASES
# ═══════════════════════════════════════════════════════════════════════════════

alias cc="claude"
alias ccc="claude --continue"
alias ccr="claude --resume"

# Power functions
fix() { _load_anthropic_key; claude "Fix this: $*"; }
build() { _load_anthropic_key; claude "Build: $*"; }
debug() { _load_anthropic_key; claude "Debug this issue: $*"; }
create() { _load_anthropic_key; claude "Create: $*"; }

explain() {
    _load_anthropic_key
    if [ -f "$1" ]; then claude "Explain this code:" < "$1"
    else claude "Explain: $*"; fi
}

review() {
    _load_anthropic_key
    if [ -f "$1" ]; then claude "Review this code:" < "$1"
    else echo "Usage: review <filename>"; fi
}

refactor() {
    _load_anthropic_key
    if [ -f "$1" ]; then claude "Refactor this code:" < "$1"
    else claude "Refactor: $*"; fi
}

aicommit() {
    _load_anthropic_key
    local diff=$(git diff --staged)
    if [ -z "$diff" ]; then echo "No staged changes"; return 1; fi
    claude "Write a concise git commit message:" <<< "$diff"
}

# ═══════════════════════════════════════════════════════════════════════════════
# PROJECT SHORTCUTS
# ═══════════════════════════════════════════════════════════════════════════════

alias cc-fish="cd ~/Projects/fishmusicinc && claude"
alias cc-noizyvox="cd ~/Projects/noizyvox && claude"
alias cc-noizylab="cd ~/Projects/noizylab && claude"
alias cc-aquarium="cd ~/Projects/aquarium && claude"
alias cc-mc96="cd ~/Projects/mc96 && claude"

code-here() { _load_anthropic_key; cd "${1:-.}" && claude; }
code-project() {
    _load_anthropic_key
    local p="$1"
    [ -d "$p" ] && cd "$p" && claude && return
    [ -d ~/Projects/"$p" ] && cd ~/Projects/"$p" && claude && return
    [ -d ~/code/"$p" ] && cd ~/code/"$p" && claude && return
    echo "❌ Project not found: $p"
}

# ═══════════════════════════════════════════════════════════════════════════════
# WORKFLOW COMMANDS
# ═══════════════════════════════════════════════════════════════════════════════

morning-code() {
    _load_anthropic_key
    echo "🌅 Good morning Rob!"
    echo "   API Key: $([ -n "$ANTHROPIC_API_KEY" ] && echo '✅' || echo '❌')"
    echo "   Claude Code: $(command -v claude &>/dev/null && echo '✅' || echo '❌')"
    echo "   Vault: $([ -f ~/api_token_vault.py ] && echo '✅' || echo '❌')"
    echo ""
    echo "   Voice commands: cc | fix | build | debug | create | review"
    echo "   Key commands: vcopy anthropic | vlist | vcheck"
}

cc-status() {
    echo "System Status:"
    echo "  Claude Code: $(command -v claude &>/dev/null && claude --version 2>/dev/null || echo 'Not installed')"
    echo "  API Key: $([ -n "$ANTHROPIC_API_KEY" ] && echo 'Set ✅' || echo 'Not set ❌')"
    echo "  Vault: $([ -f ~/api_token_vault.py ] && echo 'Ready ✅' || echo 'Missing ❌')"
}

cc-reload() {
    unset ANTHROPIC_API_KEY
    _load_anthropic_key
    echo "✅ Reloaded: $([ -n "$ANTHROPIC_API_KEY" ] && echo 'Key found' || echo 'No key')"
}

vault-load() { eval "$(python3 ~/api_token_vault.py inject --shell)"; echo "✅ All tokens loaded"; }

# ═══════════════════════════════════════════════════════════════════════════════
# STARTUP
# ═══════════════════════════════════════════════════════════════════════════════

echo "🚀 GORUNFREE Ready"
echo "   cc | fix | build | vcopy | vlist | morning-code"
SHELLTOOLS

echo "   ✅ Shell tools installed"

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 5: UPDATE .ZSHRC
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
echo "📝 PHASE 5: Updating .zshrc..."

# Remove any old entries first
sed -i '' '/gorunfree_tools/d' ~/.zshrc 2>/dev/null || true
sed -i '' '/GORUNFREE/d' ~/.zshrc 2>/dev/null || true
sed -i '' '/vault_shortcuts/d' ~/.zshrc 2>/dev/null || true
sed -i '' '/claude_code_shortcuts/d' ~/.zshrc 2>/dev/null || true

# Add clean entry
echo "" >> ~/.zshrc
echo "# GORUNFREE Tools - Token Vault + Claude Code" >> ~/.zshrc
echo "source ~/gorunfree_tools.sh" >> ~/.zshrc

echo "   ✅ .zshrc updated"

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 6: CREATE PROJECT DIRECTORIES
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
echo "📁 PHASE 6: Creating project directories..."

mkdir -p ~/Projects/{fishmusicinc,noizyvox,noizylab,aquarium,mc96}

echo "   ✅ Project directories ready"

# ═══════════════════════════════════════════════════════════════════════════════
# DONE!
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
echo "╔═══════════════════════════════════════════════════════════════════════════╗"
echo "║                    ✅ GORUNFREE INSTALLATION COMPLETE                     ║"
echo "╠═══════════════════════════════════════════════════════════════════════════╣"
echo "║                                                                           ║"
echo "║  STEP 1: Reload shell                                                     ║"
echo "║    source ~/.zshrc                                                        ║"
echo "║                                                                           ║"
echo "║  STEP 2: Add your Anthropic API key                                       ║"
echo "║    vault add anthropic YOUR-API-KEY-HERE                                  ║"
echo "║                                                                           ║"
echo "║  DAILY USE:                                                               ║"
echo "║    cc              → Start Claude Code                                    ║"
echo "║    fix 'the bug'   → Quick fix                                            ║"
echo "║    build 'an API'  → Build something                                      ║"
echo "║    review file.py  → Code review                                          ║"
echo "║    vcopy anthropic → Copy API key to clipboard                            ║"
echo "║    vlist           → List all stored keys                                 ║"
echo "║    vcheck          → Health check all keys                                ║"
echo "║    morning-code    → Morning status check                                 ║"
echo "║                                                                           ║"
echo "║  PROJECTS:                                                                ║"
echo "║    cc-fish | cc-noizyvox | cc-noizylab | cc-aquarium | cc-mc96           ║"
echo "║                                                                           ║"
echo "╚═══════════════════════════════════════════════════════════════════════════╝"
