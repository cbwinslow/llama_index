"""
LlamaIndex Political Document Manager

A comprehensive application for managing, analyzing, and querying political documents
using the LlamaIndex framework. This application provides:

- Document ingestion and processing
- Vector-based search and retrieval
- Political content analysis
- Web-based configuration management
- MCP (Model Context Protocol) server integration
- Database integration (SQL and Neo4j)
- Deployment configuration management

Author: AI Assistant
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "AI Assistant"
__description__ = "LlamaIndex Political Document Manager"

from .config_manager import ConfigurationManager
from .mcp_server import MCPServer, PoliticalDocumentMCPServer
from .web_interface import WebInterface
from .document_processor import DocumentProcessor

__all__ = [
    "ConfigurationManager",
    "MCPServer",
    "PoliticalDocumentMCPServer", 
    "WebInterface",
    "DocumentProcessor"
]