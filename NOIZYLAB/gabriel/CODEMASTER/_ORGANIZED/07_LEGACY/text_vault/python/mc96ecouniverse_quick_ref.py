#!/usr/bin/env python3
"""
MC96ECOUNIVERSE QUICK REFERENCE
Permanent link for all network device management

SEARCHABLE KEYWORDS:
- network device management
- device discovery
- network scanning
- device organization
- MC96ECOU switch
- network topology
- device registry
- IP scanning
- network monitoring
- device status
"""

# ============================================================================
# QUICK ACCESS COMMANDS
# ============================================================================

# BASIC USAGE
"""
# Launch MC96ECOUNIVERSE
python3 /Users/rsp_ms/GABRIEL/THE_FAMILY/mc96ecouniverse.py

# Scan network
python3 -c "from mc96ecouniverse import MC96ECOUniverse; mc96=MC96ECOUniverse(); mc96.scan_network(); mc96.display_status()"

# View devices
python3 -c "from mc96ecouniverse import MC96ECOUniverse; mc96=MC96ECOUniverse(); print(mc96.list_devices())"
"""

# ============================================================================
# CODE SNIPPETS - COPY & PASTE READY
# ============================================================================

# SNIPPET 1: Quick Network Scan
def quick_scan():
    from mc96ecouniverse import MC96ECOUniverse
    mc96 = MC96ECOUniverse()
    result = mc96.scan_network()
    mc96.display_status()
    return result

# SNIPPET 2: Check Device Status
def check_device(device_name):
    from mc96ecouniverse import MC96ECOUniverse
    mc96 = MC96ECOUniverse()
    device = mc96.get_device(device_name)
    if device:
        print(f"✅ {device['name']}: {device['status']}")
        print(f"   IP: {device['ip_address']}")
        print(f"   Type: {device['device_type']}")
    else:
        print(f"❌ Device '{device_name}' not found")
    return device

# SNIPPET 3: Add New Device
def add_new_device(name, ip, device_type):
    from mc96ecouniverse import MC96ECOUniverse, NetworkDevice, DeviceType, DeviceStatus
    
    mc96 = MC96ECOUniverse()
    
    new_device = NetworkDevice(
        name=name,
        ip_address=ip,
        mac_address=None,
        device_type=DeviceType[device_type.upper()],
        manufacturer=None,
        model=None,
        location='MC96 Studio',
        status=DeviceStatus.UNKNOWN,
        last_seen=None,
        ports=None,
        firmware_version=None,
        management_url=f"http://{ip}",
        notes='Added manually'
    )
    
    result = mc96.add_device(new_device)
    print(result['message'])
    return result

# SNIPPET 4: List All Online Devices
def list_online():
    from mc96ecouniverse import MC96ECOUniverse, DeviceStatus
    mc96 = MC96ECOUniverse()
    online = mc96.list_devices(filter_status=DeviceStatus.ONLINE)
    
    print(f"\n🟢 ONLINE DEVICES ({len(online)}):")
    for device in online:
        print(f"   • {device['name']:<20} {device['ip_address']:<15} [{device['device_type']}]")
    
    return online

# SNIPPET 5: Network Health Check
def network_health():
    from mc96ecouniverse import MC96ECOUniverse
    mc96 = MC96ECOUniverse()
    
    stats = mc96.stats
    health_score = (stats['online_devices'] / stats['total_devices'] * 100) if stats['total_devices'] > 0 else 0
    
    print(f"\n📊 NETWORK HEALTH SCORE: {health_score:.1f}%")
    print(f"   Total Devices: {stats['total_devices']}")
    print(f"   Online: {stats['online_devices']} 🟢")
    print(f"   Offline: {stats['offline_devices']} 🔴")
    
    if health_score >= 90:
        print("   Status: ✅ EXCELLENT")
    elif health_score >= 75:
        print("   Status: ⚠️ GOOD")
    elif health_score >= 50:
        print("   Status: ⚠️ FAIR")
    else:
        print("   Status: ❌ POOR - Investigation Required")
    
    return health_score

