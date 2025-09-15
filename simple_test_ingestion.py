#!/usr/bin/env python3
"""
Simple Test Ingestion Script for Political Document Analysis System
This script demonstrates local document ingestion without web dependencies.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

# Import only what we need for local document ingestion
from llama_index.core import SimpleDirectoryReader

def create_mock_config():
    """Create a mock configuration object for testing"""
    class MockConfig:
        SUPPORTED_FORMATS = ["pdf", "docx", "txt", "html", "json", "csv"]
        PROJECT_ROOT = Path(__file__).parent
        DATA_DIR = PROJECT_ROOT / "data"
        OUTPUT_DIR = PROJECT_ROOT / "output"
        LOG_DIR = PROJECT_ROOT / "logs"
        
    return MockConfig()

class SimplePoliticalDocumentIngestor:
    """Simplified document ingestor for local files only"""
    
    def __init__(self, config):
        self.config = config
        self.supported_formats = config.SUPPORTED_FORMATS
        
    def load_local_documents(self, directory_path):
        """
        Load political documents from a local directory
        
        Args:
            directory_path: Path to directory containing documents
            
        Returns:
            List of document objects with content and metadata
        """
        print(f"Loading documents from {directory_path}")
        
        try:
            reader = SimpleDirectoryReader(
                input_dir=str(directory_path),
                filename_as_id=True,
                recursive=True,
                required_exts=[f".{ext}" for ext in self.supported_formats]
            )
            documents = reader.load_data()
            
            print(f"Loaded {len(documents)} documents from {directory_path}")
            return documents
            
        except Exception as e:
            print(f"Error loading documents from {directory_path}: {str(e)}")
            return []

async def run_simple_test_ingestion():
    """Run a simple test ingestion of political documents"""
    
    print("Political Document Analysis System - Simple Test Ingestion")
    print("=" * 55)
    
    # Use mock config
    config = create_mock_config()
    print("\n1. Using mock configuration...")
    
    # Initialize components
    print("\n2. Initializing components...")
    ingestor = SimplePoliticalDocumentIngestor(config)
    
    # Define test sources (only local for this test)
    print("\n3. Defining test sources...")
    test_directory = "./data/sample_docs"
    
    print(f"Test source: {test_directory}")
    
    # Run ingestion
    print("\n4. Running document ingestion...")
    documents = ingestor.load_local_documents(test_directory)
    
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
    print("Simple test ingestion completed successfully!")
    print(f"Documents saved to: {output_dir.absolute()}")
    print("\nThis was a minimal test using only local document ingestion.")
    print("To enable full functionality including web crawling and entity extraction:")
    print("1. Install additional dependencies: pip install llama-index-readers-web")
    print("2. Set up API keys in the .env file")
    print("3. Run the full ingestion pipeline")

if __name__ == "__main__":
    # Run the simple test ingestion
    asyncio.run(run_simple_test_ingestion())