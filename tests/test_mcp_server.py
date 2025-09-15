"""
Test suite for MCP (Model Context Protocol) server integration.
This tests the server functionality for integrating with other services.
"""
import pytest
import json
import asyncio
from typing import Dict, Any, List
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path

class MockMCPServer:
    """Mock MCP server for testing."""
    
    def __init__(self):
        self.tools = {}
        self.resources = {}
        self.is_running = False
        self.clients = []
        
    async def start(self, host: str = "localhost", port: int = 8080):
        """Start the mock MCP server."""
        self.is_running = True
        self.host = host
        self.port = port
        
    async def stop(self):
        """Stop the mock MCP server."""
        self.is_running = False
        self.clients.clear()
        
    def register_tool(self, name: str, description: str, handler):
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


class TestMCPServerBasics:
    """Test basic MCP server functionality."""
    
    @pytest.fixture
    def mcp_server(self):
        """Create a mock MCP server for testing."""
        return MockMCPServer()
    
    @pytest.mark.asyncio
    async def test_server_start_stop(self, mcp_server):
        """Test starting and stopping the MCP server."""
        assert not mcp_server.is_running
        
        await mcp_server.start()
        assert mcp_server.is_running
        assert mcp_server.host == "localhost"
        assert mcp_server.port == 8080
        
        await mcp_server.stop()
        assert not mcp_server.is_running
        
    def test_tool_registration(self, mcp_server):
        """Test registering tools with the MCP server."""
        def sample_tool(query: str) -> str:
            return f"Processed: {query}"
        
        mcp_server.register_tool(
            "document_search",
            "Search through documents",
            sample_tool
        )
        
        assert "document_search" in mcp_server.tools
        tool = mcp_server.tools["document_search"]
        assert tool["name"] == "document_search"
        assert tool["description"] == "Search through documents"
        
    @pytest.mark.asyncio
    async def test_tool_execution(self, mcp_server):
        """Test executing tools through the MCP server."""
        def search_tool(query: str, limit: int = 10) -> List[str]:
            return [f"Result {i} for '{query}'" for i in range(min(limit, 3))]
        
        mcp_server.register_tool(
            "search",
            "Search functionality",
            search_tool
        )
        
        result = await mcp_server.handle_tool_call(
            "search",
            {"query": "political documents", "limit": 2}
        )
        
        assert len(result) == 2
        assert "political documents" in result[0]
        
    def test_resource_registration(self, mcp_server):
        """Test registering resources with the MCP server."""
        sample_data = {"type": "document", "content": "Sample political document"}
        mcp_server.register_resource("file://docs/political.json", sample_data)
        
        assert "file://docs/political.json" in mcp_server.resources
        assert mcp_server.resources["file://docs/political.json"] == sample_data


class TestMCPServerTools:
    """Test specific tools for the MCP server."""
    
    @pytest.fixture
    def mcp_server(self):
        return MockMCPServer()
    
    def test_document_indexing_tool(self, mcp_server, sample_documents):
        """Test document indexing tool."""
        def index_documents(document_paths: List[str]) -> Dict[str, Any]:
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
                    results.append({"path": path, "indexed": False, "error": "File not found"})
            
            return {"documents": results, "total_indexed": len([r for r in results if r.get("indexed")])}
        
        mcp_server.register_tool(
            "index_documents",
            "Index documents for search",
            index_documents
        )
        
        # Test with sample documents
        doc_paths = [str(doc) for doc in sample_documents]
        result = index_documents(doc_paths)
        
        assert result["total_indexed"] == len(sample_documents)
        assert len(result["documents"]) == len(sample_documents)
        
    def test_political_analysis_tool(self, mcp_server):
        """Test political document analysis tool."""
        def analyze_political_content(text: str) -> Dict[str, Any]:
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
        
        mcp_server.register_tool(
            "analyze_political_content",
            "Analyze political content in documents",
            analyze_political_content
        )
        
        # Test with political content
        political_text = """
        This document discusses healthcare reform and economic policy.
        Environmental regulations and education funding are also covered.
        The healthcare system needs improvement and economic growth is essential.
        Healthcare healthcare healthcare.
        """
        
        result = analyze_political_content(political_text)
        
        assert result["total_policy_mentions"] > 0
        assert "healthcare" in result["analysis"]
        assert result["analysis"]["healthcare"]["mentions"] > 0
        
    def test_database_query_tool(self, mcp_server, mock_database_config):
        """Test database querying tool."""
        def query_database(query: str, database_type: str = "sql") -> Dict[str, Any]:
            # Mock database query results
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
        
        mcp_server.register_tool(
            "query_database",
            "Query configured databases",
            query_database
        )
        
        # Test SQL query
        sql_result = query_database("SELECT * FROM documents WHERE category = 'political'", "sql")
        assert sql_result["database_type"] == "sql"
        assert sql_result["count"] == 2
        
        # Test Neo4j query
        neo4j_result = query_database("MATCH (d:Document) RETURN d", "neo4j")
        assert neo4j_result["database_type"] == "neo4j"
        assert neo4j_result["count"] == 2


