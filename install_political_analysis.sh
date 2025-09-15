#!/bin/bash
# Installation script for Political Document Analysis System

echo "Installing Political Document Analysis System dependencies..."

# Install Python dependencies
pip install -r political_analysis_requirements.txt

# Install Playwright browsers (for web crawling)
playwright install-deps
playwright install

# Create necessary directories
mkdir -p data/sample_docs output logs models

echo "Installation completed!"

echo "Next steps:"
echo "1. Set up your API keys in the .env.political_analysis file"
echo "2. Run the test script: python test_political_analysis.py"
echo "3. Try the demo notebook: jupyter notebook political_analysis_demo.ipynb"