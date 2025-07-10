"""
RAI Companion Flask Application v2
Real Artificial Intelligence Framework Implementation

Simplified Flask server with unified analytical engine.
"""

import os
import json
import logging
import traceback
from datetime import datetime
from typing import Dict, Any, Optional

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Import RAI framework components
try:
    from rai_wrapper import RAIWrapper
    from analytical_engine import AnalyticalEngine
    from api_dispatcher import APIDispatcher, ResponseStatus
    from output_parser import OutputParser
except ImportError as e:
    print(f"Warning: Could not import RAI components: {e}")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=[
    "https://r-a-i.org",
    "http://localhost:5000", 
    "http://127.0.0.1:5000"
])

# Global configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'rai-framework-secret-key-2025')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

class RAICompanion:
    """Simplified RAI Companion Application Manager"""
    
    def __init__(self, config_path: str = "config.json"):
        """Initialize RAI Companion with unified engine"""
        self.config = self._load_config(config_path)
        
        # Initialize RAI components
        try:
            self.rai_wrapper = RAIWrapper(config_path)
            self.analytical_engine = AnalyticalEngine()  # NEW: Unified engine
            self.api_dispatcher = APIDispatcher(config_path)
            self.output_parser = OutputParser()
            
            logger.info("RAI Companion v2 initialized successfully")
            self.components_loaded = True
            
        except Exception as e:
            logger.error(f"Failed to initialize RAI components: {str(e)}")
            self.components_loaded = False
    
    def _load_config(self, config_path: str = "config.json") -> Dict:
        """Load configuration with fallback"""
        try:
            with open("config.json", 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "app": {"debug": True, "port": 5000},
                "analysis": {"max_input_length": 10000, "timeout_seconds": 120},
                "models": {"gpt": "gpt-4", "gemini": "gemini-pro", "deepseek": "deepseek-chat"}
            }
    
    def get_available_models(self) -> Dict[str, str]:
        """Get available LLM models"""
        if self.components_loaded and self.api_dispatcher:
            try:
                available = self.api_dispatcher.get_available_models()
                return {model: model for model in available}
            except Exception as e:
                logger.error(f"Error getting available models: {e}")
        
        return self.config.get("models", {})
    
    def process_analysis_request(self, user_input: str, selected_llm: str, 
                               analysis_mode: str) -> Dict[str, Any]:
        """Main analysis processing pipeline - simplified"""
        
        try:
            # Validate input
            if not user_input or not selected_llm:
                return {"status": "error", "error": "Missing required fields"}
            
            max_length = self.config.get("analysis", {}).get("max_input_length", 10000)
            if len(user_input) > max_length:
                return {"status": "error", "error": f"Input too long. Max {max_length} characters."}
            
            logger.info(f"Processing: {len(user_input)} chars, model={selected_llm}, mode={analysis_mode}")
            
            # Step 1: Process input
            rai_result = self.rai_wrapper.process_input(user_input)
            if "error" in rai_result:
                return {"status": "error", "error": f"Input processing failed: {rai_result['error']}"}
            
            # Step 2: Select analysis components (unified - modules + premises)
            analysis_components = self.analytical_engine.select_analysis_components(
                rai_result["rai_input"], 
                analysis_mode
            )
            
            # Step 3: Build complete RAI prompt
            prompt = self._build_prompt(rai_result, analysis_components, analysis_mode)
            
            # Step 4: Send to LLM
            llm_response = self._call_llm(prompt, selected_llm)
            if "error" in llm_response:
                return llm_response
            
            # Step 5: Parse output
            parsed_result = self._parse_response(llm_response["response"], {
                "model": selected_llm,
                "mode": analysis_mode,
                "modules": analysis_components.total_modules,
                "premises": analysis_components.total_premises
            })
            
            # Step 6: Return result
            return {
                "status": "success",
                "analysis_result": parsed_result["html_content"],
                "metadata": {
                    "input_summary": parsed_result.get("input_summary", ""),
                    "processing_time": parsed_result.get("processing_time", None),
                    "model_used": selected_llm,
                    "analysis_mode": analysis_mode,
                    "modules_executed": analysis_components.total_modules,
                    "premises_applied": analysis_components.total_premises
                }
            }
            
        except Exception as e:
            logger.error(f"Analysis error: {str(e)}")
            return {"status": "error", "error": f"Processing failed: {str(e)}"}
    
    def _build_prompt(self, rai_result: Dict, analysis_components, analysis_mode: str) -> str:
        """Build RAI prompt - simplified"""
        
        prompt_parts = []
        
        # Framework activation
        prompt_parts.append("""
You are operating under the **Real Artificial Intelligence (RAI) Framework**.
Analyze with **factual precision**, **narrative coherence**, and **systemic insight**.
""")
        
        # Analysis mode
        mode_instructions = {
            "quick": "Provide final synthesis only - focus on conclusions",
            "guided": "Provide structured analysis with clear sections", 
            "expert": "Provide detailed analysis with module-by-module reasoning"
        }
        
        prompt_parts.append(f"""
**Analysis Mode:** {analysis_mode.title()}
**Output Style:** {mode_instructions.get(analysis_mode, 'Standard analysis')}
""")
        
        # Analysis components (modules + premises)
        prompt_parts.append(self.analytical_engine.format_for_prompt(analysis_components))
        
        # Input details
        rai_input = rai_result["rai_input"]
        prompt_parts.append(f"""
**Input to Analyze:**
"{rai_input.raw_input}"

**Input Classification:** {rai_input.input_type.value}
**Complexity:** {rai_input.complexity_score}/5
**Topics:** {', '.join(rai_input.detected_topics) if rai_input.detected_topics else 'General'}
""")
        
        # Analysis instructions
        prompt_parts.append(f"""
**Instructions:**
1. Apply the selected RAI modules systematically
2. Use philosophical anchoring as interpretive lenses
3. Structure your response with clear sections
4. Maintain epistemic humility - acknowledge uncertainties
5. Focus on adequacy over false neutrality

**Begin Analysis:**
""")
        
        return '\n'.join(prompt_parts)
    
    def _call_llm(self, prompt: str, selected_llm: str) -> Dict[str, Any]:
        """Call LLM with error handling"""
        
        try:
            if not self.components_loaded:
                return {"status": "error", "error": "LLM dispatcher unavailable"}
            
            # Map model names
            model_mapping = {
                "gpt": "gpt-4",
                "gemini": "gemini-pro", 
                "deepseek": "deepseek-chat"
            }
            
            model_alias = model_mapping.get(selected_llm, selected_llm)
            
            response = self.api_dispatcher.dispatch_to_llm(
                prompt, 
                model_alias,
                timeout=self.config.get("analysis", {}).get("timeout_seconds", 120)
            )
            
            if response.status != ResponseStatus.SUCCESS:
                return {"status": "error", "error": f"LLM request failed: {response.error_message}"}
            
            return {"response": response}
            
        except Exception as e:
            logger.error(f"LLM call error: {str(e)}")
            return {"status": "error", "error": f"LLM call failed: {str(e)}"}
        
    def _parse_response(self, llm_response, metadata: Dict) -> Dict[str, Any]:
        """Parse LLM response using the real output parser"""
        
        try:
            if self.components_loaded and self.output_parser:
                # Use the real parser
                parsed = self.output_parser.parse_llm_response(llm_response.content, metadata)
                return {
                    "html_content": parsed.html_content,
                    "input_summary": parsed.input_summary,
                    "processing_time": metadata.get("response_time", None)
                }
            else:
                # Fallback with cleaner styling
                return {
                    "html_content": f"""
                    <div class='rai-analysis-container' style='white-space: pre-wrap;'>
                        {self._convert_markdown_to_html(llm_response.content)}
                    </div>
                    """,
                    "input_summary": "Analysis completed",
                    "processing_time": None
                }
                
        except Exception as e:
            logger.error(f"Parse error: {str(e)}")
            # Clean fallback without ugly styling
            return {
                "html_content": f"""
                <div class='rai-analysis-container' style='white-space: pre-wrap;'>
                    {self._convert_markdown_to_html(llm_response.content)}
                </div>
                """,
                "input_summary": "Analysis completed with parsing error",
                "processing_time": None
            }

    def _convert_markdown_to_html(self, content: str) -> str:
        """Enhanced markdown to HTML conversion with better typography"""
        import re
        
        # First, handle the special first header (Final Synthesis)
        content = re.sub(
            r'^\*\*Final Synthesis[^*]*\*\*', 
            r'<div class="rai-final-synthesis-header">\g<0></div>', 
            content, 
            flags=re.MULTILINE
        )
        
        # Convert headers (keeping hierarchy)
        content = re.sub(r'^##### (.+)$', r'<h5>\1</h5>', content, flags=re.MULTILINE)
        content = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', content, flags=re.MULTILINE)  
        content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
        content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
        content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', content, flags=re.MULTILINE)
        
        # Remove # symbols from headers that are already bold
        content = re.sub(r'<h([1-6])># \*\*([^*]+)\*\*</h([1-6])>', r'<h\1>\2</h\3>', content)
        content = re.sub(r'<h([1-6])># (.+)</h([1-6])>', r'<h\1>\2</h\3>', content)
        
        # Convert bold and italic
        content = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', content)
        content = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', content)
        
        # Convert horizontal rules
        content = re.sub(r'^---+$', '<hr class="rai-section-divider">', content, flags=re.MULTILINE)
        
        # Process line by line for proper list and paragraph handling
        lines = content.split('\n')
        processed_lines = []
        in_ul = False
        in_ol = False
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Skip empty lines for now, we'll add spacing later
            if not line:
                i += 1
                continue
            
            # Check for bullet list items
            if re.match(r'^[-*+•] (.+)$', line):
                if not in_ul:
                    if in_ol:
                        processed_lines.append('</ol>')
                        in_ol = False
                    processed_lines.append('<ul class="rai-bullet-list">')
                    in_ul = True
                
                list_content = re.sub(r'^[-*+•] (.+)$', r'\1', line)
                processed_lines.append(f'<li class="rai-list-item">{list_content}</li>')
            
            # Check for numbered list items
            elif re.match(r'^\d+\. (.+)$', line):
                if not in_ol:
                    if in_ul:
                        processed_lines.append('</ul>')
                        in_ul = False
                    processed_lines.append('<ol class="rai-numbered-list">')
                    in_ol = True
                
                list_content = re.sub(r'^\d+\. (.+)$', r'\1', line)
                processed_lines.append(f'<li class="rai-list-item">{list_content}</li>')
            
            else:
                # Close any open lists
                if in_ul:
                    processed_lines.append('</ul>')
                    in_ul = False
                if in_ol:
                    processed_lines.append('</ol>')
                    in_ol = False
                
                # Handle other content
                if line.startswith('<'):
                    # Already HTML (headers, etc.)
                    processed_lines.append(line)
                else:
                    # Regular paragraph
                    processed_lines.append(f'<p class="rai-paragraph">{line}</p>')
            
            i += 1
        
        # Close any remaining open lists
        if in_ul:
            processed_lines.append('</ul>')
        if in_ol:
            processed_lines.append('</ol>')
        
        # Join with proper spacing
        return '\n'.join(processed_lines)

    def _generate_html(self, parsed_result) -> str:
        """Generate simple HTML for frontend"""
        
        html_parts = []
        
        for section in parsed_result.sections:
            html_parts.append(f'<div class="rai-section">')
            html_parts.append(f'<h3>{section.title}</h3>')
            html_parts.append(f'<div class="rai-content">{section.html_content}</div>')
            html_parts.append('</div>')
        
        return '\n'.join(html_parts)

