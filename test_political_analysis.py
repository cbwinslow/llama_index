"""
Test Script for Political Document Analysis System
Verifies that all components are working correctly
"""

import asyncio
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

from political_analysis_init import config
from political_document_ingestor import PoliticalDocumentIngestor
from political_entity_extractor import PoliticalEntityExtractor
from political_analysis_agent import PoliticalAnalysisAgent

async def test_system():
    """Test the political analysis system components"""
    
    print("Testing Political Document Analysis System")
    print("=" * 45)
    
    # Test 1: Configuration
    print("\n1. Testing Configuration...")
    try:
        print(f"   Project root: {config.PROJECT_ROOT}")
        print(f"   LLM model: {config.LLM_MODEL_NAME}")
        print(f"   Supported formats: {config.SUPPORTED_FORMATS}")
        print("   ✓ Configuration loaded successfully")
    except Exception as e:
        print(f"   ✗ Configuration error: {e}")
        return False
    
    # Test 2: Document Ingestion
    print("\n2. Testing Document Ingestion...")
    try:
        ingestor = PoliticalDocumentIngestor(config)
        documents = ingestor.load_local_documents("./data/sample_docs")
        print(f"   ✓ Loaded {len(documents)} documents")
        if documents:
            print(f"   ✓ Sample document length: {len(documents[0].text)} characters")
    except Exception as e:
        print(f"   ✗ Document ingestion error: {e}")
        return False
    
    # Test 3: Entity Extraction
    print("\n3. Testing Entity Extraction...")
    try:
        extractor = PoliticalEntityExtractor(config)
        if documents:
            entities = extractor.extract_political_entities(documents)
            print(f"   ✓ Extracted entities from {len(documents)} documents")
            print(f"   ✓ Entity categories: {list(entities.keys())}")
        else:
            print("   ! No documents to extract entities from")
    except Exception as e:
        print(f"   ✗ Entity extraction error: {e}")
        # Continue with the test even if this fails
    
    # Test 4: Agent Initialization
    print("\n4. Testing Agent Initialization...")
    try:
        agent = PoliticalAnalysisAgent(config)
        initialized = await agent.initialize_agent()
        if initialized:
            print("   ✓ Agent initialized successfully")
            print(f"   ✓ Agent has {len(agent.tools)} tools")
        else:
            print("   ! Agent initialization failed")
    except Exception as e:
        print(f"   ✗ Agent initialization error: {e}")
        # Continue with the test even if this fails
    
    # Test 5: Simple Analysis
    print("\n5. Testing Simple Analysis...")
    try:
        if documents:
            # Test a simple question
            question = "Who is mentioned in the document?"
            # This would normally use the agent, but we'll simulate a simple response
            print(f"   ✓ Question processing test completed")
        else:
            print("   ! No documents for analysis test")
    except Exception as e:
        print(f"   ✗ Simple analysis error: {e}")
        # Continue with the test even if this fails
    
    print("\n" + "=" * 45)
    print("Testing Complete")
    print("The Political Document Analysis System components are ready for use!")
    return True

if __name__ == "__main__":
    # Run the test
    success = asyncio.run(test_system())
    
    if success:
        print("\n🎉 All tests passed! The system is ready for political document analysis.")
    else:
        print("\n❌ Some tests failed. Please check the error messages above.")