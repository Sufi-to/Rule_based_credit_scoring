#!/bin/bash
set -e

echo "🐍 Python version check:"
python --version

echo "📦 Installing dependencies..."
pip install --upgrade pip==23.2.1
pip install --no-cache-dir -r requirements.txt

echo "✅ Build completed successfully!"
