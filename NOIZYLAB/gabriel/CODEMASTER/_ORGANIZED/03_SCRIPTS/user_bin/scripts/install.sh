#!/bin/bash

# Install script for a robust, automated development environment

set -e

# --- Helper Functions ---
print_header() {
  echo "
================================================================
$1
================================================================
"
}

check_brew() {
  print_header "Checking for Homebrew"
  if ! command -v brew &> /dev/null; then
      echo "🍺 Homebrew not found. Installing..."
      /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  else
      echo "✅ Homebrew is already installed."
  fi
}

install_deps() {
  print_header "📦 Installing Core Dependencies"
  brew install git node python gh jq
  echo "✅ Core dependencies installed."
}

setup_npm_project() {
  print_header "⚙️  Initializing npm Project"
  if [ ! -f "package.json" ]; then
    echo "📄 No package.json found. Creating one..."
    npm init -y
  else
    echo "✅ package.json already exists."
  fi
  echo "Installing npm dependencies..."
  npm install
  echo "Linking CLI tools..."
  npm link
}

setup_git_hooks() {
  print_header "🪝 Setting up Git Hooks with Husky"
  echo "Installing Husky..."
  npm install husky --save-dev
  echo "Initializing Husky..."
  echo "Creating pre-commit hook..."
  # Create a pre-commit hook that runs the linter
  echo "npm run lint" > .husky/pre-commit
  chmod +x .husky/pre-commit
  echo "✅ Husky pre-commit hook created. 'npm run lint' will run before each commit."
}

setup_env_file() {
  print_header "🔑 Setting up Environment File"
  [ ! -f .env ] && [ -f .env.template ] && cp .env.template .env && echo "✅ Created .env from .env.template"
}

# --- Main Execution ---
print_header "🚀 Starting Development Environment Upgrade"
check_brew
install_deps
setup_npm_project
setup_git_hooks
setup_env_file
print_header "✨ Upgrade Complete! Your environment is now fortified. ✨"