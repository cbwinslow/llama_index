"""
Test suite for web interface functionality.
This includes tests for the web-based configuration and management interface.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any, List, Optional
import json

# Mock web framework components
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
    """Mock web application for testing."""
    
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
                "status": "running"
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


class TestWebInterfaceBasics:
    """Test basic web interface functionality."""
    
    @pytest.fixture
    def web_app(self):
        """Create a web interface for testing."""
        return WebInterface()
    
    def test_home_page(self, web_app: WebInterface):
        """Test the home page endpoint."""
        request = MockRequest("GET", "/")
        response = web_app.app.handle_request(request)
        
        assert response.status_code == 200
        assert response.data["title"] == "LlamaIndex Political Document Manager"
        assert response.data["status"] == "running"
        
    def test_health_check(self, web_app: WebInterface):
        """Test the health check endpoint."""
        request = MockRequest("GET", "/api/health")
        response = web_app.app.handle_request(request)
        
        assert response.status_code == 200
        assert response.data["status"] == "healthy"
        assert "components" in response.data
        assert response.data["components"]["database"] == "connected"
        
    def test_not_found_route(self, web_app: WebInterface):
        """Test handling of non-existent routes."""
        request = MockRequest("GET", "/nonexistent")
        response = web_app.app.handle_request(request)
        
        assert response.status_code == 404
        assert "error" in response.data


class TestConfigurationEndpoints:
    """Test configuration management endpoints."""
    
    @pytest.fixture
    def web_app_with_config(self, temp_dir):
        """Create web interface with configuration manager."""
        from llama_political_manager.config_manager import ConfigurationManager
        config_manager = ConfigurationManager(temp_dir / "config")
        return WebInterface(config_manager)
    
    def test_get_all_configurations(self, web_app_with_config: WebInterface):
        """Test getting all configurations."""
        request = MockRequest("GET", "/api/config", query_params={"type": "all"})
        response = web_app_with_config.app.handle_request(request)
        
        assert response.status_code == 200
        assert "database" in response.data
        assert "deployment" in response.data
        assert "document_sources" in response.data
        
    def test_get_specific_configuration(self, web_app_with_config: WebInterface):
        """Test getting a specific configuration."""
        request = MockRequest("GET", "/api/config", query_params={"type": "database"})
        response = web_app_with_config.app.handle_request(request)
        
        assert response.status_code == 200
        assert "database" in response.data
        assert "sql_database" in response.data["database"]
        
    def test_update_configuration(self, web_app_with_config: WebInterface):
        """Test updating configuration."""
        update_data = {
            "type": "database",
            "updates": {
                "sql_database": {
                    "host": "new-database-host",
                    "port": 5433
                }
            }
        }
        
        request = MockRequest("POST", "/api/config", json_data=update_data)
        response = web_app_with_config.app.handle_request(request)
        
        assert response.status_code == 200
        assert response.data["success"] is True
        assert response.data["config_type"] == "database"
        assert response.data["updated_config"]["sql_database"]["host"] == "new-database-host"
        
    def test_invalid_configuration_update(self, web_app_with_config: WebInterface):
        """Test handling invalid configuration updates."""
        invalid_data = {
            "updates": {"some": "data"}
            # Missing required "type" field
        }
        
        request = MockRequest("POST", "/api/config", json_data=invalid_data)
        response = web_app_with_config.app.handle_request(request)
        
        assert response.status_code == 400
        assert "error" in response.data


class TestDocumentManagementEndpoints:
    """Test document management endpoints."""
    
    @pytest.fixture
    def web_app(self):
        return WebInterface()
    
    def test_list_documents(self, web_app: WebInterface):
        """Test listing documents."""
        request = MockRequest("GET", "/api/documents", query_params={"limit": "5", "offset": "0"})
        response = web_app.app.handle_request(request)
        
        assert response.status_code == 200
        assert "documents" in response.data
        assert len(response.data["documents"]) == 5
        assert response.data["total"] == 100
        
    def test_search_documents(self, web_app: WebInterface):
        """Test searching documents with query parameters."""
        request = MockRequest("GET", "/api/documents", 
                             query_params={"search": "political", "limit": "3"})
        response = web_app.app.handle_request(request)
        
        assert response.status_code == 200
        assert len(response.data["documents"]) <= 3
        for doc in response.data["documents"]:
            assert "political" in doc["title"].lower()
            
    def test_upload_document(self, web_app: WebInterface):
        """Test uploading a new document."""
        document_data = {
            "title": "New Political Document",
            "content": "This is a test political document about healthcare reform.",
            "category": "political"
        }
        
        request = MockRequest("POST", "/api/documents", json_data=document_data)
        response = web_app.app.handle_request(request)
        
        assert response.status_code == 200
        assert response.data["success"] is True
        assert response.data["document"]["title"] == "New Political Document"
        assert response.data["document"]["category"] == "political"
        
    def test_upload_document_invalid(self, web_app: WebInterface):
        """Test uploading invalid document data."""
        invalid_data = {
            "title": "Document without content"
            # Missing required "content" field
        }
        
        request = MockRequest("POST", "/api/documents", json_data=invalid_data)
        response = web_app.app.handle_request(request)
        
        assert response.status_code == 400
        assert "error" in response.data


class TestSearchEndpoints:
    """Test search functionality endpoints."""
    
    @pytest.fixture
    def web_app(self):
        return WebInterface()
    
    def test_document_search(self, web_app: WebInterface):
        """Test document search."""
        search_data = {
            "query": "healthcare policy",
            "filters": {
                "category": "political",
                "date_range": {"start": "2023-01-01", "end": "2024-01-01"}
            }
        }
        
        request = MockRequest("POST", "/api/search", json_data=search_data)
        response = web_app.app.handle_request(request)
        
        assert response.status_code == 200
        assert "results" in response.data
        assert response.data["query"] == "healthcare policy"
        assert len(response.data["results"]) > 0
        
        # Check result format
        for result in response.data["results"]:
            assert "id" in result
            assert "title" in result
            assert "snippet" in result
            assert "score" in result
            
    def test_search_without_query(self, web_app: WebInterface):
        """Test search with missing query."""
        invalid_search = {"filters": {"category": "political"}}
        
        request = MockRequest("POST", "/api/search", json_data=invalid_search)
        response = web_app.app.handle_request(request)
        
        assert response.status_code == 400
        assert "error" in response.data
        
    def test_search_with_filters(self, web_app: WebInterface):
        """Test search with various filters."""
        search_data = {
            "query": "economic reform",
            "filters": {
                "category": "political",
                "date_range": {"start": "2023-01-01"},
                "keywords": ["economy", "policy"],
                "document_type": "bill"
            }
        }
        
        request = MockRequest("POST", "/api/search", json_data=search_data)
        response = web_app.app.handle_request(request)
        
        assert response.status_code == 200
        assert response.data["filters"] == search_data["filters"]


class TestAnalyticsEndpoints:
    """Test analytics and monitoring endpoints."""
    
    @pytest.fixture
    def web_app(self):
        return WebInterface()
    
    def test_analytics_dashboard(self, web_app: WebInterface):
        """Test analytics dashboard data."""
        request = MockRequest("GET", "/api/analytics")
        response = web_app.app.handle_request(request)
        
        assert response.status_code == 200
        assert "document_stats" in response.data
        assert "search_stats" in response.data
        assert "system_stats" in response.data
        
        # Check document stats
        doc_stats = response.data["document_stats"]
        assert "total_documents" in doc_stats
        assert "political_documents" in doc_stats
        assert isinstance(doc_stats["total_documents"], int)
        
        # Check search stats
        search_stats = response.data["search_stats"]
        assert "total_searches" in search_stats
        assert "top_queries" in search_stats
        assert isinstance(search_stats["top_queries"], list)
        
        # Check system stats
        system_stats = response.data["system_stats"]
        assert "uptime" in system_stats
        assert "cpu_usage" in system_stats
        assert isinstance(system_stats["cpu_usage"], (int, float))


class TestWebInterfaceIntegration:
    """Test integration scenarios for the web interface."""
    
    @pytest.fixture
    def full_web_app(self, temp_dir):
        """Create fully configured web interface."""
        from llama_political_manager.config_manager import ConfigurationManager
        config_manager = ConfigurationManager(temp_dir / "config")
        return WebInterface(config_manager)
    
    def test_complete_document_workflow(self, full_web_app: WebInterface):
        """Test complete document processing workflow."""
        # 1. Upload document
        upload_data = {
            "title": "Healthcare Reform Bill 2024",
            "content": "This bill proposes comprehensive healthcare reform including universal coverage and cost reductions.",
            "category": "political"
        }
        
        upload_request = MockRequest("POST", "/api/documents", json_data=upload_data)
        upload_response = full_web_app.app.handle_request(upload_request)
        
        assert upload_response.status_code == 200
        assert upload_response.data["success"] is True
        
        # 2. Search for the document
        search_data = {"query": "healthcare reform"}
        search_request = MockRequest("POST", "/api/search", json_data=search_data)
        search_response = full_web_app.app.handle_request(search_request)
        
        assert search_response.status_code == 200
        assert len(search_response.data["results"]) > 0
        
        # 3. Check analytics
        analytics_request = MockRequest("GET", "/api/analytics")
        analytics_response = full_web_app.app.handle_request(analytics_request)
        
        assert analytics_response.status_code == 200
        assert analytics_response.data["document_stats"]["total_documents"] > 0
        
    def test_configuration_and_restart_workflow(self, full_web_app: WebInterface):
        """Test configuration update workflow."""
        # 1. Get current configuration
        get_config_request = MockRequest("GET", "/api/config", query_params={"type": "deployment"})
        get_response = full_web_app.app.handle_request(get_config_request)
        
        assert get_response.status_code == 200
        original_config = get_response.data["deployment"]
        
        # 2. Update configuration
        update_data = {
            "type": "deployment",
            "updates": {
                "log_level": "DEBUG",
                "max_workers": 8
            }
        }
        
        update_request = MockRequest("POST", "/api/config", json_data=update_data)
        update_response = full_web_app.app.handle_request(update_request)
        
        assert update_response.status_code == 200
        assert update_response.data["success"] is True
        
        # 3. Verify configuration was updated
        verify_request = MockRequest("GET", "/api/config", query_params={"type": "deployment"})
        verify_response = full_web_app.app.handle_request(verify_request)
        
        assert verify_response.status_code == 200
        updated_config = verify_response.data["deployment"]
        assert updated_config["log_level"] == "DEBUG"
        assert updated_config["max_workers"] == 8
        
        # 4. Check health after configuration change
        health_request = MockRequest("GET", "/api/health")
        health_response = full_web_app.app.handle_request(health_request)
        
        assert health_response.status_code == 200
        assert health_response.data["status"] == "healthy"


class TestWebInterfaceErrorHandling:
    """Test error handling in the web interface."""
    
    @pytest.fixture
    def web_app(self):
        return WebInterface()
    
    def test_malformed_json_request(self, web_app: WebInterface):
        """Test handling of malformed JSON requests."""
        # This would normally cause a JSON parse error
        # We'll simulate it by passing invalid data structure
        request = MockRequest("POST", "/api/search", json_data="invalid json structure")
        response = web_app.app.handle_request(request)
        
        # The mock should handle this gracefully
        assert response.status_code in [400, 500]
        
    def test_missing_configuration_manager(self):
        """Test behavior when configuration manager is not available."""
        web_app = WebInterface(config_manager=None)
        
        request = MockRequest("GET", "/api/config")
        response = web_app.app.handle_request(request)
        
        assert response.status_code == 500
        assert "Configuration manager not available" in response.data["error"]
        
    def test_large_request_handling(self, web_app: WebInterface):
        """Test handling of large requests."""
        # Simulate large document upload
        large_content = "Large document content. " * 10000  # ~240KB of text
        
        upload_data = {
            "title": "Very Large Document",
            "content": large_content,
            "category": "political"
        }
        
        request = MockRequest("POST", "/api/documents", json_data=upload_data)
        response = web_app.app.handle_request(request)
        
        # Should handle large documents gracefully
        assert response.status_code == 200
        assert response.data["success"] is True