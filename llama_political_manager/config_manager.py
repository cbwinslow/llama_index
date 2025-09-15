"""
Configuration management system for the LlamaIndex Political Document Manager.
"""
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

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