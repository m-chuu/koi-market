#!/bin/bash
# =============================================================================
# Koi Market - Cloud SQL Setup Script
# =============================================================================
#
# This script creates a Cloud SQL PostgreSQL instance for production.
# Run this ONCE before your first backend deployment.
#
# Prerequisites:
#   1. Google Cloud SDK installed
#   2. Authenticated: gcloud auth login
#   3. Project set: gcloud config set project YOUR_PROJECT_ID
#   4. APIs enabled:
#      gcloud services enable sqladmin.googleapis.com
#      gcloud services enable secretmanager.googleapis.com
#
# Usage:
#   ./deploy/setup-cloud-sql.sh
#
# =============================================================================

set -e

# Configuration - UPDATE THESE VALUES
PROJECT_ID="${GCP_PROJECT_ID:-your-gcp-project-id}"
REGION="${GCP_REGION:-asia-southeast1}"
INSTANCE_NAME="koi-market-db"
DB_NAME="koi_market"
DB_USER="postgres"

# Generate a random password
DB_PASSWORD=$(openssl rand -base64 24 | tr -dc 'a-zA-Z0-9' | head -c 24)

echo "=============================================="
echo "Setting up Cloud SQL for Koi Market"
echo "=============================================="
echo "Project: ${PROJECT_ID}"
echo "Region: ${REGION}"
echo "Instance: ${INSTANCE_NAME}"
echo "Database: ${DB_NAME}"
echo "=============================================="

# Create Cloud SQL instance
echo ""
echo "Creating Cloud SQL PostgreSQL instance..."
echo "(This may take 5-10 minutes)"
gcloud sql instances create "${INSTANCE_NAME}" \
  --database-version=POSTGRES_15 \
  --edition=ENTERPRISE \
  --tier=db-f1-micro \
  --region="${REGION}" \
  --storage-type=HDD \
  --storage-size=10GB \
  --no-backup \
  --no-deletion-protection

# Set the postgres user password
echo ""
echo "Setting database user password..."
gcloud sql users set-password "${DB_USER}" \
  --instance="${INSTANCE_NAME}" \
  --password="${DB_PASSWORD}"

# Create the database
echo ""
echo "Creating database..."
gcloud sql databases create "${DB_NAME}" \
  --instance="${INSTANCE_NAME}"

# Store password in Secret Manager
echo ""
echo "Storing password in Secret Manager..."
echo -n "${DB_PASSWORD}" | gcloud secrets create koi-market-db-password \
  --data-file=- \
  --replication-policy="automatic"

# Grant Cloud Run access to the secret
echo ""
echo "Granting Cloud Run access to secret..."
PROJECT_NUMBER=$(gcloud projects describe "${PROJECT_ID}" --format="value(projectNumber)")
gcloud secrets add-iam-policy-binding koi-market-db-password \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

# Get instance connection name
INSTANCE_CONNECTION_NAME=$(gcloud sql instances describe "${INSTANCE_NAME}" --format="value(connectionName)")

echo ""
echo "=============================================="
echo "Cloud SQL Setup Complete!"
echo "=============================================="
echo ""
echo "Instance Connection Name:"
echo "  ${INSTANCE_CONNECTION_NAME}"
echo ""
echo "Database Credentials:"
echo "  User: ${DB_USER}"
echo "  Database: ${DB_NAME}"
echo "  Password: (stored in Secret Manager as 'koi-market-db-password')"
echo ""
echo "Add these to your deploy script environment:"
echo "  export CLOUD_SQL_INSTANCE=${INSTANCE_CONNECTION_NAME}"
echo "  export DB_NAME=${DB_NAME}"
echo "  export DB_USER=${DB_USER}"
echo ""
echo "=============================================="
