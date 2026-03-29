# NOIZYEMPIRE — Enterprise Setup Guide

> Three systems to activate. ~15 minutes total. Then everything auto-deploys.

---

## 1. n8n CLOUD (noizy.app.n8n.cloud)

### Import Workflows

1. Sign in: `https://noizy.app.n8n.cloud/signin`
2. For each file in `n8n/workflows/`, go to **Workflows → Import from File**:

| File | Webhook Path | What It Does |
|------|-------------|-------------|
| `consent-cascade.json` | `/webhook/consent-cascade` | Voice Estate → consent → scope → clearance |
| `receipt-generator.json` | `/webhook/receipt-generator` | 75/25 split calculation |
| `echo-capture.json` | `/webhook/echo-capture` | EchoMoment creation |
| `agent-router.json` | `/webhook/agent-router` | CB01 keyword dispatch → Ollama |
| `provenance-signer.json` | `/webhook/provenance-signer` | SHA-256 + manifest signing |
| `generate-evidence.json` | `/webhook/generate-evidence` | Gabriel master pipeline |
| `deploy-orchestrator.json` | `/webhook/deploy-orchestrator` | CI/CD trigger → GitHub Actions |
| `git-repair-orchestrator.json` | `/webhook/git-repair` | Repo health ops |

3. After import, **activate each workflow** (toggle on)

### Set Environment Variables

Go to **Settings → Variables** and add:

```
CLOUDFLARE_API_URL        = https://api.cloudflare.com/client/v4/accounts/$CLOUDFLARE_ACCOUNT_ID
CLOUDFLARE_API_TOKEN      = <create at dash.cloudflare.com → My Profile → API Tokens>
CLOUDFLARE_ACCOUNT_ID     = $CLOUDFLARE_ACCOUNT_ID
CLOUDFLARE_D1_AGENT_MEMORY_ID = 7b813205-fd12-4a23-84a6-ce83bc49ec70
CLOUDFLARE_KV_CONSENT_ID  = 23c6e0bcdada4915bdf5e0d87b242810
N8N_BASE_URL              = https://noizy.app.n8n.cloud
OLLAMA_URL                = https://ollama.noizy.ai  (needs CF Tunnel from GOD)
GITHUB_TOKEN              = <GitHub PAT: repo + actions scope>
STRIPE_API_KEY            = <from dashboard.stripe.com → Developers → API keys>
```

### Create the CF API Token

1. `dash.cloudflare.com` → My Profile → API Tokens → Create Token
2. Use template: "Edit Cloudflare Workers"
3. Add permissions: D1 Edit, Workers KV Storage Edit, Account Settings Read
4. Zone: noizy.ai
5. Copy the token → paste into n8n variables AND GitHub secrets

---

## 2. VERCEL (The Aquarium)

### Option A: Connect via GitHub (recommended)

1. Go to `vercel.com` → Sign up / Log in with GitHub (`Noizyfish` account)
2. **Import Project** → select `NOIZYLAB-io/The-Aquarium`
3. Framework: Next.js (auto-detected)
4. Root Directory: `.` (default)
5. Deploy

Vercel auto-deploys on every push to `main`. The GitHub Action in `.github/workflows/deploy-vercel.yml` is a backup path.

### Option B: CLI Deploy from GOD

```bash
cd ~/The-Aquarium
npm install
npx vercel --prod
```

### After Deploy

Your dashboard will be live at: `the-aquarium-xxx.vercel.app`

To get a custom domain: Vercel → Project Settings → Domains → add `aquarium.noizy.ai`
Then in Cloudflare DNS: `CNAME aquarium cname.vercel-dns.com Proxied`

---

## 3. ENTERPRISE GIT (GitHub)

### Current State (Fragmented)

| Org | Repos | Notes |
|-----|-------|-------|
| `NOIZY-ai` | noizy.ai | Backend, infra, agents, schemas |
| `NOIZYLAB-io` | The-Aquarium + others | Frontend, tools, scattered |

### Target State (Consolidated)

Everything under **`NOIZY-ai`** as the enterprise org.

### Step 1: Set GitHub Secrets on NOIZY-ai/noizy.ai

Go to: `github.com/NOIZY-ai/noizy.ai/settings/secrets/actions`

