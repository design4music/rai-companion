"""
RAI Module Selector - Intelligent Analysis Module Selection
Real Artificial Intelligence Framework Implementation

This module analyzes input context and selects the most relevant RAI analysis modules
across all levels (CL, FL, NL, SL) based on input type, topic domain, complexity,
and strategic requirements.
"""

import json
import logging
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass
from enum import Enum
import re
from collections import defaultdict, Counter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModuleLevel(Enum):
    """RAI Framework levels"""
    CROSS_LEVEL = "CL"
    FACT_LEVEL = "FL" 
    NARRATIVE_LEVEL = "NL"
    SYSTEM_LEVEL = "SL"

class ModulePriority(Enum):
    """Module priority levels"""
    ESSENTIAL = "essential"    # Must include
    HIGH = "high"             # Very important
    MEDIUM = "medium"         # Context-dependent
    LOW = "low"               # Optional/supporting

@dataclass
class ModuleMatch:
    """Individual module matching result"""
    module_id: str
    priority: ModulePriority
    confidence: float  # 0-1 scale
    trigger_factors: List[str]
    dependency_modules: List[str]
    rationale: str

@dataclass 
class ModuleSelection:
    """Complete module selection result"""
    entry_point: ModuleLevel
    cross_level_modules: List[str]
    fact_level_modules: List[str]
    narrative_level_modules: List[str]
    system_level_modules: List[str]
    execution_order: List[str]
    total_modules: int
    selection_rationale: str

