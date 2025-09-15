"""
Document processor for political documents in the LlamaIndex Political Document Manager.
"""
import re
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import json
from datetime import datetime

class DocumentProcessor:
    """Process and analyze political documents."""
    
    def __init__(self, config_manager=None):
        self.config_manager = config_manager
        self.political_keywords = {
            "healthcare": ["healthcare", "health", "medical", "insurance", "medicare", "medicaid"],
            "economy": ["economic", "economy", "financial", "budget", "tax", "fiscal", "gdp"],
            "environment": ["environmental", "climate", "green", "pollution", "carbon", "energy"],
            "education": ["education", "school", "university", "student", "teacher", "learning"],
            "defense": ["defense", "military", "security", "armed forces", "veteran"],
            "immigration": ["immigration", "immigrant", "border", "visa", "refugee", "asylum"],
            "justice": ["justice", "court", "law", "legal", "constitutional", "rights"],
            "infrastructure": ["infrastructure", "transportation", "roads", "bridges", "broadband"]
        }
        
    def process_document(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process a document and extract relevant information."""
        metadata = metadata or {}
        
        # Basic text processing
        processed_doc = {
            "content": content,
            "metadata": metadata,
            "processed_at": datetime.now().isoformat(),
            "word_count": len(content.split()),
            "character_count": len(content),
            "language": self._detect_language(content),
            "readability_score": self._calculate_readability(content)
        }
        
        # Political analysis
        processed_doc["political_analysis"] = self._analyze_political_content(content)
        
        # Extract entities and topics
        processed_doc["entities"] = self._extract_entities(content)
        processed_doc["topics"] = self._extract_topics(content)
        
        # Sentiment analysis
        processed_doc["sentiment"] = self._analyze_sentiment(content)
        
        # Document classification
        processed_doc["classification"] = self._classify_document(content)
        
        return processed_doc
    
    def process_batch(self, documents: List[Tuple[str, Optional[Dict[str, Any]]]]) -> List[Dict[str, Any]]:
        """Process multiple documents in batch."""
        results = []
        for content, metadata in documents:
            try:
                result = self.process_document(content, metadata)
                result["processing_status"] = "success"
                results.append(result)
            except Exception as e:
                results.append({
                    "content": content[:100] + "..." if len(content) > 100 else content,
                    "metadata": metadata,
                    "processing_status": "error",
                    "error": str(e),
                    "processed_at": datetime.now().isoformat()
                })
        
        return results
    
    def _analyze_political_content(self, content: str) -> Dict[str, Any]:
        """Analyze political content and extract key topics."""
        content_lower = content.lower()
        
        analysis = {}
        for area, keywords in self.political_keywords.items():
            mentions = sum(1 for kw in keywords if kw in content_lower)
            keyword_density = mentions / len(content.split()) if content.split() else 0
            
            analysis[area] = {
                "mentions": mentions,
                "keyword_density": round(keyword_density * 100, 2),
                "relevance": self._calculate_relevance(mentions, len(content.split()))
            }
        
        # Find primary topics (top 3 by mentions)
        sorted_topics = sorted(analysis.items(), key=lambda x: x[1]["mentions"], reverse=True)
        primary_topics = [topic for topic, data in sorted_topics[:3] if data["mentions"] > 0]
        
        return {
            "analysis_by_topic": analysis,
            "total_policy_mentions": sum(a["mentions"] for a in analysis.values()),
            "primary_topics": primary_topics,
            "political_score": self._calculate_political_score(analysis)
        }
    
    def _extract_entities(self, content: str) -> Dict[str, List[str]]:
        """Extract named entities from the document."""
        # Simple entity extraction using patterns
        entities = {
            "organizations": [],
            "people": [],
            "locations": [],
            "bills": [],
            "dates": []
        }
        
        # Extract organization patterns
        org_patterns = [
            r'\b[A-Z][a-z]+ (?:Department|Agency|Commission|Bureau|Office)\b',
            r'\b(?:House|Senate) (?:of Representatives)?\b',
            r'\bCongress\b',
            r'\bWhite House\b',
            r'\bSupreme Court\b'
        ]
        
        for pattern in org_patterns:
            matches = re.findall(pattern, content)
            entities["organizations"].extend(matches)
        
        # Extract bill patterns
        bill_patterns = [
            r'\b[A-Z]+\.?[A-Z]*\.? \d+\b',  # H.R. 1234, S. 567
            r'\b(?:Bill|Act) (?:No\. )?\d+\b'
        ]
        
        for pattern in bill_patterns:
            matches = re.findall(pattern, content)
            entities["bills"].extend(matches)
        
        # Extract dates
        date_patterns = [
            r'\b\d{1,2}\/\d{1,2}\/\d{4}\b',  # MM/DD/YYYY
            r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}\b'
        ]
        
        for pattern in date_patterns:
            matches = re.findall(pattern, content)
            entities["dates"].extend(matches)
        
        # Remove duplicates
        for key in entities:
            entities[key] = list(set(entities[key]))
        
        return entities
    
    def _extract_topics(self, content: str) -> List[str]:
        """Extract main topics from the document."""
        # Simple topic extraction using keyword frequency
        words = re.findall(r'\b[a-zA-Z]{4,}\b', content.lower())
        word_freq = {}
        
        # Common stop words to ignore
        stop_words = {
            "that", "this", "with", "from", "they", "them", "their", "there", "these", "those",
            "will", "would", "could", "should", "shall", "must", "have", "been", "were", "are",
            "the", "and", "or", "but", "not", "all", "any", "can", "had", "has", "was", "is",
            "for", "of", "to", "in", "on", "at", "by", "as", "be", "do", "so", "if", "no",
            "more", "such", "only", "other", "than", "then", "them", "well", "also"
        }
        
        for word in words:
            if word not in stop_words and len(word) > 3:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Get top topics by frequency
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        topics = [word for word, freq in sorted_words[:10] if freq > 1]
        
        return topics
    
    def _analyze_sentiment(self, content: str) -> Dict[str, Any]:
        """Simple sentiment analysis."""
        # Basic sentiment word lists
        positive_words = {
            "good", "great", "excellent", "positive", "beneficial", "improve", "progress",
            "success", "effective", "strong", "support", "help", "better", "opportunity"
        }
        
        negative_words = {
            "bad", "terrible", "negative", "harmful", "problem", "crisis", "fail", "failure",
            "weak", "oppose", "against", "worse", "threat", "danger", "concern", "issue"
        }
        
        words = re.findall(r'\b[a-zA-Z]+\b', content.lower())
        
        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)
        total_sentiment_words = positive_count + negative_count
        
        if total_sentiment_words == 0:
            sentiment_score = 0.0
            sentiment_label = "neutral"
        else:
            sentiment_score = (positive_count - negative_count) / total_sentiment_words
            if sentiment_score > 0.2:
                sentiment_label = "positive"
            elif sentiment_score < -0.2:
                sentiment_label = "negative"
            else:
                sentiment_label = "neutral"
        
        return {
            "score": round(sentiment_score, 3),
            "label": sentiment_label,
            "positive_words": positive_count,
            "negative_words": negative_count,
            "confidence": abs(sentiment_score)
        }
    
    def _classify_document(self, content: str) -> Dict[str, Any]:
        """Classify the document type."""
        content_lower = content.lower()
        
        # Document type indicators
        indicators = {
            "bill": ["bill", "act", "section", "subsection", "whereas", "be it enacted"],
            "speech": ["thank you", "my fellow", "today i", "we must", "colleagues"],
            "report": ["executive summary", "findings", "recommendations", "methodology"],
            "press_release": ["for immediate release", "contact:", "announces", "statement"],
            "policy": ["policy", "framework", "guidelines", "principles", "objectives"],
            "legislation": ["congress", "senate", "house", "amendment", "vote"]
        }
        
        scores = {}
        for doc_type, keywords in indicators.items():
            score = sum(1 for keyword in keywords if keyword in content_lower)
            scores[doc_type] = score
        
        # Determine primary classification
        if scores:
            primary_type = max(scores, key=scores.get)
            confidence = scores[primary_type] / len(content.split()) * 100
        else:
            primary_type = "general"
            confidence = 0.0
        
        return {
            "primary_type": primary_type,
            "confidence": round(confidence, 2),
            "type_scores": scores
        }
    
    def _calculate_relevance(self, mentions: int, total_words: int) -> str:
        """Calculate relevance level based on mentions and document length."""
        if total_words == 0:
            return "low"
        
        density = mentions / total_words
        if density > 0.01:  # More than 1% of words are relevant
            return "high"
        elif density > 0.005:  # More than 0.5% of words are relevant
            return "medium"
        else:
            return "low"
    
    def _calculate_political_score(self, analysis: Dict[str, Any]) -> float:
        """Calculate overall political relevance score."""
        total_mentions = sum(topic["mentions"] for topic in analysis.values())
        high_relevance_topics = sum(1 for topic in analysis.values() if topic["relevance"] == "high")
        
        # Score based on total mentions and high relevance topics
        base_score = min(total_mentions / 10, 1.0)  # Normalize to 0-1
        relevance_bonus = high_relevance_topics * 0.1
        
        return round(min(base_score + relevance_bonus, 1.0), 3)
    
    def _detect_language(self, content: str) -> str:
        """Simple language detection."""
        # For now, assume English. In production, use a proper language detection library
        return "en"
    
    def _calculate_readability(self, content: str) -> float:
        """Calculate readability score (simplified Flesch Reading Ease)."""
        sentences = content.count('.') + content.count('!') + content.count('?')
        words = len(content.split())
        syllables = self._count_syllables(content)
        
        if sentences == 0 or words == 0:
            return 0.0
        
        # Simplified Flesch Reading Ease formula
        score = 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)
        return round(max(0, min(100, score)), 1)
    
    def _count_syllables(self, content: str) -> int:
        """Estimate syllable count."""
        words = re.findall(r'\b[a-zA-Z]+\b', content.lower())
        total_syllables = 0
        
        for word in words:
            # Simple syllable counting - count vowel groups
            vowels = re.findall(r'[aeiouy]+', word)
            syllables = len(vowels)
            # At least one syllable per word
            total_syllables += max(1, syllables)
        
        return total_syllables