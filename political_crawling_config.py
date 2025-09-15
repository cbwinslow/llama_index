"""
Web Crawling Configuration for Political Document Analysis System
Defines specific configurations for crawling political websites
"""

# Political websites to crawl
POLITICAL_WEBSITES = [
    # Government websites
    "https://www.congress.gov/",
    "https://www.whitehouse.gov/",
    "https://www.supremecourt.gov/",
    "https://www.loc.gov/",
    
    # Political news sources
    "https://www.reuters.com/politics/",
    "https://www.politico.com/",
    "https://www.cnn.com/politics/",
    "https://www.foxnews.com/politics",
    
    # Think tanks and policy organizations
    "https://www.brookings.edu/",
    "https://www.heritage.org/",
    "https://www.cato.org/",
    
    # Political party websites
    "https://www.democrats.org/",
    "https://www.gop.com/",
]

# RSS feeds for political news
POLITICAL_RSS_FEEDS = [
    "https://feeds.reuters.com/Reuters/PoliticsNews",
    "https://rss.cnn.com/rss/cnn_allpolitics.rss",
    "https://feeds.foxnews.com/foxnews/politics",
    "https://www.politico.com/rss/politics.xml",
    "https://www.washingtonpost.com/politics/feed/",
]

# Sitemaps for comprehensive crawling
POLITICAL_SITEMAPS = [
    "https://www.congress.gov/sitemap.xml",
    "https://www.whitehouse.gov/sitemap.xml",
]

# Configuration for web crawling
CRAWLING_CONFIG = {
    "max_depth": 3,
    "max_pages": 100,
    "respect_robots_txt": True,
    "delay_between_requests": 1.0,
    "user_agent": "PoliticalAnalysisBot/1.0",
    "allowed_domains": [
        "congress.gov",
        "whitehouse.gov",
        "supremecourt.gov",
        "loc.gov",
        "reuters.com",
        "politico.com",
        "cnn.com",
        "foxnews.com",
        "brookings.edu",
        "heritage.org",
        "cato.org",
        "democrats.org",
        "gop.com",
    ]
}

# Political entity extraction configuration
ENTITY_EXTRACTION_CONFIG = {
    "politicians": {
        "keywords": ["senator", "representative", "congressman", "congresswoman", "president", "governor", "mayor"],
        "exclusion_keywords": ["former", "ex-", "past"],
    },
    "legislation": {
        "patterns": [r"H.R.\s*\d+", r"S.\s*\d+", r"H.J.Res.\s*\d+", r"S.J.Res.\s*\d+"],
        "keywords": ["bill", "act", "resolution", "amendment"],
    },
    "political_parties": {
        "names": ["Democratic", "Republican", "Libertarian", "Green", "Independent"],
        "abbreviations": ["Dem", "GOP", "Lib", "Grn"],
    },
    "policies": {
        "keywords": [
            "healthcare", "education", "tax", "defense", "security", 
            "climate", "environment", "immigration", "trade"
        ],
    }
}

# Knowledge graph relationship types
RELATIONSHIP_TYPES = [
    "SPONSORS",           # Politician sponsors legislation
    "SUPPORTS",           # Politician/party supports policy
    "OPPOSES",            # Politician/party opposes policy
    "MEMBER_OF",          # Politician is member of party
    "VOTES_FOR",          # Politician votes for legislation
    "VOTES_AGAINST",      # Politician votes against legislation
    "ATTENDS",            # Politician attends event
    "MENTIONS",           # Document mentions entity
    "RELATED_TO",         # General relationship
    "PART_OF",            # Entity is part of larger entity
]

# Analysis categories
POLITICAL_CATEGORIES = [
    "Domestic Policy",
    "Foreign Policy",
    "Economic Policy",
    "Social Policy",
    "Environmental Policy",
    "Healthcare Policy",
    "Education Policy",
    "Defense Policy",
    "Immigration Policy",
    "Tax Policy",
]

if __name__ == "__main__":
    print("Political Web Crawling Configuration")
    print("=" * 35)
    print(f"Websites to crawl: {len(POLITICAL_WEBSITES)}")
    print(f"RSS feeds: {len(POLITICAL_RSS_FEEDS)}")
    print(f"Sitemaps: {len(POLITICAL_SITEMAPS)}")
    print(f"Allowed domains: {len(CRAWLING_CONFIG['allowed_domains'])}")
    print(f"Entity types: {len(ENTITY_EXTRACTION_CONFIG)}")
    print(f"Relationship types: {len(RELATIONSHIP_TYPES)}")