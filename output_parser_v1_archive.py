"""
RAI Output Parser - LLM Response Formatting for Frontend
Real Artificial Intelligence Framework Implementation

This module parses LLM responses and formats them into structured, HTML-ready chunks
organized by RAI analysis levels (Fact → Narrative → System → Synthesis).
"""

import re
import json
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
import html
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SectionType(Enum):
    """RAI analysis section types"""
    FACT_LEVEL = "fact_level"
    NARRATIVE_LEVEL = "narrative_level"
    SYSTEM_LEVEL = "system_level"
    FINAL_SYNTHESIS = "final_synthesis"
    CROSS_LEVEL = "cross_level"
    EPISTEMIC_STATUS = "epistemic_status"

class ContentType(Enum):
    """Content formatting types"""
    HEADING = "heading"
    SUBHEADING = "subheading"
    PARAGRAPH = "paragraph"
    BULLET_LIST = "bullet_list"
    NUMBERED_LIST = "numbered_list"
    QUOTE = "quote"
    CALLOUT = "callout"
    WARNING = "warning"
    CONCLUSION = "conclusion"
    TABLE = "table"
    CODE_BLOCK = "code_block"

@dataclass
class ContentChunk:
    """Individual content chunk with formatting"""
    content_type: ContentType
    text: str
    level: int  # Heading level (1-6) or list depth
    metadata: Dict[str, Any]
    html_class: str
    raw_text: str

@dataclass
class ModuleOutput:
    """Parsed output from a specific RAI module"""
    module_id: str
    module_name: str
    chunks: List[ContentChunk]
    summary: str
    confidence_indicators: List[str]
    warnings: List[str]

@dataclass
class ParsedSection:
    """Complete parsed section (Fact/Narrative/System/Synthesis)"""
    section_type: SectionType
    title: str
    modules: List[ModuleOutput]
    overall_summary: str
    key_insights: List[str]
    confidence_score: Optional[float]
    html_content: str

@dataclass
class RAIAnalysisResult:
    """Complete parsed RAI analysis result"""
    input_summary: str
    sections: List[ParsedSection]
    execution_metadata: Dict[str, Any]
    html_structure: Dict[str, str]
    export_formats: Dict[str, str]

