"""
Shared test configuration and fixtures for the comprehensive test suite.
"""
import os
import pytest
import tempfile
from pathlib import Path
from typing import Generator

# Set testing environment
os.environ["IS_TESTING"] = "1"

@pytest.fixture(autouse=True)
def mock_openai_credentials() -> None:
    """Mock OpenAI credentials for testing."""
    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = "sk-" + ("a" * 48)

@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)

@pytest.fixture
def sample_documents(temp_dir: Path) -> list[Path]:
    """Create sample documents for testing."""
    docs = []
    
    # Political document sample
    political_doc = temp_dir / "political_sample.txt"
    political_doc.write_text("""
    Political Document Sample
    
    This is a sample political document containing information about
    government policies, voting records, and legislative proposals.
    
    Key topics include:
    - Healthcare reform
    - Economic policy
    - Environmental regulations
    - Education funding
    """)
    docs.append(political_doc)
    
    # Technical document sample
    tech_doc = temp_dir / "technical_sample.txt"
    tech_doc.write_text("""
    Technical Documentation
    
    This document contains technical specifications and implementation details
    for data processing systems and database configurations.
    
    Topics covered:
    - Database schema design
    - API endpoints
    - Configuration management
    - Deployment procedures
    """)
    docs.append(tech_doc)
    
    return docs

@pytest.fixture
def mock_database_config():
    """Mock database configuration for testing."""
    return {
        "sql_database": {
            "type": "postgresql",
            "host": "localhost",
            "port": 5432,
            "database": "test_db",
            "username": "test_user",
            "password": "test_pass"
        },
        "neo4j_database": {
            "uri": "bolt://localhost:7687",
            "username": "neo4j",
            "password": "test_pass"
        },
        "vector_store": {
            "type": "chroma",
            "persist_directory": "./test_chroma_db"
        }
    }

@pytest.fixture
def mock_deployment_config():
    """Mock deployment configuration for testing."""
    return {
        "environment": "test",
        "debug": True,
        "log_level": "DEBUG",
        "worker_processes": 1,
        "max_workers": 4,
        "timeout": 30,
        "host": "localhost",
        "port": 8000
    }