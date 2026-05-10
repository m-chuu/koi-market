# Koi Market - Deployment Guide

This guide walks you through deploying Koi Market to Google Cloud Platform (Cloud Run + Cloud SQL) and Firebase Hosting.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         PRODUCTION                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌──────────────────┐          ┌──────────────────┐            │
│   │  Firebase        │          │  Google Cloud    │            │
│   │  Hosting         │  ──────► │  Run             │            │
│   │                  │  API     │                  │            │
│   │  React Frontend  │  Calls   │  FastAPI Backend │            │
│   └──────────────────┘          └────────┬─────────┘            │
│                                          │                       │
│                                          │ Unix Socket           │
│                                          ▼                       │
│                                 ┌──────────────────┐            │
│                                 │  Google Cloud    │            │
│                                 │  SQL (PostgreSQL)│            │
│                                 └──────────────────┘            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Prerequisites

### 1. Google Cloud Setup

```bash
# Install Google Cloud SDK
# https://cloud.google.com/sdk/docs/install

# Login and set project
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable sqladmin.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable secretmanager.googleapis.com
```

### 2. Firebase Setup

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login to Firebase
firebase login

# Update .firebaserc with your project ID
```

## Deployment Steps

### Step 1: Create Cloud SQL Database

Run the setup script to create your production PostgreSQL database:

```bash
# Set your project ID
export GCP_PROJECT_ID=your-project-id
export GCP_REGION=asia-southeast1  # or your preferred region

# Run setup script
./deploy/setup-cloud-sql.sh
```

This script will:
- Create a Cloud SQL PostgreSQL 16 instance
- Create the `koi_market` database
- Store the password in Secret Manager
- Grant Cloud Run access to the secret

**Save the Instance Connection Name** - you'll need it for the next step.

### Step 2: Deploy Backend to Cloud Run

```bash
# Set environment variables
export GCP_PROJECT_ID=your-project-id
export GCP_REGION=asia-southeast1
export CLOUD_SQL_INSTANCE=your-project-id:asia-southeast1:koi-market-db
export FRONTEND_URL=https://your-project.web.app

# Deploy backend
./deploy/deploy-backend.sh
```

After deployment, **copy the Service URL** (e.g., `https://koi-market-api-xxxxx-as.a.run.app`).

### Step 3: Migrate Production Data

```bash
# Run migration against production database
./deploy/migrate-production.sh
```

### Step 4: Update Frontend Configuration

Update `.env.production` with your Cloud Run URL:

```bash
# .env.production
VITE_API_URL=https://koi-market-api-xxxxx-as.a.run.app
```

### Step 5: Deploy Frontend to Firebase

```bash
# Update .firebaserc with your Firebase project ID first
export FIREBASE_PROJECT_ID=your-firebase-project

# Deploy frontend
./deploy/deploy-frontend.sh
```

### Step 6: Update CORS (if needed)

If your Firebase URL is different from what you set in Step 2, redeploy the backend:

```bash
export FRONTEND_URL=https://your-actual-firebase-url.web.app
./deploy/deploy-backend.sh
```

## Verification

1. **Check Backend Health:**
   ```bash
   curl https://your-cloud-run-url.run.app/health
   ```

2. **Check Products API:**
   ```bash
   curl https://your-cloud-run-url.run.app/api/v1/products
   ```

3. **Visit Frontend:**
   Open `https://your-project.web.app` in your browser.

## Environment Variables Reference

### Backend (Cloud Run)

| Variable | Description | Example |
|----------|-------------|---------|
| `INSTANCE_CONNECTION_NAME` | Cloud SQL instance | `project:region:instance` |
| `DB_NAME` | Database name | `koi_market` |
| `DB_USER` | Database user | `postgres` |
| `DB_PASS` | Database password | (from Secret Manager) |
| `ENVIRONMENT` | Environment mode | `production` |
| `FRONTEND_URL` | Frontend URL for CORS | `https://xxx.web.app` |

### Frontend (Vite)

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API URL | `https://xxx.run.app` |

## Cost Estimation

With minimal usage:

| Service | Estimated Cost |
|---------|---------------|
| Cloud SQL (db-f1-micro) | ~$7-10/month |
| Cloud Run | Pay per request (free tier: 2M requests/month) |
| Firebase Hosting | Free tier: 10GB storage, 360MB/day transfer |
| Secret Manager | Free tier: 6 active secret versions |

**Tip:** Set `--min-instances 0` on Cloud Run to scale to zero when not in use.

## Troubleshooting

### Cloud Run can't connect to Cloud SQL

1. Verify the instance connection name is correct
2. Check Cloud Run service account has `Cloud SQL Client` role
3. Ensure the `--add-cloudsql-instances` flag is set

### CORS errors on frontend

1. Check `FRONTEND_URL` environment variable on Cloud Run
2. Ensure it matches your Firebase Hosting URL exactly
3. Redeploy backend after updating

### Database connection timeout

1. Check Cloud SQL instance is running: `gcloud sql instances list`
2. Verify Secret Manager secret exists: `gcloud secrets list`
3. Check Cloud Run logs: `gcloud run services logs read koi-market-api`

## Useful Commands

```bash
# View Cloud Run logs
gcloud run services logs read koi-market-api --region asia-southeast1

# Connect to Cloud SQL locally
cloud-sql-proxy your-project:asia-southeast1:koi-market-db --port 5433

# Update a single environment variable
gcloud run services update koi-market-api \
  --region asia-southeast1 \
  --set-env-vars "FRONTEND_URL=https://new-url.web.app"

# View secret value
gcloud secrets versions access latest --secret=koi-market-db-password
```
