#!/bin/bash
set -o errexit

echo "Starting build process..."

# Upgrade pip to a stable version
echo "Upgrading pip..."
pip install --upgrade pip==23.3.1

# Install dependencies with pre-compiled wheels only
echo "Installing dependencies..."
pip install --only-binary=all -r requirements.txt

echo "Build completed successfully!"
