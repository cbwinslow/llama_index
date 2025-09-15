"""
Test suite for configuration management system.
This includes tests for database, deployment, and application configuration.
"""
import pytest
import json
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional
from unittest.mock import Mock, patch
import yaml

class ConfigurationManager:
    """Configuration manager for the application."""
    
    def __init__(self, config_dir: Optional[Path] = None):
        self.config_dir = config_dir or Path("./config")
        self.config_dir.mkdir(exist_ok=True)
        self._config_cache = {}
        
    def load_config(self, config_name: str) -> Dict[str, Any]:
        """Load configuration from file."""
        if config_name in self._config_cache:
            return self._config_cache[config_name]
        
        config_file = self.config_dir / f"{config_name}.json"
        yaml_file = self.config_dir / f"{config_name}.yaml"
        
        if config_file.exists():
            with open(config_file, 'r') as f:
                config = json.load(f)
        elif yaml_file.exists():
            with open(yaml_file, 'r') as f:
                config = yaml.safe_load(f)
        else:
            config = self._get_default_config(config_name)
        
        self._config_cache[config_name] = config
        return config
    
    def save_config(self, config_name: str, config: Dict[str, Any], format: str = "json") -> None:
        """Save configuration to file."""
        if format == "json":
            config_file = self.config_dir / f"{config_name}.json"
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
        elif format == "yaml":
            config_file = self.config_dir / f"{config_name}.yaml"
            with open(config_file, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        # Update cache
        self._config_cache[config_name] = config
    
    def update_config(self, config_name: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update configuration with new values."""
        config = self.load_config(config_name)
        
        def deep_update(base_dict, update_dict):
            for key, value in update_dict.items():
                if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                    deep_update(base_dict[key], value)
                else:
                    base_dict[key] = value
        
        deep_update(config, updates)
        self.save_config(config_name, config)
        return config
    
    def validate_config(self, config_name: str, config: Dict[str, Any]) -> bool:
        """Validate configuration against schema."""
        validators = {
            "database": self._validate_database_config,
            "deployment": self._validate_deployment_config,
            "document_sources": self._validate_document_sources_config,
            "web_interface": self._validate_web_interface_config
        }
        
        validator = validators.get(config_name)
        if validator:
            return validator(config)
        
        return True  # No specific validation
    
    def _get_default_config(self, config_name: str) -> Dict[str, Any]:
        """Get default configuration for a given config type."""
        defaults = {
            "database": {
                "sql_database": {
                    "type": "sqlite",
                    "database": "app.db",
                    "host": "localhost",
                    "port": 5432,
                    "username": "",
                    "password": ""
                },
                "neo4j_database": {
                    "uri": "bolt://localhost:7687",
                    "username": "neo4j",
                    "password": ""
                },
                "vector_store": {
                    "type": "chroma",
                    "persist_directory": "./chroma_db"
                }
            },
            "deployment": {
                "environment": "development",
                "debug": True,
                "log_level": "INFO",
                "host": "localhost",
                "port": 8000,
                "worker_processes": 1,
                "max_workers": 4,
                "timeout": 30
            },
            "document_sources": {
                "political_documents": {
                    "enabled": True,
                    "sources": [
                        {"type": "directory", "path": "./data/political"},
                        {"type": "api", "url": "https://api.example.com/political"}
                    ],
                    "update_frequency": "daily",
                    "filters": ["government", "policy", "legislation"]
                }
            },
            "web_interface": {
                "enabled": True,
                "theme": "default",
                "title": "LlamaIndex Political Document Manager",
                "features": {
                    "document_upload": True,
                    "search": True,
                    "analytics": True,
                    "configuration": True
                }
            }
        }
        
        return defaults.get(config_name, {})
    
    def _validate_database_config(self, config: Dict[str, Any]) -> bool:
        """Validate database configuration."""
        required_sections = ["sql_database", "vector_store"]
        
        for section in required_sections:
            if section not in config:
                return False
        
        # Validate SQL database config
        sql_config = config["sql_database"]
        required_sql_fields = ["type", "database"]
        for field in required_sql_fields:
            if field not in sql_config:
                return False
        
        # Validate vector store config
        vector_config = config["vector_store"]
        if "type" not in vector_config:
            return False
        
        return True
    
    def _validate_deployment_config(self, config: Dict[str, Any]) -> bool:
        """Validate deployment configuration."""
        required_fields = ["environment", "host", "port"]
        
        for field in required_fields:
            if field not in config:
                return False
        
        # Validate port is an integer
        if not isinstance(config["port"], int):
            return False
        
        # Validate environment is valid
        valid_environments = ["development", "staging", "production"]
        if config["environment"] not in valid_environments:
            return False
        
        return True
    
    def _validate_document_sources_config(self, config: Dict[str, Any]) -> bool:
        """Validate document sources configuration."""
        for source_name, source_config in config.items():
            if not isinstance(source_config, dict):
                return False
            
            if "enabled" not in source_config:
                return False
            
            if "sources" not in source_config:
                return False
            
            # Validate each source
            for source in source_config["sources"]:
                if "type" not in source:
                    return False
                
                if source["type"] == "directory" and "path" not in source:
                    return False
                elif source["type"] == "api" and "url" not in source:
                    return False
        
        return True
    
    def _validate_web_interface_config(self, config: Dict[str, Any]) -> bool:
        """Validate web interface configuration."""
        required_fields = ["enabled", "title"]
        
        for field in required_fields:
            if field not in config:
                return False
        
        if "features" in config:
            if not isinstance(config["features"], dict):
                return False
        
        return True


class TestConfigurationManager:
    """Test the configuration manager."""
    
    @pytest.fixture
    def config_manager(self, temp_dir: Path):
        """Create a configuration manager with temporary directory."""
        config_dir = temp_dir / "config"
        return ConfigurationManager(config_dir)
    
    def test_default_configurations(self, config_manager: ConfigurationManager):
        """Test loading default configurations."""
        # Test database config
        db_config = config_manager.load_config("database")
        assert "sql_database" in db_config
        assert "vector_store" in db_config
        assert db_config["sql_database"]["type"] == "sqlite"
        
        # Test deployment config
        deploy_config = config_manager.load_config("deployment")
        assert deploy_config["environment"] == "development"
        assert deploy_config["port"] == 8000
        
        # Test document sources config
        doc_config = config_manager.load_config("document_sources")
        assert "political_documents" in doc_config
        assert doc_config["political_documents"]["enabled"] is True
        
    def test_save_and_load_config(self, config_manager: ConfigurationManager):
        """Test saving and loading configuration."""
        test_config = {
            "sql_database": {
                "type": "postgresql",
                "host": "test-host",
                "port": 5432,
                "database": "test_db"
            }
        }
        
        # Save config
        config_manager.save_config("test_config", test_config)
        
        # Load config
        loaded_config = config_manager.load_config("test_config")
        assert loaded_config == test_config
        
    def test_update_config(self, config_manager: ConfigurationManager):
        """Test updating configuration."""
        # Load default database config
        original_config = config_manager.load_config("database")
        original_db_type = original_config["sql_database"]["type"]
        
        # Update config
        updates = {
            "sql_database": {
                "type": "postgresql",
                "host": "new-host"
            }
        }
        
        updated_config = config_manager.update_config("database", updates)
        
        # Verify updates
        assert updated_config["sql_database"]["type"] == "postgresql"
        assert updated_config["sql_database"]["host"] == "new-host"
        # Verify other fields are preserved
        assert "vector_store" in updated_config
        
    def test_config_validation(self, config_manager: ConfigurationManager):
        """Test configuration validation."""
        # Valid database config
        valid_db_config = {
            "sql_database": {
                "type": "postgresql",
                "database": "test_db"
            },
            "vector_store": {
                "type": "chroma"
            }
        }
        assert config_manager.validate_config("database", valid_db_config)
        
        # Invalid database config (missing required fields)
        invalid_db_config = {
            "sql_database": {
                "host": "localhost"  # Missing type and database
            }
        }
        assert not config_manager.validate_config("database", invalid_db_config)
        
        # Valid deployment config
        valid_deploy_config = {
            "environment": "production",
            "host": "0.0.0.0",
            "port": 8080
        }
        assert config_manager.validate_config("deployment", valid_deploy_config)
        
        # Invalid deployment config
        invalid_deploy_config = {
            "environment": "invalid_env",  # Invalid environment
            "host": "localhost",
            "port": "8080"  # Should be integer
        }
        assert not config_manager.validate_config("deployment", invalid_deploy_config)


class TestDatabaseConfiguration:
    """Test database configuration specifically."""
    
    @pytest.fixture
    def config_manager(self, temp_dir: Path):
        return ConfigurationManager(temp_dir / "config")
    
    def test_sql_database_config(self, config_manager: ConfigurationManager, mock_database_config):
        """Test SQL database configuration."""
        sql_config = mock_database_config["sql_database"]
        
        # Test PostgreSQL configuration
        pg_config = {
            "sql_database": {
                "type": "postgresql",
                "host": sql_config["host"],
                "port": sql_config["port"],
                "database": sql_config["database"],
                "username": sql_config["username"],
                "password": sql_config["password"]
            },
            "vector_store": {"type": "chroma"}
        }
        
        assert config_manager.validate_config("database", pg_config)
        config_manager.save_config("database", pg_config)
        
        loaded_config = config_manager.load_config("database")
        assert loaded_config["sql_database"]["type"] == "postgresql"
        assert loaded_config["sql_database"]["host"] == sql_config["host"]
        
    def test_neo4j_database_config(self, config_manager: ConfigurationManager, mock_database_config):
        """Test Neo4j database configuration."""
        neo4j_config = mock_database_config["neo4j_database"]
        
        db_config = config_manager.load_config("database")
        db_config["neo4j_database"] = neo4j_config
        
        config_manager.save_config("database", db_config)
        loaded_config = config_manager.load_config("database")
        
        assert "neo4j_database" in loaded_config
        assert loaded_config["neo4j_database"]["uri"] == neo4j_config["uri"]
        
    def test_vector_store_config(self, config_manager: ConfigurationManager):
        """Test vector store configuration."""
        vector_configs = [
            {"type": "chroma", "persist_directory": "./chroma_db"},
            {"type": "pinecone", "api_key": "test-key", "environment": "test"},
            {"type": "weaviate", "url": "http://localhost:8080"}
        ]
        
        for vector_config in vector_configs:
            db_config = {
                "sql_database": {"type": "sqlite", "database": "test.db"},
                "vector_store": vector_config
            }
            
            assert config_manager.validate_config("database", db_config)
            config_manager.save_config("test_vector", db_config)
            
            loaded = config_manager.load_config("test_vector")
            assert loaded["vector_store"]["type"] == vector_config["type"]


class TestDeploymentConfiguration:
    """Test deployment configuration."""
    
    @pytest.fixture
    def config_manager(self, temp_dir: Path):
        return ConfigurationManager(temp_dir / "config")
    
    def test_environment_configurations(self, config_manager: ConfigurationManager):
        """Test different environment configurations."""
        environments = {
            "development": {
                "environment": "development",
                "debug": True,
                "log_level": "DEBUG",
                "host": "localhost",
                "port": 8000
            },
            "staging": {
                "environment": "staging",
                "debug": False,
                "log_level": "INFO",
                "host": "0.0.0.0",
                "port": 8080
            },
            "production": {
                "environment": "production",
                "debug": False,
                "log_level": "WARNING",
                "host": "0.0.0.0",
                "port": 80,
                "worker_processes": 4,
                "max_workers": 16
            }
        }
        
        for env_name, env_config in environments.items():
            assert config_manager.validate_config("deployment", env_config)
            config_manager.save_config(f"deployment_{env_name}", env_config)
            
            loaded = config_manager.load_config(f"deployment_{env_name}")
            assert loaded["environment"] == env_name
            assert loaded["debug"] == env_config["debug"]
            
    def test_scaling_configuration(self, config_manager: ConfigurationManager):
        """Test scaling-related configuration."""
        scaling_config = {
            "environment": "production",
            "host": "0.0.0.0",
            "port": 8080,
            "worker_processes": 8,
            "max_workers": 32,
            "timeout": 60,
            "auto_scaling": {
                "enabled": True,
                "min_workers": 2,
                "max_workers": 50,
                "cpu_threshold": 70,
                "memory_threshold": 80
            }
        }
        
        assert config_manager.validate_config("deployment", scaling_config)
        config_manager.save_config("deployment_scaling", scaling_config)
        
        loaded = config_manager.load_config("deployment_scaling")
        assert loaded["worker_processes"] == 8
        assert loaded["auto_scaling"]["enabled"] is True


class TestDocumentSourcesConfiguration:
    """Test document sources configuration."""
    
    @pytest.fixture
    def config_manager(self, temp_dir: Path):
        return ConfigurationManager(temp_dir / "config")
    
    def test_political_document_sources(self, config_manager: ConfigurationManager):
        """Test configuration for political document sources."""
        political_config = {
            "political_documents": {
                "enabled": True,
                "sources": [
                    {
                        "type": "directory",
                        "path": "/data/political/federal",
                        "recursive": True,
                        "file_patterns": ["*.pdf", "*.txt", "*.docx"]
                    },
                    {
                        "type": "api",
                        "url": "https://api.congress.gov/v3",
                        "api_key": "test-key",
                        "endpoints": ["bills", "votes", "members"]
                    },
                    {
                        "type": "web_scraper",
                        "urls": ["https://www.govinfo.gov"],
                        "selectors": [".document-content"],
                        "rate_limit": 1
                    }
                ],
                "update_frequency": "daily",
                "filters": {
                    "keywords": ["healthcare", "economy", "environment"],
                    "date_range": {"start": "2020-01-01", "end": "2024-12-31"},
                    "document_types": ["bill", "resolution", "report"]
                },
                "processing": {
                    "text_extraction": True,
                    "sentiment_analysis": True,
                    "entity_recognition": True,
                    "topic_modeling": True
                }
            }
        }
        
        assert config_manager.validate_config("document_sources", political_config)
        config_manager.save_config("document_sources", political_config)
        
        loaded = config_manager.load_config("document_sources")
        assert loaded["political_documents"]["enabled"] is True
        assert len(loaded["political_documents"]["sources"]) == 3
        
    def test_multiple_document_sources(self, config_manager: ConfigurationManager):
        """Test configuration with multiple document source types."""
        multi_source_config = {
            "political_documents": {
                "enabled": True,
                "sources": [{"type": "directory", "path": "/data/political"}],
                "update_frequency": "daily"
            },
            "news_articles": {
                "enabled": True,
                "sources": [{"type": "rss", "url": "https://feeds.reuters.com/politics"}],
                "update_frequency": "hourly"
            },
            "academic_papers": {
                "enabled": False,
                "sources": [{"type": "api", "url": "https://api.arxiv.org"}],
                "update_frequency": "weekly"
            }
        }
        
        assert config_manager.validate_config("document_sources", multi_source_config)
        config_manager.save_config("document_sources_multi", multi_source_config)
        
        loaded = config_manager.load_config("document_sources_multi")
        assert "political_documents" in loaded
        assert "news_articles" in loaded
        assert "academic_papers" in loaded
        assert loaded["academic_papers"]["enabled"] is False


class TestWebInterfaceConfiguration:
    """Test web interface configuration."""
    
    @pytest.fixture
    def config_manager(self, temp_dir: Path):
        return ConfigurationManager(temp_dir / "config")
    
    def test_web_interface_basic_config(self, config_manager: ConfigurationManager):
        """Test basic web interface configuration."""
        web_config = {
            "enabled": True,
            "title": "Political Document Analysis Platform",
            "theme": "dark",
            "language": "en",
            "features": {
                "document_upload": True,
                "search": True,
                "analytics": True,
                "configuration": True,
                "user_management": False
            },
            "ui_customization": {
                "logo_url": "/static/logo.png",
                "primary_color": "#1f2937",
                "secondary_color": "#3b82f6",
                "font_family": "Inter"
            }
        }
        
        assert config_manager.validate_config("web_interface", web_config)
        config_manager.save_config("web_interface", web_config)
        
        loaded = config_manager.load_config("web_interface")
        assert loaded["enabled"] is True
        assert loaded["title"] == "Political Document Analysis Platform"
        assert loaded["features"]["search"] is True
        
    def test_web_interface_advanced_config(self, config_manager: ConfigurationManager):
        """Test advanced web interface configuration."""
        advanced_config = {
            "enabled": True,
            "title": "Advanced Political Analytics",
            "authentication": {
                "enabled": True,
                "providers": ["local", "oauth", "ldap"],
                "session_timeout": 3600,
                "require_2fa": True
            },
            "features": {
                "document_upload": True,
                "search": True,
                "analytics": True,
                "configuration": True,
                "api_access": True,
                "data_export": True,
                "collaboration": True
            },
            "permissions": {
                "admin": ["all"],
                "analyst": ["search", "analytics", "data_export"],
                "viewer": ["search"]
            },
            "integrations": {
                "slack": {"enabled": True, "webhook_url": "https://hooks.slack.com/..."},
                "email": {"enabled": True, "smtp_server": "smtp.example.com"},
                "webhook": {"enabled": True, "endpoints": ["/api/webhook/update"]}
            }
        }
        
        assert config_manager.validate_config("web_interface", advanced_config)
        config_manager.save_config("web_interface_advanced", advanced_config)
        
        loaded = config_manager.load_config("web_interface_advanced")
        assert loaded["authentication"]["enabled"] is True
        assert "oauth" in loaded["authentication"]["providers"]
        assert loaded["permissions"]["analyst"] == ["search", "analytics", "data_export"]