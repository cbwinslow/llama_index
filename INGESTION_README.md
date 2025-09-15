# Political Document Ingestion System

This directory contains scripts and tools for ingesting political documents into the Political Document Analysis System.

## Ingestion Scripts

### 1. Simple Test Ingestion (`simple_test_ingestion.py`)
A minimal script that demonstrates local document ingestion without external dependencies.

**Usage:**
```bash
python simple_test_ingestion.py
```

This script:
- Reads documents from `./data/sample_docs/`
- Processes only local files (no web crawling)
- Saves ingested documents to `./output/ingested_documents/`

### 2. Full Ingestion Pipeline (`full_ingestion_pipeline.py`)
A comprehensive ingestion pipeline that supports multiple source types.

**Usage:**
```bash
python full_ingestion_pipeline.py [config_file.json]
```

This script:
- Supports local files, websites, RSS feeds, and sitemaps
- Requires additional dependencies for web crawling
- Generates detailed ingestion reports
- Saves documents with full metadata

## Configuration

### Default Sources
The system is configured to process:
- Local documents from `./data/sample_docs/`
- (Optional) Web sources (when dependencies are installed)

### Custom Configuration
Create a JSON configuration file to specify your own sources:

```json
{
    "local_directories": [
        "./data/my_documents"
    ],
    "websites": [
        "https://example.gov/politics"
    ],
    "rss_feeds": [
        "https://example.com/politics/rss"
    ],
    "sitemaps": [
        "https://example.gov/sitemap.xml"
    ]
}
```

## Output

Ingested documents are saved to:
- `./output/ingested_documents/` (simple ingestion)
- `./output/full_ingestion/` (full pipeline)

Each document is saved as a text file with:
- Document ID
- Metadata (file path, type, size, dates)
- Full document content

## Dependencies

### Minimal Requirements
- Python 3.8+
- `llama-index-core`
- `llama-index-readers-file`

### Full Requirements
- All minimal requirements
- `llama-index-readers-web` (for web crawling)
- `python-dotenv` (for configuration)
- `pydantic`, `tqdm`, `requests`, `beautifulsoup4`

## Running with Virtual Environment

To avoid system-wide package conflicts:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install llama-index-core llama-index-readers-file

# Run ingestion
python simple_test_ingestion.py

# Deactivate when done
deactivate
```

## Next Steps

1. **Install full dependencies** to enable web crawling:
   ```bash
   pip install llama-index-readers-web python-dotenv
   ```

2. **Set up API keys** in `.env` file for LLM services

3. **Run the full pipeline** with custom sources:
   ```bash
   python full_ingestion_pipeline.py my_sources.json
   ```

4. **Process the ingested documents** with the analysis system:
   ```bash
   python political_analysis_orchestrator.py
   ```