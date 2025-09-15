# Deployment Guide: Political Document Analysis System

This guide will help you upload the Political Document Analysis System to GitHub and GitLab.

## Prerequisites

Before uploading, ensure you have:

1. Git installed on your system
2. GitHub/GitLab accounts
3. Personal access tokens for both platforms
4. SSH keys set up (recommended)

## GitHub Deployment

### Option 1: Using GitHub CLI (Recommended)

1. Install GitHub CLI:
   - Visit: https://cli.github.com/
   - Follow installation instructions for your OS

2. Run the upload script:
   ```bash
   cd /home/cbwinslow/llama_index
   ./upload_to_github.sh
   ```

3. Follow the prompts to authenticate and create the repository

### Option 2: Manual Upload

1. Create a new repository on GitHub:
   - Go to https://github.com/new
   - Name: `political-document-analysis`
   - Set to Public
   - Do NOT initialize with a README

2. Clone the repository locally:
   ```bash
   git clone https://github.com/cbwinslow/political-document-analysis.git
   cd political-document-analysis
   ```

3. Copy all files from the project directory:
   ```bash
   cp -r /home/cbwinslow/llama_index/* .
   ```

4. Commit and push:
   ```bash
   git add .
   git commit -m "Initial commit: Political Document Analysis System"
   git branch -M main
   git push -u origin main
   ```

## GitLab Deployment

### Manual Upload

1. Create a new repository on GitLab:
   - Go to https://gitlab.com/projects/new
   - Name: `political-document-analysis`
   - Set to Public
   - Do NOT initialize with a README

2. Run the upload script:
   ```bash
   cd /home/cbwinslow/llama_index
   ./upload_to_gitlab.sh
   ```

3. Follow the prompts to enter your GitLab username and complete the upload

### Alternative Manual Method

1. Navigate to your project directory:
   ```bash
   cd /home/cbwinslow/llama_index
   ```

2. Initialize git repository:
   ```bash
   git init
   ```

3. Add and commit all files:
   ```bash
   git add .
   git commit -m "Initial commit: Political Document Analysis System"
   ```

4. Add remote origin and push:
   ```bash
   git remote add origin https://gitlab.com/cbwinslow/political-document-analysis.git
   git branch -M main
   git push -u origin main
   ```

## Post-Upload Steps

After uploading, you should:

1. Verify that all files are present in the repository
2. Update the README with any platform-specific information
3. Set up any necessary webhooks or CI/CD pipelines
4. Add collaborators if needed
5. Configure repository settings (issues, wiki, etc.)

## Security Notes

- The `.gitignore` file is configured to exclude sensitive files like `.env` files
- Make sure to never commit API keys or personal credentials
- Review the repository contents before making it public

## Troubleshooting

If you encounter issues:

1. **Authentication errors**: Ensure your Git credentials are set up correctly
2. **Permission denied**: Check that you have the necessary permissions for the repository
3. **File upload issues**: Verify that all files are readable and not locked
4. **Large file errors**: Consider using Git LFS for large model or data files

For additional help, refer to:
- GitHub documentation: https://docs.github.com/
- GitLab documentation: https://docs.gitlab.com/