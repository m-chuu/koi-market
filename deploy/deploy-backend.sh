#!/bin/bash
# =============================================================================
# Koi Market - Backend Deployment Script (Google Cloud Run)
# =============================================================================
#
# Prerequisites:
#   1. Google Cloud SDK installed: https://cloud.google.com/sdk/docs/install
#   2. Authenticated: gcloud auth login
#   3. Project set: gcloud config set project YOUR_PROJECT_ID
#   4. APIs enabled (run once):
#      gcloud services enable run.googleapis.com
#      gcloud services enable sqladmin.googleapis.com
#      gcloud services enable cloudbuild.googleapis.com
#
# Usage:
#   ./deploy/deploy-backend.sh
#
# =============================================================================

set -e

# Configuration - UPDATE THESE VALUES
PROJECT_ID="${GCP_PROJECT_ID:-your-gcp-project-id}"
REGION="${GCP_REGION:-asia-southeast1}"
SERVICE_NAME="koi-market-api"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

# Cloud SQL Configuration
INSTANCE_CONNECTION_NAME="${CLOUD_SQL_INSTANCE:-${PROJECT_ID}:${REGION}:koi-market-db}"
DB_NAME="${DB_NAME:-koi_market}"
DB_USER="${DB_USER:-postgres}"

# Frontend URL for CORS (update after Firebase deployment)
FRONTEND_URL="${FRONTEND_URL:-https://your-project.web.app}"

echo "=============================================="
echo "Deploying Koi Market API to Cloud Run"
echo "=============================================="
echo "Project: ${PROJECT_ID}"
echo "Region: ${REGION}"
echo "Service: ${SERVICE_NAME}"
echo "Cloud SQL: ${INSTANCE_CONNECTION_NAME}"
echo "=============================================="

# Navigate to backend directory
cd "$(dirname "$0")/../backend"

# Build and push container image
echo ""
echo "Building container image..."
gcloud builds submit --tag "${IMAGE_NAME}" .

# Deploy to Cloud Run
echo ""
echo "Deploying to Cloud Run..."
gcloud run deploy "${SERVICE_NAME}" \
  --image "${IMAGE_NAME}" \
  --region "${REGION}" \
  --platform managed \
  --allow-unauthenticated \
  --add-cloudsql-instances "${INSTANCE_CONNECTION_NAME}" \
  --set-env-vars "INSTANCE_CONNECTION_NAME=${INSTANCE_CONNECTION_NAME}" \
  --set-env-vars "DB_NAME=${DB_NAME}" \
  --set-env-vars "DB_USER=${DB_USER}" \
  --set-env-vars "ENVIRONMENT=production" \
  --set-env-vars "FRONTEND_URL=${FRONTEND_URL}" \
  --set-secrets "DB_PASS=koi-market-db-password:latest" \
  --memory 512Mi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 10 \
  --concurrency 80

# Get the service URL
SERVICE_URL=$(gcloud run services describe "${SERVICE_NAME}" --region "${REGION}" --format="value(status.url)")

echo ""
echo "=============================================="
echo "Deployment Complete!"
echo "=============================================="
echo "Service URL: ${SERVICE_URL}"
echo ""
echo "Next steps:"
echo "1. Update .env.production with: VITE_API_URL=${SERVICE_URL}"
echo "2. Run the frontend deployment: ./deploy/deploy-frontend.sh"
echo "=============================================="
