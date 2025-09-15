#!/usr/bin/env python3
"""
Test Ingestion Script for Political Document Analysis System
This script demonstrates how to ingest political documents using our system.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

# Try to import configuration (may fail if dependencies not installed)
try:
    from political_analysis_init import config
    CONFIG_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import configuration: {e}")
    CONFIG_AVAILABLE = False

from political_document_ingestor import PoliticalDocumentIngestor

def create_mock_config():
    """Create a mock configuration object for testing"""
    class MockConfig:
        SUPPORTED_FORMATS = ["pdf", "docx", "txt", "html", "json", "csv"]
        MAX_CRAWL_DEPTH = 3
        MAX_CRAWL_PAGES = 1000
        RESPECT_ROBOTS_TXT = True
        CRAWL_DELAY = 1.0
        PROJECT_ROOT = Path(__file__).parent
        DATA_DIR = PROJECT_ROOT / "data"
        OUTPUT_DIR = PROJECT_ROOT / "output"
        LOG_DIR = PROJECT_ROOT / "logs"
        
    return MockConfig()

async def run_test_ingestion():
    """Run a test ingestion of political documents"""
    
    print("Political Document Analysis System - Test Ingestion")
    print("=" * 55)
    
    # Use real config or mock config
    if CONFIG_AVAILABLE:
        config = create_mock_config()  # Use mock for this test
        print("\n1. Using mock configuration...")
    else:
        config = create_mock_config()
        print("\n1. Using mock configuration (no real config available)...")
    
    # Initialize components
    print("\n2. Initializing components...")
    ingestor = PoliticalDocumentIngestor(config)
    
    # Define test sources (only local for this test)
    print("\n3. Defining test sources...")
    test_sources = {
        "local_directories": ["./data/sample_docs"],
        # Not using web sources in this test to avoid dependency issues
    }
    
    print("Test sources defined:")
    for source_type, sources in test_sources.items():
        print(f"  {source_type}: {len(sources)} sources")
        for source in sources:
            print(f"    - {source}")
    
    # Run ingestion
    print("\n4. Running document ingestion...")
    documents = ingestor.batch_ingest(test_sources)
    
    if not documents:
        print("❌ No documents were ingested. Check the sources and try again.")
        return
    
    print(f"✅ Successfully ingested {len(documents)} documents")
    
    # Display document information
    print("\n5. Document information:")
    for i, doc in enumerate(documents[:3]):  # Show first 3 documents
        print(f"  Document {i+1}:")
        print(f"    ID: {doc.doc_id}")
        print(f"    Text length: {len(doc.text)} characters")
        print(f"    Preview: {doc.text[:100]}...")
        print()
    
    if len(documents) > 3:
        print(f"  ... and {len(documents) - 3} more documents")
    
    # Save documents to output directory
    print("\n6. Saving documents...")
    output_dir = Path("./output/ingested_documents")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for i, doc in enumerate(documents):
        # Create a filename based on document ID or index
        filename = f"document_{i+1:03d}.txt"
        filepath = output_dir / filename
        
        # Save document text
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Document ID: {doc.doc_id}\n")
            f.write(f"Metadata: {getattr(doc, 'metadata', {})}\n")
            f.write("-" * 50 + "\n")
            f.write(doc.text)
    
    print(f"  ✅ Saved {len(documents)} documents to {output_dir}")
    
    print("\n" + "=" * 55)
    print("Test ingestion completed successfully!")
    print(f"Documents saved to: {output_dir.absolute()}")
    print("\nNext steps:")
    print("1. Install full dependencies to enable web crawling and entity extraction")
    print("2. Run the full analysis pipeline with: python political_analysis_orchestrator.py")
    print("3. Try the demo notebook with: jupyter notebook political_analysis_demo.ipynb")

if __name__ == "__main__":
    # Run the test ingestion
    asyncio.run(run_test_ingestion())