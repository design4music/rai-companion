"""
RAI Analytical Engine - Unified Analysis Component Selection
Real Artificial Intelligence Framework Implementation

git
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

# Import the centralized content library
from analytical_content import (
    MODULE_LIBRARY, 
    PREMISE_LIBRARY, 
    RAI_FRAMEWORK_CORE
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnalysisMode(Enum):
    """Analysis mode types"""
    QUICK = "quick"
    GUIDED = "guided" 
    EXPERT = "expert"

@dataclass
class AnalysisComponent:
    """Single analysis component with module and its anchored premises"""
    module_id: str
    module_name: str
    module_purpose: str
    core_questions: List[str]
    philosophical_anchoring: List[str]  # Premise IDs
    anchored_premises: List[Dict[str, str]]  # Full premise content
    wisdom_injected: List[str]

@dataclass 
class AnalysisSelection:
    """Complete analysis selection result"""
    entry_point: str
    components: List[AnalysisComponent]
    execution_order: List[str]
    total_modules: int
    total_premises: int
    selection_rationale: str

class AnalyticalEngine:
    """
    Unified RAI Analysis Engine
    
    Intelligently selects modules and their philosophical anchoring using
    semantic understanding rather than mechanical keyword matching.
    """
    
    def __init__(self):
        """Initialize with content from analytical_content.py"""
        self.modules = MODULE_LIBRARY
        self.premises = PREMISE_LIBRARY
        self.framework_core = RAI_FRAMEWORK_CORE
        
        logger.info("Analytical Engine initialized with centralized content library")
    
    def select_analysis_components(self, rai_input, analysis_mode: str = "guided", 
                                 max_modules: int = 6) -> AnalysisSelection:
        """
        Main selection function - intelligently choose modules and extract their premises
        
        Args:
            rai_input: RAIInput object from rai_wrapper
            analysis_mode: Analysis depth (quick/guided/expert)
            max_modules: Maximum modules to select
            
        Returns:
            AnalysisSelection with modules and their anchored premises
        """
        try:
            logger.info(f"Selecting analysis components: mode={analysis_mode}, max={max_modules}")
            
            # Step 1: Determine entry point
            entry_point = self._determine_entry_point(rai_input)
            
            # Step 2: Select relevant modules using semantic analysis
            selected_module_ids = self._select_modules_semantic(
                rai_input, analysis_mode, max_modules
            )
            
            # Step 3: Build analysis components with modules + anchored premises
            components = self._build_analysis_components(selected_module_ids)
            
            # Step 4: Generate execution order
            execution_order = self._generate_execution_order(components, entry_point)
            
            # Step 5: Generate selection rationale
            rationale = self._generate_rationale(rai_input, components, analysis_mode)
            
            return AnalysisSelection(
                entry_point=entry_point,
                components=components,
                execution_order=execution_order,
                total_modules=len(components),
                total_premises=sum(len(c.anchored_premises) for c in components),
                selection_rationale=rationale
            )
            
        except Exception as e:
            logger.error(f"Error in analysis component selection: {str(e)}")
            return self._fallback_selection(rai_input)
    
    def _determine_entry_point(self, rai_input) -> str:
        """Determine optimal analysis entry point"""
        
        text = rai_input.cleaned_input.lower()
        
        # System-level indicators
        system_keywords = ["power", "control", "system", "government", "geopolitical", "strategic"]
        system_score = sum(1 for word in system_keywords if word in text)
        
        # Narrative-level indicators  
        narrative_keywords = ["because", "therefore", "story", "narrative", "caused", "led to"]
        narrative_score = sum(1 for word in narrative_keywords if word in text)
        
        # Fact-level indicators
        fact_keywords = ["evidence", "proof", "confirmed", "reported", "data", "study"]
        fact_score = sum(1 for word in fact_keywords if word in text)
        
        # Input type influence
        if rai_input.input_type.value == "system_premise":
            system_score += 2
        elif rai_input.input_type.value == "narrative": 
            narrative_score += 2
        elif rai_input.input_type.value == "factual_claim":
            fact_score += 2
        
        # Complexity influence
        if rai_input.complexity_score >= 4:
            system_score += 1
        
        # Determine entry point
        if system_score >= max(narrative_score, fact_score):
            return "system"
        elif narrative_score >= fact_score:
            return "narrative"
        else:
            return "fact"
    
    def _select_modules_semantic(self, rai_input, analysis_mode: str, max_modules: int) -> List[str]:
        """
        Semantic module selection based on rich content descriptions
        
        Selects modules based on input complexity and relevance, not artificial mode limits.
        All modes get full analytical depth - they only differ in output verbosity.
        """
        
        # Essential modules that should almost always be included
        essential_modules = ["CL-0"]  # Input normalization
        
        # Input type specific modules
        type_modules = {
            "factual_claim": ["FL-1", "FL-8", "FL-3", "FL-2"],
            "narrative": ["NL-1", "NL-2", "NL-3", "NL-4"], 
            "system_premise": ["SL-1", "SL-2", "SL-4", "SL-8"],
            "mixed": ["FL-1", "NL-1", "SL-1", "FL-8"]
        }
        
        # Topic-based modules
        topic_modules = {
            "geopolitical": ["SL-1", "SL-4", "FL-7", "SL-8", "NL-4"],
            "information": ["FL-2", "FL-3", "SL-8", "FL-9", "CL-4"],
            "power_governance": ["SL-1", "SL-2", "CL-4", "CL-5"],
            "systems": ["SL-6", "SL-8", "CL-2", "SL-9"],
            "economy": ["SL-1", "SL-2", "FL-4", "FL-7"],
            "cultural": ["NL-4", "NL-5", "SL-3", "CL-3"]
        }
        
        # Start with essential modules
        selected = list(essential_modules)
        
        # Add input type modules
        input_type = rai_input.input_type.value
        type_specific = type_modules.get(input_type, type_modules["mixed"])
        for module in type_specific:
            if module not in selected:
                selected.append(module)
        
        # Add topic-specific modules
        for topic in rai_input.detected_topics:
            topic_specific = topic_modules.get(topic, [])
            for module in topic_specific:
                if module not in selected:
                    selected.append(module)
        
        # Add complexity-based modules
        if rai_input.complexity_score >= 4:
            complex_modules = ["SL-8", "CL-2", "CL-3", "SL-9", "NL-3"]
            for module in complex_modules:
                if module not in selected:
                    selected.append(module)
        
        # Add high-stakes modules for emotional/controversial content
        if rai_input.emotional_charge >= 4:
            high_stakes = ["FL-7", "FL-9", "CL-4", "CL-5", "SL-3"]
            for module in high_stakes:
                if module not in selected:
                    selected.append(module)
        
        # Ensure cross-level representation for comprehensive analysis
        levels_present = set(m.split('-')[0] for m in selected)
        
        # Add missing levels if we don't have good coverage
        if "FL" not in levels_present:
            selected.append("FL-1")  # Basic fact checking
        if "NL" not in levels_present:
            selected.append("NL-1")  # Basic narrative analysis
        if "SL" not in levels_present:
            selected.append("SL-1")  # Basic system analysis
        
        # Only limit for very simple inputs to avoid overkill
        if (rai_input.complexity_score <= 2 and 
            rai_input.emotional_charge <= 2 and 
            not rai_input.detected_topics and
            rai_input.input_type.value == "factual_claim"):
            # Simple factual claim - limit to core modules
            selected = selected[:6]
        
        logger.info(f"Selected modules: {selected}")
        return selected 
  
    def _build_analysis_components(self, module_ids: List[str]) -> List[AnalysisComponent]:
        """Build analysis components with modules and their anchored premises"""
        
        components = []
        
        for module_id in module_ids:
            # Find module in library
            module_data = self._get_module_data(module_id)
            if not module_data:
                logger.warning(f"Module {module_id} not found in library")
                continue
            
            # Get philosophical anchoring
            anchoring_ids = module_data.get("philosophical_anchoring", [])
            anchored_premises = []
            
            # Extract full premise content for each anchor
            for premise_id in anchoring_ids:
                premise_data = self._get_premise_data(premise_id)
                if premise_data:
                    anchored_premises.append({
                        "id": premise_id,
                        "title": premise_data["title"],
                        "content": premise_data["content"]
                    })
            
            # Build component
            component = AnalysisComponent(
                module_id=module_id,
                module_name=module_data["name"],
                module_purpose=module_data["purpose"], 
                core_questions=module_data.get("core_questions", []),
                philosophical_anchoring=anchoring_ids,
                anchored_premises=anchored_premises,
                wisdom_injected=module_data.get("wisdom_injected", [])
            )
            
            components.append(component)
        
        return components
    
    def _get_module_data(self, module_id: str) -> Optional[Dict]:
        """Get module data from library"""
        level = module_id.split('-')[0]
        
        if level in self.modules:
            return self.modules[level]["modules"].get(module_id)
        
        return None
    
    def _get_premise_data(self, premise_id: str) -> Optional[Dict]:
        """Get premise data from library"""
        dimension = premise_id.split('.')[0]
        
        if dimension in self.premises["dimensions"]:
            return self.premises["dimensions"][dimension]["premises"].get(premise_id)
        
        return None
    
    def _generate_execution_order(self, components: List[AnalysisComponent], entry_point: str) -> List[str]:
        """Generate optimal execution order"""
        
        # Always start with CL-0 if present
        order = []
        cl_modules = [c.module_id for c in components if c.module_id.startswith("CL")]
        fl_modules = [c.module_id for c in components if c.module_id.startswith("FL")]
        nl_modules = [c.module_id for c in components if c.module_id.startswith("NL")]
        sl_modules = [c.module_id for c in components if c.module_id.startswith("SL")]
        
        # Start with CL-0
        if "CL-0" in cl_modules:
            order.append("CL-0")
            cl_modules.remove("CL-0")
        
        # Add other CL modules
        order.extend(sorted(cl_modules))
        
        # Add levels based on entry point
        if entry_point == "system":
            order.extend(sorted(sl_modules))
            order.extend(sorted(nl_modules))
            order.extend(sorted(fl_modules))
        elif entry_point == "narrative":
            order.extend(sorted(nl_modules))
            order.extend(sorted(fl_modules))
            order.extend(sorted(sl_modules))
        else:  # fact entry point
            order.extend(sorted(fl_modules))
            order.extend(sorted(nl_modules))
            order.extend(sorted(sl_modules))
        
        return order
    
    def _generate_rationale(self, rai_input, components: List[AnalysisComponent], analysis_mode: str) -> str:
        """Generate selection rationale"""
        
        rationale_parts = []
        
        # Input analysis
        rationale_parts.append(
            f"Input classified as {rai_input.input_type.value} with "
            f"complexity {rai_input.complexity_score}/5"
        )
        
        # Topic detection
        if rai_input.detected_topics:
            rationale_parts.append(f"Detected topics: {', '.join(rai_input.detected_topics)}")
        
        # Module selection
        level_counts = {}
        for comp in components:
            level = comp.module_id.split('-')[0]
            level_counts[level] = level_counts.get(level, 0) + 1
        
        level_summary = ", ".join([f"{k}={v}" for k, v in level_counts.items()])
        rationale_parts.append(f"Selected {len(components)} modules ({level_summary}) for {analysis_mode} analysis")
        
        # Premise anchoring
        total_premises = sum(len(c.anchored_premises) for c in components)
        if total_premises > 0:
            rationale_parts.append(f"Extracted {total_premises} anchored premises for philosophical depth")
        
        return ". ".join(rationale_parts) + "."
    
    def _fallback_selection(self, rai_input) -> AnalysisSelection:
        """Fallback selection when main algorithm fails"""
        
        # Basic fallback modules
        fallback_modules = ["CL-0", "FL-1", "NL-1", "SL-1"]
        
        # Build minimal components
        components = []
        for module_id in fallback_modules:
            module_data = self._get_module_data(module_id)
            if module_data:
                component = AnalysisComponent(
                    module_id=module_id,
                    module_name=module_data["name"],
                    module_purpose=module_data["purpose"],
                    core_questions=module_data.get("core_questions", []),
                    philosophical_anchoring=[],
                    anchored_premises=[],
                    wisdom_injected=[]
                )
                components.append(component)
        
        return AnalysisSelection(
            entry_point="fact",
            components=components,
            execution_order=fallback_modules,
            total_modules=len(components),
            total_premises=0,
            selection_rationale="Fallback selection due to processing error"
        )
    
    def format_for_prompt(self, selection: AnalysisSelection) -> str:
        """
        Format selected analysis components for RAI prompt
        
        Returns the full nested structure with modules and their anchored premises
        """
        
        if not selection.components:
            return ""
        
        formatted_parts = []
        
        # Header
        formatted_parts.append("**SELECTED RAI ANALYSIS COMPONENTS:**")
        formatted_parts.append("")
        formatted_parts.append(f"**Entry Point:** {selection.entry_point.title()}-Level Analysis")
        formatted_parts.append(f"**Execution Order:** {' → '.join(selection.execution_order)}")
        formatted_parts.append("")
        
        # Components with nested structure
        for component in selection.components:
            formatted_parts.append(f"**{component.module_id}: {component.module_name}**")
            formatted_parts.append(f"*Purpose:* {component.module_purpose}")
            formatted_parts.append("")
            
            # Core questions
            if component.core_questions:
                formatted_parts.append("*Core Questions:*")
                for question in component.core_questions:
                    formatted_parts.append(f"• {question}")
                formatted_parts.append("")
            
            # Philosophical anchoring (nested with full content)
            if component.anchored_premises:
                formatted_parts.append("*Philosophical Anchoring:*")
                for premise in component.anchored_premises:
                    formatted_parts.append(f"• **{premise['id']}**: {premise['title']}")
                    formatted_parts.append(f"  {premise['content']}")
                formatted_parts.append("")
            
            # Wisdom injected
            if component.wisdom_injected:
                formatted_parts.append("*Wisdom Guidance:*")
                for wisdom in component.wisdom_injected:
                    formatted_parts.append(f"• *{wisdom}*")
                formatted_parts.append("")
            
            formatted_parts.append("---")
            formatted_parts.append("")
        
        # Selection rationale
        formatted_parts.append(f"**Selection Rationale:** {selection.selection_rationale}")
        formatted_parts.append("")
        
        return "\n".join(formatted_parts)
    
    def get_component_summary(self, selection: AnalysisSelection) -> Dict[str, Any]:
        """Get summary information for integration with app.py"""
        
        # For compatibility with existing app.py structure
        return {
            "modules": selection.execution_order,
            "entry_point": selection.entry_point,
            "cross_level": [c.module_id for c in selection.components if c.module_id.startswith("CL")],
            "fact_level": [c.module_id for c in selection.components if c.module_id.startswith("FL")],
            "narrative_level": [c.module_id for c in selection.components if c.module_id.startswith("NL")],
            "system_level": [c.module_id for c in selection.components if c.module_id.startswith("SL")],
            "total_modules": selection.total_modules,
            "total_premises": selection.total_premises,
            "rationale": selection.selection_rationale,
            "formatted_components": self.format_for_prompt(selection)
        }

"""
# Example usage and testing
if __name__ == "__main__":
    from rai_wrapper import RAIWrapper
    
    # Initialize engines
    rai_wrapper = RAIWrapper()
    analytical_engine = AnalyticalEngine()
    
    # Test input
    test_input = "Western media coverage of Ukraine conflict shows clear bias and proves information warfare is real"
    
    # Process with RAI wrapper
    rai_result = rai_wrapper.process_input(test_input)
    rai_input = rai_result['rai_input']
    
    # Select analysis components
    selection = analytical_engine.select_analysis_components(rai_input, "guided")
    
    print("=== ANALYTICAL ENGINE RESULT ===")
    print(f"Entry Point: {selection.entry_point}")
    print(f"Total Modules: {selection.total_modules}")
    print(f"Total Premises: {selection.total_premises}")
    print(f"Execution Order: {' → '.join(selection.execution_order)}")
    print(f"Rationale: {selection.selection_rationale}")
    print("\n=== FORMATTED FOR PROMPT ===")
    print(analytical_engine.format_for_prompt(selection))
