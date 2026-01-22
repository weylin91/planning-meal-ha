#!/bin/bash
# Script de build et copie du frontend React dans le dossier Home Assistant custom_component

set -e

FRONTEND_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(dirname "$FRONTEND_DIR")"
WWW_DIR="$ROOT_DIR/custom_components/meal_ha/www"

# Build du frontend
cd "$FRONTEND_DIR"
echo "➡️  Build du frontend..."
npm run build

# Création du dossier cible si besoin
mkdir -p "$WWW_DIR"

# Copie des fichiers buildés
cp -r dist/* "$WWW_DIR/"

echo "✅ Build copié dans $WWW_DIR"
