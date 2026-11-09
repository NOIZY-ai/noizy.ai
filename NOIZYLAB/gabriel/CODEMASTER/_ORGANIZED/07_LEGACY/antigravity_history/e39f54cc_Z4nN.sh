#!/bin/bash
set -e

echo "Starting Gabriel System Code Universe Setup..."

# 1. Run the Python consolidation script
echo "Step 1: Running Code Consolidation (Mining Volumes)..."
python3 /Users/m2ultra/consolidate_code.py

# 2. Go to the Universe
cd /Users/m2ultra/NOIZYLAB/Code_Universe

# 3. Initialize Git
echo "Step 2: Initializing Git Repository..."
if [ ! -d ".git" ]; then
    git init
    # Configure git if needed (using system defaults)
else
    echo "Git already initialized."
fi

# 4. Add all files
echo "Step 3: Staging files..."
git add .

# 5. Commit
echo "Step 4: Committing..."
git commit -m "Initial commit: Consolidated Code Universe from external volumes" || echo "Nothing to commit"

# 6. Create and Push to GitHub
echo "Step 5: Creating/Pushing to GitHub (NOIZYLAB-io/Code_Universe)..."
# Check if remote exists
if git remote | grep -q origin; then
    echo "Remote 'origin' exists. Pushing..."
    git push -u origin main || git push -u origin master
else
    echo "Creating repo via gh cli..."
    gh repo create NOIZYLAB-io/Code_Universe --private --source=. --description "Consolidated Code Universe from Gabriel System" --push || {
        echo "Repo create failed (maybe exists?). Attempting to add remote and push..."
        git remote add origin https://github.com/NOIZYLAB-io/Code_Universe.git
        git push -u origin main || git push -u origin master
    }
fi

echo "Gabriel System Code Universe Setup Complete!"
