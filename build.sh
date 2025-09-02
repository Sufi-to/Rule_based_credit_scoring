#!/bin/bash
set -o errexit

# Upgrade pip to a stable version
pip install --upgrade pip==23.3.1

# Install dependencies with pre-compiled wheels only
pip install --only-binary=all -r requirements.txt
