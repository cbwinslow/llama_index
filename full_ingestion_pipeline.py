#!/usr/bin/env python3
"""
Full Ingestion Pipeline Script for Political Document Analysis System
This script provides a complete ingestion pipeline when all dependencies are available.
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

def check_dependencies():
    """Check if all required dependencies are available"""
    dependencies = {
        "llama_index": False,
        "llama_index_web_readers": False,
        "dotenv": False
    }
    
    try:
        import llama_index.core
        dependencies["llama_index"] = True
    except ImportError:
        pass
    
    try:
        import llama_index.readers.web
        dependencies["llama_index_web_readers"] = True
    except ImportError:
        pass
    
    try:
        import dotenv
        dependencies["dotenv"] = True
    except ImportError:
        pass
    
    return dependencies

def load_sources_from_config(config_file: str = None) -> Dict[str, Any]:
    """
    Load sources from a configuration file or use defaults
    
    Args:
        config_file: Path to JSON configuration file
        
    Returns:
        Dictionary of sources
    """
    if config_file and os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    else:
        # Return default sources
        return {
            "local_directories": ["./data/sample_docs"],
            "websites": [
                # Uncomment to enable (requires internet and web readers)
                # "https://www.congress.gov/",
            ],
            "rss_feeds": [
                # Uncomment to enable (requires internet and web readers)
                # "https://feeds.reuters.com/Reuters/PoliticsNews",
            ],
            "sitemaps": [
                # Uncomment to enable (requires internet and web readers)
                # "https://www.congress.gov/sitemap.xml",
            ]
        }

async def run_full_ingestion_pipeline(config_file: str = None):
    """
    Run the complete ingestion pipeline when all dependencies are available
    
    Args:
        config_file: Path to configuration file
    """
    print("Political Document Analysis System - Full Ingestion Pipeline")
    print("=" * 60)
    
    # Check dependencies
    deps = check_dependencies()
    print("\n1. Dependency check:")
    for dep, available in deps.items():
        status = "✅ Available" if available else "❌ Not available"
        print(f"   {dep}: {status}")
    
    # If core dependencies are missing, exit
    if not deps["llama_index"]:
        print("\n❌ Core LlamaIndex dependencies are missing.")
        print("Please install them with: pip install llama-index-core")
        return
    
    # Load configuration
    print("\n2. Loading configuration...")
    sources = load_sources_from_config(config_file)
    
    print(f"\n3. Sources to process:")
    for source_type, source_list in sources.items():
        print(f"   {source_type}: {len(source_list)} sources")
        for source in source_list[:3]:  # Show first 3 sources
            print(f"     - {source}")
        if len(source_list) > 3:
            print(f"     ... and {len(source_list) - 3} more")
    
    # Import modules only if dependencies are available
    try:
        from political_analysis_init import config
        from political_document_ingestor import PoliticalDocumentIngestor
        print("\n✅ Using full system configuration")
        
        # Initialize ingestor
        ingestor = PoliticalDocumentIngestor(config)
        
        # Run ingestion
        print("\n4. Running document ingestion...")
        documents = ingestor.batch_ingest(sources)
        
        if not documents:
            print("❌ No documents were ingested.")
            return
        
        print(f"✅ Successfully ingested {len(documents)} documents")
        
        # Save documents
        print("\n5. Saving documents...")
        output_dir = Path("./output/full_ingestion")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for i, doc in enumerate(documents):
            # Create a filename based on document ID or index
            safe_id = str(doc.doc_id).replace("/", "_").replace("\\", "_")[:50]
            filename = f"document_{i+1:03d}_{safe_id}.txt"
            filepath = output_dir / filename
            
            # Save document text and metadata
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Document ID: {doc.doc_id}\n")
                f.write(f"Metadata: {json.dumps(getattr(doc, 'metadata', {}), indent=2, default=str)}\n")
                f.write("-" * 50 + "\n")
                f.write(doc.text)
        
        print(f"✅ Saved {len(documents)} documents to {output_dir}")
        
        # Generate report
        print("\n6. Generating report...")
        report = {
            "total_documents": len(documents),
            "sources_processed": {k: len(v) for k, v in sources.items()},
            "document_stats": {
                "total_characters": sum(len(doc.text) for doc in documents),
                "avg_characters": sum(len(doc.text) for doc in documents) // len(documents) if documents else 0,
            }
        }
        
        report_file = output_dir / "ingestion_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✅ Report saved to {report_file}")
        
    except ImportError as e:
        print(f"\n⚠️  Could not import full system modules: {e}")
        print("Falling back to simple ingestion...")
        
        # Import only what we need
        from llama_index.core import SimpleDirectoryReader
        
        # Process only local directories
        local_docs = []
        for directory in sources.get("local_directories", []):
            try:
                reader = SimpleDirectoryReader(
                    input_dir=directory,
                    filename_as_id=True,
                    recursive=True
                )
                docs = reader.load_data()
                local_docs.extend(docs)
                print(f"✅ Loaded {len(docs)} documents from {directory}")
            except Exception as e:
                print(f"❌ Error loading from {directory}: {e}")
        
        if local_docs:
            # Save documents
            output_dir = Path("./output/simple_ingestion")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            for i, doc in enumerate(local_docs):
                filename = f"document_{i+1:03d}.txt"
                filepath = output_dir / filename
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"Document ID: {doc.doc_id}\n")
                    f.write(f"Metadata: {json.dumps(getattr(doc, 'metadata', {}), indent=2, default=str)}\n")
                    f.write("-" * 50 + "\n")
                    f.write(doc.text)
            
            print(f"✅ Saved {len(local_docs)} documents to {output_dir}")
        else:
            print("❌ No documents were processed.")
    
    print("\n" + "=" * 60)
    print("Full ingestion pipeline completed!")

def main():
    """Main function"""
    # Check if a config file was provided as command line argument
    config_file = None
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    
    # Run the pipeline
    asyncio.run(run_full_ingestion_pipeline(config_file))

if __name__ == "__main__":
    main()