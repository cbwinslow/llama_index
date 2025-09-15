"""
MCP (Model Context Protocol) Server implementation for LlamaIndex Political Document Manager.
"""
import asyncio
import json
from typing import Dict, Any, List, Callable, Optional
from pathlib import Path

class MCPServer:
    """MCP server for integrating with other services."""
    
    def __init__(self):
        self.tools = {}
        self.resources = {}
        self.is_running = False
        self.clients = []
        self.host = "localhost"
        self.port = 8080
        
    async def start(self, host: str = "localhost", port: int = 8080):
        """Start the MCP server."""
        self.is_running = True
        self.host = host
        self.port = port
        print(f"MCP Server started on {host}:{port}")
        
    async def stop(self):
        """Stop the MCP server."""
        self.is_running = False
        self.clients.clear()
        print("MCP Server stopped")
        
    def register_tool(self, name: str, description: str, handler: Callable):
        """Register a tool with the MCP server."""
        self.tools[name] = {
            "name": name,
            "description": description,
            "handler": handler
        }
        
    def register_resource(self, uri: str, content: Any):
        """Register a resource with the MCP server."""
        self.resources[uri] = content
        
    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Handle a tool call."""
        if tool_name not in self.tools:
            raise ValueError(f"Tool {tool_name} not found")
        
        tool = self.tools[tool_name]
        handler = tool["handler"]
        
        if asyncio.iscoroutinefunction(handler):
            return await handler(**arguments)
        else:
            return handler(**arguments)
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List all registered tools."""
        return [
            {
                "name": tool["name"],
                "description": tool["description"]
            }
            for tool in self.tools.values()
        ]
    
    def list_resources(self) -> List[str]:
        """List all registered resources."""
        return list(self.resources.keys())


class PoliticalDocumentMCPServer(MCPServer):
    """Specialized MCP server for political document processing."""
    
    def __init__(self, config_manager=None, document_processor=None):
        super().__init__()
        self.config_manager = config_manager
        self.document_processor = document_processor
        self._register_default_tools()
    
    def _register_default_tools(self):
        """Register default tools for political document processing."""
        
        def index_documents(document_paths: List[str]) -> Dict[str, Any]:
            """Index documents for search."""
            results = []
            for path in document_paths:
                doc_path = Path(path)
                if doc_path.exists():
                    content = doc_path.read_text()
                    results.append({
                        "path": path,
                        "indexed": True,
                        "content_length": len(content),
                        "keywords": len([w for w in content.split() if len(w) > 3])
                    })
                else:
                    results.append({
                        "path": path, 
                        "indexed": False, 
                        "error": "File not found"
                    })
            
            return {
                "documents": results, 
                "total_indexed": len([r for r in results if r.get("indexed")])
            }
        
        def analyze_political_content(text: str) -> Dict[str, Any]:
            """Analyze political content in documents."""
            text_lower = text.lower()
            
            policy_areas = {
                "healthcare": ["healthcare", "health", "medical", "insurance"],
                "economy": ["economic", "economy", "financial", "budget", "tax"],
                "environment": ["environmental", "climate", "green", "pollution"],
                "education": ["education", "school", "university", "student"]
            }
            
            analysis = {}
            for area, keywords in policy_areas.items():
                mentions = sum(1 for kw in keywords if kw in text_lower)
                analysis[area] = {
                    "mentions": mentions,
                    "relevance": "high" if mentions > 2 else "medium" if mentions > 0 else "low"
                }
            
            return {
                "analysis": analysis,
                "total_policy_mentions": sum(a["mentions"] for a in analysis.values()),
                "primary_topics": [area for area, data in analysis.items() if data["relevance"] == "high"]
            }
        
        def query_database(query: str, database_type: str = "sql") -> Dict[str, Any]:
            """Query configured databases."""
            if database_type == "sql":
                return {
                    "query": query,
                    "results": [
                        {"id": 1, "title": "Document 1", "category": "political"},
                        {"id": 2, "title": "Document 2", "category": "technical"}
                    ],
                    "count": 2,
                    "database_type": "sql"
                }
            elif database_type == "neo4j":
                return {
                    "query": query,
                    "results": [
                        {"node": {"id": 1, "type": "Document", "title": "Doc 1"}},
                        {"relationship": {"type": "RELATED_TO", "weight": 0.8}}
                    ],
                    "count": 2,
                    "database_type": "neo4j"
                }
            else:
                raise ValueError(f"Unsupported database type: {database_type}")
        
        def get_configuration(config_type: str) -> Dict[str, Any]:
            """Get configuration from the configuration manager."""
            if not self.config_manager:
                raise RuntimeError("Configuration manager not available")
            
            return self.config_manager.load_config(config_type)
        
        def update_configuration(config_type: str, updates: Dict[str, Any]) -> Dict[str, Any]:
            """Update configuration through the configuration manager."""
            if not self.config_manager:
                raise RuntimeError("Configuration manager not available")
            
            updated_config = self.config_manager.update_config(config_type, updates)
            return {
                "config_type": config_type,
                "updates_applied": updates,
                "status": "updated",
                "updated_config": updated_config
            }
        
        # Register tools
        self.register_tool(
            "index_documents",
            "Index documents for search and retrieval",
            index_documents
        )
        
        self.register_tool(
            "analyze_political_content",
            "Analyze political content and extract key topics",
            analyze_political_content
        )
        
        self.register_tool(
            "query_database",
            "Query configured databases (SQL or Neo4j)",
            query_database
        )
        
        self.register_tool(
            "get_config",
            "Get application configuration",
            get_configuration
        )
        
        self.register_tool(
            "update_config",
            "Update application configuration",
            update_configuration
        )
    
    async def call_external_api(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Call external API endpoints."""
        # Mock external API call for now
        return {
            "endpoint": endpoint,
            "status": "success",
            "data": data,
            "response": f"Processed request to {endpoint}"
        }
    
    def validate_tool_access(self, tool_name: str, api_key: Optional[str] = None) -> bool:
        """Validate access to tools (basic security)."""
        if not api_key:
            return False
        
        # Basic API key validation (in production, use proper authentication)
        valid_keys = ["valid-api-key", "admin-key", "service-key"]
        return api_key in valid_keys
    
    async def handle_secure_tool_call(self, tool_name: str, arguments: Dict[str, Any], 
                                    api_key: Optional[str] = None) -> Any:
        """Handle tool call with security validation."""
        if not self.validate_tool_access(tool_name, api_key):
            raise PermissionError("Invalid API key or insufficient permissions")
        
        return await self.handle_tool_call(tool_name, arguments)