#!/usr/bin/env python3
"""
Demonstration script for the LlamaIndex Political Document Manager.

This script showcases the key features and capabilities of the system.
"""
import sys
from pathlib import Path

# Add the parent directory to the path so we can import our modules
sys.path.append(str(Path(__file__).parent))

from llama_political_manager.config_manager import ConfigurationManager
from llama_political_manager.mcp_server import PoliticalDocumentMCPServer
from llama_political_manager.web_interface import WebInterface, MockRequest
from llama_political_manager.document_processor import DocumentProcessor

def demo_configuration_management():
    """Demonstrate configuration management functionality."""
    print("=" * 60)
    print("CONFIGURATION MANAGEMENT DEMO")
    print("=" * 60)
    
    # Create a temporary config manager
    config_manager = ConfigurationManager(Path("./demo_config"))
    
    # Show default configurations
    print("\n1. Default Database Configuration:")
    db_config = config_manager.load_config("database")
    print(f"   SQL Database Type: {db_config['sql_database']['type']}")
    print(f"   Vector Store Type: {db_config['vector_store']['type']}")
    
    # Update configuration
    print("\n2. Updating Database Configuration:")
    updates = {
        "sql_database": {
            "type": "postgresql",
            "host": "production-db.example.com",
            "port": 5432
        }
    }
    updated_config = config_manager.update_config("database", updates)
    print(f"   Updated SQL Database Type: {updated_config['sql_database']['type']}")
    print(f"   Updated Host: {updated_config['sql_database']['host']}")
    
    # Show deployment configuration
    print("\n3. Deployment Configuration:")
    deploy_config = config_manager.load_config("deployment")
    print(f"   Environment: {deploy_config['environment']}")
    print(f"   Host: {deploy_config['host']}")
    print(f"   Port: {deploy_config['port']}")
    
    print("\n✓ Configuration management working correctly!")

def demo_document_processing():
    """Demonstrate document processing functionality."""
    print("\n" + "=" * 60)
    print("DOCUMENT PROCESSING DEMO")
    print("=" * 60)
    
    processor = DocumentProcessor()
    
    # Sample political document
    sample_document = """
    Healthcare Reform Act of 2024
    
    This comprehensive healthcare reform legislation aims to expand access to affordable 
    healthcare for all Americans. The bill includes provisions for Medicare expansion, 
    prescription drug cost reduction, and mental health support.
    
    Key provisions include:
    1. Public option for health insurance
    2. Lowering Medicare eligibility age to 60
    3. Dental and vision coverage for Medicare beneficiaries
    4. Price transparency requirements for hospitals
    5. Investment in community health centers
    
    This legislation represents a significant step toward ensuring healthcare is a right,
    not a privilege, for every American citizen.
    """
    
    print("\n1. Processing Political Document:")
    result = processor.process_document(sample_document, {"source": "demo", "type": "legislation"})
    
    print(f"   Word Count: {result['word_count']}")
    print(f"   Language: {result['language']}")
    print(f"   Readability Score: {result['readability_score']}")
    
    print("\n2. Political Analysis:")
    political_analysis = result['political_analysis']
    print(f"   Total Political Mentions: {political_analysis['total_policy_mentions']}")
    print(f"   Primary Topics: {', '.join(political_analysis['primary_topics'])}")
    print(f"   Political Score: {political_analysis['political_score']}")
    
    print("\n3. Healthcare Topic Analysis:")
    healthcare_analysis = political_analysis['analysis_by_topic']['healthcare']
    print(f"   Healthcare Mentions: {healthcare_analysis['mentions']}")
    print(f"   Keyword Density: {healthcare_analysis['keyword_density']}%")
    print(f"   Relevance: {healthcare_analysis['relevance']}")
    
    print("\n4. Sentiment Analysis:")
    sentiment = result['sentiment']
    print(f"   Sentiment: {sentiment['label']} (score: {sentiment['score']})")
    print(f"   Positive Words: {sentiment['positive_words']}")
    print(f"   Negative Words: {sentiment['negative_words']}")
    
    print("\n5. Document Classification:")
    classification = result['classification']
    print(f"   Document Type: {classification['primary_type']}")
    print(f"   Confidence: {classification['confidence']}%")
    
    print("\n6. Extracted Entities:")
    entities = result['entities']
    if entities['bills']:
        print(f"   Bills: {', '.join(entities['bills'])}")
    if entities['dates']:
        print(f"   Dates: {', '.join(entities['dates'])}")
    
    print("\n✓ Document processing working correctly!")

