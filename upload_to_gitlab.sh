#!/bin/bash
# Upload to GitLab Script

# Check if git is installed
if ! command -v git &> /dev/null
then
    echo "git is not installed. Please install git first."
    exit 1
fi

# Check if GitLab CLI is installed
# Note: GitLab doesn't have an official CLI like GitHub, so we'll use git directly

echo "Please ensure you have:"
echo "1. A GitLab account"
echo "2. A personal access token with 'api' scope"
echo "3. Git configured with your username and email"
echo ""
echo "Press Enter to continue..."
read

# Create repository using GitLab API
echo "Creating new repository on GitLab..."
# You'll need to manually create the repo on GitLab.com first
# Or use curl with your personal access token:
# curl --header "PRIVATE-TOKEN: YOUR_ACCESS_TOKEN" \
#      --data "name=political-document-analysis&visibility=public" \
#      "https://gitlab.com/api/v4/projects"

echo "Please create a new repository on GitLab manually:"
echo "1. Go to https://gitlab.com/projects/new"
echo "2. Name it 'political-document-analysis'"
echo "3. Set visibility to Public"
echo "4. Do NOT initialize with a README"
echo ""
echo "Press Enter after creating the repository..."
read

# Get the repository URL
echo "Enter your GitLab username:"
read GITLAB_USERNAME

# Navigate to the llama_index directory
cd /home/cbwinslow/llama_index

# Initialize git repository if not already
git init

# Add all files
git add .

# Commit files
git commit -m "Initial commit: Political Document Analysis System"

# Add remote origin (replace with your actual GitLab repo URL)
git remote add origin https://gitlab.com/$GITLAB_USERNAME/political-document-analysis.git

# Push to GitLab
git branch -M main
git push -u origin main

echo "Repository uploaded to GitLab successfully!"
echo "Visit: https://gitlab.com/$GITLAB_USERNAME/political-document-analysis"