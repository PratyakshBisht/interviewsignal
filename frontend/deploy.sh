#!/bin/bash
set -e

echo "🚀 InterviewSignal Deployment Script"
echo "==================================="

ENVIRONMENT=${1:-staging}
DOCKER_REGISTRY="ghcr.io"
IMAGE_NAME="interviewsignal/frontend"
BACKEND_IMAGE_NAME="interviewsignal/backend"

echo "Environment: $ENVIRONMENT"

deploy_frontend() {
    echo "▶ Building frontend bundle..."
    cd frontend && npm run build && cd ..
    echo "✓ Frontend bundle built successfully"
}

deploy_backend() {
    echo "▶ Verifying backend tests..."
    cd backend && python test_api.py && cd ..
    echo "✓ Backend tests passed successfully"
}

deploy_frontend
deploy_backend

echo "🎉 Deployment checks to $ENVIRONMENT completed successfully!"
