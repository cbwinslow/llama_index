"""
Political Analysis Agent Module for Political Document Analysis System
Handles intelligent analysis of political documents using LLMs and tools
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional, Union
from llama_index.core.agent import FunctionAgent
from llama_index.core.tools import BaseTool, ToolMetadata
from llama_index.llms.openai import OpenAI
from llama_index.core import Document
from political_entity_extractor import PoliticalEntityExtractor
from political_knowledge_graph import PoliticalKnowledgeGraph
from political_mcp_integration import PoliticalMCPIntegration

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PoliticalAnalysisAgent:
    """Intelligent agent for analyzing political documents and answering questions"""
    
    def __init__(self, config):
        self.config = config
        self.llm = OpenAI(
            model=config.LLM_MODEL_NAME,
            temperature=config.LLM_TEMPERATURE,
            max_tokens=config.LLM_MAX_TOKENS
        )
        
        # Initialize components
        self.entity_extractor = PoliticalEntityExtractor(config)
        self.knowledge_graph = PoliticalKnowledgeGraph(config)
        self.mcp_integration = PoliticalMCPIntegration(config)
        
        # Initialize agent
        self.agent = None
        self.tools = []
        
    async def initialize_agent(self) -> bool:
        """
        Initialize the political analysis agent with tools
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            logger.info("Initializing political analysis agent")
            
            # Load MCP tools
            mcp_tools = await self.mcp_integration.connect_to_political_mcp_servers()
            
            # Flatten all tools into a single list
            all_tools = []
            for tools in mcp_tools.values():
                all_tools.extend(tools)
            
            # Add custom tools
            custom_tools = self._create_custom_tools()
            all_tools.extend(custom_tools)
            
            self.tools = all_tools
            
            # Create agent
            self.agent = FunctionAgent(
                tools=all_tools,
                llm=self.llm,
                max_iterations=self.config.MAX_AGENT_ITERATIONS,
                system_prompt=self._get_system_prompt()
            )
            
            logger.info(f"Political analysis agent initialized with {len(all_tools)} tools")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing political analysis agent: {str(e)}")
            return False
    
    def _create_custom_tools(self) -> List[BaseTool]:
        """
        Create custom tools for political analysis
        
        Returns:
            List of custom tools
        """
        tools = []
        
        # Add knowledge graph query tool
        kg_tool = BaseTool(
            fn=self._query_knowledge_graph,
            metadata=ToolMetadata(
                name="query_political_knowledge_graph",
                description="Query the political knowledge graph for relationships between entities"
            )
        )
        tools.append(kg_tool)
        
        # Add entity extraction tool
        extract_tool = BaseTool(
            fn=self._extract_political_entities,
            metadata=ToolMetadata(
                name="extract_political_entities",
                description="Extract political entities (politicians, parties, legislation, etc.) from text"
            )
        )
        tools.append(extract_tool)
        
        # Add document analysis tool
        analyze_tool = BaseTool(
            fn=self._analyze_document,
            metadata=ToolMetadata(
                name="analyze_political_document",
                description="Perform comprehensive analysis of a political document"
            )
        )
        tools.append(analyze_tool)
        
        return tools
    
    def _get_system_prompt(self) -> str:
        """
        Get the system prompt for the political analysis agent
        
        Returns:
            System prompt string
        """
        return """
        You are an expert political analyst AI assistant. Your role is to analyze political documents,
        extract relevant information, and answer questions about political entities, relationships,
        and trends.
        
        You have access to specialized tools for:
        1. Extracting political entities (politicians, parties, legislation, policies)
        2. Querying a knowledge graph of political relationships
        3. Fact-checking political claims
        4. Tracking legislative progress
        5. Analyzing campaign finance data
        6. Reviewing voting records
        
        When analyzing documents:
        - Focus on key political entities and their relationships
        - Identify important policy positions and statements
        - Note any factual claims that should be verified
        - Highlight significant political events or developments
        - Summarize the main points clearly and concisely
        
        Always maintain objectivity and cite sources when possible.
        """
    
    async def analyze_documents(self, documents: List[Document]) -> Dict[str, Any]:
        """
        Analyze political documents and extract insights
        
        Args:
            documents: List of LlamaIndex Documents
            
        Returns:
            Dictionary with analysis results
        """
        logger.info(f"Analyzing {len(documents)} political documents")
        
        try:
            # Extract entities
            entities = self.entity_extractor.extract_political_entities(documents)
            
            # Build knowledge graph
            kg_results = self.knowledge_graph.build_from_documents(documents)
            
            # Perform sentiment analysis
            sentiment_results = self._analyze_sentiment(documents)
            
            # Identify key themes
            themes = self._identify_themes(documents)
            
            # Generate summary
            summary = await self._generate_summary(documents, entities, themes)
            
            results = {
                "entities": entities,
                "knowledge_graph": kg_results,
                "sentiment": sentiment_results,
                "themes": themes,
                "summary": summary,
                "document_count": len(documents)
            }
            
            logger.info("Document analysis completed")
            return results
            
        except Exception as e:
            logger.error(f"Error analyzing documents: {str(e)}")
            return {}
    
    def _query_knowledge_graph(self, query: str) -> List[Dict[str, Any]]:
        """
        Query the political knowledge graph (tool function)
        
        Args:
            query: Query string
            
        Returns:
            Query results
        """
        return self.knowledge_graph.query_graph(query)
    
    def _extract_political_entities(self, text: str) -> Dict[str, Any]:
        """
        Extract political entities from text (tool function)
        
        Args:
            text: Text to analyze
            
        Returns:
            Extracted entities
        """
        # Create a mock document for extraction
        from llama_index.core import Document
        doc = Document(text=text)
        
        return self.entity_extractor.extract_political_entities([doc])
    
    def _analyze_document(self, document_text: str) -> Dict[str, Any]:
        """
        Analyze a political document (tool function)
        
        Args:
            document_text: Text of the document to analyze
            
        Returns:
            Analysis results
        """
        # Create a mock document for analysis
        from llama_index.core import Document
        doc = Document(text=document_text)
        
        # Perform basic analysis
        entities = self.entity_extractor.extract_political_entities([doc])
        sentiment = self._analyze_sentiment([doc])
        themes = self._identify_themes([doc])
        
        return {
            "entities": entities,
            "sentiment": sentiment,
            "themes": themes
        }
    
    def _analyze_sentiment(self, documents: List[Document]) -> Dict[str, Any]:
        """
        Analyze sentiment in political documents
        
        Args:
            documents: List of documents
            
        Returns:
            Sentiment analysis results
        """
        # In a real implementation, this would use a sentiment analysis model
        # For now, we'll return mock results
        return {
            "overall_sentiment": "neutral",
            "positive_statements": 15,
            "negative_statements": 10,
            "neutral_statements": 25
        }
    
    def _identify_themes(self, documents: List[Document]) -> List[str]:
        """
        Identify key themes in political documents
        
        Args:
            documents: List of documents
            
        Returns:
            List of key themes
        """
        # In a real implementation, this would use topic modeling
        # For now, we'll return mock themes
        return [
            "Economic Policy",
            "Healthcare Reform",
            "National Security",
            "Climate Change",
            "Education"
        ]
    
    async def _generate_summary(self, documents: List[Document], entities: Dict[str, Any], themes: List[str]) -> str:
        """
        Generate a summary of political documents
        
        Args:
            documents: List of documents
            entities: Extracted entities
            themes: Key themes
            
        Returns:
            Summary text
        """
        # Combine document texts
        combined_text = "\n\n".join([doc.text[:500] for doc in documents[:3]])  # Limit length
        
        # Create summary prompt
        prompt = f"""
        Summarize the following political documents, focusing on:
        1. Key political entities mentioned
        2. Main themes and topics
        3. Important policy positions
        4. Significant developments or events
        
        Documents:
        {combined_text[:2000]}...
        
        Key Entities:
        {str(entities)[:500]}...
        
        Main Themes:
        {', '.join(themes)}
        
        Provide a concise, objective summary.
        """
        
        # Generate summary using LLM
        response = self.llm.complete(prompt)
        return response.text
    
    async def answer_question(self, question: str, context: Optional[str] = None) -> str:
        """
        Answer a political question using the agent
        
        Args:
            question: Question to answer
            context: Additional context (optional)
            
        Returns:
            Answer text
        """
        if not self.agent:
            await self.initialize_agent()
            
        try:
            logger.info(f"Answering question: {question}")
            
            # Format query with context if provided
            query = question
            if context:
                query = f"Context: {context}\n\nQuestion: {question}"
            
            # Use agent to answer
            response = await self.agent.arun(query)
            
            logger.info("Question answered successfully")
            return str(response)
            
        except Exception as e:
            logger.error(f"Error answering question: {str(e)}")
            return f"Error answering question: {str(e)}"

# Example usage
if __name__ == "__main__":
    # Import configuration
    from political_analysis_init import config
    
    # Initialize agent
    async def main():
        agent = PoliticalAnalysisAgent(config)
        initialized = await agent.initialize_agent()
        
        if initialized:
            print("Political Analysis Agent initialized successfully")
        else:
            print("Failed to initialize Political Analysis Agent")
    
    # Run async function
    asyncio.run(main())