# SNIPPET 6: Export Network Topology
def export_topology(filename='network_topology.json'):
    import json
    from mc96ecouniverse import MC96ECOUniverse
    
    mc96 = MC96ECOUniverse()
    topology = mc96.get_network_topology()
    
    with open(filename, 'w') as f:
        json.dump(topology, f, indent=2)
    
    print(f"✅ Network topology exported to {filename}")
    return topology

# SNIPPET 7: Monitor Critical Device
def monitor_critical_device(device_name, alert_if_down=True):
    from mc96ecouniverse import MC96ECOUniverse, DeviceStatus
    mc96 = MC96ECOUniverse()
    
    device = mc96.get_device(device_name)
    
    if not device:
        print(f"❌ Device '{device_name}' not found in registry")
        return None
    
    is_online = mc96.ping_device(device['ip_address'])
    
    if is_online:
        print(f"✅ {device_name} is ONLINE ({device['ip_address']})")
        mc96.update_device(device_name, status=DeviceStatus.ONLINE)
    else:
        print(f"❌ {device_name} is OFFLINE ({device['ip_address']})")
        mc96.update_device(device_name, status=DeviceStatus.OFFLINE)
        if alert_if_down:
            print(f"⚠️ ALERT: Critical device {device_name} is not responding!")
    
    return is_online

# SNIPPET 8: Update Device Info
def update_device_info(device_name, **kwargs):
    from mc96ecouniverse import MC96ECOUniverse
    mc96 = MC96ECOUniverse()
    result = mc96.update_device(device_name, **kwargs)
    print(result['message'])
    return result

# ============================================================================
# DEVICE TYPE REFERENCE
# ============================================================================

DEVICE_TYPES = {
    'SWITCH': 'Network switches (MC96ECOU, etc.)',
    'ROUTER': 'Internet routers and gateways',
    'ACCESS_POINT': 'WiFi access points',
    'NAS': 'Network-attached storage',
    'WORKSTATION': 'Computers and workstations',
    'SERVER': 'Server systems',
    'IOT_DEVICE': 'Smart home devices',
    'PRINTER': 'Network printers',
    'CAMERA': 'IP cameras',
    'AUDIO_INTERFACE': 'Network audio devices',
    'UNKNOWN': 'Unidentified devices'
}

# ============================================================================
# COMMON PORT REFERENCES
# ============================================================================

COMMON_PORTS = {
    80: 'HTTP (Web Interface)',
    443: 'HTTPS (Secure Web)',
    22: 'SSH (Secure Shell)',
    445: 'SMB (File Sharing)',
    139: 'NetBIOS (File Sharing)',
    3389: 'RDP (Remote Desktop)',
    5900: 'VNC (Remote Desktop)',
    631: 'IPP (Printer)',
    554: 'RTSP (Camera Stream)',
    8080: 'HTTP-Alt (IoT)',
    21: 'FTP (File Transfer)',
    23: 'Telnet (Legacy)',
    3306: 'MySQL (Database)',
    5432: 'PostgreSQL (Database)',
    6379: 'Redis (Cache)'
}

# ============================================================================
# MC96ECOU SWITCH REFERENCE
# ============================================================================

MC96ECOU_SPECS = {
    'name': 'MC96ECOU',
    'manufacturer': 'D-Link',
    'model': 'DGS-1210-10',
    'type': 'Smart Managed Switch',
    'ports': 10,
    'speed': 'Gigabit (1000 Mbps)',
    'ip_address': '192.168.0.2',
    'management_url': 'http://192.168.0.2',
    'default_user': 'admin',
    'features': [
        'VLAN support',
        'QoS (Quality of Service)',
        'Port mirroring',
        'Link aggregation',
        'IGMP snooping',
        'Port-based security',
        'Web-based management',
        'SNMP support'
    ]
}

