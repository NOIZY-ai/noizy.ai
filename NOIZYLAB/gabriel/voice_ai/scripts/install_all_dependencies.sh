#!/bin/bash
# 🛠️ INSTALL ALL DEPENDENCIES - 100% PERFECT
# GORUNFREE Protocol

set -e

echo "🔧 Installing all GABRIEL dependencies..."
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python version: $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install requirements
echo "📥 Installing requirements..."
pip install -r requirements.txt

# Install infrastructure requirements
if [ -f "infrastructure/requirements.txt" ]; then
    echo "📥 Installing infrastructure requirements..."
    pip install -r infrastructure/requirements.txt
fi

# Verify installations
echo ""
echo "✅ Verifying installations..."
python3 -c "import fastapi; print('✅ FastAPI')" || echo "❌ FastAPI"
python3 -c "import sqlalchemy; print('✅ SQLAlchemy')" || echo "❌ SQLAlchemy"
python3 -c "import redis; print('✅ Redis')" || echo "❌ Redis"
python3 -c "import boto3; print('✅ Boto3')" || echo "❌ Boto3"
python3 -c "import celery; print('✅ Celery')" || echo "❌ Celery"
python3 -c "import stripe; print('✅ Stripe')" || echo "❌ Stripe"
python3 -c "import structlog; print('✅ Structlog')" || echo "❌ Structlog"
python3 -c "import prometheus_client; print('✅ Prometheus')" || echo "❌ Prometheus"
python3 -c "import pytest; print('✅ Pytest')" || echo "❌ Pytest"

echo ""
echo "🎉 Installation complete!"
echo ""
echo "To activate the virtual environment:"
echo "  source .venv/bin/activate"

