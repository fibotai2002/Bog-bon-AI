#!/bin/bash

# Loyiha ID si (buni o'zingiznikiga o'zgartiring yoki gcloud config dan oladi)
PROJECT_ID=$(gcloud config get-value project)
APP_NAME="agro-ai-bot"
REGION="us-central1" # Yoki o'zingizga qulay region

echo "🚀 Deploy jarayoni boshlanmoqda..."
echo "Project ID: $PROJECT_ID"
echo "App Name: $APP_NAME"

# 1. Docker rasmini qurish
echo "🔨 Docker imijini qurish..."
docker build -t gcr.io/$PROJECT_ID/$APP_NAME .

# 2. Docker rasmini GCR ga yuklash
echo "⬆️ GCR ga yuklash..."
docker push gcr.io/$PROJECT_ID/$APP_NAME

# 3. Cloud Run ga deploy qilish
echo "☁️ Cloud Run ga deploy qilish..."
gcloud run deploy $APP_NAME \
    --image gcr.io/$PROJECT_ID/$APP_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --set-env-vars "$(grep -v '^#' .env | xargs | sed 's/ /,/g')"

echo "✅ Deploy muvaffaqiyatli yakunlandi!"
