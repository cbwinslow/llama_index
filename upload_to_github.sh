#!/bin/bash
# Upload to GitHub Script

# Check if git is installed
if ! command -v git &> /dev/null
then
    echo "git is not installed. Please install git first."
    exit 1
fi

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null
then
    echo "GitHub CLI (gh) is not installed. Please install it first:"
    echo "Visit: https://cli.github.com/"
    exit 1
fi

# Authenticate with GitHub (you'll need to do this manually)
echo "Please authenticate with GitHub:"
gh auth login

# Create a new repository on GitHub
echo "Creating new repository on GitHub..."
gh repo create political-document-analysis --public --clone

# Navigate to the repository directory
cd political-document-analysis

# Copy all files from the llama_index directory
echo "Copying files to repository..."
cp -r /home/cbwinslow/llama_index/* .

# Initialize git repository if not already
git init

# Add all files
git add .

# Commit files
git commit -m "Initial commit: Political Document Analysis System"

# Push to GitHub
git branch -M main
git remote add origin https://github.com/cbwinslow/political-document-analysis.git
git push -u origin main

echo "Repository uploaded to GitHub successfully!"
echo "Visit: https://github.com/cbwinslow/political-document-analysis"