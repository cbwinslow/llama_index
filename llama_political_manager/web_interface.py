"""
Web interface implementation for the LlamaIndex Political Document Manager.
"""
from typing import Dict, Any, List, Optional
import json

class MockRequest:
    """Mock HTTP request object."""
    
    def __init__(self, method: str = "GET", path: str = "/", json_data: Optional[Dict] = None, 
                 query_params: Optional[Dict] = None, form_data: Optional[Dict] = None):
        self.method = method
        self.path = path
        self.json_data = json_data or {}
        self.query_params = query_params or {}
        self.form_data = form_data or {}
        self.headers = {}
        
    def get_json(self):
        return self.json_data
    
    def get_form(self):
        return self.form_data


class MockResponse:
    """Mock HTTP response object."""
    
    def __init__(self, data: Any = None, status_code: int = 200, headers: Optional[Dict] = None):
        self.data = data
        self.status_code = status_code
        self.headers = headers or {}
        
    def json(self):
        return self.data


class MockWebApp:
    """Mock web application for testing and demonstration."""
    
    def __init__(self):
        self.routes = {}
        self.middleware = []
        self.config = {}
        
    def route(self, path: str, methods: List[str] = None):
        """Decorator to register routes."""
        methods = methods or ["GET"]
        
        def decorator(func):
            for method in methods:
                route_key = f"{method}:{path}"
                self.routes[route_key] = func
            return func
        
        return decorator
    
    def handle_request(self, request: MockRequest) -> MockResponse:
        """Handle a mock HTTP request."""
        route_key = f"{request.method}:{request.path}"
        
        if route_key in self.routes:
            handler = self.routes[route_key]
            try:
                result = handler(request)
                if isinstance(result, MockResponse):
                    return result
                else:
                    return MockResponse(result)
            except Exception as e:
                return MockResponse({"error": str(e)}, status_code=500)
        else:
            return MockResponse({"error": "Not found"}, status_code=404)


