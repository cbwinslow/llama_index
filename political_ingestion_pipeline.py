#!/usr/bin/env python3
"""
Comprehensive Ingestion Script for Political Document Analysis System
This script provides a full-featured ingestion pipeline for political documents.
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

from political_analysis_init import config
from political_document_ingestor import PoliticalDocumentIngestor
from political_entity_extractor import PoliticalEntityExtractor
from political_analysis_agent import PoliticalAnalysisAgent

class PoliticalDocumentIngestionPipeline:
    \"\"\"A comprehensive pipeline for ingesting political documents\"\"\"
    
    def __init__(self):
        self.config = config
        self.ingestor = PoliticalDocumentIngestor(config)
        self.extractor = PoliticalEntityExtractor(config)
        self.agent = PoliticalAnalysisAgent(config)
        
    def load_sources_from_config(self, config_file: str = None) -> Dict[str, Any]:
        \"\"\"
        Load sources from a configuration file or use defaults
        
        Args:
            config_file: Path to JSON configuration file
            
        Returns:
            Dictionary of sources
        \"\"\"
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
        else:
            # Return default sources
            return {
                "local_directories": ["./data/sample_docs"],
                "websites": [
                    # Uncomment to enable (requires internet)
                    # "https://www.congress.gov/",
                    # "https://www.whitehouse.gov/briefing-room/",
                ],
                "rss_feeds": [
                    # Uncomment to enable (requires internet)
                    # "https://feeds.reuters.com/Reuters/PoliticsNews",
                    # "https://rss.cnn.com/rss/cnn_allpolitics.rss",
                ],
                "sitemaps": [
                    # Uncomment to enable (requires internet)
                    # "https://www.congress.gov/sitemap.xml",
                ]
            }
    
    async def run_ingestion(self, sources: Dict[str, Any] = None, 
                          extract_entities: bool = False,
                          save_output: bool = True) -> List[Any]:
        \"\"\"
        Run the complete ingestion pipeline
        
        Args:
            sources: Dictionary of sources to ingest from
            extract_entities: Whether to extract entities from documents
            save_output: Whether to save documents to output directory
            
        Returns:
            List of ingested documents
        \"\"\"
        print("Political Document Ingestion Pipeline")
        print("=" * 40)
        
        # Use provided sources or load from config
        if sources is None:
            sources = self.load_sources_from_config()
        
        print(f"\n1. Ingesting documents from {len(sources)} source types:")
        for source_type, source_list in sources.items():
            print(f"   {source_type}: {len(source_list)} sources")
        
        # Run ingestion
        print("\n2. Running document ingestion...")
        documents = self.ingestor.batch_ingest(sources)
        
        if not documents:
            print("❌ No documents were ingested.")
            return []
        
        print(f"✅ Successfully ingested {len(documents)} documents")
        
        # Extract entities if requested
        if extract_entities:
            print("\n3. Extracting entities from documents...")
            try:
                agent_initialized = await self.agent.initialize_agent()
                if agent_initialized:
                    entities = self.extractor.extract_political_entities(documents)
                    print("✅ Entity extraction completed")
                    print("Entities summary:")
                    for entity_type, entity_list in entities.items():
                        print(f"  {entity_type}: {len(entity_list)} items")
                else:
                    print("⚠️  Agent initialization failed")
            except Exception as e:
                print(f"⚠️  Entity extraction failed: {str(e)}")
        
        # Save output if requested
        if save_output:
            print("\n4. Saving documents to output directory...")
            await self.save_documents(documents)
        
        # Generate ingestion report
        print("\n5. Generating ingestion report...")
        report = self.generate_report(documents, sources)
        
        if save_output:
            await self.save_report(report)
        
        print("\n" + "=" * 40)
        print("Ingestion pipeline completed successfully!")
        
        return documents
    
    async def save_documents(self, documents: List[Any]):
        \"\"\"Save documents to output directory\"\"\"
        output_dir = Path("./output/ingested_documents")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for i, doc in enumerate(documents):
            # Create a filename based on document ID or index
            safe_id = str(doc.doc_id).replace("/", "_").replace("\\\\", "_")[:50]
            filename = f"document_{i+1:03d}_{safe_id}.txt"
            filepath = output_dir / filename
            
            # Save document text and metadata
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Document ID: {doc.doc_id}\n")
                f.write(f"Metadata: {json.dumps(doc.metadata, indent=2, default=str)}\n")
                f.write("-" * 50 + "\n")
                f.write(doc.text)
        
        print(f"✅ Saved {len(documents)} documents to {output_dir}")
    
    def generate_report(self, documents: List[Any], sources: Dict[str, Any]) -> Dict[str, Any]:
        \"\"\"Generate a report of the ingestion process\"\"\"
        report = {
            "total_documents": len(documents),
            "sources_processed": sources,
            "document_stats": {
                "total_characters": sum(len(doc.text) for doc in documents),
                "avg_characters": sum(len(doc.text) for doc in documents) // len(documents) if documents else 0,
                "max_characters": max(len(doc.text) for doc in documents) if documents else 0,
                "min_characters": min(len(doc.text) for doc in documents) if documents else 0,
            },
            "documents": [
                {
                    "id": doc.doc_id,
                    "text_length": len(doc.text),
                    "metadata_keys": list(doc.metadata.keys()) if hasattr(doc, 'metadata') else []
                }
                for doc in documents[:10]  # Only include first 10 for brevity
            ]
        }
        return report
    
    async def save_report(self, report: Dict[str, Any]):
        \"\"\"Save the ingestion report to a file\"\"\"
        output_dir = Path("./output/reports")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        report_file = output_dir / "ingestion_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"✅ Ingestion report saved to {report_file}")
        
        # Also save a human-readable version
        report_text_file = output_dir / "ingestion_report.txt"
        with open(report_text_file, 'w') as f:
            f.write("Political Document Ingestion Report\n")
            f.write("=" * 35 + "\n\n")
            f.write(f"Total Documents Ingested: {report['total_documents']}\n")
            f.write(f"Total Characters: {report['document_stats']['total_characters']:,}\n")
            f.write(f"Average Document Length: {report['document_stats']['avg_characters']:,} characters\n\n")
            f.write("Sources Processed:\n")
            for source_type, sources in report['sources_processed'].items():
                f.write(f"  {source_type}: {len(sources)} sources\n")
            f.write("\nFirst 10 Documents:\n")
            for doc in report['documents']:
                f.write(f"  ID: {doc['id']}\n")
                f.write(f"  Length: {doc['text_length']:,} characters\n")
                f.write(f"  Metadata: {', '.join(doc['metadata_keys'])}\n\n")
        
        print(f"✅ Human-readable report saved to {report_text_file}")

async def main():
    \"\"\"Main function to run the ingestion pipeline\"\"\"
    # Create pipeline instance
    pipeline = PoliticalDocumentIngestionPipeline()
    
    # Define sources (you can modify this or load from a config file)
    sources = {
        "local_directories": ["./data/sample_docs"],
        # Uncomment the following lines to enable web sources (requires internet)
        # "websites": [
        #     "https://www.congress.gov/",
        # ],
        # "rss_feeds": [
        #     "https://feeds.reuters.com/Reuters/PoliticsNews",
        # ],
    }
    
    # Run the ingestion pipeline
    documents = await pipeline.run_ingestion(
        sources=sources,
        extract_entities=False,  # Set to True if you have API keys configured
        save_output=True
    )
    
    print(f"\nIngestion completed. Processed {len(documents)} documents.")

if __name__ == "__main__":
    asyncio.run(main())