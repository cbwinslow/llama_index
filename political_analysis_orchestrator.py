"""
Main Orchestration Script for Political Document Analysis System
Coordinates all components of the political analysis pipeline
"""

import asyncio
import logging
from pathlib import Path
from typing import List, Dict, Any
from llama_index.core import Document

# Import our modules
from political_analysis_init import config
from political_document_ingestor import PoliticalDocumentIngestor
from political_entity_extractor import PoliticalEntityExtractor
from political_knowledge_graph import PoliticalKnowledgeGraph
from political_mcp_integration import PoliticalMCPIntegration
from political_analysis_agent import PoliticalAnalysisAgent

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PoliticalAnalysisOrchestrator:
    """Main orchestrator for the political document analysis system"""
    
    def __init__(self):
        self.config = config
        self.ingestor = PoliticalDocumentIngestor(config)
        self.extractor = PoliticalEntityExtractor(config)
        self.kg = PoliticalKnowledgeGraph(config)
        self.mcp = PoliticalMCPIntegration(config)
        self.agent = PoliticalAnalysisAgent(config)
        
    async def run_complete_analysis(self, sources: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run a complete political document analysis pipeline
        
        Args:
            sources: Dictionary of data sources to analyze
            
        Returns:
            Dictionary with complete analysis results
        """
        logger.info("Starting complete political document analysis pipeline")
        
        try:
            # Step 1: Ingest documents
            logger.info("Step 1: Ingesting documents")
            documents = self.ingestor.batch_ingest(sources)
            
            if not documents:
                logger.warning("No documents ingested, aborting analysis")
                return {"error": "No documents ingested"}
            
            # Step 2: Extract entities
            logger.info("Step 2: Extracting political entities")
            entities = self.extractor.extract_political_entities(documents)
            
            # Step 3: Build knowledge graph
            logger.info("Step 3: Building knowledge graph")
            kg_results = self.kg.build_from_documents(documents)
            
            # Step 4: Initialize agent
            logger.info("Step 4: Initializing analysis agent")
            agent_initialized = await self.agent.initialize_agent()
            
            if not agent_initialized:
                logger.warning("Agent initialization failed, continuing with basic analysis")
            
            # Step 5: Perform comprehensive analysis
            logger.info("Step 5: Performing comprehensive analysis")
            analysis_results = await self.agent.analyze_documents(documents)
            
            # Step 6: Connect to MCP servers
            logger.info("Step 6: Connecting to specialized political tools")
            mcp_tools = await self.mcp.connect_to_political_mcp_servers()
            
            # Compile final results
            results = {
                "document_count": len(documents),
                "entities": entities,
                "knowledge_graph": kg_results,
                "analysis": analysis_results,
                "mcp_tools": {name: len(tools) for name, tools in mcp_tools.items()},
                "status": "completed"
            }
            
            logger.info("Complete political document analysis pipeline finished successfully")
            return results
            
        except Exception as e:
            logger.error(f"Error in complete analysis pipeline: {str(e)}")
            return {"error": str(e), "status": "failed"}
    
    async def run_targeted_analysis(self, question: str, context_sources: Dict[str, Any] = None) -> str:
        """
        Run a targeted analysis to answer a specific political question
        
        Args:
            question: Specific question to answer
            context_sources: Optional sources for context
            
        Returns:
            Answer to the question
        """
        logger.info(f"Running targeted analysis for question: {question}")
        
        try:
            # If context sources provided, ingest them first
            context_documents = []
            if context_sources:
                context_documents = self.ingestor.batch_ingest(context_sources)
            
            # Initialize agent if not already done
            if not self.agent.agent:
                await self.agent.initialize_agent()
            
            # Answer the question
            answer = await self.agent.answer_question(question, str(context_documents[:2]))
            
            logger.info("Targeted analysis completed")
            return answer
            
        except Exception as e:
            logger.error(f"Error in targeted analysis: {str(e)}")
            return f"Error: {str(e)}"
    
    def save_results(self, results: Dict[str, Any], output_path: str = None) -> bool:
        """
        Save analysis results to file
        
        Args:
            results: Analysis results to save
            output_path: Path to save results (optional)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            import json
            from datetime import datetime
            
            # Generate output path if not provided
            if not output_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"./output/political_analysis_{timestamp}.json"
            
            # Ensure output directory exists
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Save results
            with open(output_path, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            logger.info(f"Results saved to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving results: {str(e)}")
            return False

# Example usage and demonstration
async def main():
    """Main function to demonstrate the political analysis system"""
    
    # Initialize orchestrator
    orchestrator = PoliticalAnalysisOrchestrator()
    
    # Example sources for political documents
    sources = {
        "local_directories": ["./data/sample_docs"],
        "websites": [
            "https://www.congress.gov/",  # Example government website
        ],
        "rss_feeds": [
            "https://feeds.reuters.com/Reuters/PoliticsNews",
        ]
    }
    
    # Run complete analysis
    print("Running complete political document analysis...")
    results = await orchestrator.run_complete_analysis(sources)
    
    # Save results
    orchestrator.save_results(results)
    
    # Example targeted question
    question = "What are the key policy positions of the current administration on climate change?"
    print(f"\nAnswering targeted question: {question}")
    answer = await orchestrator.run_targeted_analysis(question)
    print(f"Answer: {answer}")
    
    print("\nPolitical Document Analysis System demonstration completed!")

# Command-line interface
if __name__ == "__main__":
    print("Political Document Analysis System")
    print("=" * 40)
    
    # Run the demonstration
    asyncio.run(main())