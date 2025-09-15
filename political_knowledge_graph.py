"""
Knowledge Graph Module for Political Document Analysis System
Handles construction and querying of political knowledge graphs
"""

from typing import List, Dict, Any, Optional, Union
from neo4j import GraphDatabase
import logging
from political_entity_extractor import (
    Politician, PoliticalParty, Legislation, Policy, PoliticalEvent, PoliticalRelationship
)
from llama_index.core import Document
from llama_index.graph_stores.neo4j import Neo4jGraphStore
from llama_index.core.indices.property_graph import PropertyGraphIndex
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PoliticalKnowledgeGraph:
    """Manages political knowledge graph construction and querying"""
    
    def __init__(self, config):
        self.config = config
        self.llm = OpenAI(
            model=config.LLM_MODEL_NAME,
            temperature=config.LLM_TEMPERATURE
        )
        self.embed_model = OpenAIEmbedding(
            model=config.EMBEDDING_MODEL_NAME,
            dimensions=config.EMBEDDING_DIMENSIONS
        )
        
        # Initialize Neo4j connection
        try:
            self.graph_store = Neo4jGraphStore(
                username="neo4j",
                password=config.NEO4J_PASSWORD,
                url=config.NEO4J_URI,
                database="neo4j"
            )
            logger.info("Connected to Neo4j graph database")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {str(e)}")
            self.graph_store = None
    
    def create_entity_nodes(self, entities: Dict[str, Any]) -> int:
        """
        Create nodes in the knowledge graph for political entities
        
        Args:
            entities: Dictionary of extracted entities
            
        Returns:
            Number of nodes created
        """
        if not self.graph_store:
            logger.warning("No graph store available")
            return 0
            
        nodes_created = 0
        
        # Create politician nodes
        for politician_data in entities.get("politicians", []):
            try:
                # Parse politician data (simplified)
                name = politician_data.get("name", "Unknown")
                party = politician_data.get("party", "Unknown")
                position = politician_data.get("position", "Unknown")
                
                # Create node in Neo4j
                query = """
                MERGE (p:Politician {name: $name})
                SET p.party = $party, p.position = $position
                RETURN p
                """
                
                with self.graph_store.client.session() as session:
                    result = session.run(query, name=name, party=party, position=position)
                    nodes_created += 1
                    
            except Exception as e:
                logger.warning(f"Error creating politician node: {str(e)}")
                continue
        
        # Create party nodes
        for party_data in entities.get("parties", []):
            try:
                name = party_data.get("name", "Unknown")
                ideology = party_data.get("ideology", "Unknown")
                
                query = """
                MERGE (p:PoliticalParty {name: $name})
                SET p.ideology = $ideology
                RETURN p
                """
                
                with self.graph_store.client.session() as session:
                    result = session.run(query, name=name, ideology=ideology)
                    nodes_created += 1
                    
            except Exception as e:
                logger.warning(f"Error creating party node: {str(e)}")
                continue
        
        # Create legislation nodes
        for legislation_data in entities.get("legislation", []):
            try:
                title = legislation_data.get("title", "Unknown")
                status = legislation_data.get("status", "Unknown")
                
                query = """
                MERGE (l:Legislation {title: $title})
                SET l.status = $status
                RETURN l
                """
                
                with self.graph_store.client.session() as session:
                    result = session.run(query, title=title, status=status)
                    nodes_created += 1
                    
            except Exception as e:
                logger.warning(f"Error creating legislation node: {str(e)}")
                continue
        
        # Create policy nodes
        for policy_data in entities.get("policies", []):
            try:
                name = policy_data.get("name", "Unknown")
                description = policy_data.get("description", "Unknown")
                
                query = """
                MERGE (p:Policy {name: $name})
                SET p.description = $description
                RETURN p
                """
                
                with self.graph_store.client.session() as session:
                    result = session.run(query, name=name, description=description)
                    nodes_created += 1
                    
            except Exception as e:
                logger.warning(f"Error creating policy node: {str(e)}")
                continue
        
        logger.info(f"Created {nodes_created} entity nodes in knowledge graph")
        return nodes_created
    
    def create_relationships(self, relationships: List[Dict[str, Any]]) -> int:
        """
        Create relationships between entities in the knowledge graph
        
        Args:
            relationships: List of relationship data
            
        Returns:
            Number of relationships created
        """
        if not self.graph_store:
            logger.warning("No graph store available")
            return 0
            
        relationships_created = 0
        
        for rel_data in relationships:
            try:
                # Parse relationship data (simplified)
                source = rel_data.get("source", "Unknown")
                target = rel_data.get("target", "Unknown")
                rel_type = rel_data.get("relationship_type", "RELATED_TO")
                strength = rel_data.get("strength", 0.5)
                
                # Create relationship in Neo4j
                query = """
                MATCH (a), (b)
                WHERE a.name = $source AND b.name = $target
                MERGE (a)-[r:%s {strength: $strength}]->(b)
                RETURN r
                """ % rel_type.upper().replace(" ", "_")
                
                with self.graph_store.client.session() as session:
                    result = session.run(query, source=source, target=target, strength=strength)
                    relationships_created += 1
                    
            except Exception as e:
                logger.warning(f"Error creating relationship: {str(e)}")
                continue
        
        logger.info(f"Created {relationships_created} relationships in knowledge graph")
        return relationships_created
    
    def build_from_documents(self, documents: List[Document]) -> Dict[str, int]:
        """
        Build knowledge graph from documents
        
        Args:
            documents: List of LlamaIndex Documents
            
        Returns:
            Dictionary with counts of created nodes and relationships
        """
        logger.info(f"Building knowledge graph from {len(documents)} documents")
        
        # In a real implementation, this would:
        # 1. Extract entities from documents
        # 2. Extract relationships between entities
        # 3. Create nodes and relationships in the graph
        
        # For now, we'll return placeholder results
        results = {
            "nodes_created": 0,
            "relationships_created": 0
        }
        
        logger.info("Knowledge graph construction completed")
        return results
    
    def query_graph(self, query: str) -> List[Dict[str, Any]]:
        """
        Query the political knowledge graph
        
        Args:
            query: Natural language query about political entities/relationships
            
        Returns:
            List of query results
        """
        if not self.graph_store:
            logger.warning("No graph store available")
            return []
            
        try:
            # Convert natural language query to Cypher (simplified)
            cypher_query = self._nl_to_cypher(query)
            
            # Execute query
            with self.graph_store.client.session() as session:
                result = session.run(cypher_query)
                records = [dict(record) for record in result]
                
            logger.info(f"Query returned {len(records)} results")
            return records
            
        except Exception as e:
            logger.error(f"Error querying knowledge graph: {str(e)}")
            return []
    
    def _nl_to_cypher(self, query: str) -> str:
        """
        Convert natural language query to Cypher query (simplified)
        
        Args:
            query: Natural language query
            
        Returns:
            Cypher query string
        """
        # In a real implementation, this would use an LLM to convert
        # natural language to Cypher. For now, we'll return a placeholder.
        
        # Example conversion logic:
        if "politicians" in query.lower() and "party" in query.lower():
            return "MATCH (p:Politician)-[:MEMBER_OF]->(pp:PoliticalParty) RETURN p.name, pp.name"
        elif "legislation" in query.lower() and "sponsor" in query.lower():
            return "MATCH (p:Politician)-[:SPONSORS]->(l:Legislation) RETURN p.name, l.title"
        else:
            # Default query
            return "MATCH (n) RETURN n LIMIT 10"
    
    def get_entity_details(self, entity_name: str, entity_type: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific political entity
        
        Args:
            entity_name: Name of the entity
            entity_type: Type of entity (Politician, PoliticalParty, etc.)
            
        Returns:
            Dictionary with entity details
        """
        if not self.graph_store:
            logger.warning("No graph store available")
            return {}
            
        try:
            # Create query based on entity type
            if entity_type.lower() == "politician":
                query = """
                MATCH (p:Politician {name: $name})
                OPTIONAL MATCH (p)-[r]->(related)
                RETURN p, collect({type: type(r), target: related.name}) as relationships
                """
            elif entity_type.lower() == "politicalparty":
                query = """
                MATCH (pp:PoliticalParty {name: $name})
                OPTIONAL MATCH (p:Politician)-[:MEMBER_OF]->(pp)
                RETURN pp, collect(p.name) as members
                """
            else:
                query = """
                MATCH (n {%s: $name})
                RETURN n
                """ % entity_type.lower()
            
            with self.graph_store.client.session() as session:
                result = session.run(query, name=entity_name)
                record = result.single()
                
                if record:
                    return dict(record)
                else:
                    return {}
                    
        except Exception as e:
            logger.error(f"Error getting entity details: {str(e)}")
            return {}

# Example usage
if __name__ == "__main__":
    # Import configuration
    from political_analysis_init import config
    
    # Initialize knowledge graph
    kg = PoliticalKnowledgeGraph(config)
    
    # Example usage would go here
    print("Political Knowledge Graph initialized")