"""
Entity Extraction Module for Political Document Analysis System
Handles extraction of political entities, relationships, and metadata
"""

from typing import List, Dict, Any, Union
from llama_index.core import Document
from llama_index.core.extractors import (
    EntityExtractor,
    TitleExtractor,
    KeywordExtractor,
    QuestionsAnsweredExtractor,
    SummaryExtractor
)
from llama_index.extractors.entity import EntityExtractor
from llama_index.llms.openai import OpenAI
from llama_index.core.node_parser import SentenceSplitter
import logging
from pydantic import BaseModel, Field
from typing import Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define Pydantic models for political entities
class Politician(BaseModel):
    """Model for politician entity"""
    name: str = Field(description="Full name of the politician")
    party: Optional[str] = Field(description="Political party affiliation")
    position: Optional[str] = Field(description="Current political position")
    district: Optional[str] = Field(description="Electoral district or region")
    biography: Optional[str] = Field(description="Brief biographical information")

class PoliticalParty(BaseModel):
    """Model for political party entity"""
    name: str = Field(description="Official name of the political party")
    abbreviation: Optional[str] = Field(description="Common abbreviation")
    ideology: Optional[str] = Field(description="Political ideology or platform")
    founded: Optional[str] = Field(description="Year founded")
    leader: Optional[str] = Field(description="Current party leader")

class Legislation(BaseModel):
    """Model for legislation entity"""
    title: str = Field(description="Official title of the legislation")
    bill_number: Optional[str] = Field(description="Bill number or identifier")
    sponsors: Optional[List[str]] = Field(description="List of sponsors")
    status: Optional[str] = Field(description="Current status (introduced, passed, etc.)")
    date_introduced: Optional[str] = Field(description="Date introduced")
    summary: Optional[str] = Field(description="Brief summary of the legislation")

class Policy(BaseModel):
    """Model for policy entity"""
    name: str = Field(description="Name of the policy")
    description: Optional[str] = Field(description="Description of the policy")
    proponents: Optional[List[str]] = Field(description="Key supporters")
    opponents: Optional[List[str]] = Field(description="Key opponents")
    related_legislation: Optional[List[str]] = Field(description="Related bills or laws")

class PoliticalEvent(BaseModel):
    """Model for political event entity"""
    name: str = Field(description="Name of the event")
    date: Optional[str] = Field(description="Date of the event")
    location: Optional[str] = Field(description="Location of the event")
    participants: Optional[List[str]] = Field(description="Key participants")
    significance: Optional[str] = Field(description="Political significance")

class PoliticalRelationship(BaseModel):
    """Model for relationships between political entities"""
    source: str = Field(description="Source entity")
    target: str = Field(description="Target entity")
    relationship_type: str = Field(description="Type of relationship")
    strength: Optional[float] = Field(description="Strength of relationship (0.0-1.0)")
    evidence: Optional[str] = Field(description="Evidence for this relationship")

