#!/bin/bash

# Simple script to update documentation locally
# Usage: ./update-docs.sh

echo "Updating documentation from repositories..."

# Check if Python dependencies are installed
python3 -c "import requests, yaml" 2>/dev/null || {
    echo "Installing Python dependencies..."
    pip3 install requests pyyaml
}

# Run the fetch script
python3 fetch_readmes.py

echo "Documentation updated successfully!"
echo "Preview with: bundle exec jekyll serve"