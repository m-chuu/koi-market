#!/bin/bash
# =============================================================================
# Koi Market - Frontend Deployment Script (Firebase Hosting)
# =============================================================================
#
# Prerequisites:
#   1. Firebase CLI installed: npm install -g firebase-tools
#   2. Authenticated: firebase login
#   3. Project linked: Update .firebaserc with your project ID
#   4. Backend deployed: Get the Cloud Run URL first
#
# Usage:
#   ./deploy/deploy-frontend.sh
#
# =============================================================================

set -e

# Configuration
FIREBASE_PROJECT="${FIREBASE_PROJECT_ID:-your-firebase-project-id}"

echo "=============================================="
echo "Deploying Koi Market Frontend to Firebase"
echo "=============================================="
echo "Project: ${FIREBASE_PROJECT}"
echo "=============================================="

# Navigate to project root
cd "$(dirname "$0")/.."

# Check if .env.production has been updated
if grep -q "your-cloud-run-service-url" .env.production; then
  echo ""
  echo "WARNING: .env.production still contains placeholder URL!"
  echo "Please update VITE_API_URL with your Cloud Run service URL."
  echo ""
  read -p "Continue anyway? (y/N) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
  fi
fi

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
  echo ""
  echo "Installing dependencies..."
  npm install
fi

# Build production bundle
echo ""
echo "Building production bundle..."
npm run build

# Deploy to Firebase
echo ""
echo "Deploying to Firebase Hosting..."
firebase deploy --only hosting --project "${FIREBASE_PROJECT}"

echo ""
echo "=============================================="
echo "Frontend Deployment Complete!"
echo "=============================================="
echo ""
echo "Your site is live at:"
echo "  https://${FIREBASE_PROJECT}.web.app"
echo "  https://${FIREBASE_PROJECT}.firebaseapp.com"
echo "=============================================="
