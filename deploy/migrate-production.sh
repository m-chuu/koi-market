#!/bin/bash
# =============================================================================
# Koi Market - Production Data Migration Script
# =============================================================================
#
# Runs the data migration against the Cloud SQL production database.
# Uses Cloud SQL Auth Proxy for secure local connection.
#
# Prerequisites:
#   1. Cloud SQL Auth Proxy installed:
#      https://cloud.google.com/sql/docs/postgres/connect-auth-proxy
#   2. Cloud SQL instance created (run setup-cloud-sql.sh first)
#   3. Python environment with dependencies installed
#
# Usage:
#   ./deploy/migrate-production.sh
#
# =============================================================================

set -e

# Configuration - UPDATE THESE VALUES
PROJECT_ID="${GCP_PROJECT_ID:-your-gcp-project-id}"
REGION="${GCP_REGION:-asia-southeast1}"
INSTANCE_NAME="koi-market-db"
INSTANCE_CONNECTION_NAME="${PROJECT_ID}:${REGION}:${INSTANCE_NAME}"
DB_NAME="koi_market"
DB_USER="postgres"
LOCAL_PORT=5433  # Use different port to avoid conflict with local PostgreSQL

echo "=============================================="
echo "Production Data Migration"
echo "=============================================="
echo "Instance: ${INSTANCE_CONNECTION_NAME}"
echo "Database: ${DB_NAME}"
echo "=============================================="

# Get password from Secret Manager
echo ""
echo "Fetching database password from Secret Manager..."
DB_PASSWORD=$(gcloud secrets versions access latest --secret="koi-market-db-password")

# Check if Cloud SQL Auth Proxy is installed
if ! command -v cloud-sql-proxy &> /dev/null; then
  echo ""
  echo "ERROR: cloud-sql-proxy not found!"
  echo ""
  echo "Install it from:"
  echo "  https://cloud.google.com/sql/docs/postgres/connect-auth-proxy#install"
  echo ""
  echo "macOS: brew install cloud-sql-proxy"
  echo "Or download from: https://dl.google.com/cloudsql/cloud-sql-proxy.darwin.amd64"
  exit 1
fi

# Start Cloud SQL Auth Proxy in background
echo ""
echo "Starting Cloud SQL Auth Proxy..."
cloud-sql-proxy "${INSTANCE_CONNECTION_NAME}" --port ${LOCAL_PORT} &
PROXY_PID=$!

# Wait for proxy to start
sleep 3

# Check if proxy is running
if ! kill -0 ${PROXY_PID} 2>/dev/null; then
  echo "ERROR: Cloud SQL Auth Proxy failed to start"
  exit 1
fi

echo "Proxy running on localhost:${LOCAL_PORT} (PID: ${PROXY_PID})"

# Navigate to backend directory
cd "$(dirname "$0")/../backend"

# Create virtual environment if needed
if [ ! -d "venv" ]; then
  echo ""
  echo "Creating Python virtual environment..."
  python3 -m venv venv
fi

# Activate virtual environment and install dependencies
source venv/bin/activate
pip install -q -r requirements.txt

# Run migration
echo ""
echo "Running migration..."
DATABASE_URL="postgresql://${DB_USER}:${DB_PASSWORD}@localhost:${LOCAL_PORT}/${DB_NAME}" \
  python migrate_data.py --clear

# Cleanup: Stop proxy
echo ""
echo "Stopping Cloud SQL Auth Proxy..."
kill ${PROXY_PID} 2>/dev/null || true

echo ""
echo "=============================================="
echo "Production Migration Complete!"
echo "=============================================="