class ModuleSelector:
    """
    Intelligent Module Selection Engine
    
    Analyzes input characteristics and selects optimal RAI modules based on:
    1. Input type classification (factual claim, narrative, system premise, etc.)
    2. Topic domain analysis (geopolitical, information, cultural, etc.)
    3. Complexity and risk assessment
    4. Strategic significance detection
    5. Module dependencies and synergies
    """
    
    def __init__(self):
        """Initialize module selector with complete module library"""
        self.module_library = self._build_module_library()
        self.domain_patterns = self._build_domain_patterns()
        self.trigger_keywords = self._build_trigger_keywords()
        self.module_dependencies = self._build_dependencies()
        self.strategic_indicators = self._build_strategic_indicators()
        
    def _build_module_library(self) -> Dict:
        """Build comprehensive module library with metadata"""
        return {
            "CL": {
                "CL-0": {
                    "name": "Input Clarity and Narrative Normalization",
                    "purpose": "Pre-process user input to normalize vague, emotional, or broad claims",
                    "triggers": ["all_inputs"],
                    "priority": "essential",
                    "output_type": "cleaned_input",
                    "keywords": ["normalize", "clarify", "clean", "reframe"],
                    "contexts": ["preprocessing", "input_analysis"],
                    "dependencies": []
                },
                "CL-0.1": {
                    "name": "Wisdom Premise Calibration", 
                    "purpose": "Dynamically align analysis with relevant Macro Premises",
                    "triggers": ["geopolitical", "strategic", "complex", "ideological"],
                    "priority": "high",
                    "output_type": "premise_overlay",
                    "keywords": ["premises", "wisdom", "strategic", "geopolitical"],
                    "contexts": ["complex_analysis", "strategic_content"],
                    "dependencies": []
                },
                "CL-1": {
                    "name": "Narrative Logic Compression",
                    "purpose": "Trace how facts are linked into narrative arcs",
                    "triggers": ["narrative", "causal_claims", "logical_linkage"],
                    "priority": "medium",
                    "output_type": "narrative_analysis",
                    "keywords": ["compression", "linkage", "narrative", "facts"],
                    "contexts": ["narrative_analysis", "logical_coherence"],
                    "dependencies": ["CL-0"]
                },
                "CL-2": {
                    "name": "Epistemic Load Balance",
                    "purpose": "Test how knowledge burdens are distributed",
                    "triggers": ["assumptions", "burden_of_proof", "implicit_claims"],
                    "priority": "medium",
                    "output_type": "assumption_audit",
                    "keywords": ["assumptions", "burden", "proof", "implicit"],
                    "contexts": ["epistemic_analysis", "assumption_checking"],
                    "dependencies": ["CL-0"]
                },
                "CL-3": {
                    "name": "Narrative Stack Tracking",
                    "purpose": "Map layered or nested narratives",
                    "triggers": ["complex_narrative", "meta_narrative", "ideological"],
                    "priority": "medium",
                    "output_type": "narrative_layers",
                    "keywords": ["layers", "stack", "meta", "ideology"],
                    "contexts": ["complex_narrative", "ideological_analysis"],
                    "dependencies": ["CL-1"]
                },
                "CL-4": {
                    "name": "Moral and Strategic Fusion Detection",
                    "purpose": "Identify moral language fused with strategic logic",
                    "triggers": ["moral_strategic", "virtue_signaling", "geopolitical"],
                    "priority": "high",
                    "output_type": "fusion_detection",
                    "keywords": ["moral", "strategic", "virtue", "fusion"],
                    "contexts": ["moral_strategic", "geopolitical_analysis"],
                    "dependencies": ["CL-0"]
                },
                "CL-5": {
                    "name": "Evaluative Symmetry Enforcement",
                    "purpose": "Ensure consistent standards across different actors",
                    "triggers": ["double_standards", "bias", "asymmetric_judgment"],
                    "priority": "high",
                    "output_type": "symmetry_check",
                    "keywords": ["symmetry", "standards", "bias", "consistent"],
                    "contexts": ["bias_detection", "fairness_analysis"],
                    "dependencies": ["CL-0"]
                }
            },
            "FL": {
                "FL-1": {
                    "name": "Claim Clarity and Anchoring",
                    "purpose": "Isolate and verify core factual claims",
                    "triggers": ["factual_claim", "verification", "clarity"],
                    "priority": "essential",
                    "output_type": "verified_claims",
                    "keywords": ["claims", "facts", "verify", "anchor", "specific"],
                    "contexts": ["fact_checking", "claim_verification"],
                    "dependencies": ["CL-0"]
                },
                "FL-2": {
                    "name": "Asymmetrical Amplification Awareness",
                    "purpose": "Detect unnatural promotion or suppression of claims",
                    "triggers": ["media_bias", "amplification", "suppression"],
                    "priority": "high",
                    "output_type": "amplification_analysis",
                    "keywords": ["amplification", "suppression", "media", "promotion"],
                    "contexts": ["media_analysis", "information_warfare"],
                    "dependencies": ["FL-1"]
                },
                "FL-3": {
                    "name": "Source Independence Audit",
                    "purpose": "Evaluate source independence and reliability",
                    "triggers": ["source_analysis", "independence", "coordination"],
                    "priority": "high",
                    "output_type": "source_audit",
                    "keywords": ["sources", "independence", "reliability", "coordination"],
                    "contexts": ["source_verification", "coordination_detection"],
                    "dependencies": ["FL-1"]
                },
                "FL-4": {
                    "name": "Strategic Relevance and Selection",
                    "purpose": "Evaluate whether facts are strategically chosen",
                    "triggers": ["cherry_picking", "strategic_selection", "distraction"],
                    "priority": "medium",
                    "output_type": "relevance_analysis",
                    "keywords": ["strategic", "selection", "cherry", "relevance"],
                    "contexts": ["strategic_analysis", "manipulation_detection"],
                    "dependencies": ["FL-1"]
                },
                "FL-5": {
                    "name": "Scale and Proportion Calibration",
                    "purpose": "Prevent inflation or minimization through scale framing",
                    "triggers": ["scale_manipulation", "proportion", "framing"],
                    "priority": "medium",
                    "output_type": "scale_analysis",
                    "keywords": ["scale", "proportion", "framing", "calibration"],
                    "contexts": ["scale_analysis", "framing_detection"],
                    "dependencies": ["FL-1"]
                },
                "FL-6": {
                    "name": "Neglected Primary Speech Recognition",
                    "purpose": "Identify omitted or misrepresented primary statements",
                    "triggers": ["primary_sources", "speech_analysis", "omission"],
                    "priority": "medium",
                    "output_type": "speech_analysis",
                    "keywords": ["primary", "speech", "statements", "omission"],
                    "contexts": ["primary_source_analysis", "speech_verification"],
                    "dependencies": ["FL-3"]
                },
                "FL-7": {
                    "name": "Risk Context Adjustment", 
                    "purpose": "Tune skepticism based on stakes",
                    "triggers": ["high_stakes", "risk_assessment", "consequences"],
                    "priority": "high",
                    "output_type": "risk_assessment",
                    "keywords": ["risk", "stakes", "consequences", "skepticism"],
                    "contexts": ["risk_analysis", "high_stakes_content"],
                    "dependencies": ["FL-1"]
                },
                "FL-8": {
                    "name": "Time & Place Anchoring",
                    "purpose": "Ensure claims are tied to specific moments and locations",
                    "triggers": ["temporal_anchoring", "location_verification", "specificity"],
                    "priority": "essential",
                    "output_type": "temporal_analysis",
                    "keywords": ["time", "place", "anchor", "specific", "location"],
                    "contexts": ["temporal_verification", "location_analysis"],
                    "dependencies": ["FL-1"]
                },
                "FL-9": {
                    "name": "Toxic Label Audit",
                    "purpose": "Detect judgment-distorting labels",
                    "triggers": ["toxic_labels", "prejudgment", "disqualification"],
                    "priority": "high",
                    "output_type": "label_audit",
                    "keywords": ["labels", "toxic", "conspiracy", "populist", "regime"],
                    "contexts": ["label_detection", "prejudgment_analysis"],
                    "dependencies": ["CL-0"]
                }
            },
            "NL": {
                "NL-1": {
                    "name": "Cause-Effect Chain Analysis",
                    "purpose": "Evaluate cause-and-effect logic coherence",
                    "triggers": ["causal_claims", "causality", "chain_logic"],
                    "priority": "essential", 
                    "output_type": "causal_analysis",
                    "keywords": ["cause", "effect", "chain", "logic", "sequence"],
                    "contexts": ["causal_analysis", "logical_coherence"],
                    "dependencies": ["CL-1"]
                },
                "NL-2": {
                    "name": "Narrative Plausibility & Internal Coherence",
                    "purpose": "Test story's internal logic and plausibility",
                    "triggers": ["narrative_coherence", "plausibility", "internal_logic"],
                    "priority": "high",
                    "output_type": "coherence_analysis",
                    "keywords": ["plausibility", "coherence", "internal", "logic"],
                    "contexts": ["narrative_analysis", "coherence_checking"],
                    "dependencies": ["NL-1"]
                },
                "NL-3": {
                    "name": "Competing Narratives Contrast",
                    "purpose": "Surface alternative narratives and interpretations",
                    "triggers": ["alternative_narratives", "multiple_perspectives", "contrast"],
                    "priority": "high",
                    "output_type": "narrative_comparison",
                    "keywords": ["competing", "alternative", "contrast", "perspectives"],
                    "contexts": ["perspective_analysis", "narrative_comparison"],
                    "dependencies": ["NL-2"]
                },
                "NL-4": {
                    "name": "Identity, Memory, and Group Interest Framing",
                    "purpose": "Identify how group identities shape narrative preference",
                    "triggers": ["identity_politics", "group_interest", "memory", "trauma"],
                    "priority": "high",
                    "output_type": "identity_analysis",
                    "keywords": ["identity", "memory", "group", "trauma", "loyalty"],
                    "contexts": ["identity_analysis", "group_dynamics"],
                    "dependencies": ["NL-1"]
                },
                "NL-5": {
                    "name": "Allegory, Analogy, and Symbol Injection",
                    "purpose": "Flag metaphor and symbolism distorting clarity",
                    "triggers": ["metaphor", "analogy", "symbolism", "distortion"],
                    "priority": "medium",
                    "output_type": "symbolic_analysis",
                    "keywords": ["allegory", "analogy", "symbol", "metaphor"],
                    "contexts": ["symbolic_analysis", "metaphor_detection"],
                    "dependencies": ["NL-2"]
                }
            },
            "SL": {
                "SL-1": {
                    "name": "Power and Incentive Mapping",
                    "purpose": "Trace who benefits from claims or interpretations",
                    "triggers": ["power_analysis", "incentives", "beneficiaries"],
                    "priority": "essential",
                    "output_type": "power_analysis",
                    "keywords": ["power", "incentives", "benefits", "mapping"],
                    "contexts": ["power_analysis", "strategic_analysis"],
                    "dependencies": []
                },
                "SL-2": {
                    "name": "Institutional Behavior and Enforcement Patterns",
                    "purpose": "Examine institutional alignment and enforcement",
                    "triggers": ["institutional_analysis", "enforcement", "alignment"],
                    "priority": "high",
                    "output_type": "institutional_analysis",
                    "keywords": ["institutional", "enforcement", "alignment", "patterns"],
                    "contexts": ["institutional_analysis", "system_behavior"],
                    "dependencies": ["SL-1"]
                },
                "SL-3": {
                    "name": "Identity and Memory Exploitation",
                    "purpose": "Uncover exploitation of collective memory and trauma",
                    "triggers": ["memory_exploitation", "trauma", "identity_manipulation"],
                    "priority": "high",
                    "output_type": "memory_analysis",
                    "keywords": ["memory", "exploitation", "trauma", "identity"],
                    "contexts": ["memory_analysis", "exploitation_detection"],
                    "dependencies": ["SL-1"]
                },
                "SL-4": {
                    "name": "Function and Purpose Analysis",
                    "purpose": "Determine deeper goals of claims or framing",
                    "triggers": ["strategic_purpose", "goals", "function"],
                    "priority": "high",
                    "output_type": "purpose_analysis",
                    "keywords": ["function", "purpose", "goals", "strategic"],
                    "contexts": ["purpose_analysis", "strategic_intent"],
                    "dependencies": ["SL-1"]
                },
                "SL-5": {
                    "name": "Systemic Resistance and Inversion",
                    "purpose": "Detect authentic vs performative resistance",
                    "triggers": ["resistance", "inversion", "performative"],
                    "priority": "medium",
                    "output_type": "resistance_analysis",
                    "keywords": ["resistance", "inversion", "performative", "authentic"],
                    "contexts": ["resistance_analysis", "system_opposition"],
                    "dependencies": ["SL-4"]
                },
                "SL-6": {
                    "name": "Feedback Systems and Loop Control",
                    "purpose": "Identify reinforcement loops and suppression",
                    "triggers": ["feedback_loops", "reinforcement", "suppression"],
                    "priority": "medium",
                    "output_type": "feedback_analysis",
                    "keywords": ["feedback", "loops", "reinforcement", "suppression"],
                    "contexts": ["feedback_analysis", "loop_detection"],
                    "dependencies": ["SL-2"]
                },
                "SL-7": {
                    "name": "Strategic Forecast and Predictive Testing",
                    "purpose": "Test implications by projecting future outcomes",
                    "triggers": ["prediction", "forecast", "implications"],
                    "priority": "medium",
                    "output_type": "predictive_analysis",
                    "keywords": ["forecast", "prediction", "implications", "testing"],
                    "contexts": ["predictive_analysis", "outcome_testing"],
                    "dependencies": ["SL-4"]
                },
                "SL-8": {
                    "name": "Systemic Blind Spots and Vulnerabilities",
                    "purpose": "Reveal what systems cannot process",
                    "triggers": ["blind_spots", "vulnerabilities", "forbidden_topics"],
                    "priority": "high",
                    "output_type": "blind_spot_analysis",
                    "keywords": ["blind", "spots", "vulnerabilities", "forbidden"],
                    "contexts": ["blind_spot_analysis", "system_limits"],
                    "dependencies": ["SL-2"]
                },
                "SL-9": {
                    "name": "Adaptive Evolution Awareness",
                    "purpose": "Track how claims evolve in response to pressure",
                    "triggers": ["evolution", "adaptation", "narrative_shift"],
                    "priority": "medium",
                    "output_type": "evolution_analysis",
                    "keywords": ["evolution", "adaptation", "shift", "change"],
                    "contexts": ["evolution_analysis", "narrative_tracking"],
                    "dependencies": ["SL-4"]
                }
            }
        }
    
    def _build_domain_patterns(self) -> Dict[str, List[str]]:
        """Build domain-specific trigger patterns"""
        return {
            "geopolitical": {
                "keywords": ["war", "conflict", "military", "sanctions", "alliance", "nuclear", 
                           "deterrence", "strategy", "security", "geopolitical", "international"],
                "modules": ["CL-4", "FL-2", "FL-7", "SL-1", "SL-4", "SL-8"]
            },
            "information_warfare": {
                "keywords": ["media", "propaganda", "narrative", "censorship", "bias", "fake", 
                           "news", "disinformation", "platform", "algorithm"],
                "modules": ["CL-1", "FL-2", "FL-3", "FL-9", "NL-3", "SL-6", "SL-8"]
            },
            "power_governance": {
                "keywords": ["election", "democracy", "government", "power", "politics", 
                           "legitimacy", "authority", "regime", "transition"],
                "modules": ["CL-4", "CL-5", "FL-7", "SL-1", "SL-2", "SL-4"]
            },
            "economic_control": {
                "keywords": ["debt", "capital", "finance", "trade", "resources", "energy", 
                           "supply", "chain", "economic", "market"],
                "modules": ["SL-1", "SL-2", "SL-4", "FL-4", "FL-7"]
            },
            "cultural_identity": {
                "keywords": ["culture", "identity", "values", "ideology", "memory", "trauma", 
                           "civilization", "heritage", "victim"],
                "modules": ["NL-4", "NL-5", "SL-3", "CL-3", "FL-9"]
            },
            "systemic_analysis": {
                "keywords": ["system", "complexity", "feedback", "control", "stability", 
                           "fragility", "institutional", "structural"],
                "modules": ["CL-2", "SL-2", "SL-6", "SL-8", "SL-9"]
            },
            "factual_disputes": {
                "keywords": ["evidence", "proof", "sources", "verify", "confirm", "happened", 
                           "reported", "claim", "fact"],
                "modules": ["FL-1", "FL-3", "FL-6", "FL-8", "NL-1", "NL-2"]
            },
            "moral_strategic": {
                "keywords": ["moral", "ethics", "values", "virtue", "justice", "rights", 
                           "humanitarian", "human rights"],
                "modules": ["CL-4", "CL-5", "NL-4", "SL-4", "FL-9"]
            }
        }
    
    def _build_trigger_keywords(self) -> Dict[str, List[str]]:
        """Build comprehensive trigger keyword mapping"""
        triggers = defaultdict(list)
        
        for level_id, level_modules in self.module_library.items():
            for module_id, module_data in level_modules.items():
                for keyword in module_data["keywords"]:
                    triggers[keyword.lower()].append(module_id)
                for context in module_data["contexts"]:
                    triggers[context.lower()].append(module_id)
                    
        return dict(triggers)
    
    def _build_dependencies(self) -> Dict[str, List[str]]:
        """Build module dependency mapping"""
        dependencies = {}
        
        for level_id, level_modules in self.module_library.items():
            for module_id, module_data in level_modules.items():
                dependencies[module_id] = module_data.get("dependencies", [])
                
        return dependencies
    
    def _build_strategic_indicators(self) -> Dict[str, float]:
        """Build strategic significance indicators"""
        return {
            # High-stakes geopolitical
            "nuclear": 0.95,
            "war": 0.9,
            "conflict": 0.85,
            "military": 0.8,
            "sanctions": 0.85,
            "geopolitical": 0.9,
            
            # Power and control
            "power": 0.8,
            "control": 0.75,
            "regime": 0.8,
            "government": 0.7,
            "elite": 0.75,
            
            # Information warfare
            "propaganda": 0.8,
            "disinformation": 0.85,
            "censorship": 0.8,
            "narrative": 0.7,
            "media": 0.6,
            
            # Economic leverage
            "debt": 0.7,
            "resources": 0.75,
            "energy": 0.8,
            "supply chain": 0.8,
            "economic": 0.6,
            
            # Systemic issues
            "systemic": 0.8,
            "institutional": 0.7,
            "structural": 0.7,
            "strategic": 0.8
        }
    
    def select_modules(self, rai_input, max_modules_per_level: int = 7, 
                      output_mode: str = "brief") -> ModuleSelection:
        """
        Main module selection function
        
        Args:
            rai_input: RAIInput object from wrapper
            max_modules_per_level: Maximum modules per level
            output_mode: Output complexity level
            
        Returns:
            ModuleSelection object with selected modules and execution plan
        """
        try:
            # Step 1: Determine entry point
            entry_point = self._determine_entry_point(rai_input)
            
            # Step 2: Generate module matches across all levels
            matches = self._generate_module_matches(rai_input)
            
            # Step 3: Score and prioritize modules
            scored_modules = self._score_modules(matches, rai_input)
            
            # Step 4: Select modules by level with constraints
            selected_by_level = self._select_by_level(
                scored_modules, max_modules_per_level, output_mode
            )
            
            # Step 5: Add dependencies
            final_selection = self._add_dependencies(selected_by_level)
            
            # Step 6: Generate execution order
            execution_order = self._generate_execution_order(
                final_selection, entry_point
            )
            
            # Step 7: Generate rationale
            rationale = self._generate_selection_rationale(
                rai_input, final_selection, entry_point
            )
            
            return ModuleSelection(
                entry_point=entry_point,
                cross_level_modules=final_selection.get("CL", []),
                fact_level_modules=final_selection.get("FL", []),
                narrative_level_modules=final_selection.get("NL", []),
                system_level_modules=final_selection.get("SL", []),
                execution_order=execution_order,
                total_modules=sum(len(modules) for modules in final_selection.values()),
                selection_rationale=rationale
            )
            
        except Exception as e:
            logger.error(f"Error in module selection: {str(e)}")
            return self._fallback_selection(rai_input)
    
    def _determine_entry_point(self, rai_input) -> ModuleLevel:
        """Determine optimal entry point based on input analysis"""
        
        # System-level indicators
        system_indicators = [
            "power", "control", "system", "elite", "government", "geopolitical", 
            "strategic", "institutional", "regime", "sanctions"
        ]
        
        # Narrative-level indicators
        narrative_indicators = [
            "because", "therefore", "led to", "caused", "story", "narrative", 
            "moral", "identity", "values", "memory", "trauma", "ideology"
        ]
        
        # Fact-level indicators
        fact_indicators = [
            "happened", "occurred", "reported", "confirmed", "evidence", 
            "data", "statistics", "study", "proof", "verify"
        ]
        
        text = rai_input.cleaned_input.lower()
        words = text.split()
        
        # Calculate scores
        system_score = sum(1 for word in words if word in system_indicators)
        narrative_score = sum(1 for word in words if word in narrative_indicators)
        fact_score = sum(1 for word in words if word in fact_indicators)
        
        # Add input type weights
        if rai_input.input_type.value == "system_premise":
            system_score += 2
        elif rai_input.input_type.value == "narrative":
            narrative_score += 2
        elif rai_input.input_type.value == "factual_claim":
            fact_score += 2
        
        # Add complexity and strategic weights
        if rai_input.complexity_score >= 4:
            system_score += 1
        
        # Strategic significance boost
        strategic_boost = sum(
            self.strategic_indicators.get(word, 0) 
            for word in words 
            if word in self.strategic_indicators
        )
        
        if strategic_boost >= 2.0:
            system_score += 2
        
        # Determine entry point
        if system_score >= max(narrative_score, fact_score):
            return ModuleLevel.SYSTEM_LEVEL
        elif narrative_score >= fact_score:
            return ModuleLevel.NARRATIVE_LEVEL
        else:
            return ModuleLevel.FACT_LEVEL
    
    def _generate_module_matches(self, rai_input) -> List[ModuleMatch]:
        """Generate module matches based on input analysis"""
        matches = []
        text = rai_input.cleaned_input.lower()
        words = set(text.split())
        
        # Analyze each module
        for level_id, level_modules in self.module_library.items():
            for module_id, module_data in level_modules.items():
                match = self._analyze_module_match(
                    module_id, module_data, text, words, rai_input
                )
                matches.append(match)
        
        return matches
    
    def _analyze_module_match(self, module_id: str, module_data: Dict, 
                             text: str, words: Set[str], rai_input) -> ModuleMatch:
        """Analyze how well a module matches the input"""
        
        # Keyword matching
        keyword_matches = []
        for keyword in module_data["keywords"]:
            if keyword.lower() in text:
                keyword_matches.append(keyword)
        
        # Context matching  
        context_matches = []
        for context in module_data["contexts"]:
            if self._matches_context_pattern(context, text, rai_input):
                context_matches.append(context)
        
        # Trigger matching
        trigger_matches = []
        for trigger in module_data["triggers"]:
            if self._matches_trigger(trigger, rai_input, text):
                trigger_matches.append(trigger)
        
        # Calculate base confidence
        keyword_score = len(keyword_matches) / max(len(module_data["keywords"]), 1)
        context_score = len(context_matches) / max(len(module_data["contexts"]), 1)
        trigger_score = len(trigger_matches) / max(len(module_data["triggers"]), 1)
        
        base_confidence = (keyword_score * 0.4 + context_score * 0.3 + trigger_score * 0.3)
        
        # Apply input-specific modifiers
        modified_confidence = self._apply_module_modifiers(
            base_confidence, module_id, rai_input, keyword_matches
        )
        
        # Determine priority
        if module_data["priority"] == "essential" or modified_confidence >= 0.8:
            priority = ModulePriority.ESSENTIAL
        elif modified_confidence >= 0.6 or module_data["priority"] == "high":
            priority = ModulePriority.HIGH
        elif modified_confidence >= 0.3 or module_data["priority"] == "medium":
            priority = ModulePriority.MEDIUM
        else:
            priority = ModulePriority.LOW
        
        # Generate rationale
        rationale = self._generate_module_rationale(
            module_id, keyword_matches, context_matches, trigger_matches
        )
        
        return ModuleMatch(
            module_id=module_id,
            priority=priority,
            confidence=modified_confidence,
            trigger_factors=keyword_matches + context_matches + trigger_matches,
            dependency_modules=module_data.get("dependencies", []),
            rationale=rationale
        )
    
    def _matches_context_pattern(self, context: str, text: str, rai_input) -> bool:
        """Check if input matches a contextual pattern"""
        
        # Domain pattern matching
        for domain, pattern_data in self.domain_patterns.items():
            if context.lower() in [kw.lower() for kw in pattern_data.get("keywords", [])]:
                return True
        
        # Direct context matching
        context_patterns = {
            "preprocessing": ["all"],
            "input_analysis": ["all"],
            "complex_analysis": lambda: rai_input.complexity_score >= 4,
            "strategic_content": lambda: any(word in text for word in ["strategic", "geopolitical", "power"]),
            "narrative_analysis": lambda: rai_input.input_type.value in ["narrative", "mixed"],
            "fact_checking": lambda: rai_input.input_type.value == "factual_claim",
            "media_analysis": lambda: any(word in text for word in ["media", "news", "press"]),
            "information_warfare": lambda: any(word in text for word in ["propaganda", "disinformation", "narrative"]),
            "geopolitical_analysis": lambda: any(word in text for word in ["geopolitical", "international", "war"]),
            "power_analysis": lambda: any(word in text for word in ["power", "control", "elite"]),
            "high_stakes_content": lambda: rai_input.emotional_charge >= 4 or any(
                self.strategic_indicators.get(word, 0) > 0.7 
                for word in text.split()
            )
        }
        
        if context in context_patterns:
            pattern = context_patterns[context]
            if callable(pattern):
                return pattern()
            elif pattern == ["all"]:
                return True
        
        return False
    
    def _matches_trigger(self, trigger: str, rai_input, text: str) -> bool:
        """Check if input matches a trigger condition"""
        
        trigger_conditions = {
            "all_inputs": True,
            "geopolitical": any(word in text for word in ["geopolitical", "international", "war", "conflict"]),
            "strategic": any(word in text for word in ["strategic", "strategy", "power"]),
            "complex": rai_input.complexity_score >= 4,
            "ideological": any(word in text for word in ["ideology", "belief", "values"]),
            "factual_claim": rai_input.input_type.value == "factual_claim",
            "narrative": rai_input.input_type.value in ["narrative", "mixed"],
            "causal_claims": any(word in text for word in ["because", "caused", "led to", "therefore"]),
            "logical_linkage": any(word in text for word in ["thus", "therefore", "so", "hence"]),
            "verification": any(word in text for word in ["verify", "confirm", "check", "prove"]),
            "clarity": any(word in text for word in ["unclear", "vague", "confusing"]),
            "media_bias": any(word in text for word in ["media", "bias", "propaganda"]),
            "amplification": any(word in text for word in ["promoted", "suppressed", "amplified"]),
            "suppression": any(word in text for word in ["censored", "hidden", "suppressed"]),
            "source_analysis": any(word in text for word in ["source", "citation", "reference"]),
            "independence": any(word in text for word in ["independent", "biased", "aligned"]),
            "coordination": any(word in text for word in ["coordinated", "synchronized", "aligned"]),
            "moral_strategic": any(word in text for word in ["moral", "ethical", "values"]) and 
                              any(word in text for word in ["strategic", "political", "power"]),
            "virtue_signaling": any(word in text for word in ["virtue", "moral", "righteous"]),
            "double_standards": any(word in text for word in ["double", "standard", "hypocr"]),
            "bias": any(word in text for word in ["bias", "unfair", "partial"]),
            "asymmetric_judgment": any(word in text for word in ["unfair", "unequal", "asymmetric"]),
            "power_analysis": any(word in text for word in ["power", "control", "influence"]),
            "incentives": any(word in text for word in ["incentive", "benefit", "gain"]),
            "beneficiaries": any(word in text for word in ["benefit", "advantage", "gain"]),
            "institutional_analysis": any(word in text for word in ["institution", "government", "organization"]),
            "high_stakes": rai_input.emotional_charge >= 4 or any(
                self.strategic_indicators.get(word, 0) > 0.7 
                for word in text.split()
            ),
            "risk_assessment": any(word in text for word in ["risk", "danger", "threat"]),
            "consequences": any(word in text for word in ["consequence", "result", "outcome"]),
            "toxic_labels": any(word in text for word in ["conspiracy", "populist", "regime", "authoritarian"]),
            "prejudgment": any(word in text for word in ["obviously", "clearly", "definitely"]),
            "disqualification": any(word in text for word in ["dismiss", "reject", "ignore"])
        }
        
        return trigger_conditions.get(trigger, False)
    
    def _apply_module_modifiers(self, base_confidence: float, module_id: str, 
                               rai_input, keyword_matches: List[str]) -> float:
        """Apply input-specific modifiers to module confidence"""
        confidence = base_confidence
        
        # Essential modules always get boosted
        if module_id in ["CL-0", "FL-1", "FL-8", "NL-1", "SL-1"]:
            confidence = max(confidence, 0.8)
        
        # Input type alignment boosts
        if rai_input.input_type.value == "factual_claim":
            if module_id.startswith("FL"):
                confidence *= 1.3
            elif module_id in ["CL-0", "CL-5"]:
                confidence *= 1.2
        elif rai_input.input_type.value == "narrative":
            if module_id.startswith("NL"):
                confidence *= 1.3
            elif module_id in ["CL-1", "CL-3"]:
                confidence *= 1.2
        elif rai_input.input_type.value == "system_premise":
            if module_id.startswith("SL"):
                confidence *= 1.3
            elif module_id in ["CL-4", "CL-5"]:
                confidence *= 1.2
        
        # Complexity boosts
        if rai_input.complexity_score >= 4:
            if module_id in ["CL-0.1", "CL-3", "SL-2", "SL-6", "SL-8"]:
                confidence *= 1.2
        
        # Emotional charge boosts
        if rai_input.emotional_charge >= 4:
            if module_id in ["CL-4", "FL-9", "NL-4", "SL-3"]:
                confidence *= 1.15
        
        # Strategic significance boosts
        strategic_score = sum(
            self.strategic_indicators.get(word.lower(), 0) 
            for word in keyword_matches
        )
        
        if strategic_score > 1.5:
            if module_id in ["CL-4", "FL-7", "SL-1", "SL-4", "SL-8"]:
                confidence *= 1.25
        
        # Topic domain boosts
        for topic in rai_input.detected_topics:
            domain_modules = self.domain_patterns.get(topic, {}).get("modules", [])
            if module_id in domain_modules:
                confidence *= 1.15
        
        # Style flag considerations
        if "hyperbole" in rai_input.style_flags:
            if module_id in ["FL-9", "CL-4", "NL-5"]:
                confidence *= 1.1
        
        if "mockery" in rai_input.style_flags:
            if module_id in ["CL-5", "FL-9", "NL-3"]:
                confidence *= 1.1
        
        return min(confidence, 1.0)  # Cap at 1.0
    
    def _generate_module_rationale(self, module_id: str, keyword_matches: List[str],
                                  context_matches: List[str], trigger_matches: List[str]) -> str:
        """Generate rationale for module selection"""
        rationale_parts = []
        
        if keyword_matches:
            rationale_parts.append(f"Keywords: {', '.join(keyword_matches[:3])}")
        
        if context_matches:
            rationale_parts.append(f"Context: {', '.join(context_matches[:2])}")
        
        if trigger_matches:
            rationale_parts.append(f"Triggers: {', '.join(trigger_matches[:2])}")
        
        return "; ".join(rationale_parts) if rationale_parts else "Base relevance"
    
    def _score_modules(self, matches: List[ModuleMatch], rai_input) -> Dict[str, List[Tuple[str, float]]]:
        """Score and rank modules by level"""
        scored_by_level = defaultdict(list)
        
        for match in matches:
            level = match.module_id.split("-")[0]
            scored_by_level[level].append((match.module_id, match.confidence, match.priority))
        
        # Sort each level by priority then confidence
        for level in scored_by_level:
            scored_by_level[level].sort(key=lambda x: (
                0 if x[2] == ModulePriority.ESSENTIAL else
                1 if x[2] == ModulePriority.HIGH else
                2 if x[2] == ModulePriority.MEDIUM else 3,
                -x[1]  # Negative for descending order
            ))
        
        return dict(scored_by_level)
    
    def _select_by_level(self, scored_modules: Dict[str, List[Tuple[str, float, ModulePriority]]], 
                        max_per_level: int, output_mode: str) -> Dict[str, List[str]]:
        """Select modules by level with constraints"""
        selected = {}
        
        # Adjust limits based on output mode
        if output_mode == "analytical":
            max_per_level = min(max_per_level + 2, 9)
        elif output_mode == "brief":
            max_per_level = min(max_per_level - 1, 5)
        
        for level, module_scores in scored_modules.items():
            selected_modules = []
            
            # Always include essential modules
            for module_id, confidence, priority in module_scores:
                if priority == ModulePriority.ESSENTIAL:
                    selected_modules.append(module_id)
            
            # Add high priority modules up to limit
            for module_id, confidence, priority in module_scores:
                if (len(selected_modules) < max_per_level and 
                    module_id not in selected_modules and
                    priority == ModulePriority.HIGH and
                    confidence >= 0.5):
                    selected_modules.append(module_id)
            
            # Fill remaining slots with medium priority if needed
            for module_id, confidence, priority in module_scores:
                if (len(selected_modules) < max_per_level and 
                    module_id not in selected_modules and
                    priority == ModulePriority.MEDIUM and
                    confidence >= 0.4):
                    selected_modules.append(module_id)
            
            selected[level] = selected_modules
        
        return selected
    
    def _add_dependencies(self, selected_by_level: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """Add required dependencies for selected modules"""
        final_selection = {}
        
        for level, modules in selected_by_level.items():
            final_modules = set(modules)
            
            # Add dependencies
            for module_id in modules:
                dependencies = self.module_dependencies.get(module_id, [])
                for dep in dependencies:
                    final_modules.add(dep)
            
            final_selection[level] = list(final_modules)
        
        return final_selection
    
    def _generate_execution_order(self, selected_modules: Dict[str, List[str]], 
                                 entry_point: ModuleLevel) -> List[str]:
        """Generate optimal execution order for selected modules"""
        execution_order = []
        
        # Always start with CL-0 if present
        if "CL-0" in selected_modules.get("CL", []):
            execution_order.append("CL-0")
        
        # Add other cross-level modules
        for module in selected_modules.get("CL", []):
            if module != "CL-0" and module not in execution_order:
                execution_order.append(module)
        
        # Determine level order based on entry point
        if entry_point == ModuleLevel.SYSTEM_LEVEL:
            level_order = ["SL", "NL", "FL"]
        elif entry_point == ModuleLevel.NARRATIVE_LEVEL:
            level_order = ["NL", "FL", "SL"]
        else:  # FACT_LEVEL
            level_order = ["FL", "NL", "SL"]
        
        # Add modules in level order, respecting dependencies
        for level in level_order:
            level_modules = selected_modules.get(level, [])
            # Sort by dependency order and natural sequence
            sorted_modules = self._sort_modules_by_dependencies(level_modules, level)
            execution_order.extend(sorted_modules)
        
        return execution_order
    
    def _sort_modules_by_dependencies(self, modules: List[str], level: str) -> List[str]:
        """Sort modules within a level by dependencies"""
        if not modules:
            return []
        
        # Create dependency graph
        module_deps = {}
        for module in modules:
            deps_in_level = [dep for dep in self.module_dependencies.get(module, []) 
                           if dep.startswith(level) and dep in modules]
            module_deps[module] = deps_in_level
        
        # Topological sort
        sorted_modules = []
        remaining = set(modules)
        
        while remaining:
            # Find modules with no unsatisfied dependencies in this level
            ready = [m for m in remaining if not set(module_deps[m]) & remaining]
            
            if not ready:
                # If circular dependency, just add in natural order
                ready = [min(remaining)]
            
            # Sort ready modules by natural sequence (e.g., FL-1, FL-2, FL-3)
            ready.sort(key=lambda x: int(x.split('-')[1]) if '-' in x and x.split('-')[1].isdigit() else 999)
            
            for module in ready:
                sorted_modules.append(module)
                remaining.remove(module)
        
        return sorted_modules
    
    def _generate_selection_rationale(self, rai_input, selected_modules: Dict[str, List[str]], 
                                    entry_point: ModuleLevel) -> str:
        """Generate explanation for module selection"""
        rationale_parts = []
        
        # Entry point reasoning
        rationale_parts.append(f"Entry point: {entry_point.value} based on input type '{rai_input.input_type.value}'")
        
        # Input characteristics
        if rai_input.complexity_score >= 4:
            rationale_parts.append(f"High complexity ({rai_input.complexity_score}/5) triggered system-level modules")
        
        if rai_input.emotional_charge >= 4:
            rationale_parts.append(f"High emotional charge ({rai_input.emotional_charge}/5) added bias detection modules")
        
        # Topic domains
        if rai_input.detected_topics:
            rationale_parts.append(f"Detected domains: {', '.join(rai_input.detected_topics)}")
        
        # Module counts
        total_modules = sum(len(modules) for modules in selected_modules.values())
        rationale_parts.append(f"Selected {total_modules} modules across {len(selected_modules)} levels")
        
        # Special considerations
        if any("FL-7" in modules for modules in selected_modules.values()):
            rationale_parts.append("High-stakes content detected, added risk assessment")
        
        if any("SL-8" in modules for modules in selected_modules.values()):
            rationale_parts.append("Potential blind spots identified, added vulnerability analysis")
        
        return ". ".join(rationale_parts) + "."
    
    def _fallback_selection(self, rai_input) -> ModuleSelection:
        """Fallback selection when main algorithm fails"""
        
        # Basic selection based on input type
        fallback_modules = {
            "factual_claim": {
                "CL": ["CL-0"],
                "FL": ["FL-1", "FL-8", "FL-3"],
                "NL": ["NL-1"],
                "SL": ["SL-1"]
            },
            "narrative": {
                "CL": ["CL-0", "CL-1"],
                "FL": ["FL-1"],
                "NL": ["NL-1", "NL-2", "NL-3"],
                "SL": ["SL-1", "SL-4"]
            },
            "system_premise": {
                "CL": ["CL-0", "CL-4"],
                "FL": ["FL-1"],
                "NL": ["NL-1"],
                "SL": ["SL-1", "SL-2", "SL-4"]
            },
            "mixed": {
                "CL": ["CL-0"],
                "FL": ["FL-1", "FL-8"],
                "NL": ["NL-1", "NL-2"],
                "SL": ["SL-1"]
            },
            "question": {
                "CL": ["CL-0"],
                "FL": ["FL-1"],
                "NL": ["NL-1"],
                "SL": ["SL-1"]
            }
        }
        
        input_type = rai_input.input_type.value
        modules = fallback_modules.get(input_type, fallback_modules["mixed"])
        
        # Generate execution order
        execution_order = []
        for level in ["CL", "FL", "NL", "SL"]:
            execution_order.extend(modules.get(level, []))
        
        return ModuleSelection(
            entry_point=ModuleLevel.FACT_LEVEL,
            cross_level_modules=modules.get("CL", []),
            fact_level_modules=modules.get("FL", []),
            narrative_level_modules=modules.get("NL", []),
            system_level_modules=modules.get("SL", []),
            execution_order=execution_order,
            total_modules=sum(len(mods) for mods in modules.values()),
            selection_rationale="Fallback selection due to processing error."
        )
    
    def format_modules_for_prompt(self, selection: ModuleSelection) -> str:
        """Format selected modules for inclusion in RAI prompt"""
        
        if not selection.execution_order:
            return ""
        
        formatted_parts = []
        
        # Header
        formatted_parts.append("**SELECTED RAI MODULES FOR EXECUTION:**")
        formatted_parts.append("")
        
        # Entry point
        formatted_parts.append(f"**Entry Point:** {selection.entry_point.value}")
        formatted_parts.append("")
        
        # Modules by level
        if selection.cross_level_modules:
            formatted_parts.append("**Cross-Level Modules:**")
            for module_id in selection.cross_level_modules:
                module_data = self._get_module_data(module_id)
                if module_data:
                    formatted_parts.append(f"• **{module_id}**: {module_data['name']}")
                    formatted_parts.append(f"  {module_data['purpose']}")
            formatted_parts.append("")
        
        if selection.fact_level_modules:
            formatted_parts.append("**Fact-Level Modules:**")
            for module_id in selection.fact_level_modules:
                module_data = self._get_module_data(module_id)
                if module_data:
                    formatted_parts.append(f"• **{module_id}**: {module_data['name']}")
            formatted_parts.append("")
        
        if selection.narrative_level_modules:
            formatted_parts.append("**Narrative-Level Modules:**")
            for module_id in selection.narrative_level_modules:
                module_data = self._get_module_data(module_id)
                if module_data:
                    formatted_parts.append(f"• **{module_id}**: {module_data['name']}")
            formatted_parts.append("")
        
        if selection.system_level_modules:
            formatted_parts.append("**System-Level Modules:**")
            for module_id in selection.system_level_modules:
                module_data = self._get_module_data(module_id)
                if module_data:
                    formatted_parts.append(f"• **{module_id}**: {module_data['name']}")
            formatted_parts.append("")
        
        # Execution order
        formatted_parts.append("**Execution Order:**")
        formatted_parts.append(" → ".join(selection.execution_order))
        formatted_parts.append("")
        
        # Selection rationale
        formatted_parts.append(f"**Selection Rationale:** {selection.selection_rationale}")
        formatted_parts.append("")
        
        return "\n".join(formatted_parts)
    
    def _get_module_data(self, module_id: str) -> Optional[Dict]:
        """Get module data by ID"""
        level = module_id.split("-")[0]
        
        if level in self.module_library:
            return self.module_library[level].get(module_id)
        
        return None
    
    def get_module_summary(self, module_id: str) -> str:
        """Get a brief summary of a module"""
        module_data = self._get_module_data(module_id)
        if module_data:
            return f"{module_id}: {module_data['name']} - {module_data['purpose']}"
        return f"{module_id}: Unknown module"


# Integration example
if __name__ == "__main__":
    from rai_wrapper import RAIWrapper
    from premise_engine import PremiseEngine
    
    # Initialize engines
    rai_wrapper = RAIWrapper()
    premise_engine = PremiseEngine()
    module_selector = ModuleSelector()
    
    # Test input
    test_input = "The Western media coverage of Ukraine clearly shows coordinated propaganda designed to justify NATO expansion and this proves the military-industrial complex controls the narrative."
    
    # Process with RAI wrapper
    rai_result = rai_wrapper.process_input(test_input)
    rai_input = rai_result['input']
    
    # Select premises and modules
    premise_selection = premise_engine.select_premises(rai_input)
    module_selection = module_selector.select_modules(rai_input)
    
    print("=== MODULE SELECTION RESULT ===")
    print(f"Entry Point: {module_selection.entry_point.value}")
    print(f"Total Modules: {module_selection.total_modules}")
    print(f"Cross-Level: {module_selection.cross_level_modules}")
    print(f"Fact-Level: {module_selection.fact_level_modules}")
    print(f"Narrative-Level: {module_selection.narrative_level_modules}")
    print(f"System-Level: {module_selection.system_level_modules}")
    print(f"Execution Order: {' → '.join(module_selection.execution_order)}")
    print(f"Rationale: {module_selection.selection_rationale}")
    print("\n=== FORMATTED FOR PROMPT ===")
    print(module_selector.format_modules_for_prompt(module_selection))