async def demo_mcp_server():
    """Demonstrate MCP server functionality."""
    print("\n" + "=" * 60)
    print("MCP SERVER DEMO")
    print("=" * 60)
    
    # Create MCP server with configuration
    config_manager = ConfigurationManager(Path("./demo_config"))
    mcp_server = PoliticalDocumentMCPServer(config_manager=config_manager)
    
    print("\n1. Starting MCP Server:")
    await mcp_server.start("localhost", 8080)
    print(f"   Server running: {mcp_server.is_running}")
    print(f"   Host: {mcp_server.host}")
    print(f"   Port: {mcp_server.port}")
    
    print("\n2. Available Tools:")
    tools = mcp_server.list_tools()
    for tool in tools:
        print(f"   - {tool['name']}: {tool['description']}")
    
    print("\n3. Testing Political Content Analysis Tool:")
    political_text = "This bill addresses healthcare reform and economic policy to improve healthcare access."
    
    analysis_result = await mcp_server.handle_tool_call(
        "analyze_political_content",
        {"text": political_text}
    )
    
    print(f"   Total Policy Mentions: {analysis_result['total_policy_mentions']}")
    print(f"   Primary Topics: {', '.join(analysis_result['primary_topics'])}")
    
    print("\n4. Testing Configuration Tool:")
    config_result = await mcp_server.handle_tool_call(
        "get_config",
        {"config_type": "deployment"}
    )
    
    print(f"   Environment: {config_result['environment']}")
    print(f"   Debug Mode: {config_result['debug']}")
    
    print("\n5. Testing Database Query Tool:")
    query_result = await mcp_server.handle_tool_call(
        "query_database",
        {"query": "SELECT * FROM documents WHERE category = 'political'", "database_type": "sql"}
    )
    
    print(f"   Query Results: {query_result['count']} documents found")
    print(f"   Database Type: {query_result['database_type']}")
    
    await mcp_server.stop()
    print("\n✓ MCP server working correctly!")

def demo_web_interface():
    """Demonstrate web interface functionality."""
    print("\n" + "=" * 60)
    print("WEB INTERFACE DEMO")
    print("=" * 60)
    
    config_manager = ConfigurationManager(Path("./demo_config"))
    web_app = WebInterface(config_manager=config_manager)
    
    print("\n1. Testing Home Page:")
    home_request = MockRequest("GET", "/")
    home_response = web_app.app.handle_request(home_request)
    print(f"   Status: {home_response.status_code}")
    print(f"   Title: {home_response.data['title']}")
    print(f"   Features: {len(home_response.data['features'])} available")
    
    print("\n2. Testing Health Check:")
    health_request = MockRequest("GET", "/api/health")
    health_response = web_app.app.handle_request(health_request)
    print(f"   Status: {health_response.status_code}")
    print(f"   System Status: {health_response.data['status']}")
    print(f"   Components: {', '.join(health_response.data['components'].keys())}")
    
    print("\n3. Testing Document Upload:")
    upload_data = {
        "title": "Demo Political Document",
        "content": "This is a demo document about healthcare policy and economic reform.",
        "category": "political"
    }
    upload_request = MockRequest("POST", "/api/documents", json_data=upload_data)
    upload_response = web_app.app.handle_request(upload_request)
    print(f"   Upload Status: {upload_response.status_code}")
    print(f"   Document ID: {upload_response.data['document']['id']}")
    print(f"   Document Title: {upload_response.data['document']['title']}")
    
    print("\n4. Testing Document Search:")
    search_data = {"query": "healthcare policy"}
    search_request = MockRequest("POST", "/api/search", json_data=search_data)
    search_response = web_app.app.handle_request(search_request)
    print(f"   Search Status: {search_response.status_code}")
    print(f"   Results Found: {search_response.data['total']}")
    print(f"   Query Time: {search_response.data['took_ms']}ms")
    
    print("\n5. Testing Analytics:")
    analytics_request = MockRequest("GET", "/api/analytics")
    analytics_response = web_app.app.handle_request(analytics_request)
    print(f"   Analytics Status: {analytics_response.status_code}")
    print(f"   Total Documents: {analytics_response.data['document_stats']['total_documents']}")
    print(f"   Political Documents: {analytics_response.data['document_stats']['political_documents']}")
    
    print("\n6. Testing Configuration Management:")
    config_request = MockRequest("GET", "/api/config", query_params={"type": "database"})
    config_response = web_app.app.handle_request(config_request)
    print(f"   Config Status: {config_response.status_code}")
    print(f"   Database Type: {config_response.data['database']['sql_database']['type']}")
    
    print("\n✓ Web interface working correctly!")