class PoliticalEntityExtractor:
    """Extracts political entities and relationships from documents"""
    
    def __init__(self, config):
        self.config = config
        self.llm = OpenAI(
            model=config.LLM_MODEL_NAME,
            temperature=config.LLM_TEMPERATURE,
            max_tokens=config.LLM_MAX_TOKENS
        )
        
        # Initialize extractors
        self.entity_extractor = EntityExtractor(
            llm=self.llm,
            extraction_template="Extract political entities including politicians, political parties, legislation, policies, and political events. Include relationships between these entities."
        )
        
        # Initialize specialized extractors
        self.title_extractor = TitleExtractor(nodes=5)
        self.keyword_extractor = KeywordExtractor(keywords=10)
        self.qa_extractor = QuestionsAnsweredExtractor(questions=3)
        self.summary_extractor = SummaryExtractor(summaries=["prev", "self"])
        
        # Political entity types
        self.political_entity_types = config.POLITICAL_ENTITIES
        
    def extract_entities(self, documents: List[Document]) -> List[Dict[str, Any]]:
        """
        Extract political entities from documents
        
        Args:
            documents: List of LlamaIndex Documents
            
        Returns:
            List of extracted entities with metadata
        """
        logger.info(f"Extracting entities from {len(documents)} documents")
        
        all_entities = []
        
        # Process each document
        for i, doc in enumerate(documents):
            try:
                logger.info(f"Processing document {i+1}/{len(documents)}: {doc.doc_id}")
                
                # Extract basic entities
                entities = self.entity_extractor.extract(doc)
                all_entities.extend(entities)
                
                # Extract additional metadata
                title_metadata = self.title_extractor.extract(doc)
                keyword_metadata = self.keyword_extractor.extract(doc)
                qa_metadata = self.qa_extractor.extract(doc)
                summary_metadata = self.summary_extractor.extract(doc)
                
                # Combine all metadata
                combined_metadata = {
                    "titles": title_metadata,
                    "keywords": keyword_metadata,
                    "questions": qa_metadata,
                    "summaries": summary_metadata,
                    "entities": entities
                }
                
                # Add to document metadata
                doc.metadata.update(combined_metadata)
                
            except Exception as e:
                logger.warning(f"Error extracting entities from document {doc.doc_id}: {str(e)}")
                continue
        
        logger.info(f"Extracted {len(all_entities)} entities from {len(documents)} documents")
        return all_entities
    
    def extract_political_entities(self, documents: List[Document]) -> Dict[str, Any]:
        """
        Extract specialized political entities using Pydantic models
        
        Args:
            documents: List of LlamaIndex Documents
            
        Returns:
            Dictionary with categorized political entities
        """
        logger.info("Extracting specialized political entities")
        
        # Prepare extraction prompts for each entity type
        extraction_prompts = {
            "politicians": "Extract information about politicians mentioned in this text. Include their names, party affiliations, positions, and districts.",
            "parties": "Extract information about political parties mentioned in this text. Include party names, abbreviations, ideologies, and leaders.",
            "legislation": "Extract information about legislation mentioned in this text. Include bill titles, numbers, sponsors, status, and summaries.",
            "policies": "Extract information about policies mentioned in this text. Include policy names, descriptions, proponents, and opponents.",
            "events": "Extract information about political events mentioned in this text. Include event names, dates, locations, participants, and significance."
        }
        
        # Initialize results dictionary
        results = {
            "politicians": [],
            "parties": [],
            "legislation": [],
            "policies": [],
            "events": [],
            "relationships": []
        }
        
        # Process each document
        for i, doc in enumerate(documents):
            try:
                logger.info(f"Extracting political entities from document {i+1}/{len(documents)}")
                
                # Extract each entity type
                for entity_type, prompt in extraction_prompts.items():
                    try:
                        # Create extraction query
                        query = f"{prompt}\n\nText: {doc.text[:2000]}..."  # Limit text length
                        
                        # Get LLM response
                        response = self.llm.complete(query)
                        
                        # Parse response (in a real implementation, this would be more sophisticated)
                        # For now, we'll store the raw response
                        results[entity_type].append({
                            "document_id": doc.doc_id,
                            "extraction": response.text,
                            "confidence": 0.8  # Placeholder confidence score
                        })
                        
                    except Exception as e:
                        logger.warning(f"Error extracting {entity_type} from document {doc.doc_id}: {str(e)}")
                        continue
                        
            except Exception as e:
                logger.warning(f"Error processing document {doc.doc_id}: {str(e)}")
                continue
        
        logger.info(f"Political entity extraction completed")
        return results
    
    def extract_relationships(self, documents: List[Document]) -> List[PoliticalRelationship]:
        """
        Extract relationships between political entities
        
        Args:
            documents: List of LlamaIndex Documents
            
        Returns:
            List of PoliticalRelationship objects
        """
        logger.info("Extracting relationships between political entities")
        
        relationships = []
        
        # Relationship extraction prompt
        relationship_prompt = """
        Identify relationships between political entities in the following text. 
        Look for relationships such as:
        - X sponsors Y (politician sponsors legislation)
        - X supports Y (politician supports policy)
        - X opposes Y (politician opposes policy)
        - X is member of Y (politician belongs to party)
        - X votes for Y (politician votes on legislation)
        - X attends Y (politician attends event)
        
        For each relationship, provide:
        1. Source entity
        2. Target entity
        3. Relationship type
        4. Strength (0.0-1.0)
        5. Evidence from text
        
        Text: {text}
        """
        
        # Process each document
        for doc in documents:
            try:
                # Split document into chunks for better processing
                splitter = SentenceSplitter(chunk_size=2000, chunk_overlap=200)
                chunks = splitter.get_nodes_from_documents([doc])
                
                for chunk in chunks:
                    # Create relationship extraction query
                    query = relationship_prompt.format(text=chunk.text)
                    
                    # Get LLM response
                    response = self.llm.complete(query)
                    
                    # In a real implementation, we would parse the response
                    # and create PoliticalRelationship objects
                    # For now, we'll store the raw response
                    relationships.append({
                        "document_id": doc.doc_id,
                        "chunk_id": chunk.node_id,
                        "raw_response": response.text
                    })
                    
            except Exception as e:
                logger.warning(f"Error extracting relationships from document {doc.doc_id}: {str(e)}")
                continue
        
        logger.info(f"Extracted {len(relationships)} relationship candidates")
        return relationships

# Example usage
if __name__ == "__main__":
    # Import configuration
    from political_analysis_init import config
    
    # Initialize extractor
    extractor = PoliticalEntityExtractor(config)
    
    # Example usage would go here
    print("Political Entity Extractor initialized")