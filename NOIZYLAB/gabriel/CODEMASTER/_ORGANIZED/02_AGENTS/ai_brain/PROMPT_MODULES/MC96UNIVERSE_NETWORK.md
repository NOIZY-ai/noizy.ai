# MC96UNIVERSE_NETWORK v1.0

## ROUTER TAGS

- `/network` `/mc96` `/infrastructure`
- category: DEVOPS/NETWORK
- outputs: `config` | `status` | `diagram`

## THE MC96UNIVERSE

> **Central Hub:** DGS-1210-10 "MC96" Smart Managed Switch

```
┌─────────────────────────────────────────────────────────────────┐
│                    MC96UNIVERSE NETWORK MAP                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                    ┌──────────────────┐                          │
│                    │   DGS-1210-10    │                          │
│                    │     "MC96"       │                          │
│                    │  10-Port Switch  │                          │
│                    └────────┬─────────┘                          │
│                             │                                    │
│     ┌───────────┬───────────┼───────────┬───────────┐           │
│     │           │           │           │           │           │
│     ▼           ▼           ▼           ▼           ▼           │
│ ┌───────┐  ┌───────┐  ┌─────────┐  ┌───────┐  ┌─────────┐      │
│ │  GOD  │  │GABRIEL│  │ HP-OMEN │  │ FISH  │  │ ROUTER  │      │
│ │M2Ultra│  │ (NAS) │  │(Windows)│  │(Mac)  │  │(Gateway)│      │
│ └───────┘  └───────┘  └─────────┘  └───────┘  └─────────┘      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## DEVICE REGISTRY

| Device | Type | IP | MAC | Port | Role |
|--------|------|-----|-----|------|------|
| GOD | Mac Studio M2 Ultra | 192.168.1.100 | - | 1 | Primary Workstation |
| GABRIEL | NAS/Volume | 192.168.1.101 | - | 2 | Storage/AI Brain |
| HP-OMEN | Windows PC | 192.168.1.102 | - | 3 | Windows Dev/Gaming |
| FISH | Mac Pro | 192.168.1.103 | - | 4 | Secondary Mac |
| Router | Gateway | 192.168.1.1 | - | 10 | Internet Gateway |

## EXTERNAL VOLUMES

| Volume | Location | Purpose |
|--------|----------|---------|
| GABRIEL | Network/USB | Main AI Brain storage |
| JOE | USB | Audio samples |
| RED DRAGON | USB | Backup |
| 6TB | USB | Archive |
| 4TB BLK | USB | Projects |
| M2Ultra | Boot | System drive |

## DGS-1210-10 CONFIGURATION

```bash
# Access switch web interface
open http://192.168.1.254

# Default credentials
# User: admin
# Pass: admin (CHANGE THIS)

# SSH access (if enabled)
ssh admin@192.168.1.254
```

### Recommended Settings

| Setting | Value | Reason |
|---------|-------|--------|
| Jumbo Frames | 9216 | Max throughput for large files |
| VLAN 1 | All ports | Default network |
| Port 1 | GOD | Static, priority high |
| Port 2 | GABRIEL | Static, priority high |
| Port 3 | HP-OMEN | Static |
| QoS | Enabled | Prioritize audio/video |

## QUICK NETWORK COMMANDS

```bash
# Scan local network
arp -a

# Find all devices
nmap -sn 192.168.1.0/24

# Check specific host
ping -c 3 192.168.1.101

# Check open ports
nmap 192.168.1.101

# DNS lookup
dig @192.168.1.1 mc96.local

# Network speed test between machines
iperf3 -s  # On server (GABRIEL)
iperf3 -c 192.168.1.101  # On client (GOD)

# Mount GABRIEL volume
mount -t nfs 192.168.1.101:/share /Volumes/GABRIEL

# SSH to HP-OMEN (requires OpenSSH)
ssh user@192.168.1.102
```

## CLOUDFLARE DNS SETUP

```
# Cloudflare manages DNS for:
# - mc96.ecouniverse.com
# - *.mc96.ecouniverse.com

# DNS Records (example)
A     @           -> Cloudflare Worker IP
CNAME www         -> @
CNAME api         -> @
TXT   _dmarc      -> v=DMARC1; p=none
```

## DEFAULTS

- Switch IP: 192.168.1.254
- Gateway: 192.168.1.1
- Subnet: 255.255.255.0 (/24)
- DNS: Cloudflare (1.1.1.1)
- DHCP Range: 192.168.1.50-199
- Static Range: 192.168.1.100-149