def demo_integration_workflow():
    """Demonstrate complete integration workflow."""
    print("\n" + "=" * 60)
    print("INTEGRATION WORKFLOW DEMO")
    print("=" * 60)
    
    print("\n1. Initializing Complete System:")
    
    # Initialize all components
    config_manager = ConfigurationManager(Path("./demo_config"))
    processor = DocumentProcessor(config_manager)
    web_app = WebInterface(config_manager)
    
    print("   ✓ Configuration Manager initialized")
    print("   ✓ Document Processor initialized")
    print("   ✓ Web Interface initialized")
    
    print("\n2. Processing Sample Documents:")
    
    # Load sample documents
    data_dir = Path("./data")
    if data_dir.exists():
        documents = list(data_dir.glob("*.txt"))
        print(f"   Found {len(documents)} sample documents")
        
        for doc_path in documents[:2]:  # Process first 2 documents
            content = doc_path.read_text()
            result = processor.process_document(content, {"source": str(doc_path)})
            
            print(f"   Processed: {doc_path.name}")
            print(f"     - Political Score: {result['political_analysis']['political_score']}")
            print(f"     - Primary Topics: {', '.join(result['political_analysis']['primary_topics'])}")
    else:
        print("   No sample documents found (run with --create-sample-data first)")
    
    print("\n3. Configuration Validation:")
    
    # Test configuration validation
    db_config = config_manager.load_config("database")
    is_valid = config_manager.validate_config("database", db_config)
    print(f"   Database configuration valid: {is_valid}")
    
    deploy_config = config_manager.load_config("deployment")
    is_valid = config_manager.validate_config("deployment", deploy_config)
    print(f"   Deployment configuration valid: {is_valid}")
    
    print("\n4. End-to-End Document Workflow:")
    
    # Simulate complete workflow
    new_document = """
    Climate Action Framework 2024
    
    This framework outlines comprehensive climate action strategies including:
    - Renewable energy transition
    - Carbon emission reduction
    - Environmental justice initiatives
    - Green job creation programs
    
    The plan aims to achieve net-zero emissions by 2050 while ensuring
    economic growth and environmental sustainability.
    """
    
    # Process document
    processed_doc = processor.process_document(new_document, {"type": "policy"})
    print(f"   Document processed successfully")
    print(f"   Climate relevance: {processed_doc['political_analysis']['analysis_by_topic']['environment']['relevance']}")
    
    # Simulate web upload
    upload_data = {
        "title": "Climate Action Framework 2024",
        "content": new_document,
        "category": "policy"
    }
    upload_request = MockRequest("POST", "/api/documents", json_data=upload_data)
    upload_response = web_app.app.handle_request(upload_request)
    print(f"   Document uploaded via web interface: {upload_response.data['success']}")
    
    # Simulate search
    search_data = {"query": "climate action"}
    search_request = MockRequest("POST", "/api/search", json_data=search_data)
    search_response = web_app.app.handle_request(search_request)
    print(f"   Document searchable: {search_response.data['total']} results")
    
    print("\n✓ Complete integration workflow working correctly!")

async def main():
    """Run all demonstrations."""
    print("LlamaIndex Political Document Manager - Comprehensive Demo")
    print("=" * 80)
    
    try:
        # Run all demos
        demo_configuration_management()
        demo_document_processing()
        await demo_mcp_server()
        demo_web_interface()
        demo_integration_workflow()
        
        print("\n" + "=" * 80)
        print("DEMO COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print("\nAll components are working correctly:")
        print("✓ Configuration Management")
        print("✓ Document Processing & Political Analysis")
        print("✓ MCP Server Integration")
        print("✓ Web Interface & APIs")
        print("✓ End-to-End Workflows")
        
        print("\nThe LlamaIndex Political Document Manager is ready for:")
        print("• Political document ingestion and analysis")
        print("• Integration with external services via MCP")
        print("• Web-based configuration and management")
        print("• Database integration (SQL, Neo4j, Vector stores)")
        print("• Scalable deployment configurations")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())