"""
Document Ingestion Module for Political Document Analysis System
Handles loading and preprocessing of political documents from various sources
"""

import os
from pathlib import Path
from typing import List, Union, Dict, Any
from llama_index.core import SimpleDirectoryReader
from llama_index.readers.web import (
    SpiderWebReader,
    WholeSiteReader,
    RSSNewsReader,
    SitemapReader
)
import requests
from tqdm import tqdm
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PoliticalDocumentIngestor:
    """Handles ingestion of political documents from various sources"""
    
    def __init__(self, config):
        self.config = config
        self.supported_formats = config.SUPPORTED_FORMATS
        
    def load_local_documents(self, directory_path: Union[str, Path]) -> List[Dict[str, Any]]:
        """
        Load political documents from a local directory
        
        Args:
            directory_path: Path to directory containing documents
            
        Returns:
            List of document dictionaries with content and metadata
        """
        logger.info(f"Loading documents from {directory_path}")
        
        try:
            reader = SimpleDirectoryReader(
                input_dir=str(directory_path),
                filename_as_id=True,
                recursive=True,
                required_exts=[f".{ext}" for ext in self.supported_formats]
            )
            documents = reader.load_data()
            
            logger.info(f"Loaded {len(documents)} documents from {directory_path}")
            return documents
            
        except Exception as e:
            logger.error(f"Error loading documents from {directory_path}: {str(e)}")
            return []
    
    def crawl_website(self, base_url: str, max_depth: int = None) -> List[Dict[str, Any]]:
        """
        Crawl a political website to extract documents
        
        Args:
            base_url: Base URL of the website to crawl
            max_depth: Maximum depth to crawl (None for config default)
            
        Returns:
            List of document dictionaries with content and metadata
        """
        logger.info(f"Crawling website: {base_url}")
        
        try:
            max_depth = max_depth or self.config.MAX_CRAWL_DEPTH
            
            # Try different web readers based on the website
            reader = SpiderWebReader()
            documents = reader.load_data(
                url=base_url,
                depth=max_depth,
                max_pages=self.config.MAX_CRAWL_PAGES
            )
            
            logger.info(f"Crawled {len(documents)} pages from {base_url}")
            return documents
            
        except Exception as e:
            logger.error(f"Error crawling {base_url}: {str(e)}")
            return []
    
    def load_rss_feeds(self, rss_urls: List[str]) -> List[Dict[str, Any]]:
        """
        Load political news from RSS feeds
        
        Args:
            rss_urls: List of RSS feed URLs
            
        Returns:
            List of document dictionaries with content and metadata
        """
        logger.info(f"Loading RSS feeds from {len(rss_urls)} sources")
        
        try:
            reader = RSSNewsReader()
            documents = []
            
            for url in tqdm(rss_urls, desc="Processing RSS feeds"):
                try:
                    feed_docs = reader.load_data(url=url)
                    documents.extend(feed_docs)
                except Exception as e:
                    logger.warning(f"Error loading RSS feed {url}: {str(e)}")
                    continue
            
            logger.info(f"Loaded {len(documents)} articles from RSS feeds")
            return documents
            
        except Exception as e:
            logger.error(f"Error loading RSS feeds: {str(e)}")
            return []
    
    def load_sitemap(self, sitemap_url: str) -> List[Dict[str, Any]]:
        """
        Load documents from a website sitemap
        
        Args:
            sitemap_url: URL of the sitemap.xml file
            
        Returns:
            List of document dictionaries with content and metadata
        """
        logger.info(f"Loading documents from sitemap: {sitemap_url}")
        
        try:
            reader = SitemapReader()
            documents = reader.load_data(sitemap_url=sitemap_url)
            
            logger.info(f"Loaded {len(documents)} documents from sitemap")
            return documents
            
        except Exception as e:
            logger.error(f"Error loading sitemap {sitemap_url}: {str(e)}")
            return []
    
    def download_file(self, url: str, save_path: Union[str, Path]) -> bool:
        """
        Download a political document from a URL
        
        Args:
            url: URL of the document to download
            save_path: Path where to save the document
            
        Returns:
            True if successful, False otherwise
        """
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                f.write(response.content)
                
            logger.info(f"Downloaded {url} to {save_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error downloading {url}: {str(e)}")
            return False
    
    def batch_ingest(self, sources: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Ingest documents from multiple sources in batch
        
        Args:
            sources: Dictionary with source types and configurations
                {
                    "local_directories": ["/path/to/docs1", "/path/to/docs2"],
                    "websites": ["https://example.gov", "https://news.example.com"],
                    "rss_feeds": ["https://example.com/rss", "https://news.example.com/feed"],
                    "sitemaps": ["https://example.gov/sitemap.xml"]
                }
                
        Returns:
            List of all ingested documents
        """
        all_documents = []
        
        # Load local documents
        if "local_directories" in sources:
            for directory in sources["local_directories"]:
                documents = self.load_local_documents(directory)
                all_documents.extend(documents)
        
        # Crawl websites
        if "websites" in sources:
            for website in sources["websites"]:
                documents = self.crawl_website(website)
                all_documents.extend(documents)
        
        # Load RSS feeds
        if "rss_feeds" in sources:
            documents = self.load_rss_feeds(sources["rss_feeds"])
            all_documents.extend(documents)
        
        # Load sitemaps
        if "sitemaps" in sources:
            for sitemap in sources["sitemaps"]:
                documents = self.load_sitemap(sitemap)
                all_documents.extend(documents)
        
        logger.info(f"Batch ingestion completed. Total documents: {len(all_documents)}")
        return all_documents

# Example usage
if __name__ == "__main__":
    # Import configuration
    from political_analysis_init import config
    
    # Initialize ingestor
    ingestor = PoliticalDocumentIngestor(config)
    
    # Example sources for political documents
    sources = {
        "local_directories": ["./data/sample_docs"],
        "websites": [
            "https://www.congress.gov/",  # Example government website
            "https://www.whitehouse.gov/briefing-room/"  # Example political news source
        ],
        "rss_feeds": [
            "https://feeds.reuters.com/Reuters/PoliticsNews",
            "https://rss.cnn.com/rss/cnn_allpolitics.rss"
        ],
        "sitemaps": [
            "https://www.congress.gov/sitemap.xml"
        ]
    }
    
    # Perform batch ingestion
    documents = ingestor.batch_ingest(sources)
    print(f"Ingested {len(documents)} political documents")