class WebInterface:
    """Web interface for configuration and document management."""
    
    def __init__(self, config_manager=None):
        self.app = MockWebApp()
        self.config_manager = config_manager
        self._setup_routes()
        
    def _setup_routes(self):
        """Setup web application routes."""
        
        @self.app.route("/")
        def home(request):
            return {
                "title": "LlamaIndex Political Document Manager",
                "version": "1.0.0",
                "status": "running",
                "features": [
                    "Document upload and processing",
                    "Political content analysis",
                    "Configuration management",
                    "Database integration",
                    "MCP server integration"
                ]
            }
        
        @self.app.route("/api/config", ["GET"])
        def get_config(request):
            config_type = request.query_params.get("type", "all")
            
            if not self.config_manager:
                return MockResponse({"error": "Configuration manager not available"}, 500)
            
            if config_type == "all":
                configs = {
                    "database": self.config_manager.load_config("database"),
                    "deployment": self.config_manager.load_config("deployment"),
                    "document_sources": self.config_manager.load_config("document_sources"),
                    "web_interface": self.config_manager.load_config("web_interface")
                }
                return MockResponse(configs)
            else:
                config = self.config_manager.load_config(config_type)
                return MockResponse({config_type: config})
        
        @self.app.route("/api/config", ["POST"])
        def update_config(request):
            if not self.config_manager:
                return MockResponse({"error": "Configuration manager not available"}, 500)
            
            data = request.get_json()
            config_type = data.get("type")
            updates = data.get("updates", {})
            
            if not config_type:
                return MockResponse({"error": "Configuration type required"}, 400)
            
            try:
                updated_config = self.config_manager.update_config(config_type, updates)
                return MockResponse({
                    "success": True,
                    "config_type": config_type,
                    "updated_config": updated_config
                })
            except Exception as e:
                return MockResponse({"error": str(e)}, 500)
        
        @self.app.route("/api/documents", ["GET"])
        def list_documents(request):
            # Mock document listing
            limit = int(request.query_params.get("limit", 10))
            offset = int(request.query_params.get("offset", 0))
            search = request.query_params.get("search", "")
            
            # Mock documents
            documents = [
                {
                    "id": i + offset,
                    "title": f"Political Document {i + offset}",
                    "content": f"Sample content for document {i + offset}",
                    "category": "political",
                    "date": "2024-01-01",
                    "keywords": ["policy", "government", "reform"]
                }
                for i in range(limit)
                if not search or search.lower() in f"political document {i + offset}".lower()
            ]
            
            return MockResponse({
                "documents": documents,
                "total": 100,
                "limit": limit,
                "offset": offset
            })
        
        @self.app.route("/api/documents", ["POST"])
        def upload_document(request):
            data = request.get_json()
            
            if "content" not in data:
                return MockResponse({"error": "Document content required"}, 400)
            
            # Mock document processing
            document = {
                "id": 12345,
                "title": data.get("title", "Untitled Document"),
                "content": data["content"],
                "category": data.get("category", "uncategorized"),
                "status": "processed",
                "created_at": "2024-01-01T00:00:00Z"
            }
            
            return MockResponse({
                "success": True,
                "document": document
            })
        
        @self.app.route("/api/search", ["POST"])
        def search_documents(request):
            data = request.get_json()
            query = data.get("query", "")
            filters = data.get("filters", {})
            
            if not query:
                return MockResponse({"error": "Search query required"}, 400)
            
            # Mock search results
            results = [
                {
                    "id": i,
                    "title": f"Document {i} - {query}",
                    "snippet": f"...relevant content about {query}...",
                    "score": 0.9 - (i * 0.1),
                    "category": "political",
                    "date": "2024-01-01"
                }
                for i in range(5)
            ]
            
            return MockResponse({
                "results": results,
                "total": len(results),
                "query": query,
                "filters": filters,
                "took_ms": 25
            })
        
        @self.app.route("/api/analytics", ["GET"])
        def get_analytics(request):
            # Mock analytics data
            analytics = {
                "document_stats": {
                    "total_documents": 1250,
                    "political_documents": 890,
                    "processed_today": 45,
                    "average_processing_time": 2.3
                },
                "search_stats": {
                    "total_searches": 3420,
                    "searches_today": 127,
                    "average_response_time": 0.15,
                    "top_queries": ["healthcare policy", "economic reform", "climate change"]
                },
                "system_stats": {
                    "uptime": "5 days, 3 hours",
                    "cpu_usage": 45.2,
                    "memory_usage": 67.8,
                    "disk_usage": 23.1
                }
            }
            
            return MockResponse(analytics)
        
        @self.app.route("/api/health", ["GET"])
        def health_check(request):
            return MockResponse({
                "status": "healthy",
                "timestamp": "2024-01-01T00:00:00Z",
                "version": "1.0.0",
                "components": {
                    "database": "connected",
                    "vector_store": "connected",
                    "document_processor": "running"
                }
            })
        
        @self.app.route("/config", ["GET"])
        def config_page(request):
            """Configuration management page."""
            return {
                "page": "configuration",
                "title": "Configuration Management",
                "sections": [
                    {
                        "name": "Database Configuration",
                        "description": "Configure SQL, Neo4j, and vector store settings",
                        "endpoint": "/api/config?type=database"
                    },
                    {
                        "name": "Deployment Configuration", 
                        "description": "Configure environment, scaling, and deployment settings",
                        "endpoint": "/api/config?type=deployment"
                    },
                    {
                        "name": "Document Sources",
                        "description": "Configure document ingestion sources and filters",
                        "endpoint": "/api/config?type=document_sources"
                    },
                    {
                        "name": "Web Interface",
                        "description": "Configure UI settings and features",
                        "endpoint": "/api/config?type=web_interface"
                    }
                ]
            }
    
    def run(self, host: str = "localhost", port: int = 8000, debug: bool = False):
        """Run the web interface (mock implementation)."""
        print(f"Starting LlamaIndex Political Document Manager on {host}:{port}")
        print(f"Debug mode: {debug}")
        print("Available endpoints:")
        print("  / - Home page")
        print("  /config - Configuration management")
        print("  /api/health - Health check")
        print("  /api/config - Configuration API")
        print("  /api/documents - Document management API")
        print("  /api/search - Search API")
        print("  /api/analytics - Analytics API")
        
        # In a real implementation, this would start a web server
        return True