# Political Document Analysis System

A comprehensive system for analyzing political documents using LlamaIndex, featuring entity extraction, knowledge graph construction, web crawling, and intelligent agent capabilities.

## Features

- **Document Ingestion**: Load political documents from local files, websites, RSS feeds, and sitemaps
- **Entity Extraction**: Extract political entities including politicians, parties, legislation, and policies
- **Knowledge Graph**: Build and query relationships between political entities using Neo4j
- **Web Crawling**: Crawl political websites and news sources for real-time data
- **MCP Integration**: Connect to specialized political tools via Model Context Protocol
- **Intelligent Agents**: AI agents for analyzing documents and answering political questions
- **Advanced Analysis**: Sentiment analysis, theme identification, and trend detection

## Components

1. **PoliticalDocumentIngestor**: Handles loading documents from various sources
2. **PoliticalEntityExtractor**: Extracts political entities and relationships
3. **PoliticalKnowledgeGraph**: Manages knowledge graph construction and querying
4. **PoliticalMCPIntegration**: Connects to specialized political tools
5. **PoliticalAnalysisAgent**: Intelligent agent for document analysis
6. **PoliticalAnalysisOrchestrator**: Coordinates the complete analysis pipeline

## Installation

```bash
# Run the installation script
./install_political_analysis.sh

# Set up your API keys in .env.political_analysis
```

## Usage

1. **Run the test script**:
   ```bash
   python test_political_analysis.py
   ```

2. **Try the demo notebook**:
   ```bash
   jupyter notebook political_analysis_demo.ipynb
   ```

3. **Use the orchestrator directly**:
   ```python
   from political_analysis_orchestrator import PoliticalAnalysisOrchestrator
   
   orchestrator = PoliticalAnalysisOrchestrator()
   results = await orchestrator.run_complete_analysis(sources)
   ```

## Configuration

The system is configured through:
- `political_analysis_config.ini`: Main configuration file
- `.env.political_analysis`: Environment variables and API keys
- `political_crawling_config.py`: Web crawling settings

## Requirements

See `political_analysis_requirements.txt` for a complete list of dependencies.

## Next Steps

1. Set up Neo4j for knowledge graph storage
2. Configure MCP servers for specialized political tools
3. Implement advanced web crawling for political websites
4. Add predictive analytics for political trends
5. Create visualization tools for political networks