#!/usr/bin/env python3
"""
🌐 TERMINUS + TERMIUS API BRIDGE
Ultimate remote terminal management for the MC96ECOUNIVERSE
Deploy, connect, and control terminals across all devices
"""

import subprocess
import sys
import os
from pathlib import Path
import json
import requests
from typing import Dict, List, Optional
import time

class TermiusBridge:
    """
    🌐 Termius API Bridge Integration
    Manage remote terminals across the entire MC96ECOUNIVERSE
    """
    
    def __init__(self, bridge_url: str = "http://localhost:8080"):
        self.bridge_url = bridge_url
        self.credentials_file = Path.home() / ".termius" / "termius-bridge-credentials.json"
        self.workspace = Path.cwd()
        self.docker_image = "termius/api-bridge:latest"
        self.container_name = "termius-api-bridge"
        
        print("\n" + "=" * 80)
        print("🌐 TERMINUS + TERMIUS API BRIDGE")
        print("   Remote Terminal Control for MC96ECOUNIVERSE")
        print("=" * 80)
    
    def check_docker(self) -> bool:
        """Check if Docker is available."""
        print("\n🐋 Checking Docker...")
        try:
            result = subprocess.run(['docker', '--version'], 
                                  capture_output=True, text=True, check=False)
            if result.returncode == 0:
                print(f"✅ Docker found: {result.stdout.strip()}")
                return True
            else:
                print("❌ Docker not found")
                return False
        except FileNotFoundError:
            print("❌ Docker not installed")
            return False
    
    def setup_credentials(self) -> bool:
        """Setup Termius API Bridge credentials."""
        print("\n🔑 Setting up Termius API Bridge credentials...")
        
        if self.credentials_file.exists():
            print(f"✅ Credentials file found: {self.credentials_file}")
            return True
        
        print(f"⚠️  Credentials file not found: {self.credentials_file}")
        print("\n📝 To set up Termius API Bridge:")
        print("   1. Go to Termius app > Settings > API Bridge")
        print("   2. Create new API Bridge")
        print("   3. Download credentials JSON file")
        print(f"   4. Save to: {self.credentials_file}")
        
        # Create directory if needed
        self.credentials_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Option to paste credentials
        print("\n💡 Or paste your credentials JSON here (press Ctrl+D when done):")
        try:
            lines = []
            while True:
                try:
                    line = input()
                    lines.append(line)
                except EOFError:
                    break
            
            if lines:
                credentials_json = '\n'.join(lines)
                try:
                    # Validate JSON
                    json.loads(credentials_json)
                    
                    # Save to file
                    with open(self.credentials_file, 'w') as f:
                        f.write(credentials_json)
                    
                    print(f"\n✅ Credentials saved to: {self.credentials_file}")
                    return True
                except json.JSONDecodeError:
                    print("❌ Invalid JSON format")
                    return False
        except KeyboardInterrupt:
            print("\n⏸️  Setup cancelled")
            return False
        
        return False
    
    def deploy_bridge(self, port: int = 8080) -> bool:
        """Deploy Termius API Bridge using Docker."""
        print(f"\n🚀 Deploying Termius API Bridge on port {port}...")
        
        if not self.check_docker():
            return False
        
        if not self.credentials_file.exists():
            if not self.setup_credentials():
                return False
        
        # Stop existing container if running
        print("\n🧹 Cleaning up existing container...")
        subprocess.run(['docker', 'stop', self.container_name], 
                      capture_output=True, check=False)
        subprocess.run(['docker', 'rm', self.container_name], 
                      capture_output=True, check=False)
        
        # Pull latest image
        print("\n📥 Pulling latest Termius API Bridge image...")
        result = subprocess.run([
            'docker', 'pull', self.docker_image
        ], capture_output=True, text=True, check=False)
        
        if result.returncode != 0:
            print(f"❌ Failed to pull image: {result.stderr}")
            return False
        
        print("✅ Image pulled successfully")
        
        # Run container
        print(f"\n🚀 Starting API Bridge container...")
        cmd = [
            'docker', 'run',
            '--name', self.container_name,
            '--pull=always',
            '-p', f'{port}:8080',
            '--volume', f'{self.credentials_file}:/home/termius/.termius/termius-bridge-credentials.json',
            '-d',  # Detached mode
            self.docker_image
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        
        if result.returncode != 0:
            print(f"❌ Failed to start container: {result.stderr}")
            return False
        
        container_id = result.stdout.strip()
        print(f"✅ Container started: {container_id[:12]}")
        
        # Wait for API to be ready
        print("\n⏳ Waiting for API Bridge to be ready...")
        for i in range(10):
            time.sleep(2)
            if self.check_bridge_health():
                print("✅ API Bridge is ready!")
                print(f"\n🌐 Access API documentation at: {self.bridge_url}")
                return True
            print(f"   Attempt {i+1}/10...")
        
        print("⚠️  API Bridge started but health check timed out")
        return True
    
    def check_bridge_health(self) -> bool:
        """Check if API Bridge is healthy."""
        try:
            response = requests.get(f"{self.bridge_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def stop_bridge(self) -> bool:
        """Stop Termius API Bridge container."""
        print("\n🛑 Stopping API Bridge...")
        
        result = subprocess.run(['docker', 'stop', self.container_name],
                              capture_output=True, text=True, check=False)
        
        if result.returncode == 0:
            print("✅ API Bridge stopped")
            return True
        else:
            print(f"❌ Failed to stop: {result.stderr}")
            return False
    
    def restart_bridge(self) -> bool:
        """Restart API Bridge."""
        print("\n🔄 Restarting API Bridge...")
        
        result = subprocess.run(['docker', 'restart', self.container_name],
                              capture_output=True, text=True, check=False)
        
        if result.returncode == 0:
            print("✅ API Bridge restarted")
            return True
        else:
            print(f"❌ Failed to restart: {result.stderr}")
            return False
    
    def show_bridge_status(self):
        """Show API Bridge status."""
        print("\n📊 TERMIUS API BRIDGE STATUS:")
        print("=" * 80)
        
        # Check Docker
        docker_ok = self.check_docker()
        print(f"Docker:       {'✅ Available' if docker_ok else '❌ Not available'}")
        
        # Check credentials
        creds_ok = self.credentials_file.exists()
        print(f"Credentials:  {'✅ Found' if creds_ok else '❌ Not found'}")
        
        # Check container
        result = subprocess.run(['docker', 'ps', '--filter', f'name={self.container_name}'],
                              capture_output=True, text=True, check=False)
        
        container_running = self.container_name in result.stdout
        print(f"Container:    {'✅ Running' if container_running else '⚪ Not running'}")
        
        # Check API health
        if container_running:
            api_healthy = self.check_bridge_health()
            print(f"API Health:   {'✅ Healthy' if api_healthy else '❌ Unhealthy'}")
            print(f"API URL:      {self.bridge_url}")
        
        print("=" * 80)
        
        # Show container logs if running
        if container_running:
            print("\n📜 Recent logs:")
            result = subprocess.run(['docker', 'logs', '--tail', '20', self.container_name],
                                  capture_output=True, text=True, check=False)
            if result.stdout:
                print(result.stdout)
    
    def show_docker_compose(self):
        """Generate docker-compose.yml for API Bridge."""
        compose_content = f"""version: '3.8'

services:
  termius-api-bridge:
    image: {self.docker_image}
    container_name: {self.container_name}
    ports:
      - "8080:8080"
    volumes:
      - {self.credentials_file}:/home/termius/.termius/termius-bridge-credentials.json
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
"""
        
        print("\n📝 DOCKER COMPOSE CONFIGURATION:")
        print("=" * 80)
        print(compose_content)
        print("=" * 80)
        
        # Option to save
        save = input("\n💾 Save to docker-compose.yml? (y/n): ").strip().lower()
        if save == 'y':
            compose_file = self.workspace / 'docker-compose.yml'
            with open(compose_file, 'w') as f:
                f.write(compose_content)
            print(f"✅ Saved to: {compose_file}")
            print("\n🚀 To deploy with docker-compose:")
            print("   docker-compose up -d")
    
    def create_deployment_script(self):
        """Create deployment script for easy setup."""
        script_content = f"""#!/bin/bash
# Termius API Bridge Deployment Script for GABRIEL

set -e

echo "🌐 Deploying Termius API Bridge..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Set credentials file path
export BRIDGE_CREDENTIALS_FILE="{self.credentials_file}"

# Check if credentials file exists
if [ ! -f "$BRIDGE_CREDENTIALS_FILE" ]; then
    echo "❌ Credentials file not found: $BRIDGE_CREDENTIALS_FILE"
    echo ""
    echo "📝 To get credentials:"
    echo "   1. Open Termius app"
    echo "   2. Go to Settings > API Bridge"
    echo "   3. Create new API Bridge"
    echo "   4. Download credentials JSON"
    echo "   5. Save to: $BRIDGE_CREDENTIALS_FILE"
    exit 1
fi

# Stop and remove existing container
echo "🧹 Cleaning up existing container..."
docker stop {self.container_name} 2>/dev/null || true
docker rm {self.container_name} 2>/dev/null || true

# Pull latest image
echo "📥 Pulling latest image..."
docker pull {self.docker_image}

# Run container
echo "🚀 Starting API Bridge..."
docker run --name "{self.container_name}" \\
  --pull=always -p "8080:8080" \\
  --volume "$BRIDGE_CREDENTIALS_FILE:/home/termius/.termius/termius-bridge-credentials.json" \\
  -d \\
  {self.docker_image}

# Wait for API to be ready
echo "⏳ Waiting for API Bridge to be ready..."
for i in {{1..30}}; do
    if curl -s http://localhost:8080/health > /dev/null 2>&1; then
        echo "✅ API Bridge is ready!"
        echo ""
        echo "🌐 API Documentation: http://localhost:8080"
        echo "🎯 Container: {self.container_name}"
        echo ""
        echo "📊 To check status:  docker logs {self.container_name}"
        echo "🛑 To stop:         docker stop {self.container_name}"
        echo "🔄 To restart:      docker restart {self.container_name}"
        exit 0
    fi
    echo "   Attempt $i/30..."
    sleep 2
done

echo "⚠️  API Bridge started but health check timed out"
echo "📊 Check logs: docker logs {self.container_name}"
exit 1
"""
        
        script_file = self.workspace / 'deploy_termius_bridge.sh'
        with open(script_file, 'w') as f:
            f.write(script_content)
        
        os.chmod(script_file, 0o755)
        
        print(f"\n✅ Deployment script created: {script_file}")
        print("\n🚀 To deploy, run:")
        print(f"   ./{script_file.name}")
        
        return script_file


def main():
    """Main menu for Termius API Bridge management."""
    bridge = TermiusBridge()
    
    while True:
        print("\n" + "=" * 80)
        print("🌐 TERMINUS + TERMIUS API BRIDGE - MANAGEMENT")
        print("=" * 80)
        
        print("\n📋 OPTIONS:")
        print("  1. Deploy API Bridge (Docker)")
        print("  2. Stop API Bridge")
        print("  3. Restart API Bridge")
        print("  4. Show status")
        print("  5. Setup credentials")
        print("  6. Generate docker-compose.yml")
        print("  7. Create deployment script")
        print("  8. Open API documentation")
        print("  9. Show container logs")
        print("  0. Exit")
        
        choice = input("\n🌐 Select option: ").strip()
        
        if choice == '1':
            port = input("Port (default 8080): ").strip() or "8080"
            bridge.deploy_bridge(int(port))
            
        elif choice == '2':
            bridge.stop_bridge()
            
        elif choice == '3':
            bridge.restart_bridge()
            
        elif choice == '4':
            bridge.show_bridge_status()
            
        elif choice == '5':
            bridge.setup_credentials()
            
        elif choice == '6':
            bridge.show_docker_compose()
            
        elif choice == '7':
            bridge.create_deployment_script()
            
        elif choice == '8':
            print(f"\n🌐 Opening {bridge.bridge_url} in browser...")
            subprocess.run(['open', bridge.bridge_url], check=False)
            
        elif choice == '9':
            print("\n📜 Container logs:")
            subprocess.run(['docker', 'logs', '--tail', '50', bridge.container_name])
            
        elif choice == '0':
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid option")
        
        input("\n⏸️  Press Enter to continue...")


if __name__ == "__main__":
    main()
