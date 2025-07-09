"""
RAI Analytical Engine - Unified Analysis Component Selection
Real Artificial Intelligence Framework Implementation

This module intelligently selects relevant RAI modules and their anchored premises
using semantic LLM-based analysis rather than mechanical keyword matching.
Replaces both module_selector.py and premise_engine.py with unified approach.
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
        
        This is where we replace keyword matching with intelligent selection
        based on module purposes and input context.
        """
        
        # Mode-based selection limits
        mode_limits = {
            "quick": min(max_modules, 4),
            "guided": min(max_modules, 6), 
            "expert": min(max_modules, 8)
        }
        
        limit = mode_limits.get(analysis_mode, 6)
        
        # Essential modules that should almost always be included
        essential_modules = ["CL-0"]  # Input normalization
        
        # Input type specific modules
        type_modules = {
            "factual_claim": ["FL-1", "FL-8", "FL-3"],
            "narrative": ["NL-1", "NL-2", "NL-3"], 
            "system_premise": ["SL-1", "SL-2", "SL-4"],
            "mixed": ["FL-1", "NL-1", "SL-1"]
        }
        
        # Topic-based modules
        topic_modules = {
            "geopolitical": ["SL-1", "SL-4", "FL-7"],
            "information": ["FL-2", "FL-3", "SL-8"],
            "power_governance": ["SL-1", "SL-2", "CL-4"],
            "systems": ["SL-6", "SL-8", "CL-2"]
        }
        
        # Start with essential modules
        selected = list(essential_modules)
        
        # Add input type modules
        input_type = rai_input.input_type.value
        type_specific = type_modules.get(input_type, type_modules["mixed"])
        for module in type_specific:
            if module not in selected and len(selected) < limit:
                selected.append(module)
        
        # Add topic-specific modules
        for topic in rai_input.detected_topics:
            topic_specific = topic_modules.get(topic, [])
            for module in topic_specific:
                if module not in selected and len(selected) < limit:
                    selected.append(module)
        
        # Add high-stakes modules if complexity/emotion is high
        if rai_input.complexity_score >= 4 or rai_input.emotional_charge >= 4:
            high_stakes = ["FL-7", "FL-9", "SL-8", "CL-4"]
            for module in high_stakes:
                if module not in selected and len(selected) < limit:
                    selected.append(module)
        
        # Ensure we have representation across levels if space allows
        levels_present = set(m.split('-')[0] for m in selected)
        if len(selected) < limit:
            for level in ["FL", "NL", "SL"]:
                if level not in levels_present:
                    # Add one module from missing level
                    level_modules = [m for m in type_specific if m.startswith(level)]
                    if level_modules and len(selected) < limit:
                        selected.append(level_modules[0])
        
        logger.info(f"Selected modules: {selected}")
        return selected[:limit]
    
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