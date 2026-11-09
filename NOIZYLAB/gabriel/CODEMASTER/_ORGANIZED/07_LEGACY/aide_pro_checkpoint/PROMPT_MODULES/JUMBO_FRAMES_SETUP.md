# JUMBO_FRAMES_SETUP v1.0

## DGS-1210-10 JUMBO FRAMES CONFIGURATION

> **Purpose:** Maximize throughput for large file transfers across MC96UNIVERSE

### What Are Jumbo Frames?

- Standard Ethernet frame: **1500 bytes** (MTU)
- Jumbo frame: **9000+ bytes** (up to 9216)
- **Benefit:** Fewer packets = less CPU overhead = faster transfers

### Requirements

- All devices on the path MUST support jumbo frames
- Switch, source, and destination all set to same MTU
- DGS-1210-10 supports up to **9216 bytes**

## SWITCH CONFIGURATION

### Via Web Interface

1. Open browser: `http://192.168.1.254`
2. Login: admin / [password]
3. Navigate: **System > Port Configuration**
4. Set **Jumbo Frame** to `9216` for all ports
5. Apply and save

### Via CLI (if available)

```
config jumbo_frame ports 1-10 state enable
config jumbo_frame ports 1-10 max_size 9216
save
```

## MACOS CONFIGURATION (GOD - M2 Ultra)

```bash
# Check current MTU
ifconfig en0 | grep mtu

# Set jumbo frames (temporary)
sudo ifconfig en0 mtu 9000

# Make permanent - create launch daemon
sudo tee /Library/LaunchDaemons/com.mc96.jumboframes.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.mc96.jumboframes</string>
    <key>ProgramArguments</key>
    <array>
        <string>/sbin/ifconfig</string>
        <string>en0</string>
        <string>mtu</string>
        <string>9000</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
EOF

# Load immediately
sudo launchctl load /Library/LaunchDaemons/com.mc96.jumboframes.plist

# Verify
ifconfig en0 | grep mtu
```

## WINDOWS CONFIGURATION (HP-OMEN)

```powershell
# Check current MTU
netsh interface ipv4 show subinterfaces

# Set jumbo frames via registry
# Open Device Manager > Network Adapter > Properties > Advanced
# Set "Jumbo Packet" or "Jumbo Frame" to 9014

# Or via PowerShell (requires admin)
Set-NetAdapterAdvancedProperty -Name "Ethernet" -RegistryKeyword "*JumboPacket" -RegistryValue 9014

# Verify
ping 192.168.1.100 -f -l 8972
# If successful, jumbo frames work
```

## LINUX/NAS CONFIGURATION (GABRIEL)

```bash
# Check current MTU
ip link show eth0

# Set temporarily
sudo ip link set eth0 mtu 9000

# Make permanent (Debian/Ubuntu)
sudo tee -a /etc/network/interfaces << 'EOF'
auto eth0
iface eth0 inet dhcp
    mtu 9000
EOF

# Or via netplan (Ubuntu 18.04+)
sudo tee /etc/netplan/01-jumbo.yaml << 'EOF'
network:
  version: 2
  ethernets:
    eth0:
      mtu: 9000
EOF
sudo netplan apply
```

## TESTING JUMBO FRAMES

```bash
# Test from GOD to GABRIEL
# MTU 9000 - IP header (20) - ICMP header (8) = 8972

# macOS/Linux
ping -s 8972 -D 192.168.1.101

# If you get "Message too long", jumbo not working
# If ping succeeds, jumbo frames active

# Speed test
iperf3 -c 192.168.1.101 -t 10
```

## TROUBLESHOOTING

| Issue | Solution |
|-------|----------|
| Packet too large | Device on path doesn't support jumbo |
| Connection drops | MTU mismatch, check all devices |
| Slow transfer | Check duplex settings, cable quality |
| Can't reach device | Revert to MTU 1500, test again |

## RECOMMENDED MTU VALUES

| Device | MTU | Notes |
|--------|-----|-------|
| DGS-1210-10 | 9216 | Maximum supported |
| GOD (Mac) | 9000 | Standard jumbo |
| HP-OMEN | 9014 | Windows standard |
| GABRIEL | 9000 | Match Mac |
| Router | 1500 | Internet requires standard MTU |

> **WARNING:** Only enable jumbo frames on LAN. Internet traffic MUST use MTU 1500.
