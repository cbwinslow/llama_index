#!/bin/bash
# Cloudflare Pages build script for LlamaIndex documentation

echo "Starting LlamaIndex documentation build for Cloudflare Pages"

# Install system dependencies
echo "Installing system dependencies..."
apt-get update && apt-get install -y git

# Install poetry
echo "Installing poetry..."
curl -sSL https://install.python-poetry.org | python3 -

# Add poetry to PATH
export PATH="$HOME/.local/bin:$PATH"

# Install Python dependencies
echo "Installing Python dependencies..."
poetry install

# Pull external documentation
echo "Pulling external documentation..."
poetry run python scripts/merge_external_docs.py

# Prepare documentation for build
echo "Preparing documentation for build..."
poetry run prepare-for-build

# Build documentation
echo "Building documentation..."
poetry run mkdocs build

# Move built documentation to Cloudflare Pages output directory
echo "Moving built documentation to output directory..."
mkdir -p /opt/buildhome/repo/dist
cp -r site/* /opt/buildhome/repo/dist/

# Copy functions to output directory
echo "Copying Cloudflare Pages functions..."
mkdir -p /opt/buildhome/repo/functions
cp -r functions/* /opt/buildhome/repo/functions/

echo "Documentation build completed successfully!"