class OutputParser:
    """
    RAI Output Parser
    
    Transforms LLM responses into structured, HTML-ready content:
    - Identifies RAI sections and modules
    - Parses content into semantic chunks
    - Generates clean HTML with proper styling classes
    - Extracts key insights and confidence indicators
    - Creates export-ready formats
    """
    
    def __init__(self):
        """Initialize parser with formatting rules"""
        self.section_patterns = self._build_section_patterns()
        self.module_patterns = self._build_module_patterns()
        self.formatting_rules = self._build_formatting_rules()
        self.confidence_patterns = self._build_confidence_patterns()
        self.html_templates = self._build_html_templates()
        
    def _build_section_patterns(self) -> Dict[SectionType, List[str]]:
        """Build regex patterns for section detection"""
        return {
            SectionType.FACT_LEVEL: [
                r'(?i)(?:^|\n)\s*(?:\*\*|##|###)?\s*(?:fact[‐\-]?level|fl[‐\-]?analysis|factual\s+analysis)',
                r'(?i)(?:^|\n)\s*(?:\*\*|##|###)?\s*(?:step\s+)?(?:1|one)[:.]?\s*(?:fact|factual)',
                r'(?i)(?:^|\n)\s*(?:\*\*|##|###)?\s*fl[‐\-]?\d+',
                r'(?i)(?:^|\n)\s*(?:\*\*|##|###)?\s*(?:🔍|📊|✅).*(?:fact|claim|evidence)'
            ],
            SectionType.NARRATIVE_LEVEL: [
                r'(?i)(?:^|\n)\s*(?:\*\*|##|###)?\s*(?:narrative[‐\-]?level|nl[‐\-]?analysis|narrative\s+analysis)',
                r'(?i)(?:^|\n)\s*(?:\*\*|##|###)?\s*(?:step\s+)?(?:2|two)[:.]?\s*(?:narrative|story)',
                r'(?i)(?:^|\n)\s*(?:\*\*|##|###)?\s*nl[‐\-]?\d+',
                r'(?i)(?:^|\n)\s*(?:\*\*|##|###)?\s*(?:📖|🧠|📚).*(?:narrative|story|coherence)'
            ],
            SectionType.SYSTEM_LEVEL: [
                r'(?i)(?:^|\n)\s*(?:\*\*|##|###)?\s*(?:system[‐\-]?level|sl[‐\-]?analysis|systemic\s+analysis)',
                r'(?i)(?:^|\n)\s*(?:\*\*|##|###)?\s*(?:step\s+)?(?:3|three)[:.]?\s*(?:system|systemic)',
                r'(?i)(?:^|\n)\s*(?:\*\*|##|###)?\s*sl[‐\-]?\d+',
                r'(?i)(?:^|\n)\s*(?:\*\*|##|###)?\s*(?:🧠|⚙️|🔄).*(?:system|power|strategic)'
            ],
            SectionType.FINAL_SYNTHESIS: [
                r'(?i)(?:^|\n)\s*(?:\*\*|##|###)?\s*(?:final\s+synthesis|synthesis|conclusion|final\s+evaluation)',
                r'(?i)(?:^|\n)\s*(?:\*\*|##|###)?\s*(?:🧾|📋|✨).*(?:synthesis|conclusion|final)',
                r'(?i)(?:^|\n)\s*(?:\*\*|##|###)?\s*(?:overall|integrated|final)\s+(?:assessment|analysis|judgment)'
            ],
            SectionType.CROSS_LEVEL: [
                r'(?i)(?:^|\n)\s*(?:\*\*|##|###)?\s*(?:cross[‐\-]?level|cl[‐\-]?analysis|meta[‐\-]?analysis)',
                r'(?i)(?:^|\n)\s*(?:\*\*|##|###)?\s*cl[‐\-]?\d+',
                r'(?i)(?:^|\n)\s*(?:\*\*|##|###)?\s*(?:🎯|🔧|⚖️).*(?:cross|meta|framing)'
            ]
        }
    
    def _build_module_patterns(self) -> Dict[str, str]:
        """Build patterns for specific RAI module detection"""
        return {
            # Cross-Level modules
            "CL-0": r'(?i)(?:cl[‐\-]?0|input\s+clarity|narrative\s+normalization)',
            "CL-1": r'(?i)(?:cl[‐\-]?1|narrative\s+logic|compression)',
            "CL-2": r'(?i)(?:cl[‐\-]?2|epistemic\s+load|burden)',
            "CL-3": r'(?i)(?:cl[‐\-]?3|narrative\s+stack|tracking)',
            "CL-4": r'(?i)(?:cl[‐\-]?4|moral.*strategic|fusion)',
            "CL-5": r'(?i)(?:cl[‐\-]?5|symmetry|double\s+standard)',
            
            # Fact-Level modules
            "FL-1": r'(?i)(?:fl[‐\-]?1|claim\s+clarity|anchoring)',
            "FL-2": r'(?i)(?:fl[‐\-]?2|amplification|asymmetrical)',
            "FL-3": r'(?i)(?:fl[‐\-]?3|source.*independence|audit)',
            "FL-4": r'(?i)(?:fl[‐\-]?4|strategic\s+relevance|selection)',
            "FL-5": r'(?i)(?:fl[‐\-]?5|scale.*proportion|calibration)',
            "FL-6": r'(?i)(?:fl[‐\-]?6|primary\s+speech|neglected)',
            "FL-7": r'(?i)(?:fl[‐\-]?7|risk\s+context|adjustment)',
            "FL-8": r'(?i)(?:fl[‐\-]?8|time.*place|anchoring)',
            "FL-9": r'(?i)(?:fl[‐\-]?9|toxic\s+label|audit)',
            
            # Narrative-Level modules
            "NL-1": r'(?i)(?:nl[‐\-]?1|cause[‐\-]?effect|chain)',
            "NL-2": r'(?i)(?:nl[‐\-]?2|plausibility|coherence)',
            "NL-3": r'(?i)(?:nl[‐\-]?3|competing\s+narratives|contrast)',
            "NL-4": r'(?i)(?:nl[‐\-]?4|identity.*memory|group\s+interest)',
            "NL-5": r'(?i)(?:nl[‐\-]?5|allegory|analogy|symbol)',
            
            # System-Level modules
            "SL-1": r'(?i)(?:sl[‐\-]?1|power.*incentive|mapping)',
            "SL-2": r'(?i)(?:sl[‐\-]?2|institutional|enforcement)',
            "SL-3": r'(?i)(?:sl[‐\-]?3|memory\s+exploitation|identity)',
            "SL-4": r'(?i)(?:sl[‐\-]?4|function.*purpose|analysis)',
            "SL-5": r'(?i)(?:sl[‐\-]?5|resistance|inversion)',
            "SL-6": r'(?i)(?:sl[‐\-]?6|feedback\s+systems|loop)',
            "SL-7": r'(?i)(?:sl[‐\-]?7|forecast|predictive)',
            "SL-8": r'(?i)(?:sl[‐\-]?8|blind\s+spots|vulnerabilities)',
            "SL-9": r'(?i)(?:sl[‐\-]?9|evolution|adaptive)'
        }
    
    def _build_formatting_rules(self) -> Dict[str, Dict]:
        """Build content formatting rules"""
        return {
            "headings": {
                "pattern": r'^(#{1,6})\s+(.+)$',
                "class_prefix": "rai-heading-"
            },
            "bold_sections": {
                "pattern": r'\*\*([^*]+)\*\*',
                "class": "rai-emphasis"
            },
            "bullet_points": {
                "pattern": r'^[-•*+]\s+(.+)$',
                "class": "rai-bullet-item"
            },
            "numbered_points": {
                "pattern": r'^\d+\.\s+(.+)$',
                "class": "rai-numbered-item"
            },
            "quotes": {
                "pattern": r'^>\s+(.+)$',
                "class": "rai-quote"
            },
            "callouts": {
                "pattern": r'(?:⚠️|🔍|📊|✅|❌|💡|🎯|🧠|📈)\s*(.+)',
                "class": "rai-callout"
            },
            "epistemic_status": {
                "pattern": r'(?i)(?:status|confidence|evidence)[:]\s*([^.\n]+)',
                "class": "rai-epistemic"
            }
        }
    
    def _build_confidence_patterns(self) -> List[str]:
        """Build patterns for confidence/certainty indicators"""
        return [
            r'(?i)(?:high|strong|confident|certain|verified|confirmed)',
            r'(?i)(?:medium|moderate|partial|likely|probable)',
            r'(?i)(?:low|weak|uncertain|unclear|unverified|contested)',
            r'(?i)(?:unknown|insufficient|inadequate|missing)'
        ]
    
    def _build_html_templates(self) -> Dict[str, str]:
        """Build HTML templates for different content types"""
        return {
            "section_wrapper": '''
            <div class="rai-section rai-{section_type}" data-section="{section_type}">
                <div class="rai-section-header">
                    <h2 class="rai-section-title">{title}</h2>
                    {confidence_badge}
                </div>
                <div class="rai-section-content">
                    {content}
                </div>
                {summary_box}
            </div>
            ''',
            
            "module_wrapper": '''
            <div class="rai-module" data-module="{module_id}">
                <div class="rai-module-header">
                    <h3 class="rai-module-title">{module_name}</h3>
                    <span class="rai-module-id">{module_id}</span>
                </div>
                <div class="rai-module-content">
                    {content}
                </div>
                {warnings}
            </div>
            ''',
            
            "confidence_badge": '''
            <span class="rai-confidence rai-confidence-{level}">
                <i class="rai-confidence-icon"></i>
                Confidence: {level}
            </span>
            ''',
            
            "summary_box": '''
            <div class="rai-summary-box">
                <h4>Key Insights</h4>
                <ul class="rai-insights-list">
                    {insights}
                </ul>
            </div>
            ''',
            
            "warning_box": '''
            <div class="rai-warning-box">
                <i class="rai-warning-icon">⚠️</i>
                <span class="rai-warning-text">{text}</span>
            </div>
            ''',
            
            "callout_box": '''
            <div class="rai-callout rai-callout-{type}">
                <div class="rai-callout-icon">{icon}</div>
                <div class="rai-callout-content">{content}</div>
            </div>
            ''',
            
            "epistemic_status": '''
            <div class="rai-epistemic-status">
                <div class="rai-epistemic-header">Epistemic Status</div>
                <div class="rai-epistemic-items">
                    {items}
                </div>
            </div>
            ''',
            
            "navigation_menu": '''
            <nav class="rai-navigation">
                <ul class="rai-nav-list">
                    {nav_items}
                </ul>
            </nav>
            '''
        }
    
    def parse_llm_response(self, raw_response: str, metadata: Optional[Dict] = None) -> RAIAnalysisResult:
        """
        Main parsing function - converts LLM response to structured format
        
        Args:
            raw_response: Raw LLM response text
            metadata: Optional metadata (provider, model, etc.)
            
        Returns:
            RAIAnalysisResult with structured, HTML-ready content
        """
        try:
            # Step 1: Extract input summary
            input_summary = self._extract_input_summary(raw_response)
            
            # Step 2: Split response into sections
            raw_sections = self._split_into_sections(raw_response)
            
            # Step 3: Parse each section
            parsed_sections = []
            for section_type, content in raw_sections.items():
                if content.strip():
                    parsed_section = self._parse_section(section_type, content)
                    parsed_sections.append(parsed_section)
            
            # Step 4: Generate HTML structure
            html_structure = self._generate_html_structure(parsed_sections)
            
            # Step 5: Create export formats
            export_formats = self._generate_export_formats(parsed_sections)
            
            # Step 6: Build execution metadata
            execution_metadata = {
                "parsed_at": datetime.now().isoformat(),
                "sections_found": len(parsed_sections),
                "total_modules": sum(len(section.modules) for section in parsed_sections),
                "provider_metadata": metadata or {},
                "parsing_version": "1.0"
            }
            
            return RAIAnalysisResult(
                input_summary=input_summary,
                sections=parsed_sections,
                execution_metadata=execution_metadata,
                html_structure=html_structure,
                export_formats=export_formats
            )
            
        except Exception as e:
            logger.error(f"Error parsing LLM response: {str(e)}")
            return self._create_fallback_result(raw_response, str(e))
    
    def _extract_input_summary(self, response: str) -> str:
        """Extract or generate input summary"""
        
        # Look for explicit input summary
        summary_patterns = [
            r'(?i)(?:input\s+summary|analyzing|claim)[:]\s*([^.\n]+)',
            r'(?i)(?:the\s+claim|statement|input)[:]\s*["""]([^"""]+)["""]',
            r'(?i)(?:user\s+input|original\s+claim)[:]\s*(.+?)(?:\n|$)'
        ]
        
        for pattern in summary_patterns:
            match = re.search(pattern, response[:500])
            if match:
                return match.group(1).strip()
        
        # Fallback: extract first sentence mentioning analysis
        sentences = response.split('.')[:3]
        for sentence in sentences:
            if any(word in sentence.lower() for word in ['analyz', 'claim', 'statement', 'assert']):
                return sentence.strip()
        
        return "Analysis of user input"
    
    def _split_into_sections(self, response: str) -> Dict[SectionType, str]:
        """Split response into RAI sections"""
        sections = {}
        
        # Find section boundaries
        section_boundaries = []
        
        for section_type, patterns in self.section_patterns.items():
            for pattern in patterns:
                for match in re.finditer(pattern, response, re.MULTILINE):
                    section_boundaries.append({
                        'start': match.start(),
                        'end': match.end(),
                        'type': section_type,
                        'text': match.group()
                    })
        
        # Sort by position
        section_boundaries.sort(key=lambda x: x['start'])
        
        # Extract content between boundaries
        for i, boundary in enumerate(section_boundaries):
            start_pos = boundary['end']
            
            # Find end position (next section or end of text)
            if i + 1 < len(section_boundaries):
                end_pos = section_boundaries[i + 1]['start']
            else:
                end_pos = len(response)
            
            content = response[start_pos:end_pos].strip()
            sections[boundary['type']] = content
        
        # If no sections found, treat entire response as synthesis
        if not sections:
            sections[SectionType.FINAL_SYNTHESIS] = response
        
        return sections
    
    def _parse_section(self, section_type: SectionType, content: str) -> ParsedSection:
        """Parse individual section content"""
        
        # Extract modules within section
        modules = self._extract_modules(content)
        
        # Generate section title
        title = self._generate_section_title(section_type)
        
        # Extract key insights
        key_insights = self._extract_key_insights(content)
        
        # Calculate confidence score
        confidence_score = self._calculate_confidence_score(content)
        
        # Generate overall summary
        overall_summary = self._generate_section_summary(content, modules)
        
        # Generate HTML content
        html_content = self._generate_section_html(section_type, modules, content)
        
        return ParsedSection(
            section_type=section_type,
            title=title,
            modules=modules,
            overall_summary=overall_summary,
            key_insights=key_insights,
            confidence_score=confidence_score,
            html_content=html_content
        )
    
    def _extract_modules(self, content: str) -> List[ModuleOutput]:
        """Extract individual RAI modules from section content"""
        modules = []
        
        # Find module boundaries
        module_boundaries = []
        
        for module_id, pattern in self.module_patterns.items():
            for match in re.finditer(pattern, content, re.MULTILINE | re.IGNORECASE):
                module_boundaries.append({
                    'start': match.start(),
                    'module_id': module_id,
                    'match_text': match.group()
                })
        
        # Sort by position
        module_boundaries.sort(key=lambda x: x['start'])
        
        # Extract module content
        for i, boundary in enumerate(module_boundaries):
            module_id = boundary['module_id']
            start_pos = boundary['start']
            
            # Find end position
            if i + 1 < len(module_boundaries):
                end_pos = module_boundaries[i + 1]['start']
            else:
                end_pos = len(content)
            
            module_content = content[start_pos:end_pos].strip()
            
            if module_content:
                module = self._parse_module_content(module_id, module_content)
                modules.append(module)
        
        # If no modules detected, create a generic module
        if not modules:
            generic_module = self._parse_module_content("GENERIC", content)
            modules.append(generic_module)
        
        return modules
    
    def _parse_module_content(self, module_id: str, content: str) -> ModuleOutput:
        """Parse content for a specific module"""
        
        # Parse content into chunks
        chunks = self._parse_content_chunks(content)
        
        # Extract module name
        module_name = self._get_module_name(module_id)
        
        # Generate summary
        summary = self._generate_module_summary(content)
        
        # Extract confidence indicators
        confidence_indicators = self._extract_confidence_indicators(content)
        
        # Extract warnings
        warnings = self._extract_warnings(content)
        
        return ModuleOutput(
            module_id=module_id,
            module_name=module_name,
            chunks=chunks,
            summary=summary,
            confidence_indicators=confidence_indicators,
            warnings=warnings
        )
    
    def _parse_content_chunks(self, content: str) -> List[ContentChunk]:
        """Parse content into semantic chunks"""
        chunks = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            chunk = self._classify_content_line(line)
            if chunk:
                chunks.append(chunk)
        
        return chunks
    
    def _classify_content_line(self, line: str) -> Optional[ContentChunk]:
        """Classify a line of content and create appropriate chunk"""
        
        # Check for headings
        heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if heading_match:
            level = len(heading_match.group(1))
            text = heading_match.group(2)
            return ContentChunk(
                content_type=ContentType.HEADING,
                text=text,
                level=level,
                metadata={'heading_level': level},
                html_class=f"rai-heading-{level}",
                raw_text=line
            )
        
        # Check for bullet points
        if re.match(r'^[-•*+]\s+', line):
            text = re.sub(r'^[-•*+]\s+', '', line)
            return ContentChunk(
                content_type=ContentType.BULLET_LIST,
                text=text,
                level=1,
                metadata={'list_type': 'bullet'},
                html_class="rai-bullet-item",
                raw_text=line
            )
        
        # Check for numbered points
        numbered_match = re.match(r'^(\d+)\.\s+(.+)$', line)
        if numbered_match:
            number = numbered_match.group(1)
            text = numbered_match.group(2)
            return ContentChunk(
                content_type=ContentType.NUMBERED_LIST,
                text=text,
                level=1,
                metadata={'number': number, 'list_type': 'numbered'},
                html_class="rai-numbered-item",
                raw_text=line
            )
        
        # Check for quotes
        if line.startswith('>'):
            text = line[1:].strip()
            return ContentChunk(
                content_type=ContentType.QUOTE,
                text=text,
                level=1,
                metadata={'quote_type': 'blockquote'},
                html_class="rai-quote",
                raw_text=line
            )
        
        # Check for callouts with emojis
        callout_match = re.match(r'^(⚠️|🔍|📊|✅|❌|💡|🎯|🧠|📈)\s*(.+)$', line)
        if callout_match:
            icon = callout_match.group(1)
            text = callout_match.group(2)
            callout_type = self._get_callout_type(icon)
            return ContentChunk(
                content_type=ContentType.CALLOUT,
                text=text,
                level=1,
                metadata={'icon': icon, 'callout_type': callout_type},
                html_class=f"rai-callout rai-callout-{callout_type}",
                raw_text=line
            )
        
        # Check for strong emphasis (bold text)
        if '**' in line:
            return ContentChunk(
                content_type=ContentType.PARAGRAPH,
                text=line,
                level=1,
                metadata={'has_emphasis': True},
                html_class="rai-paragraph rai-has-emphasis",
                raw_text=line
            )
        
        # Default to paragraph
        return ContentChunk(
            content_type=ContentType.PARAGRAPH,
            text=line,
            level=1,
            metadata={},
            html_class="rai-paragraph",
            raw_text=line
        )
    
    def _get_callout_type(self, icon: str) -> str:
        """Get callout type based on emoji"""
        callout_types = {
            '⚠️': 'warning',
            '🔍': 'analysis',
            '📊': 'data',
            '✅': 'success',
            '❌': 'error',
            '💡': 'insight',
            '🎯': 'conclusion',
            '🧠': 'thinking',
            '📈': 'trend'
        }
        return callout_types.get(icon, 'info')
    
    def _get_module_name(self, module_id: str) -> str:
        """Get human-readable module name"""
        module_names = {
            "CL-0": "Input Clarity and Narrative Normalization",
            "CL-1": "Narrative Logic Compression", 
            "CL-2": "Epistemic Load Balance",
            "CL-3": "Narrative Stack Tracking",
            "CL-4": "Moral and Strategic Fusion Detection",
            "CL-5": "Evaluative Symmetry Enforcement",
            
            "FL-1": "Claim Clarity and Anchoring",
            "FL-2": "Asymmetrical Amplification Awareness",
            "FL-3": "Source Independence Audit",
            "FL-4": "Strategic Relevance and Selection",
            "FL-5": "Scale and Proportion Calibration",
            "FL-6": "Neglected Primary Speech Recognition",
            "FL-7": "Risk Context Adjustment",
            "FL-8": "Time & Place Anchoring",
            "FL-9": "Toxic Label Audit",
            
            "NL-1": "Cause-Effect Chain Analysis",
            "NL-2": "Narrative Plausibility & Internal Coherence",
            "NL-3": "Competing Narratives Contrast",
            "NL-4": "Identity, Memory, and Group Interest Framing",
            "NL-5": "Allegory, Analogy, and Symbol Injection",
            
            "SL-1": "Power and Incentive Mapping",
            "SL-2": "Institutional Behavior and Enforcement Patterns", 
            "SL-3": "Identity and Memory Exploitation",
            "SL-4": "Function and Purpose Analysis",
            "SL-5": "Systemic Resistance and Inversion",
            "SL-6": "Feedback Systems and Loop Control",
            "SL-7": "Strategic Forecast and Predictive Testing",
            "SL-8": "Systemic Blind Spots and Vulnerabilities",
            "SL-9": "Adaptive Evolution Awareness"
        }
        return module_names.get(module_id, f"Module {module_id}")
    
    def _generate_section_title(self, section_type: SectionType) -> str:
        """Generate human-readable section title"""
        titles = {
            SectionType.FACT_LEVEL: "Fact-Level Analysis",
            SectionType.NARRATIVE_LEVEL: "Narrative-Level Analysis", 
            SectionType.SYSTEM_LEVEL: "System-Level Analysis",
            SectionType.FINAL_SYNTHESIS: "Final Synthesis",
            SectionType.CROSS_LEVEL: "Cross-Level Meta-Analysis",
            SectionType.EPISTEMIC_STATUS: "Epistemic Status Assessment"
        }
        return titles.get(section_type, section_type.value.replace('_', ' ').title())
    
    def _extract_key_insights(self, content: str) -> List[str]:
        """Extract key insights from content"""
        insights = []
        
        # Look for explicit insight markers
        insight_patterns = [
            r'(?i)(?:key\s+(?:insight|finding|point))[:]\s*(.+)',
            r'(?i)(?:importantly?|crucially?|notably?)[:]\s*(.+)',
            r'(?i)(?:💡|🎯|⭐)\s*(.+)',
            r'(?i)(?:conclusion|finding)[:]\s*(.+)'
        ]
        
        for pattern in insight_patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            for match in matches:
                cleaned = re.sub(r'[*#]+', '', match).strip()
                if len(cleaned) > 10:  # Filter out too short insights
                    insights.append(cleaned)
        
        # Extract sentences with high confidence indicators
        sentences = re.split(r'[.!?]', content)
        for sentence in sentences:
            if any(indicator in sentence.lower() for indicator in 
                   ['clearly', 'definitely', 'demonstrates', 'proves', 'confirms']):
                cleaned = sentence.strip()
                if 20 < len(cleaned) < 150:  # Reasonable length
                    insights.append(cleaned)
        
        return insights[:5]  # Limit to top 5 insights
    
    def _calculate_confidence_score(self, content: str) -> Optional[float]:
        """Calculate confidence score based on language indicators"""
        
        # High confidence indicators
        high_confidence = ['confirmed', 'verified', 'clearly', 'definitely', 'proven', 'certain']
        medium_confidence = ['likely', 'probable', 'suggests', 'indicates', 'appears']
        low_confidence = ['unclear', 'uncertain', 'possibly', 'maybe', 'contested', 'disputed']
        
        content_lower = content.lower()
        
        high_count = sum(1 for word in high_confidence if word in content_lower)
        medium_count = sum(1 for word in medium_confidence if word in content_lower)
        low_count = sum(1 for word in low_confidence if word in content_lower)
        
        total_indicators = high_count + medium_count + low_count
        
        if total_indicators == 0:
            return None
        
        # Calculate weighted score
        score = (high_count * 1.0 + medium_count * 0.6 + low_count * 0.2) / total_indicators
        return round(score, 2)
    
    def _generate_section_summary(self, content: str, modules: List[ModuleOutput]) -> str:
        """Generate overall section summary"""
        
        # Try to find explicit summary
        summary_patterns = [
            r'(?i)(?:summary|overview|in\s+summary)[:]\s*(.+?)(?:\n\n|\n$|$)',
            r'(?i)(?:overall|in\s+conclusion)[:]\s*(.+?)(?:\n\n|\n$|$)'
        ]
        
        for pattern in summary_patterns:
            match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
            if match:
                return match.group(1).strip()
        
        # Generate summary from module summaries
        if modules:
            module_summaries = [m.summary for m in modules if m.summary]
            if module_summaries:
                return " ".join(module_summaries[:2])  # First 2 module summaries
        
        # Fallback: first substantial sentence
        sentences = re.split(r'[.!?]', content)
        for sentence in sentences:
            if len(sentence.strip()) > 30:
                return sentence.strip()
        
        return "Analysis completed with available information."
    
    def _generate_module_summary(self, content: str) -> str:
        """Generate summary for individual module"""
        sentences = re.split(r'[.!?]', content)
        
        # Find the most substantial sentence
        best_sentence = ""
        for sentence in sentences:
            cleaned = sentence.strip()
            if 20 < len(cleaned) < 200 and not cleaned.startswith(('**', '#', '-', '•')):
                if len(cleaned) > len(best_sentence):
                    best_sentence = cleaned
        
        return best_sentence or "Module analysis completed."
    
    def _extract_confidence_indicators(self, content: str) -> List[str]:
        """Extract confidence/certainty indicators"""
        indicators = []
        
        # Pattern for epistemic status blocks
        status_pattern = r'(?i)(?:status|confidence|evidence)[:]\s*([^.\n]+)'
        matches = re.findall(status_pattern, content)
        indicators.extend(matches)
        
        # Pattern for confidence expressions
        confidence_patterns = [
            r'(?i)(high|strong|confident|certain)\s+(?:confidence|certainty|evidence)',
            r'(?i)(low|weak|uncertain|unclear)\s+(?:confidence|certainty|evidence)',
            r'(?i)(verified|confirmed|proven|established)',
            r'(?i)(unverified|unconfirmed|disputed|contested)'
        ]
        
        for pattern in confidence_patterns:
            matches = re.findall(pattern, content)
            indicators.extend(matches)
        
        return list(set(indicators))  # Remove duplicates
    
    def _extract_warnings(self, content: str) -> List[str]:
        """Extract warnings and caveats"""
        warnings = []
        
        # Warning patterns
        warning_patterns = [
            r'(?i)(?:⚠️|warning|caution|note)[:]\s*(.+?)(?:\n|$)',
            r'(?i)(?:however|but|although|caveat)[:]\s*(.+?)(?:\n|$)',
            r'(?i)(?:limitation|uncertainty|gap)[:]\s*(.+?)(?:\n|$)'
        ]
        
        for pattern in warning_patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            for match in matches:
                cleaned = match.strip()
                if len(cleaned) > 10:
                    warnings.append(cleaned)
        
        return warnings
    
    def _generate_section_html(self, section_type: SectionType, modules: List[ModuleOutput], content: str) -> str:
        """Generate HTML for section"""
        
        html_parts = []
        
        # Generate module HTML
        for module in modules:
            module_html = self._generate_module_html(module)
            html_parts.append(module_html)
        
        # If no modules, convert content directly
        if not modules:
            chunks = self._parse_content_chunks(content)
            content_html = self._chunks_to_html(chunks)
            html_parts.append(content_html)
        
        return '\n'.join(html_parts)
    
    def _generate_module_html(self, module: ModuleOutput) -> str:
        """Generate HTML for individual module"""
        
        # Convert chunks to HTML
        content_html = self._chunks_to_html(module.chunks)
        
        # Add warnings if any
        warnings_html = ""
        if module.warnings:
            warning_items = []
            for warning in module.warnings:
                warning_items.append(self.html_templates["warning_box"].format(text=html.escape(warning)))
            warnings_html = '\n'.join(warning_items)
        
        # Use module template
        return self.html_templates["module_wrapper"].format(
            module_id=module.module_id,
            module_name=html.escape(module.module_name),
            content=content_html,
            warnings=warnings_html
        )
    
    def _chunks_to_html(self, chunks: List[ContentChunk]) -> str:
        """Convert content chunks to HTML"""
        html_parts = []
        
        current_list = None
        list_items = []
        
        for chunk in chunks:
            if chunk.content_type in [ContentType.BULLET_LIST, ContentType.NUMBERED_LIST]:
                # Handle lists
                if current_list != chunk.content_type:
                    # Close previous list
                    if current_list and list_items:
                        html_parts.append(self._close_list(current_list, list_items))
                        list_items = []
                    current_list = chunk.content_type
                
                # Add list item
                list_items.append(f'<li class="{chunk.html_class}">{self._format_text(chunk.text)}</li>')
            
            else:
                # Close any open list
                if current_list and list_items:
                    html_parts.append(self._close_list(current_list, list_items))
                    current_list = None
                    list_items = []
                
                # Generate HTML for chunk
                chunk_html = self._chunk_to_html(chunk)
                html_parts.append(chunk_html)
        
        # Close final list if needed
        if current_list and list_items:
            html_parts.append(self._close_list(current_list, list_items))
        
        return '\n'.join(html_parts)
    
    def _chunk_to_html(self, chunk: ContentChunk) -> str:
        """Convert individual chunk to HTML"""
        
        if chunk.content_type == ContentType.HEADING:
            tag = f"h{min(chunk.level + 2, 6)}"  # Adjust heading levels for nested structure
            return f'<{tag} class="{chunk.html_class}">{self._format_text(chunk.text)}</{tag}>'
        
        elif chunk.content_type == ContentType.PARAGRAPH:
            return f'<p class="{chunk.html_class}">{self._format_text(chunk.text)}</p>'
        
        elif chunk.content_type == ContentType.QUOTE:
            return f'<blockquote class="{chunk.html_class}">{self._format_text(chunk.text)}</blockquote>'
        
        elif chunk.content_type == ContentType.CALLOUT:
            icon = chunk.metadata.get('icon', '💡')
            callout_type = chunk.metadata.get('callout_type', 'info')
            return self.html_templates["callout_box"].format(
                type=callout_type,
                icon=icon,
                content=self._format_text(chunk.text)
            )
        
        else:
            # Default to paragraph
            return f'<p class="{chunk.html_class}">{self._format_text(chunk.text)}</p>'
    
    def _close_list(self, list_type: ContentType, items: List[str]) -> str:
        """Close a list and return HTML"""
        if list_type == ContentType.NUMBERED_LIST:
            return f'<ol class="rai-numbered-list">{"".join(items)}</ol>'
        else:
            return f'<ul class="rai-bullet-list">{"".join(items)}</ul>'
    
    def _format_text(self, text: str) -> str:
        """Format text with markdown-like styling"""
        
        # Escape HTML first
        formatted = html.escape(text)
        
        # Convert **bold** to <strong>
        formatted = re.sub(r'\*\*([^*]+)\*\*', r'<strong class="rai-emphasis">\1</strong>', formatted)
        
        # Convert *italic* to <em>
        formatted = re.sub(r'\*([^*]+)\*', r'<em class="rai-italic">\1</em>', formatted)
        
        # Convert `code` to <code>
        formatted = re.sub(r'`([^`]+)`', r'<code class="rai-code">\1</code>', formatted)
        
        return formatted
    
    def _generate_html_structure(self, sections: List[ParsedSection]) -> Dict[str, str]:
        """Generate complete HTML structure"""
        
        # Generate navigation
        nav_items = []
        for section in sections:
            nav_items.append(
                f'<li><a href="#{section.section_type.value}" class="rai-nav-link">'
                f'{section.title}</a></li>'
            )
        
        navigation_html = self.html_templates["navigation_menu"].format(
            nav_items='\n'.join(nav_items)
        )
        
        # Generate section HTML
        sections_html = []
        for section in sections:
            
            # Generate confidence badge
            confidence_badge = ""
            if section.confidence_score is not None:
                level = "high" if section.confidence_score > 0.7 else "medium" if section.confidence_score > 0.4 else "low"
                confidence_badge = self.html_templates["confidence_badge"].format(
                    level=level
                )
            
            # Generate summary box
            summary_box = ""
            if section.key_insights:
                insights_html = '\n'.join(f'<li>{html.escape(insight)}</li>' for insight in section.key_insights)
                summary_box = self.html_templates["summary_box"].format(
                    insights=insights_html
                )
            
            # Generate section HTML
            section_html = self.html_templates["section_wrapper"].format(
                section_type=section.section_type.value,
                title=html.escape(section.title),
                confidence_badge=confidence_badge,
                content=section.html_content,
                summary_box=summary_box
            )
            
            sections_html.append(section_html)
        
        return {
            "navigation": navigation_html,
            "sections": '\n'.join(sections_html),
            "complete": navigation_html + '\n' + '\n'.join(sections_html)
        }
    
    def _generate_export_formats(self, sections: List[ParsedSection]) -> Dict[str, str]:
        """Generate export formats (markdown, plain text, etc.)"""
        
        # Generate Markdown
        markdown_parts = []
        markdown_parts.append("# RAI Analysis Report\n")
        
        for section in sections:
            markdown_parts.append(f"## {section.title}\n")
            
            if section.overall_summary:
                markdown_parts.append(f"**Summary:** {section.overall_summary}\n")
            
            for module in section.modules:
                markdown_parts.append(f"### {module.module_name} ({module.module_id})\n")
                
                for chunk in module.chunks:
                    if chunk.content_type == ContentType.HEADING:
                        markdown_parts.append(f"{'#' * (chunk.level + 3)} {chunk.text}\n")
                    elif chunk.content_type == ContentType.BULLET_LIST:
                        markdown_parts.append(f"- {chunk.text}\n")
                    elif chunk.content_type == ContentType.NUMBERED_LIST:
                        markdown_parts.append(f"1. {chunk.text}\n")
                    else:
                        markdown_parts.append(f"{chunk.text}\n")
                
                markdown_parts.append("\n")
            
            if section.key_insights:
                markdown_parts.append("**Key Insights:**\n")
                for insight in section.key_insights:
                    markdown_parts.append(f"- {insight}\n")
                markdown_parts.append("\n")
        
        # Generate Plain Text
        plain_text = re.sub(r'<[^>]+>', '', '\n'.join(markdown_parts))
        plain_text = re.sub(r'\*\*([^*]+)\*\*', r'\1', plain_text)
        plain_text = re.sub(r'\*([^*]+)\*', r'\1', plain_text)
        
        # Generate JSON
        json_data = {
            "sections": [
                {
                    "type": section.section_type.value,
                    "title": section.title,
                    "summary": section.overall_summary,
                    "confidence": section.confidence_score,
                    "insights": section.key_insights,
                    "modules": [
                        {
                            "id": module.module_id,
                            "name": module.module_name,
                            "summary": module.summary,
                            "confidence_indicators": module.confidence_indicators,
                            "warnings": module.warnings
                        }
                        for module in section.modules
                    ]
                }
                for section in sections
            ]
        }
        
        return {
            "markdown": '\n'.join(markdown_parts),
            "plain_text": plain_text,
            "json": json.dumps(json_data, indent=2)
        }
    
    def _create_fallback_result(self, raw_response: str, error: str) -> RAIAnalysisResult:
        """Create fallback result when parsing fails"""
        
        # Create basic chunks from raw response
        chunks = []
        paragraphs = raw_response.split('\n\n')
        
        for para in paragraphs[:5]:  # Limit to first 5 paragraphs
            if para.strip():
                chunk = ContentChunk(
                    content_type=ContentType.PARAGRAPH,
                    text=para.strip(),
                    level=1,
                    metadata={},
                    html_class="rai-paragraph",
                    raw_text=para
                )
                chunks.append(chunk)
        
        # Create fallback module
        fallback_module = ModuleOutput(
            module_id="FALLBACK",
            module_name="Response Content",
            chunks=chunks,
            summary="Raw LLM response (parsing failed)",
            confidence_indicators=[],
            warnings=[f"Parsing error: {error}"]
        )
        
        # Create fallback section
        fallback_section = ParsedSection(
            section_type=SectionType.FINAL_SYNTHESIS,
            title="Analysis Response",
            modules=[fallback_module],
            overall_summary="Response parsing encountered errors",
            key_insights=[],
            confidence_score=None,
            html_content=self._generate_module_html(fallback_module)
        )
        
        return RAIAnalysisResult(
            input_summary="Input analysis",
            sections=[fallback_section],
            execution_metadata={
                "parsed_at": datetime.now().isoformat(),
                "parsing_error": error,
                "fallback_used": True
            },
            html_structure={"complete": fallback_section.html_content},
            export_formats={"plain_text": raw_response}
        )
    
    def to_json(self, result: RAIAnalysisResult) -> str:
        """Convert result to JSON string"""
        return json.dumps(asdict(result), indent=2, default=str)
    
    def to_dict(self, result: RAIAnalysisResult) -> Dict:
        """Convert result to dictionary"""
        return asdict(result)


