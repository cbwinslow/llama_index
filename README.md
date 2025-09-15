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

## Quick Start

1. Clone the repository
2. Install dependencies: `./install_political_analysis.sh`
3. Set up your API keys in `.env.political_analysis`
4. Run the test: `python test_political_analysis.py`
5. Try the demo: `jupyter notebook political_analysis_demo.ipynb`

## Components

- **PoliticalDocumentIngestor**: Handles loading documents from various sources
- **PoliticalEntityExtractor**: Extracts political entities and relationships
- **PoliticalKnowledgeGraph**: Manages knowledge graph construction and querying
- **PoliticalMCPIntegration**: Connects to specialized political tools
- **PoliticalAnalysisAgent**: Intelligent agent for document analysis
- **PoliticalAnalysisOrchestrator**: Coordinates the complete analysis pipeline

## Requirements

See `political_analysis_requirements.txt` for a complete list of dependencies.