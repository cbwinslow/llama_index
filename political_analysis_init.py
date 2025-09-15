"""
Political Document Analysis System
Main initialization and configuration module
"""

import os
from dotenv import load_dotenv
import configparser
from pathlib import Path

# Load environment variables
env_path = Path(__file__).parent / ".env.political_analysis"
load_dotenv(env_path)

# Load configuration
config = configparser.ConfigParser()
config_path = Path(__file__).parent / "political_analysis_config.ini"
config.read(config_path)

# System paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / config.get("paths", "data_dir", fallback="./data")
OUTPUT_DIR = PROJECT_ROOT / config.get("paths", "output_dir", fallback="./output")
LOG_DIR = PROJECT_ROOT / config.get("paths", "log_dir", fallback="./logs")
MODEL_DIR = PROJECT_ROOT / config.get("paths", "model_dir", fallback="./models")

# Create directories if they don't exist
for directory in [DATA_DIR, OUTPUT_DIR, LOG_DIR, MODEL_DIR]:
    directory.mkdir(exist_ok=True)

# System configuration
class Config:
    """Configuration class for the Political Document Analysis System"""
    
    # Ingestion settings
    SUPPORTED_FORMATS = config.get("ingestion", "supported_formats", fallback=["pdf", "docx", "txt", "html", "json", "csv"])
    MAX_CRAWL_DEPTH = config.getint("ingestion", "max_depth", fallback=3)
    MAX_CRAWL_PAGES = config.getint("ingestion", "max_pages", fallback=1000)
    RESPECT_ROBOTS_TXT = config.getboolean("ingestion", "respect_robots_txt", fallback=True)
    CRAWL_DELAY = config.getfloat("ingestion", "delay_between_requests", fallback=1.0)
    
    # Extraction settings
    ENABLE_NER = config.getboolean("extraction", "enable_named_entity_recognition", fallback=True)
    ENABLE_RELATION_EXTRACTION = config.getboolean("extraction", "enable_relation_extraction", fallback=True)
    ENABLE_SENTIMENT_ANALYSIS = config.getboolean("extraction", "enable_sentiment_analysis", fallback=True)
    POLITICAL_ENTITIES = config.get("extraction", "political_entities", fallback=["politician", "political_party", "legislation", "policy", "vote", "election"])
    
    # Graph settings
    GRAPH_DATABASE = config.get("graph", "graph_database", fallback="neo4j")
    ENABLE_DYNAMIC_UPDATES = config.getboolean("graph", "enable_dynamic_updates", fallback=True)
    ENABLE_VISUALIZATION = config.getboolean("graph", "enable_visualization", fallback=True)
    MIN_CONFIDENCE_SCORE = config.getfloat("graph", "min_confidence_score", fallback=0.7)
    MAX_RELATIONSHIPS_PER_ENTITY = config.getint("graph", "max_relationships_per_entity", fallback=50)
    
    # MCP settings
    MCP_SERVER_URL = config.get("mcp", "mcp_server_url", fallback="http://localhost:8000")
    ENABLE_OAUTH = config.getboolean("mcp", "enable_oauth", fallback=False)
    MAX_MCP_RETRIES = config.getint("mcp", "max_retries", fallback=3)
    
    # Agent settings
    MAX_AGENT_ITERATIONS = config.getint("agents", "max_iterations", fallback=10)
    ENABLE_TOOL_USAGE = config.getboolean("agents", "enable_tool_usage", fallback=True)
    ENABLE_MEMORY = config.getboolean("agents", "enable_memory", fallback=True)
    
    # LLM settings
    LLM_MODEL_NAME = config.get("llm", "model_name", fallback="gpt-4")
    LLM_TEMPERATURE = config.getfloat("llm", "temperature", fallback=0.7)
    LLM_MAX_TOKENS = config.getint("llm", "max_tokens", fallback=2000)
    
    # Embedding settings
    EMBEDDING_MODEL_NAME = config.get("embedding", "model_name", fallback="text-embedding-3-large")
    EMBEDDING_DIMENSIONS = config.getint("embedding", "dimensions", fallback=3072)
    
    # Evaluation settings
    ENABLE_AUTO_EVALUATION = config.getboolean("evaluation", "enable_auto_evaluation", fallback=True)
    EVALUATION_DATASET_PATH = PROJECT_ROOT / config.get("evaluation", "evaluation_dataset_path", fallback="./data/evaluation")

# Initialize configuration
config = Config()

if __name__ == "__main__":
    print("Political Document Analysis System Configuration")
    print("=" * 50)
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Data Directory: {DATA_DIR}")
    print(f"Output Directory: {OUTPUT_DIR}")
    print(f"Log Directory: {LOG_DIR}")
    print(f"Model Directory: {MODEL_DIR}")
    print(f"Supported Formats: {config.SUPPORTED_FORMATS}")
    print(f"LLM Model: {config.LLM_MODEL_NAME}")
    print(f"Embedding Model: {config.EMBEDDING_MODEL_NAME}")