# Example usage and testing
if __name__ == "__main__":
    # Initialize parser
    parser = OutputParser()
    
    # Test with sample RAI response
    sample_response = """
    **Analyzing:** "The media shows clear bias in political coverage."
    
    ## Fact-Level Analysis
    
    ### FL-1: Claim Clarity and Anchoring
    
    **Cleaned Claim:** Media organizations demonstrate systematic bias in political coverage.
    
    - ✅ **Verifiability:** Medium - Observable through content analysis
    - ⚠️ **Specificity:** Low - "bias" and "media" need definition
    - 📍 **Anchoring:** Missing time frame and specific outlets
    
    The claim lacks temporal and institutional specificity. "Media" could refer to mainstream news, social media, or alternative outlets.
    
    ### FL-2: Asymmetrical Amplification Awareness
    
    💡 **Key Finding:** Bias accusations themselves follow amplification patterns
    
    - Different political groups cite different evidence
    - Conservative sources emphasize liberal media bias
    - Liberal sources emphasize conservative media bias
    
    ## Narrative-Level Analysis
    
    ### NL-1: Cause-Effect Chain Analysis
    
    **Causal Logic:** Media bias → Distorted public perception → Political polarization
    
    🧠 **Chain Coherence:** Partially valid but oversimplified
    - Media influence on perception: Well-documented
    - Bias as sole cause of polarization: Questionable
    - Alternative causes: Social media algorithms, partisan sorting
    
    ### NL-3: Competing Narratives Contrast
    
    **Alternative Framings:**
    1. **Market Response:** Media caters to audience preferences
    2. **Structural:** Business models incentivize engagement over accuracy
    3. **Democratic:** Multiple perspectives reflect healthy pluralism
    
    ## System-Level Analysis
    
    ### SL-1: Power and Incentive Mapping
    
    🎯 **Strategic Function:** Bias accusations serve to:
    - Discredit unfavorable coverage
    - Rally in-group support
    - Justify alternative information sources
    
    **Beneficiaries:**
    - Political actors seeking to deflect criticism
    - Alternative media platforms
    - Polarization entrepreneurs
    
    ### SL-4: Function and Purpose Analysis
    
    ⚠️ **Warning:** "Bias" accusations can be weaponized regardless of accuracy
    
    The claim functions as both:
    - Legitimate media criticism
    - Strategic narrative weapon
    
    ## Final Synthesis
    
    🧾 **Integrated Assessment:**
    
    **Fact Status:** Partially verified - Media bias exists but varies by outlet and definition
    **Narrative Coherence:** Oversimplified - Ignores market dynamics and audience agency  
    **System Function:** Strategic - Often serves political rather than epistemic goals
    
    **Key Insights:**
    - Media bias is measurable but context-dependent
    - Bias accusations follow predictable patterns
    - Focus on "bias" may distract from deeper structural issues
    
    **Epistemic Status:** Medium confidence - Well-studied phenomenon with contested interpretations
    """
    
    # Parse the response
    result = parser.parse_llm_response(sample_response)
    
    print("=== PARSING RESULT ===")
    print(f"Input Summary: {result.input_summary}")
    print(f"Sections Found: {len(result.sections)}")
    print(f"Total Modules: {result.execution_metadata['total_modules']}")
    
    print("\n=== SECTION BREAKDOWN ===")
    for section in result.sections:
        print(f"\n**{section.title}**")
        print(f"  Modules: {len(section.modules)}")
        print(f"  Confidence: {section.confidence_score}")
        print(f"  Key Insights: {len(section.key_insights)}")
        
        for insight in section.key_insights[:2]:
            print(f"    - {insight}")
    
    print("\n=== HTML STRUCTURE ===")
    print("Navigation HTML:", len(result.html_structure.get("navigation", "")), "characters")
    print("Sections HTML:", len(result.html_structure.get("sections", "")), "characters")
    
    print("\n=== EXPORT FORMATS ===")
    print("Markdown:", len(result.export_formats.get("markdown", "")), "characters")
    print("Plain Text:", len(result.export_formats.get("plain_text", "")), "characters")
    print("JSON:", len(result.export_formats.get("json", "")), "characters")
    
    # Save sample output
    with open("sample_parsed_output.json", "w") as f:
        f.write(parser.to_json(result))
    
    print("\nSample output saved to 'sample_parsed_output.json'")
