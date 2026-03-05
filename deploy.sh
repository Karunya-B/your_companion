#!/bin/bash

# Karunya Companion Deployment Script

echo "🚀 Karunya Companion Deployment Script"
echo "====================================="

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Installing Railway CLI..."
    npm install -g @railway/cli
fi

# Login to Railway
echo "🔑 Login to Railway..."
railway login

# Deploy backend
echo "🔧 Deploying backend..."
railway init
railway up

# Get backend URL
BACKEND_URL=$(railway domain)

echo "✅ Backend deployed at: $BACKEND_URL"

# Deploy frontend
echo "🎨 Deploying frontend..."
cd frontend

# Set API URL for production
echo "VITE_API_URL=$BACKEND_URL/api/v1" > .env.production

# Build frontend
npm run build

# Deploy to Vercel (or you can use Railway for both)
if command -v vercel &> /dev/null; then
    echo "📤 Deploying frontend to Vercel..."
    vercel --prod
else
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
    vercel --prod
fi

echo "🎉 Deployment complete!"
echo "🌐 Your app is live!"
echo "📖 Check README.md for more deployment options"