class TestMCPServerIntegration:
    """Test MCP server integration with external services."""
    
    @pytest.fixture
    def mcp_server(self):
        return MockMCPServer()
    
    @pytest.mark.asyncio
    async def test_external_api_integration(self, mcp_server):
        """Test integration with external APIs."""
        async def call_external_api(endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
            # Mock external API call
            return {
                "endpoint": endpoint,
                "status": "success",
                "data": data,
                "response": f"Processed request to {endpoint}"
            }
        
        mcp_server.register_tool(
            "external_api_call",
            "Call external API endpoints",
            call_external_api
        )
        
        result = await mcp_server.handle_tool_call(
            "external_api_call",
            {
                "endpoint": "/api/v1/analyze",
                "data": {"text": "Sample political document"}
            }
        )
        
        assert result["status"] == "success"
        assert result["endpoint"] == "/api/v1/analyze"
        
    def test_configuration_management(self, mcp_server, mock_database_config, mock_deployment_config):
        """Test configuration management through MCP server."""
        def get_configuration(config_type: str) -> Dict[str, Any]:
            configs = {
                "database": mock_database_config,
                "deployment": mock_deployment_config
            }
            
            if config_type not in configs:
                raise ValueError(f"Unknown configuration type: {config_type}")
            
            return configs[config_type]
        
        def update_configuration(config_type: str, updates: Dict[str, Any]) -> Dict[str, Any]:
            # Mock configuration update
            return {
                "config_type": config_type,
                "updates_applied": updates,
                "status": "updated",
                "timestamp": "2024-01-01T00:00:00Z"
            }
        
        mcp_server.register_tool("get_config", "Get configuration", get_configuration)
        mcp_server.register_tool("update_config", "Update configuration", update_configuration)
        
        # Test getting configuration
        db_config = get_configuration("database")
        assert "sql_database" in db_config
        assert db_config["sql_database"]["type"] == "postgresql"
        
        # Test updating configuration
        update_result = update_configuration(
            "database",
            {"sql_database": {"host": "new-host"}}
        )
        assert update_result["status"] == "updated"
        assert update_result["config_type"] == "database"


class TestMCPServerSecurity:
    """Test security aspects of the MCP server."""
    
    @pytest.fixture
    def mcp_server(self):
        return MockMCPServer()
    
    def test_tool_access_control(self, mcp_server):
        """Test access control for tools."""
        def secure_tool(api_key: str, data: str) -> str:
            if not api_key or api_key != "valid-api-key":
                raise PermissionError("Invalid API key")
            return f"Processed: {data}"
        
        mcp_server.register_tool(
            "secure_operation",
            "Secure operation requiring API key",
            secure_tool
        )
        
        # Test with valid API key
        try:
            result = secure_tool("valid-api-key", "test data")
            assert "Processed: test data" == result
        except PermissionError:
            pytest.fail("Should not raise PermissionError with valid API key")
        
        # Test with invalid API key
        with pytest.raises(PermissionError):
            secure_tool("invalid-key", "test data")
            
    def test_input_validation(self, mcp_server):
        """Test input validation for tools."""
        def validated_tool(query: str, max_length: int = 100) -> str:
            if not isinstance(query, str):
                raise TypeError("Query must be a string")
            if len(query) > max_length:
                raise ValueError(f"Query too long: {len(query)} > {max_length}")
            if not query.strip():
                raise ValueError("Query cannot be empty")
            
            return f"Valid query: {query[:50]}..."
        
        mcp_server.register_tool(
            "validated_search",
            "Search with input validation",
            validated_tool
        )
        
        # Test valid input
        result = validated_tool("valid search query")
        assert "Valid query:" in result
        
        # Test invalid inputs
        with pytest.raises(TypeError):
            validated_tool(123)
        
        with pytest.raises(ValueError):
            validated_tool("x" * 101)  # Too long
        
        with pytest.raises(ValueError):
            validated_tool("")  # Empty