# ============================================================================
# INTEGRATION EXAMPLES
# ============================================================================

# EXAMPLE 1: SHIRL Integration
def shirl_network_command(command):
    """
    Voice commands for network management via SHIRL
    
    Commands:
    - "scan network"
    - "show network status"
    - "check device MC96ECOU"
    - "list online devices"
    """
    from mc96ecouniverse import MC96ECOUniverse
    mc96 = MC96ECOUniverse()
    
    if 'scan' in command.lower():
        mc96.scan_network()
        return "Network scan complete"
    elif 'status' in command.lower():
        mc96.display_status()
        return "Network status displayed"
    elif 'check device' in command.lower():
        device_name = command.split('check device')[-1].strip()
        device = mc96.get_device(device_name)
        return f"Device {device_name}: {device['status']}" if device else "Device not found"
    elif 'online' in command.lower():
        online = list_online()
        return f"Found {len(online)} online devices"

# EXAMPLE 2: PERFMON Integration
def perfmon_network_check():
    """
    Monitor network devices with PERFMON
    """
    from mc96ecouniverse import MC96ECOUniverse
    mc96 = MC96ECOUniverse()
    
    devices = mc96.list_devices()
    results = []
    
    for device in devices:
        is_online = mc96.ping_device(device['ip_address'])
        results.append({
            'device': device['name'],
            'status': 'online' if is_online else 'offline',
            'response_time': 'TBD'  # Could measure actual ping time
        })
    
    return results

# EXAMPLE 3: Daily Automation
def daily_network_report():
    """
    Generate daily network report
    """
    from datetime import datetime
    from mc96ecouniverse import MC96ECOUniverse
    
    mc96 = MC96ECOUniverse()
    mc96.scan_network()
    
    report = {
        'date': datetime.now().isoformat(),
        'total_devices': mc96.stats['total_devices'],
        'online': mc96.stats['online_devices'],
        'offline': mc96.stats['offline_devices'],
        'health_score': (mc96.stats['online_devices'] / mc96.stats['total_devices'] * 100) if mc96.stats['total_devices'] > 0 else 0,
        'devices': mc96.list_devices()
    }
    
    return report

# ============================================================================
# FILE LOCATIONS
# ============================================================================

FILE_LOCATIONS = {
    'main_script': '/Users/rsp_ms/GABRIEL/THE_FAMILY/mc96ecouniverse.py',
    'database': '/Users/rsp_ms/GABRIEL/THE_FAMILY/mc96eco_devices.json',
    'documentation': '/Users/rsp_ms/GABRIEL/MC96ECOUNIVERSE_COMPLETE.md',
    'quick_ref': '/Users/rsp_ms/GABRIEL/mc96ecouniverse_quick_ref.py'
}

# ============================================================================
# QUICK COMMANDS
# ============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("\n🌐 MC96ECOUNIVERSE QUICK COMMANDS\n")
        print("Usage: python3 mc96ecouniverse_quick_ref.py [command]\n")
        print("Commands:")
        print("  scan        - Scan network for devices")
        print("  status      - Show network status")
        print("  online      - List online devices")
        print("  health      - Network health check")
        print("  topology    - Export network topology")
        print("  check NAME  - Check specific device")
        print("  add NAME IP TYPE - Add new device")
        sys.exit(0)
    
    command = sys.argv[1].lower()
    
    if command == 'scan':
        quick_scan()
    elif command == 'status':
        from mc96ecouniverse import MC96ECOUniverse
        mc96 = MC96ECOUniverse()
        mc96.display_status()
    elif command == 'online':
        list_online()
    elif command == 'health':
        network_health()
    elif command == 'topology':
        export_topology()
    elif command == 'check' and len(sys.argv) > 2:
        check_device(sys.argv[2])
    elif command == 'add' and len(sys.argv) > 4:
        add_new_device(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print(f"Unknown command: {command}")
        print("Use: python3 mc96ecouniverse_quick_ref.py (no arguments) for help")