# Initialize RAI Companion
rai_companion = RAICompanion()

# Flask Routes

@app.route('/')
def index():
    """Serve the main analysis form"""
    try:
        with open('analyst.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return """
        <html>
        <head><title>RAI Companion v2</title></head>
        <body>
            <h1>RAI Companion v2</h1>
            <form method="POST" action="/analyze">
                <textarea name="content" placeholder="Enter content to analyze" rows="10" cols="80"></textarea><br><br>
                <select name="model">
                    <option value="gpt">GPT-4</option>
                    <option value="gemini">Gemini</option>
                    <option value="deepseek">DeepSeek</option>
                </select><br><br>
                <input type="radio" name="mode" value="quick"> Quick
                <input type="radio" name="mode" value="guided" checked> Guided
                <input type="radio" name="mode" value="expert"> Expert<br><br>
                <button type="submit">Analyze</button>
            </form>
        </body>
        </html>
        """

@app.route('/analyze', methods=['POST'])
def analyze():
    """Main analysis endpoint"""
    try:
        # Handle both JSON and form data
        if request.is_json:
            data = request.get_json()
            user_input = data.get('user_input') or data.get('input')
            selected_llm = data.get('selected_llm') or data.get('model')
            analysis_mode = data.get('analysis_mode') or data.get('mode', 'guided')
        else:
            user_input = request.form.get('content')
            selected_llm = request.form.get('model')
            analysis_mode = request.form.get('mode', 'guided')
        
        # Validate
        if not user_input or not selected_llm:
            return jsonify({"status": "error", "error": "Missing required fields"}), 400
        
        # Process
        result = rai_companion.process_analysis_request(user_input, selected_llm, analysis_mode)
        
        # Return result
        status_code = 200 if result["status"] == "success" else 400
        return jsonify(result), status_code
        
    except Exception as e:
        logger.error(f"Analyze endpoint error: {str(e)}")
        return jsonify({"status": "error", "error": f"Server error: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "components_loaded": rai_companion.components_loaded,
        "available_models": list(rai_companion.get_available_models().keys())
    })

@app.route('/config', methods=['GET'])
def get_config():
    """Get configuration"""
    return jsonify({
        "available_models": rai_companion.get_available_models(),
        "analysis_modes": ["quick", "guided", "expert"],
        "max_input_length": rai_companion.config.get("analysis", {}).get("max_input_length", 10000)
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"status": "error", "error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({"status": "error", "error": "Internal server error"}), 500

if __name__ == '__main__':
    # Simple startup
    host = "0.0.0.0"
    port = int(os.environ.get("PORT", 5000))
    debug = rai_companion.config.get("app", {}).get("debug", True)
    
    logger.info(f"Starting RAI Companion v2 on {host}:{port}")
    
    app.run(host=host, port=port, debug=debug, threaded=True)