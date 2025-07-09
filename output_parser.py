"""
Simple RAI Output Parser v2 - Trust the LLM
Real Artificial Intelligence Framework Implementation

Minimal parser that trusts LLMs to format content intelligently.
Provides clean container and basic styling, lets content speak for itself.
"""

import re
import logging
from typing import Dict, Any
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ParsedResult:
    """Simple parsed result structure"""
    input_summary: str
    html_content: str
    sections_count: int
    processing_time: Any

class OutputParser:
    """
    Simple Output Parser - Trust the LLM
    
    Philosophy: LLMs are intelligent and format content well.
    Our job is to provide a clean container and basic styling.
    """
    
    def __init__(self):
        """Initialize with minimal styling rules"""
        pass
    
    def parse_llm_response(self, raw_response: str, metadata: Dict = None) -> ParsedResult:
        """
        Simple parsing - clean up and containerize LLM output
        
        Args:
            raw_response: Raw LLM response text
            metadata: Optional metadata
            
        Returns:
            ParsedResult with clean HTML
        """
        try:
            # Extract input summary (first line that mentions analysis)
            input_summary = self._extract_summary(raw_response)
            
            # Clean and format the content
            html_content = self._format_content(raw_response)
            
            # Count sections (rough estimate)
            sections_count = self._count_sections(raw_response)
            
            return ParsedResult(
                input_summary=input_summary,
                html_content=html_content,
                sections_count=sections_count,
                processing_time=metadata.get("response_time") if metadata else None
            )
            
        except Exception as e:
            logger.error(f"Parsing error: {str(e)}")
            return self._fallback_parse(raw_response)
    
    def _extract_summary(self, content: str) -> str:
        """Extract a simple summary from the beginning"""
        lines = content.split('\n')[:5]  # First 5 lines
        
        for line in lines:
            line = line.strip()
            # Look for lines that mention analysis, claim, or input
            if any(word in line.lower() for word in ['analyz', 'claim', 'input', 'statement']):
                # Clean up the line
                clean_line = re.sub(r'[#*]+', '', line).strip()
                if len(clean_line) > 10:
                    return clean_line
        
        return "RAI Analysis completed"
    
    def _format_content(self, content: str) -> str:
        """Format content with minimal, clean HTML"""
        
        # Split into lines for processing
        lines = content.split('\n')
        formatted_lines = []
        
        for line in lines:
            formatted_line = self._format_line(line)
            if formatted_line:  # Skip empty lines
                formatted_lines.append(formatted_line)
        
        # Wrap in container
        html_content = f"""
        <div class="rai-analysis-container">
            {''.join(formatted_lines)}
        </div>
        """
        
        return html_content
    
    def _format_line(self, line: str) -> str:
        """Format individual line with simple rules"""
        line = line.strip()
        
        if not line:
            return ""
        
        # Handle headings (### or **Text**)
        if line.startswith('###'):
            text = line.replace('###', '').strip()
            return f'<h3 class="rai-heading">{self._format_text(text)}</h3>\n'
        
        elif line.startswith('##'):
            text = line.replace('##', '').strip()
            return f'<h2 class="rai-section-title">{self._format_text(text)}</h2>\n'
        
        elif line.startswith('#'):
            text = line.replace('#', '').strip()
            return f'<h1 class="rai-main-title">{self._format_text(text)}</h1>\n'
        
        # Handle bullet points
        elif re.match(r'^[-•*+]\s+', line):
            text = re.sub(r'^[-•*+]\s+', '', line)
            return f'<li class="rai-bullet-item">{self._format_text(text)}</li>\n'
        
        # Handle numbered lists
        elif re.match(r'^\d+\.\s+', line):
            text = re.sub(r'^\d+\.\s+', '', line)
            return f'<li class="rai-numbered-item">{self._format_text(text)}</li>\n'
        
        # Handle emphasized lines (starting with emojis or **text**)
        elif re.match(r'^(⚠️|🔍|📊|✅|❌|💡|🎯|🧠|📈)', line):
            return f'<p class="rai-emphasis">{self._format_text(line)}</p>\n'
        
        elif line.startswith('**') and line.endswith('**'):
            text = line.strip('*').strip()
            return f'<h4 class="rai-subheading">{self._format_text(text)}</h4>\n'
        
        # Handle quotes
        elif line.startswith('>'):
            text = line[1:].strip()
            return f'<blockquote class="rai-quote">{self._format_text(text)}</blockquote>\n'
        
        # Regular paragraph
        else:
            return f'<p class="rai-paragraph">{self._format_text(line)}</p>\n'
    
    def _format_text(self, text: str) -> str:
        """Apply simple text formatting"""
        
        # Convert **bold** to <strong>
        text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
        
        # Convert *italic* to <em>
        text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
        
        # Convert `code` to <code>
        text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
        
        return text
    
    def _count_sections(self, content: str) -> int:
        """Rough count of sections"""
        # Count lines that look like major headings
        major_headings = len(re.findall(r'^#{1,3}\s+', content, re.MULTILINE))
        return max(major_headings, 1)
    
    def _fallback_parse(self, content: str) -> ParsedResult:
        """Fallback when parsing fails"""
        
        # Just wrap in a simple container
        html_content = f"""
        <div class="rai-analysis-container">
            <div class="rai-raw-content">
                <pre>{content}</pre>
            </div>
        </div>
        """
        
        return ParsedResult(
            input_summary="Analysis completed",
            html_content=html_content,
            sections_count=1,
            processing_time=None
        )


# Example usage
if __name__ == "__main__":
    parser = OutputParser()
    
    # Test with sample content
    test_content = """
    ### RAI Framework Analysis: "The deep state controls government policy"
    
    ## CL-0: Input Clarity and Narrative Normalization
    **Purpose:** Reframe the input into an analyzable claim.
    
    - **Input Type:** Claim (systemic assertion about power structures)
    - **Reframed Claim:** *Government policy is significantly influenced by unelected bureaucratic actors*
    
    **Philosophical Anchoring (D1.1, D6.2):**
    - Power shifts occur through elite consensus (**D1.1**)
    - Moral language may mask strategic interests (**D6.2**)
    
    ## Final Synthesis
    
    🎯 **Conclusion:** The claim is *partially adequate* but lacks nuance.
    
    **Key Findings:**
    1. Bureaucratic influence exists but varies by domain
    2. "Deep state" rhetoric serves political agendas
    3. More precise analysis needed
    
    > *Follow the gain, not the claim.*
    """
    
    result = parser.parse_llm_response(test_content)
    
    print("=== SIMPLE PARSER TEST ===")
    print(f"Summary: {result.input_summary}")
    print(f"Sections: {result.sections_count}")
    print(f"HTML length: {len(result.html_content)} chars")
    print("\n=== FORMATTED HTML ===")
    print(result.html_content)