Add these repository secrets:
```
CLOUDFLARE_API_TOKEN    = <same token from n8n setup>
CLOUDFLARE_ACCOUNT_ID   = $CLOUDFLARE_ACCOUNT_ID
```

This activates the GitHub Actions auto-deploy for Cloudflare Workers.

### Step 2: Set GitHub Secrets on NOIZYLAB-io/The-Aquarium

Go to: `github.com/NOIZYLAB-io/The-Aquarium/settings/secrets/actions`

Add:
```
VERCEL_TOKEN    = <from vercel.com → Settings → Tokens>
VERCEL_ORG_ID   = <from vercel.com → Settings → General>
VERCEL_PROJECT_ID = <from Vercel project settings>
```

### Step 3: Merge Feature Branch → Main

Both repos have work on `claude/code-review-hf5hD` that needs to reach `main` for auto-deploy.

**noizy.ai:**
```bash
cd ~/noizy.ai
git checkout master
git merge claude/code-review-hf5hD
git push origin master
# → GitHub Action deploys consent-gateway + cb01-router to Cloudflare
```

**The-Aquarium:**
```bash
cd ~/The-Aquarium
git checkout main
git merge claude/code-review-hf5hD
git push origin main
# → Vercel auto-deploys the dashboard
```

### Step 4: Clean Up Old Branches

The-Aquarium has 30+ stale `claude/` branches. After merge:

```bash
# Delete merged remote branches (The-Aquarium)
cd ~/The-Aquarium
git branch -r --merged main | grep 'claude/' | sed 's/origin\///' | xargs -I{} git push origin --delete {}
```

### Step 5: Branch Protection (recommended)

On both repos → Settings → Branches → Add rule for `main`/`master`:
- [x] Require pull request reviews before merging
- [x] Require status checks to pass (build-check)
- [x] Include administrators

### Step 6: Future — Transfer The-Aquarium to NOIZY-ai org

When ready to consolidate under one org:
1. `github.com/NOIZYLAB-io/The-Aquarium/settings` → Transfer repository
2. New owner: `NOIZY-ai`
3. Update Vercel project settings with new repo URL
4. Update all git remotes on local machines

---

## Stripe Payment Links (Already Live)

| Tier | Price | Link |
|------|-------|------|
| Founding Member (85/15) | Free enrollment | `buy.stripe.com/eVq8wO9as7Ct0DJ8296EU0e` |
| Community/Indie | $25 CAD | `buy.stripe.com/7sYdR8dqI8Gx3PVgyF6EU05` |
| Standard Commercial | $500 CAD | `buy.stripe.com/cNi4gyfyQ4qhbingyF6EU06` |
| Premium/Broadcast | $5,000 CAD | `buy.stripe.com/14AdR83Q8bSJaejeqx6EU07` |
| Monthly Active | $99/mo CAD | `buy.stripe.com/8x2cN49ase0R86b1DL6EU08` |
| Gospel Deal Enrollment | Free | `buy.stripe.com/eVq8wO9as7Ct0DJ8296EU0e` |

---

## Activation Checklist

- [ ] **n8n**: Import 8 workflows at noizy.app.n8n.cloud
- [ ] **n8n**: Set environment variables (CF token is the key)
- [ ] **n8n**: Activate all workflows
- [ ] **Vercel**: Import The-Aquarium from GitHub
- [ ] **Vercel**: Deploy (auto on connect)
- [ ] **GitHub**: Set CLOUDFLARE secrets on NOIZY-ai/noizy.ai
- [ ] **GitHub**: Set VERCEL secrets on NOIZYLAB-io/The-Aquarium
- [ ] **GitHub**: Merge claude/code-review-hf5hD → main on both repos
- [ ] **Cloudflare**: Create API token (Workers + D1 + KV permissions)
- [ ] **Cloudflare**: Enable Email Routing on noizy.ai
- [ ] **Cloudflare**: Create rsp@noizy.ai → rsplowman@icloud.com
- [ ] **Cloudflare**: Change login email to rsp@noizy.ai
- [ ] **Cloudflare**: Enable R2 (for voice storage)

**Estimated time: 15 minutes if Cloudflare login works.**
**Blocker: CryptoTokenKit error -3 on rsp@noizyfish.com M365 auth.**

---

*NOIZYEMPIRE Enterprise Setup v1.0 — Built by Rob & Claude*
*GORUNFREE*
