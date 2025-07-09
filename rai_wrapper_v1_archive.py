"""
RAI Wrapper - Core Logic Layer
Real Artificial Intelligence Framework Implementation

This module wraps user input in the RAI module structure and orchestrates
the analysis flow (Fact-Level → Narrative-Level → System-Level).
"""

import json
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OutputMode(Enum):
    """Output modes for RAI analysis"""
    BRIEF = "brief"           # Summary at each level
    ANALYTICAL = "analytical" # Detailed output from all modules
    SYNTHESIS = "synthesis"   # Final synthesis only

class StartLevel(Enum):
    """Starting analysis levels"""
    FACT = "fact"
    NARRATIVE = "narrative"
    SYSTEM = "system"
    AUTO = "auto"

class InputType(Enum):
    """Types of user input"""
    FACTUAL_CLAIM = "factual_claim"
    NARRATIVE = "narrative"
    SYSTEM_PREMISE = "system_premise"
    MIXED = "mixed"
    QUESTION = "question"

@dataclass
class RAIInput:
    """Structured representation of user input"""
    raw_input: str
    cleaned_input: str
    input_type: InputType
    style_flags: List[str]
    emotional_charge: int  # 1-5 scale
    complexity_score: int  # 1-5 scale
    detected_topics: List[str]
    suggested_premises: List[str]

@dataclass
class RAIConfig:
    """Configuration for RAI analysis"""
    output_mode: OutputMode
    start_level: StartLevel
    include_premises: bool
    max_modules: int
    wisdom_overlay: bool
    