"""
# Example usage and testing
if __name__ == "__main__":
    from rai_wrapper import RAIWrapper
    
    # Initialize engines
    rai_wrapper = RAIWrapper()
    analytical_engine = AnalyticalEngine()
    
    # Test cases with different types of inputs
    test_cases = [
        {
            "name": "Information Warfare",
            "input": "Western media coverage of Ukraine conflict shows clear bias and proves information warfare is real",
            "expected_focus": "Information/Media analysis"
        },
        {
            "name": "Factual Dispute", 
            "input": "On March 15, 2024, reports confirmed that 50 civilians were killed in Mariupol bombing",
            "expected_focus": "Fact verification and sourcing"
        },
        {
            "name": "Power Analysis",
            "input": "The deep state controls government policy through unelected bureaucrats and corporate influence",
            "expected_focus": "Power dynamics and system analysis"
        },
        {
            "name": "Causal Narrative",
            "input": "NATO expansion led to Russian aggression because it threatened their security sphere",
            "expected_focus": "Causal logic and narrative analysis"
        },
        {
            "name": "Economic Argument",
            "input": "Rising debt levels will force governments to implement austerity measures affecting social programs",
            "expected_focus": "Economic power and resource control"
        },
        {
            "name": "Cultural Identity",
            "input": "American values of individual freedom are being eroded by collectivist ideologies from academia",
            "expected_focus": "Cultural analysis and identity framing"
        }
    ]
    
    print("=" * 80)
    print("ANALYTICAL ENGINE DYNAMIC TESTING")
    print("=" * 80)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 TEST CASE {i}: {test_case['name']}")
        print(f"Input: \"{test_case['input']}\"")
        print(f"Expected Focus: {test_case['expected_focus']}")
        print("-" * 60)
        
        try:
            # Process with RAI wrapper
            rai_result = rai_wrapper.process_input(test_case['input'])
            rai_input = rai_result['rai_input']
            
            # Select analysis components
            selection = analytical_engine.select_analysis_components(rai_input, "guided")
            
            # Display results
            print(f"📊 RESULTS:")
            print(f"   Entry Point: {selection.entry_point}")
            print(f"   Input Type: {rai_input.input_type.value}")
            print(f"   Complexity: {rai_input.complexity_score}/5")
            print(f"   Detected Topics: {', '.join(rai_input.detected_topics) if rai_input.detected_topics else 'None'}")
            print(f"   Selected Modules: {', '.join(selection.execution_order)}")
            print(f"   Total Premises: {selection.total_premises}")
            print(f"   Rationale: {selection.selection_rationale}")
            
            # Show module breakdown by level
            levels = {"CL": [], "FL": [], "NL": [], "SL": []}
            for comp in selection.components:
                level = comp.module_id.split('-')[0]
                if level in levels:
                    levels[level].append(comp.module_id)
            
            print(f"   Level Breakdown:")
            for level, modules in levels.items():
                if modules:
                    print(f"     {level}: {', '.join(modules)}")
            
            # Show philosophical anchoring summary
            all_premises = []
            for comp in selection.components:
                all_premises.extend(comp.philosophical_anchoring)
            unique_premises = list(set(all_premises))
            
            if unique_premises:
                print(f"   Philosophical Anchoring: {', '.join(sorted(unique_premises))}")
            
        except Exception as e:
            print(f"   ❌ ERROR: {str(e)}")
        
        print()
    
    print("=" * 80)
    print("🎯 ANALYSIS ACCURACY CHECK")
    print("=" * 80)
    print("Review the results above to assess:")
    print("• Does entry point selection make sense for each input type?")
    print("• Are the right modules being selected for each topic?")
    print("• Do philosophical premises align with the content?")
    print("• Is the selection rationale clear and logical?")
    print("=" * 80)