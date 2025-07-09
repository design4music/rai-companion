"""
RAI Wrapper v2 - Minimal Input Processing
Real Artificial Intelligence Framework Implementation

Minimal wrapper that trusts LLM intelligence instead of mechanical keyword matching.
Focuses on basic input cleaning and lets analytical_engine.py do the smart work.
"""

import json
import logging
import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InputType(Enum):
    """Basic input types - let LLM handle nuance"""
    FACTUAL_CLAIM = "factual_claim"
    NARRATIVE = "narrative" 
    SYSTEM_PREMISE = "system_premise"
    QUESTION = "question"
    MIXED = "mixed"

@dataclass
class RAIInput:
    """Minimal input structure - trust LLM for the rest"""
    raw_input: str
    cleaned_input: str
    input_type: InputType
    style_flags: List[str]
    emotional_charge: int  # Basic 1-5 scale
    complexity_score: int  # Basic 1-5 scale
    detected_topics: List[str]  # Minimal topic hints
    suggested_premises: List[str]  # Let analytical_engine handle this

class RAIWrapper:
    """
    Minimal RAI Wrapper - Trust the LLM
    
    Philosophy: Do basic cleanup, provide minimal hints, 
    let analytical_engine.py and LLM do the smart work.
    """
    
    def __init__(self, config_path: str = "config.json"):
        """Initialize with minimal configuration"""
        self.config = self._load_config(config_path)
        logger.info("RAI Wrapper v2 initialized - trusting LLM intelligence")
    
    def _load_config(self, config_path: str) -> Dict:
        """Load basic configuration"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file not found, using defaults")
            return {"max_input_length": 10000}
    
    def process_input(self, user_input: str, 
                     output_mode: Optional[str] = None,
                     start_level: Optional[str] = None) -> Dict[str, Any]:
        """
        Minimal processing - clean input and create RAIInput object
        
        Args:
            user_input: Raw user input
            output_mode: Passed through (not used here)
            start_level: Passed through (not used here)
            
        Returns:
            Dict with RAIInput object for analytical_engine
        """
        try:
            # Basic validation
            if not user_input or len(user_input.strip()) < 5:
                return {"error": "Input too short"}
            
            max_length = self.config.get("max_input_length", 10000)
            if len(user_input) > max_length:
                return {"error": f"Input too long (max {max_length} chars)"}
            
            # Create minimal RAIInput
            rai_input = self._create_rai_input(user_input)
            
            return {
                "rai_input": rai_input,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Error processing input: {str(e)}")
            return {"error": str(e)}
    
    def _create_rai_input(self, raw_input: str) -> RAIInput:
        """Create RAIInput with minimal processing"""
        
        # Basic text cleanup
        cleaned = self._clean_input(raw_input)
        
        # Simple input type detection
        input_type = self._detect_input_type(cleaned)
        
        # Basic style flags
        style_flags = self._detect_basic_style(raw_input)
        
        # Simple metrics (let LLM handle sophistication)
        emotional_charge = self._basic_emotion_check(raw_input)
        complexity_score = self._basic_complexity_check(cleaned)
        
        # Minimal topic hints (very broad)
        detected_topics = self._detect_broad_topics(cleaned)
        
        return RAIInput(
            raw_input=raw_input,
            cleaned_input=cleaned,
            input_type=input_type,
            style_flags=style_flags,
            emotional_charge=emotional_charge,
            complexity_score=complexity_score,
            detected_topics=detected_topics,
            suggested_premises=[]  # Let analytical_engine handle this
        )
    
    def _clean_input(self, raw_input: str) -> str:
        """Basic input cleaning - preserve meaning"""
        
        # Remove excessive punctuation
        cleaned = re.sub(r'[!]{3,}', '!!', raw_input)
        cleaned = re.sub(r'[?]{3,}', '??', cleaned)
        
        # Normalize whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        # Remove very obvious noise (but keep meaningful punctuation)
        cleaned = re.sub(r'(.)\1{4,}', r'\1\1', cleaned)  # Limit repeated chars
        
        return cleaned
    
    def _detect_input_type(self, text: str) -> InputType:
        """Basic input type detection - let LLM handle nuance"""
        
        text_lower = text.lower()
        
        # Questions (obvious patterns)
        if '?' in text or text_lower.startswith(('what', 'why', 'how', 'when', 'where', 'who')):
            return InputType.QUESTION
        
        # Factual claims (has specific time/place markers)
        if re.search(r'\b(on|in|at|during)\s+\d{4}|\b(yesterday|today|recently|reported|confirmed)', text, re.IGNORECASE):
            return InputType.FACTUAL_CLAIM
        
        # System premises (broad power/system language)
        system_hints = ['system', 'power', 'control', 'government', 'elite', 'deep state']
        if any(hint in text_lower for hint in system_hints):
            return InputType.SYSTEM_PREMISE
        
        # Narrative (causal language)
        narrative_hints = ['because', 'therefore', 'led to', 'caused', 'story', 'resulted in']
        if any(hint in text_lower for hint in narrative_hints):
            return InputType.NARRATIVE
        
        # Default to mixed - let analytical_engine decide
        return InputType.MIXED
    
    def _detect_basic_style(self, text: str) -> List[str]:
        """Basic style detection - minimal flags"""
        flags = []
        
        # Emotional language
        if text.count('!') >= 2:
            flags.append("emotional")
        
        # Caps (shouting)
        if any(word.isupper() and len(word) > 3 for word in text.split()):
            flags.append("caps")
        
        # Quotes (sarcasm/mockery)
        if '"' in text or "so-called" in text.lower():
            flags.append("quotes")
        
        return flags
    
    def _basic_emotion_check(self, text: str) -> int:
        """Basic emotional charge (1-5 scale)"""
        
        charge = 1
        
        # Exclamation marks
        if text.count('!') >= 1:
            charge += 1
        if text.count('!') >= 3:
            charge += 1
        
        # Strong words (very basic list)
        strong_words = ['outrageous', 'disgusting', 'amazing', 'terrible', 'incredible', 'shocking']
        if any(word in text.lower() for word in strong_words):
            charge += 1
        
        # All caps words
        if any(word.isupper() and len(word) > 3 for word in text.split()):
            charge += 1
        
        return min(charge, 5)
    
    def _basic_complexity_check(self, text: str) -> int:
        """Basic complexity assessment (1-5 scale)"""
        
        complexity = 1
        
        # Length
        if len(text) > 100:
            complexity += 1
        if len(text) > 300:
            complexity += 1
        
        # Multiple sentences
        if text.count('.') > 1:
            complexity += 1
        
        # Technical terms (very basic check)
        technical_terms = ['geopolitical', 'systemic', 'institutional', 'asymmetric', 'strategic']
        if any(term in text.lower() for term in technical_terms):
            complexity += 1
        
        return min(complexity, 5)
    
    def _detect_broad_topics(self, text: str) -> List[str]:
        """Very broad topic detection - minimal hints for analytical_engine"""
        
        topics = []
        text_lower = text.lower()
        
        # Very broad categories
        if any(word in text_lower for word in ['war', 'military', 'conflict', 'geopolitical', 'international']):
            topics.append('geopolitical')
        
        if any(word in text_lower for word in ['media', 'news', 'information', 'propaganda', 'narrative']):
            topics.append('information')
        
        if any(word in text_lower for word in ['power', 'government', 'politics', 'election', 'control']):
            topics.append('power_governance')
        
        if any(word in text_lower for word in ['economy', 'economic', 'money', 'financial', 'market']):
            topics.append('economy')
        
        if any(word in text_lower for word in ['culture', 'identity', 'values', 'moral', 'ethics']):
            topics.append('cultural')
        
        return topics


# Example usage
if __name__ == "__main__":
    wrapper = RAIWrapper()
    
    # Test cases
    test_inputs = [
        "The media shows clear bias in political coverage",
        "Why did the conflict in Ukraine start?",
        "On March 15, 2024, reports confirmed civilian casualties",
        "The deep state controls government policy through bureaucrats",
        "NATO expansion led to Russian aggression because it threatened security"
    ]
    
    print("=== RAI WRAPPER V2 TESTING ===")
    
    for i, test_input in enumerate(test_inputs, 1):
        print(f"\n🧪 TEST {i}: {test_input}")
        
        result = wrapper.process_input(test_input)
        
        if "error" in result:
            print(f"   ❌ Error: {result['error']}")
        else:
            rai_input = result["rai_input"]
            print(f"   📊 Type: {rai_input.input_type.value}")
            print(f"   📈 Complexity: {rai_input.complexity_score}/5")
            print(f"   🎭 Emotion: {rai_input.emotional_charge}/5")
            print(f"   🏷️ Topics: {', '.join(rai_input.detected_topics) if rai_input.detected_topics else 'None'}")
            print(f"   🎨 Style: {', '.join(rai_input.style_flags) if rai_input.style_flags else 'None'}")
    
    print("\n✅ Testing complete - minimal processing, maximum LLM trust!")