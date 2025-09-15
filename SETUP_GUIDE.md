# Setup Guide: Political Document Analysis System

This guide will help you set up and run the Political Document Analysis System on your local machine.

## System Requirements

- Python 3.8 or higher
- Git
- At least 4GB RAM (8GB recommended)
- 10GB free disk space (for dependencies and data)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/cbwinslow/political-document-analysis.git
cd political-document-analysis
```

### 2. Set Up Python Environment

It's recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
./install_political_analysis.sh
```

Or manually install dependencies:

```bash
pip install -r political_analysis_requirements.txt
playwright install-deps
playwright install
```

### 4. Configure Environment Variables

Create a `.env` file based on the example:

```bash
cp .env.political_analysis .env
```

Edit the `.env` file to add your API keys:

- OpenAI API key
- Neo4j database credentials
- Web crawling service keys (if needed)

### 5. Create Required Directories

```bash
mkdir -p data/sample_docs output logs models
```

### 6. Test the Installation

```bash
python test_political_analysis.py
```

### 7. Run the Demo

```bash
jupyter notebook political_analysis_demo.ipynb
```

## Configuration

### Main Configuration File

Edit `political_analysis_config.ini` to adjust system settings:

- Ingestion parameters
- Extraction settings
- Graph database configuration
- LLM and embedding model settings

### Web Crawling Configuration

Review `political_crawling_config.py` for:

- Political websites to crawl
- RSS feeds to monitor
- Sitemaps to process
- Crawling parameters

## Usage

### Basic Document Analysis

```python
from political_analysis_orchestrator import PoliticalAnalysisOrchestrator

# Initialize orchestrator
orchestrator = PoliticalAnalysisOrchestrator()

# Define sources
sources = {
    "local_directories": ["./data/sample_docs"],
    "websites": ["https://example.gov/politics"],
    "rss_feeds": ["https://example.com/politics/rss"]
}

# Run analysis
results = await orchestrator.run_complete_analysis(sources)
```

### Question Answering

```python
# Ask specific questions about political content
answer = await orchestrator.run_targeted_analysis(
    "What are the key policy positions on climate change?"
)
```

## Component Overview

### Document Ingestion
- `PoliticalDocumentIngestor`: Loads documents from multiple sources
- Supports local files, websites, RSS feeds, sitemaps

### Entity Extraction
- `PoliticalEntityExtractor`: Extracts political entities
- Identifies politicians, parties, legislation, policies

### Knowledge Graph
- `PoliticalKnowledgeGraph`: Manages entity relationships
- Uses Neo4j for graph storage and querying

### Tool Integration
- `PoliticalMCPIntegration`: Connects to specialized tools
- Supports Model Context Protocol servers

### Analysis Agent
- `PoliticalAnalysisAgent`: Intelligent document analysis
- Answers questions using LLMs and tools

### Orchestration
- `PoliticalAnalysisOrchestrator`: Coordinates all components
- Provides high-level analysis workflow

## Troubleshooting

### Common Issues

1. **Missing dependencies**: Run the installation script again
2. **API key errors**: Verify your `.env` file contains valid keys
3. **Import errors**: Ensure you're in the correct directory and virtual environment
4. **Memory errors**: Close other applications or increase swap space

### Getting Help

- Check the logs in the `logs/` directory
- Review error messages carefully
- Consult the documentation in README files
- Open an issue on GitHub if you encounter bugs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.