class RAIWrapper:
    """
    Main RAI Framework Wrapper
    
    Processes user input through the RAI module structure:
    1. Input normalization and classification
    2. Premise selection and injection
    3. Module selection and sequencing
    4. Prompt construction for LLM
    """
    
    def __init__(self, config_path: str = "config.json"):
        """Initialize RAI Wrapper with configuration"""
        self.config = self._load_config(config_path)
        self.premise_keywords = self._load_premise_keywords()
        self.toxic_labels = [
            "conspiracy theory", "misinformation", "disinformation",
            "populist", "far-right", "far-left", "extremist",
            "authoritarian regime", "propaganda", "fake news"
        ]
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file {config_path} not found, using defaults")
            return self._default_config()
    
    def _default_config(self) -> Dict:
        """Default configuration"""
        return {
            "default_output_mode": "brief",
            "default_start_level": "auto",
            "max_modules_per_level": 7,
            "enable_wisdom_overlay": True,
            "premise_threshold": 3,
            "llm_configs": {
                "openai": {"model": "gpt-4", "max_tokens": 4000},
                "deepseek": {"model": "deepseek-chat", "max_tokens": 4000}
            }
        }
    
    def _load_premise_keywords(self) -> Dict[str, List[str]]:
        """Load keyword mappings for premise selection"""
        return {
            "power_governance": [
                "election", "democracy", "government", "power", "politics",
                "legitimacy", "authority", "regime", "transition"
            ],
            "geopolitical": [
                "war", "conflict", "military", "sanctions", "alliance",
                "geopolitics", "international", "nuclear", "deterrence"
            ],
            "information": [
                "media", "propaganda", "censorship", "information",
                "narrative", "news", "platform", "algorithm"
            ],
            "civilization": [
                "culture", "identity", "memory", "trauma", "history",
                "civilization", "values", "heritage", "legacy"
            ],
            "systems": [
                "complexity", "feedback", "system", "control", "stability",
                "fragility", "resilience", "transparency"
            ],
            "ethics": [
                "moral", "ethics", "justice", "values", "virtue",
                "rights", "good", "evil", "responsibility"
            ],
            "temporal": [
                "history", "future", "time", "cycles", "evolution",
                "change", "development", "progress", "decline"
            ],
            "economy": [
                "economic", "money", "capital", "wealth", "class",
                "labor", "debt", "resources", "trade", "market"
            ]
        }
    
    def process_input(self, user_input: str, 
                     output_mode: Optional[str] = None,
                     start_level: Optional[str] = None) -> Dict[str, Any]:
        """
        Main processing function
        
        Args:
            user_input: Raw user input
            output_mode: Override default output mode
            start_level: Override default start level
            
        Returns:
            Dict containing processed input and analysis structure
        """
        try:
            # Step 1: Normalize and classify input
            rai_input = self._normalize_input(user_input)
            
            # Step 2: Configure analysis parameters
            config = self._build_analysis_config(
                rai_input, output_mode, start_level
            )
            
            # Step 3: Select relevant premises
            premises = self._suggest_premises(rai_input.detected_topics)
            
            # Step 4: Determine module sequence
            modules = self._select_modules(rai_input, config)
            
            # Step 5: Build complete RAI prompt
            prompt = self._build_rai_prompt(rai_input, config, premises, modules)
            
            return {
                "rai_input": rai_input,
                "config": config,
                "premises": premises,
                "modules": modules,
                "prompt": prompt,
                "metadata": {
                    "processing_time": None,  # To be filled by dispatcher
                    "llm_used": None,
                    "token_count": len(prompt.split())
                }
            }
            
        except Exception as e:
            logger.error(f"Error processing input: {str(e)}")
            return {"error": str(e)}
    
    def _normalize_input(self, raw_input: str) -> RAIInput:
        """
        CL-0: Input Clarity and Narrative Normalization
        
        Cleans and classifies user input for analysis
        """
        # Clean and normalize
        cleaned = self._clean_input(raw_input)
        
        # Classify input type
        input_type = self._classify_input(cleaned)
        
        # Detect style flags
        style_flags = self._detect_style_flags(raw_input)
        
        # Measure emotional charge
        emotional_charge = self._measure_emotional_charge(raw_input)
        
        # Assess complexity
        complexity_score = self._assess_complexity(cleaned)
        
        # Detect topics
        topics = self._detect_topics(cleaned)
        
        # Suggest premises
        premises = self._suggest_premises(topics)
        
        return RAIInput(
            raw_input=raw_input,
            cleaned_input=cleaned,
            input_type=input_type,
            style_flags=style_flags,
            emotional_charge=emotional_charge,
            complexity_score=complexity_score,
            detected_topics=topics,
            suggested_premises=premises
        )
    
    def _clean_input(self, raw_input: str) -> str:
        """Clean input of noise while preserving meaning"""
        # Remove excessive punctuation
        cleaned = re.sub(r'[!]{2,}', '!', raw_input)
        cleaned = re.sub(r'[?]{2,}', '?', cleaned)
        
        # Normalize whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        # Flag but don't remove toxic labels (for FL-9 processing)
        return cleaned
    
    def _classify_input(self, input_text: str) -> InputType:
        """Classify the type of input"""
        # Check for questions
        if '?' in input_text or input_text.lower().startswith(('what', 'why', 'how', 'when', 'where', 'who')):
            return InputType.QUESTION
        
        # Check for factual claims (specific, time-bound)
        if re.search(r'\b(on|in|at|during)\s+\d{4}|\b(yesterday|today|recently)', input_text, re.IGNORECASE):
            return InputType.FACTUAL_CLAIM
        
        # Check for system-level premises
        system_keywords = ['system', 'power', 'control', 'government', 'elite', 'conspiracy']
        if any(keyword in input_text.lower() for keyword in system_keywords):
            return InputType.SYSTEM_PREMISE
        
        # Check for narrative indicators
        narrative_keywords = ['story', 'narrative', 'because', 'therefore', 'led to', 'caused']
        if any(keyword in input_text.lower() for keyword in narrative_keywords):
            return InputType.NARRATIVE
        
        return InputType.MIXED
    
    def _detect_style_flags(self, raw_input: str) -> List[str]:
        """Detect style characteristics"""
        flags = []
        
        # Slang detection
        slang_patterns = [r'\b(gonna|wanna|gotta|dunno)\b', r'\b\w+n\'t\b']
        if any(re.search(pattern, raw_input, re.IGNORECASE) for pattern in slang_patterns):
            flags.append("slang")
        
        # Hyperbole detection
        hyperbole_words = ['always', 'never', 'everyone', 'nobody', 'everything', 'nothing']
        if any(word in raw_input.lower() for word in hyperbole_words):
            flags.append("hyperbole")
        
        # Mockery detection
        if '"' in raw_input or "so-called" in raw_input.lower():
            flags.append("mockery")
        
        # Emotional language
        emotional_words = ['outrageous', 'disgusting', 'amazing', 'terrible', 'incredible']
        if any(word in raw_input.lower() for word in emotional_words):
            flags.append("emotional")
        
        return flags
    
    def _measure_emotional_charge(self, raw_input: str) -> int:
        """Measure emotional intensity (1-5 scale)"""
        charge = 1
        
        # Exclamation marks
        charge += min(raw_input.count('!'), 2)
        
        # Caps
        if raw_input.isupper():
            charge += 2
        elif any(word.isupper() for word in raw_input.split()):
            charge += 1
        
        # Strong emotional words
        strong_words = ['hate', 'love', 'disgust', 'outrage', 'fury', 'ecstasy']
        if any(word in raw_input.lower() for word in strong_words):
            charge += 1
        
        return min(charge, 5)
    
    def _assess_complexity(self, input_text: str) -> int:
        """Assess input complexity (1-5 scale)"""
        complexity = 1
        
        # Length factor
        if len(input_text) > 200:
            complexity += 1
        if len(input_text) > 500:
            complexity += 1
        
        # Multiple claims
        if input_text.count('.') > 2:
            complexity += 1
        
        # Technical terms
        technical_terms = ['geopolitical', 'systemic', 'institutional', 'asymmetric']
        if any(term in input_text.lower() for term in technical_terms):
            complexity += 1
        
        return min(complexity, 5)
    
    def _detect_topics(self, input_text: str) -> List[str]:
        """Detect relevant topic domains"""
        topics = []
        
        for domain, keywords in self.premise_keywords.items():
            if any(keyword in input_text.lower() for keyword in keywords):
                topics.append(domain)
        
        return topics
    
    def _suggest_premises(self, topics: List[str]) -> List[str]:
        """Suggest relevant macro premises based on topics"""
        premise_map = {
            "power_governance": ["D1.1", "D1.2", "D1.3"],
            "geopolitical": ["D2.1", "D2.2", "D2.3", "D2.4"],
            "information": ["D3.1", "D3.2", "D3.3"],
            "civilization": ["D4.1", "D4.2", "D4.3"],
            "systems": ["D5.1", "D5.2", "D5.3"],
            "ethics": ["D6.1", "D6.2", "D6.3"],
            "temporal": ["D7.1", "D7.2", "D7.3"],
            "economy": ["D8.1", "D8.2", "D8.3"]
        }
        
        premises = []
        for topic in topics:
            if topic in premise_map:
                premises.extend(premise_map[topic])
        
        return list(set(premises))  # Remove duplicates
    
    def _build_analysis_config(self, rai_input: RAIInput, 
                              output_mode: Optional[str],
                              start_level: Optional[str]) -> RAIConfig:
        """Build analysis configuration"""
        
        # Determine output mode
        if output_mode:
            mode = OutputMode(output_mode)
        else:
            mode = OutputMode(self.config.get("default_output_mode", "brief"))
        
        # Determine start level
        if start_level:
            level = StartLevel(start_level)
        else:
            level = self._auto_detect_start_level(rai_input)
        
        # Determine if wisdom overlay is needed
        wisdom_overlay = (
            len(rai_input.suggested_premises) >= self.config.get("premise_threshold", 3)
            or rai_input.complexity_score >= 4
        )
        
        return RAIConfig(
            output_mode=mode,
            start_level=level,
            include_premises=len(rai_input.suggested_premises) > 0,
            max_modules=self.config.get("max_modules_per_level", 7),
            wisdom_overlay=wisdom_overlay
        )
    
    def _auto_detect_start_level(self, rai_input: RAIInput) -> StartLevel:
        """Auto-detect appropriate starting level"""
        
        # System-level indicators
        system_indicators = [
            "power", "control", "system", "elite", "government",
            "geopolitical", "strategic", "institutional"
        ]
        
        # Narrative-level indicators  
        narrative_indicators = [
            "because", "therefore", "led to", "caused", "story",
            "narrative", "moral", "identity", "values"
        ]
        
        # Fact-level indicators
        fact_indicators = [
            "happened", "occurred", "reported", "confirmed",
            "evidence", "data", "statistics", "study"
        ]
        
        text = rai_input.cleaned_input.lower()
        
        system_score = sum(1 for indicator in system_indicators if indicator in text)
        narrative_score = sum(1 for indicator in narrative_indicators if indicator in text)
        fact_score = sum(1 for indicator in fact_indicators if indicator in text)
        
        if system_score >= narrative_score and system_score >= fact_score:
            return StartLevel.SYSTEM
        elif narrative_score >= fact_score:
            return StartLevel.NARRATIVE
        else:
            return StartLevel.FACT
    
    def _select_modules(self, rai_input: RAIInput, config: RAIConfig) -> Dict[str, List[str]]:
        """Select relevant modules for analysis"""
        
        modules = {
            "cross_level": ["CL-0"],  # Always include input normalization
            "fact_level": [],
            "narrative_level": [],
            "system_level": []
        }
        
        # Add modules based on input characteristics
        if rai_input.input_type == InputType.FACTUAL_CLAIM:
            modules["fact_level"].extend([
                "FL-1", "FL-2", "FL-3", "FL-8", "FL-9"
            ])
        
        if rai_input.input_type in [InputType.NARRATIVE, InputType.MIXED]:
            modules["narrative_level"].extend([
                "NL-1", "NL-2", "NL-3", "NL-4"
            ])
        
        if rai_input.input_type == InputType.SYSTEM_PREMISE or len(rai_input.suggested_premises) > 2:
            modules["system_level"].extend([
                "SL-1", "SL-2", "SL-3", "SL-4"
            ])
        
        # Add modules based on detected topics
        if "geopolitical" in rai_input.detected_topics:
            modules["system_level"].extend(["SL-1", "SL-7"])
        
        if "information" in rai_input.detected_topics:
            modules["fact_level"].extend(["FL-2", "FL-3"])
            modules["system_level"].extend(["SL-8"])
        
        # Remove duplicates and limit
        for level in modules:
            modules[level] = list(set(modules[level]))[:config.max_modules]
        
        return modules
    
    def _build_rai_prompt(self, rai_input: RAIInput, config: RAIConfig, 
                         premises: List[str], modules: Dict[str, List[str]]) -> str:
        """Build the complete RAI prompt for LLM"""
        
        prompt_parts = []
        
        # 1. Framework activation
        prompt_parts.append("""
You are operating under the **Real Artificial Intelligence (RAI) Framework**.
This framework ensures analysis meets high standards of **factual precision**, **narrative coherence**, and **systemic insight** — guided by philosophical adequacy over mechanical neutrality.
""")
        
        # 2. Output mode specification
        prompt_parts.append(f"""
**Output Mode:** {config.output_mode.value.title()}
**Starting Level:** {config.start_level.value.title()}
""")
        
        # 3. Premise injection (if applicable)
        if config.include_premises and premises:
            prompt_parts.append(f"""
**Relevant Macro Premises for this analysis:**
{', '.join(premises)}

These premises should guide your interpretive lens and deepen contextual judgment.
""")
        
        # 4. Input analysis summary
        prompt_parts.append(f"""
**Input Analysis:**
- Original Input: "{rai_input.raw_input}"
- Cleaned Input: "{rai_input.cleaned_input}"
- Input Type: {rai_input.input_type.value}
- Style Flags: {', '.join(rai_input.style_flags) if rai_input.style_flags else 'None'}
- Emotional Charge: {rai_input.emotional_charge}/5
- Complexity Score: {rai_input.complexity_score}/5
- Detected Topics: {', '.join(rai_input.detected_topics) if rai_input.detected_topics else 'None'}
""")
        
        # 5. Module execution instructions
        prompt_parts.append(f"""
**Execute the following RAI modules:**

Cross-Level Modules: {', '.join(modules['cross_level'])}
Fact-Level Modules: {', '.join(modules['fact_level']) if modules['fact_level'] else 'None'}
Narrative-Level Modules: {', '.join(modules['narrative_level']) if modules['narrative_level'] else 'None'}
System-Level Modules: {', '.join(modules['system_level']) if modules['system_level'] else 'None'}
""")
        
        # 6. Analysis instructions
        prompt_parts.append("""
**Analysis Instructions:**
1. Apply the specified modules systematically
2. Use the Macro Premises as interpretive lenses where relevant
3. Maintain epistemic humility - flag uncertainties and limitations
4. Prioritize adequacy over acceptability
5. Provide a structured output with clear reasoning at each level
6. Conclude with a Final Synthesis that integrates all insights

**Begin Analysis:**
""")
        
        return '\n'.join(prompt_parts)


# Example usage and testing
if __name__ == "__main__":
    # Initialize RAI Wrapper
    rai = RAIWrapper()
    
    # Test with sample input
    test_input = "The media is clearly biased against Trump and this proves the deep state is real!"
    
    result = rai.process_input(test_input)
    
    print("=== RAI PROCESSING RESULT ===")
    print(f"Input Type: {result['input'].input_type.value}")
    print(f"Style Flags: {result['input'].style_flags}")
    print(f"Emotional Charge: {result['input'].emotional_charge}/5")
    print(f"Detected Topics: {result['input'].detected_topics}")
    print(f"Suggested Premises: {result['premises']}")
    print(f"Start Level: {result['config'].start_level.value}")
    print(f"Selected Modules: {result['modules']}")
    print(f"\nPrompt Length: {len(result['prompt'])} characters")
    
    # Print first 500 characters of prompt
    print(f"\nPrompt Preview:\n{result['prompt'][:500]}...")
