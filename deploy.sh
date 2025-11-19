#!/usr/bin/env bash
# Helper script to create a GitHub repo for this project and push current branch.
# Requires: git, (optionally) gh CLI for automatic repo creation.
# Usage:
#   ./deploy.sh <github-username> <repo-name>
# Examples:
#   ./deploy.sh kishan Heart-Attack-Analysis-Prediction

set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <github-username> <repo-name>"
  exit 1
fi

USER="$1"
REPO="$2"

# initialize git if needed
if [ ! -d .git ]; then
  echo "Initializing git repository..."
  git init
  git add .
  git commit -m "Initial commit"
else
  echo "Git repository already initialized."
fi

# Try to use gh if available
if command -v gh >/dev/null 2>&1; then
  echo "Creating remote repo using gh..."
  gh repo create "$USER/$REPO" --public --source=. --remote=origin --push || true
  echo "Pushed to https://github.com/$USER/$REPO"
else
  echo "gh CLI not found. Please create an empty repository on GitHub and then run the following commands:" 
  echo "  git remote add origin https://github.com/$USER/$REPO.git"
  echo "  git branch -M main"
  echo "  git push -u origin main"
fi

echo "Done. Now go to https://share.streamlit.io and create a new app using the repository https://github.com/$USER/$REPO and point the app file to 'heart.py'."
