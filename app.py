"""
RAI Companion Flask Application
Real Artificial Intelligence Framework Implementation

Main Flask server that orchestrates the complete RAI analysis pipeline:
1. Input processing and normalization
2. Premise selection and module selection
3. LLM dispatch and response handling
4. Output parsing and formatting
"""

import os
import json
import logging
import traceback
from datetime import datetime
from typing import Dict, Any, Optional

from flask import Flask, request, jsonify, render_template_string, send_from_directory
from flask_cors import CORS

# Import RAI framework components
try:
    from rai_wrapper import RAIWrapper
    from premise_engine import PremiseEngine
    from module_selector import ModuleSelector
    from api_dispatcher import APIDispatcher, ResponseStatus
    from output_parser import OutputParser
except ImportError as e:
    print(f"Warning: Could not import RAI components: {e}")
    print("Some functionality may be limited in development mode.")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('rai_app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Global configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'rai-framework-secret-key-2025')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max request size

class RAICompanion:
    """
    RAI Companion Application Manager
    
    Orchestrates the complete RAI analysis pipeline and manages
    all framework components with proper error handling and logging.
    """
    
    def __init__(self, config_path: str = "config.json"):
        """Initialize RAI Companion with all components"""
        self.config_path = config_path
        self.config = self._load_config()
        
        # Initialize RAI components
        try:
            self.rai_wrapper = RAIWrapper(config_path)
            self.premise_engine = PremiseEngine()
            self.module_selector = ModuleSelector()
            self.api_dispatcher = APIDispatcher(config_path)
            self.output_parser = OutputParser()
            
            logger.info("RAI Companion initialized successfully")
            self.components_loaded = True
            
        except Exception as e:
            logger.error(f"Failed to initialize RAI components: {str(e)}")
            self.components_loaded = False
            self._init_fallback_mode()
    
    def _load_config(self) -> Dict:
        """Load application configuration"""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                logger.info(f"Configuration loaded from {self.config_path}")
                return config
        except FileNotFoundError:
            logger.warning(f"Config file {self.config_path} not found, using defaults")
            return self._default_config()
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file: {e}")
            return self._default_config()
    
    def _default_config(self) -> Dict:
        """Default configuration fallback"""
        return {
            "app": {
                "name": "RAI Companion",
                "version": "1.0.0",
                "debug": True,
                "host": "localhost",
                "port": 5000
            },
            "analysis": {
                "default_mode": "full",
                "max_input_length": 10000,
                "timeout_seconds": 120
            },
            "models": {
                "gpt": "gpt-4",
                "gemini": "gemini-pro", 
                "deepseek": "deepseek-chat"
            }
        }
    
    def _init_fallback_mode(self):
        """Initialize fallback mode when components fail to load"""
        self.rai_wrapper = None
        self.premise_engine = None
        self.module_selector = None
        self.api_dispatcher = None
        self.output_parser = None
        logger.warning("Running in fallback mode - limited functionality")
    
    def get_available_models(self) -> Dict[str, str]:
        """Get available LLM models"""
        if self.components_loaded and self.api_dispatcher:
            try:
                available = self.api_dispatcher.get_available_models()
                return {model: model for model in available}
            except Exception as e:
                logger.error(f"Error getting available models: {e}")
        
        # Fallback to config models
        return self.config.get("models", {
            "gpt": "gpt-4",
            "gemini": "gemini-pro",
            "deepseek": "deepseek-chat"
        })
    
    def process_analysis_request(self, user_input: str, selected_llm: str, 
                               analysis_mode: str) -> Dict[str, Any]:
        """
        Main analysis processing pipeline
        
        Args:
            user_input: User's input text/claim
            selected_llm: Selected LLM model (gpt, gemini, deepseek)
            analysis_mode: Analysis mode (quick, guided, expert)
            
        Returns:
            Dict with analysis results or error information
        """
        try:
            # Input validation
            validation_result = self._validate_input(user_input, selected_llm, analysis_mode)
            if not validation_result["valid"]:
                return {
                    "status": "error",
                    "error": validation_result["error"],
                    "error_type": "validation"
                }
            
            logger.info(f"DEBUG STEP 0: Received input: '{user_input}'")
            logger.info(f"Starting analysis: model={selected_llm}, mode={analysis_mode}")
            
            # Step 1: Process input through RAI Wrapper
            rai_result = self._process_input_wrapper(user_input)
            logger.info(f"DEBUG STEP 1: RAI Wrapper result keys: {list(rai_result.keys())}")
            if 'input' in rai_result:
                logger.info(f"DEBUG STEP 1: Raw input in result: '{rai_result['input'].raw_input}'")
        
            if "error" in rai_result:
                return rai_result
            
            # Step 2: Select relevant premises
            premise_result = self._select_premises(rai_result["rai_input"])
            logger.info(f"DEBUG STEP 2: Premises selected: {len(premise_result.get('premises', []))}")
            if "error" in premise_result:
                return premise_result
            
            # Step 3: Select analysis modules
            module_result = self._select_modules(rai_result["rai_input"], analysis_mode)
            logger.info(f"DEBUG STEP 3: Modules selected: {len(module_result.get('modules', []))}")
            if "error" in module_result:
                return module_result
            
            # Step 4: Build complete RAI prompt
            complete_prompt = self._build_complete_prompt(
                rai_result, premise_result, module_result, analysis_mode
            )
            logger.info(f"DEBUG STEP 4: Prompt length: {len(complete_prompt)} chars")
            logger.info(f"DEBUG STEP 4: First 200 chars of prompt: {complete_prompt[:200]}")
            
            # Step 5: Dispatch to selected LLM
            llm_result = self._dispatch_to_llm(complete_prompt, selected_llm)
            if "error" in llm_result:
                return llm_result
            
            # Step 6: Parse and format output
            parsed_result = self._parse_output(llm_result["response"], {
                "model": selected_llm,
                "mode": analysis_mode,
                "premises": len(premise_result.get("premises", [])),
                "modules": len(module_result.get("modules", []))
            })
            
            # Step 7: Build final response
            return {
                "status": "success",
                "analysis_result": parsed_result["html_content"],
                "metadata": {
                    "input_summary": parsed_result.get("input_summary", ""),
                    "sections_analyzed": parsed_result.get("sections_count", 0),
                    "confidence_score": parsed_result.get("average_confidence", None),
                    "processing_time": parsed_result.get("processing_time", None),
                    "model_used": selected_llm,
                    "analysis_mode": analysis_mode,
                    "premises_applied": len(premise_result.get("premises", [])),
                    "modules_executed": len(module_result.get("modules", []))
                },
                "export_formats": parsed_result.get("export_formats", {}),
                "raw_response": llm_result["response"].content if self.config.get("debug", False) else None
            }
            
        except Exception as e:
            logger.error(f"Analysis processing error: {str(e)}")
            logger.error(traceback.format_exc())
            return {
                "status": "error",
                "error": f"Processing failed: {str(e)}",
                "error_type": "processing",
                "traceback": traceback.format_exc() if self.config.get("debug", False) else None
            }
    
    def _validate_input(self, user_input: str, selected_llm: str, 
                       analysis_mode: str) -> Dict[str, Any]:
        """Validate input parameters"""
        
        # Check input length
        max_length = self.config.get("analysis", {}).get("max_input_length", 10000)
        if len(user_input) > max_length:
            return {
                "valid": False,
                "error": f"Input too long. Maximum {max_length} characters allowed."
            }
        
        if len(user_input.strip()) < 10:
            return {
                "valid": False,
                "error": "Input too short. Please provide at least 10 characters."
            }
        
        # Check model availability
        available_models = self.get_available_models()
        if selected_llm not in available_models:
            return {
                "valid": False,
                "error": f"Model '{selected_llm}' not available. Available: {list(available_models.keys())}"
            }
        
        # Check analysis mode
        valid_modes = ["quick", "guided", "expert", "full"]  # full for backward compatibility
        if analysis_mode not in valid_modes:
            return {
                "valid": False,
                "error": f"Invalid analysis mode. Valid modes: {valid_modes}"
            }
        
        return {"valid": True}
    
    def _process_input_wrapper(self, user_input: str) -> Dict[str, Any]:
        """Process input through RAI Wrapper"""
        try:
            if not self.components_loaded or not self.rai_wrapper:
                # Fallback mode
                return {
                    "rai_input": self._create_fallback_input(user_input),
                    "config": {"output_mode": "brief"},
                    "prompt": f"Analyze this input using RAI framework: {user_input}"
                }
            
            result = self.rai_wrapper.process_input(user_input)
            
            if "error" in result:
                return {
                    "status": "error",
                    "error": f"Input processing failed: {result['error']}",
                    "error_type": "input_processing"
                }
            
            return result
            
        except Exception as e:
            logger.error(f"RAI Wrapper error: {str(e)}")
            return {
                "status": "error",
                "error": f"Input wrapper failed: {str(e)}",
                "error_type": "wrapper"
            }
    
    def _create_fallback_input(self, user_input: str):
        """Create fallback input object when RAI Wrapper is unavailable"""
        from dataclasses import dataclass
        from enum import Enum
        
        class InputType(Enum):
            MIXED = "mixed"
        
        @dataclass
        class FallbackInput:
            raw_input: str
            cleaned_input: str
            input_type: InputType
            style_flags: list
            emotional_charge: int
            complexity_score: int
            detected_topics: list
            suggested_premises: list
        
        return FallbackInput(
            raw_input=user_input,
            cleaned_input=user_input.strip(),
            input_type=InputType.MIXED,
            style_flags=[],
            emotional_charge=3,
            complexity_score=3,
            detected_topics=["general"],
            suggested_premises=[]
        )
    
    def _select_premises(self, rai_input) -> Dict[str, Any]:
        """Select relevant premises"""
        try:
            if not self.components_loaded or not self.premise_engine:
                return {"premises": [], "rationale": "Premise engine unavailable"}
            
            premise_selection = self.premise_engine.select_premises(rai_input)
            
            return {
                "premises": premise_selection.primary_premises + premise_selection.secondary_premises,
                "primary_premises": premise_selection.primary_premises,
                "secondary_premises": premise_selection.secondary_premises,
                "wisdom_overlay": premise_selection.wisdom_overlay,
                "rationale": premise_selection.selection_rationale,
                "formatted_premises": self.premise_engine.format_premises_for_prompt(premise_selection)
            }
            
        except Exception as e:
            logger.error(f"Premise selection error: {str(e)}")
            return {
                "status": "error",
                "error": f"Premise selection failed: {str(e)}",
                "error_type": "premise_selection"
            }
    
    def _select_modules(self, rai_input, analysis_mode: str) -> Dict[str, Any]:
        """Select analysis modules based on mode"""
        try:
            if not self.components_loaded or not self.module_selector:
                return {"modules": [], "rationale": "Module selector unavailable"}
            
            # Map analysis modes to module limits
            mode_config = {
                "quick": {"max_modules": 3, "output_mode": "brief"},
                "guided": {"max_modules": 5, "output_mode": "analytical"},
                "expert": {"max_modules": 7, "output_mode": "analytical"},
                "full": {"max_modules": 7, "output_mode": "analytical"}  # backward compatibility
            }
            
            config = mode_config.get(analysis_mode, mode_config["guided"])
            
            module_selection = self.module_selector.select_modules(
                rai_input, 
                max_modules_per_level=config["max_modules"],
                output_mode=config["output_mode"]
            )
            
            return {
                "modules": module_selection.execution_order,
                "entry_point": module_selection.entry_point.value,
                "cross_level": module_selection.cross_level_modules,
                "fact_level": module_selection.fact_level_modules,
                "narrative_level": module_selection.narrative_level_modules,
                "system_level": module_selection.system_level_modules,
                "total_modules": module_selection.total_modules,
                "rationale": module_selection.selection_rationale,
                "formatted_modules": self.module_selector.format_modules_for_prompt(module_selection)
            }
            
        except Exception as e:
            logger.error(f"Module selection error: {str(e)}")
            return {
                "status": "error", 
                "error": f"Module selection failed: {str(e)}",
                "error_type": "module_selection"
            }
    
    def _build_complete_prompt(self, rai_result: Dict, premise_result: Dict, 
                              module_result: Dict, analysis_mode: str) -> str:
        """Build complete RAI prompt for LLM"""
        try:
            prompt_parts = []
            
            # 1. Framework activation
            prompt_parts.append("""
You are operating under the **Real Artificial Intelligence (RAI) Framework**.
This framework ensures analysis meets high standards of **factual precision**, **narrative coherence**, and **systemic insight** — guided by philosophical adequacy over mechanical neutrality.
""")
            
            # 2. Analysis mode specification
            mode_descriptions = {
                "quick": "Brief analysis focusing on key insights",
                "guided": "Structured analysis with clear explanations", 
                "expert": "Comprehensive analysis with detailed reasoning",
                "full": "Complete analysis across all levels"
            }
            
            prompt_parts.append(f"""
**Analysis Mode:** {analysis_mode.title()} - {mode_descriptions.get(analysis_mode, 'Standard analysis')}
""")
            
            # 3. Add premises if available
            if premise_result.get("formatted_premises"):
                prompt_parts.append(premise_result["formatted_premises"])
            
            # 4. Add modules if available
            if module_result.get("formatted_modules"):
                prompt_parts.append(module_result["formatted_modules"])
            
            # 5. Input analysis from wrapper
            if "input" in rai_result:
                rai_input = rai_result["input"]
                prompt_parts.append(f"""
**Input Analysis:**
- Original Input: "{rai_input.raw_input}"
- Input Type: {rai_input.input_type.value}
- Complexity Score: {rai_input.complexity_score}/5
- Detected Topics: {', '.join(rai_input.detected_topics) if rai_input.detected_topics else 'None'}
""")
            
            # 6. Analysis instructions
            prompt_parts.append("""
**Analysis Instructions:**
1. Apply the RAI framework systematically across Fact, Narrative, and System levels
2. Use any provided Macro Premises as interpretive lenses where relevant
3. Maintain epistemic humility - flag uncertainties and limitations
4. Prioritize adequacy over acceptability
5. Provide structured output with clear headings for each analysis level
6. Conclude with a Final Synthesis that integrates all insights

**Structure your response with clear sections:**
- **Fact-Level Analysis** - Examine claims, evidence, and verifiability
- **Narrative-Level Analysis** - Analyze story coherence and framing
- **System-Level Analysis** - Explore power dynamics and systemic factors  
- **Final Synthesis** - Integrate insights across all levels

**Begin Analysis:**
""")
            
            # return '\n'.join(prompt_parts)
            prompt = '\n'.join(prompt_parts)
            
            # TEMPORARY DEBUG - Log what we're sending to DeepSeek
            logger.info("=" * 50)
            logger.info(f"USER INPUT WAS: {rai_result.get('input', {}).get('raw_input', 'NO INPUT FOUND')}")
            logger.info("=" * 50)
            logger.info(f"FULL PROMPT BEING SENT TO DEEPSEEK:")
            logger.info(prompt)
            logger.info("=" * 50)
            
            return prompt
        except Exception as e:
            logger.error(f"Prompt building error: {str(e)}")
            # Fallback prompt
            return f"""
Analyze the following input using structured reasoning across fact, narrative, and system levels:

"{rai_result.get('input', {}).get('raw_input', 'Input processing failed')}"

Please provide:
1. Factual analysis
2. Narrative analysis  
3. Systemic analysis
4. Final synthesis
"""
    
    def _dispatch_to_llm(self, prompt: str, selected_llm: str) -> Dict[str, Any]:
        """Dispatch prompt to selected LLM"""
        try:
            if not self.components_loaded or not self.api_dispatcher:
                return {
                    "status": "error",
                    "error": "LLM dispatcher unavailable - running in demo mode",
                    "error_type": "dispatcher_unavailable"
                }
            
            # Map frontend model names to dispatcher aliases
            model_mapping = {
                "gpt": "gpt-4",
                "gemini": "gemini-pro", 
                "deepseek": "deepseek-chat"
            }
            
            model_alias = model_mapping.get(selected_llm, selected_llm)
            
            response = self.api_dispatcher.dispatch_to_llm(
                prompt, 
                model_alias,
                max_retries=2,
                timeout=self.config.get("analysis", {}).get("timeout_seconds", 120)
            )
            
            if response.status != ResponseStatus.SUCCESS:
                return {
                    "status": "error",
                    "error": f"LLM request failed: {response.error_message}",
                    "error_type": "llm_error",
                    "provider": response.provider
                }
            
            return {
                "response": response,
                "tokens_used": response.tokens_used,
                "response_time": response.response_time,
                "provider": response.provider
            }
            
        except Exception as e:
            logger.error(f"LLM dispatch error: {str(e)}")
            return {
                "status": "error",
                "error": f"LLM dispatch failed: {str(e)}",
                "error_type": "dispatch"
            }
    
    def _parse_output(self, llm_response, metadata: Dict) -> Dict[str, Any]:
        """Parse LLM output into structured format"""
        try:
            if not self.components_loaded or not self.output_parser:
                # Fallback parsing
                return self._fallback_parse_output(llm_response.content, metadata)
            
            parsed_result = self.output_parser.parse_llm_response(
                llm_response.content, 
                metadata
            )
            
            # Convert to format expected by frontend
            html_content = self._generate_frontend_html(parsed_result)
            
            return {
                "html_content": html_content,
                "input_summary": parsed_result.input_summary,
                "sections_count": len(parsed_result.sections),
                "average_confidence": self._calculate_average_confidence(parsed_result.sections),
                "export_formats": parsed_result.export_formats,
                "processing_time": metadata.get("response_time", None)
            }
            
        except Exception as e:
            logger.error(f"Output parsing error: {str(e)}")
            return self._fallback_parse_output(llm_response.content, metadata)
    
    def _fallback_parse_output(self, content: str, metadata: Dict) -> Dict[str, Any]:
        """Fallback output parsing when parser is unavailable"""
        
        # Simple HTML formatting
        html_content = f"""
        <div class="rai-analysis-result">
            <div class="rai-metadata">
                <h3>📊 Analysis Complete</h3>
                <p><strong>Model:</strong> {metadata.get('model', 'Unknown')}</p>
                <p><strong>Mode:</strong> {metadata.get('mode', 'Standard')}</p>
            </div>
            <div class="rai-content">
                <h3>🔍 Analysis Results</h3>
                <div class="rai-response">
                    {self._format_basic_html(content)}
                </div>
            </div>
        </div>
        """
        
        return {
            "html_content": html_content,
            "input_summary": "Analysis completed",
            "sections_count": 1,
            "average_confidence": None,
            "export_formats": {"plain_text": content},
            "processing_time": metadata.get("response_time", None)
        }
    
    def _format_basic_html(self, content: str) -> str:
        """Basic HTML formatting for fallback mode"""
        # Convert line breaks to paragraphs
        paragraphs = content.split('\n\n')
        formatted_paragraphs = []
        
        for para in paragraphs:
            if para.strip():
                # Check for headings
                if para.startswith('#'):
                    level = len(para) - len(para.lstrip('#'))
                    text = para.lstrip('# ').strip()
                    formatted_paragraphs.append(f'<h{min(level + 2, 6)}>{text}</h{min(level + 2, 6)}>')
                elif para.startswith('**') and para.endswith('**'):
                    text = para.strip('*').strip()
                    formatted_paragraphs.append(f'<h4>{text}</h4>')
                else:
                    # Convert **bold** and *italic*
                    formatted = para.replace('**', '<strong>').replace('**', '</strong>')
                    formatted = formatted.replace('*', '<em>').replace('*', '</em>')
                    formatted_paragraphs.append(f'<p>{formatted}</p>')
        
        return '\n'.join(formatted_paragraphs)
    
    def _generate_frontend_html(self, parsed_result) -> str:
        """Generate HTML optimized for frontend display"""
        
        html_parts = []
        
        # Add navigation if multiple sections
        if len(parsed_result.sections) > 1:
            html_parts.append('<div class="rai-navigation">')
            html_parts.append('<h4>Analysis Sections</h4>')
            html_parts.append('<ul class="rai-nav-list">')
            for section in parsed_result.sections:
                section_id = section.section_type.value
                html_parts.append(f'<li><a href="#{section_id}">{section.title}</a></li>')
            html_parts.append('</ul>')
            html_parts.append('</div>')
        
        # Add sections
        for section in parsed_result.sections:
            section_id = section.section_type.value
            html_parts.append(f'<div id="{section_id}" class="rai-section rai-{section_id}">')
            html_parts.append(f'<h3 class="rai-section-title">{section.title}</h3>')
            
            # Add confidence badge if available
            if section.confidence_score is not None:
                confidence_level = "high" if section.confidence_score > 0.7 else "medium" if section.confidence_score > 0.4 else "low"
                html_parts.append(f'<span class="rai-confidence rai-confidence-{confidence_level}">Confidence: {confidence_level.title()}</span>')
            
            # Add section content
            html_parts.append('<div class="rai-section-content">')
            html_parts.append(section.html_content)
            html_parts.append('</div>')
            
            # Add key insights if available
            if section.key_insights:
                html_parts.append('<div class="rai-insights">')
                html_parts.append('<h4>Key Insights</h4>')
                html_parts.append('<ul>')
                for insight in section.key_insights:
                    html_parts.append(f'<li>{insight}</li>')
                html_parts.append('</ul>')
                html_parts.append('</div>')
            
            html_parts.append('</div>')
        
        return '\n'.join(html_parts)
    
    def _calculate_average_confidence(self, sections) -> Optional[float]:
        """Calculate average confidence across sections"""
        confidence_scores = [s.confidence_score for s in sections if s.confidence_score is not None]
        if confidence_scores:
            return round(sum(confidence_scores) / len(confidence_scores), 2)
        return None

# Initialize RAI Companion
rai_companion = RAICompanion()

# Flask Routes

@app.route('/')
def index():
    """Serve the main analysis form"""
    try:
        # Read the HTML file you provided
        with open('analyst.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        return html_content
    except FileNotFoundError:
        # Fallback HTML if file not found
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>RAI Companion</title>
            <meta charset="UTF-8">
        </head>
        <body>
            <h1>RAI Companion</h1>
            <p>Analysis form not found. Please ensure analyst.html is in the project directory.</p>
            <form method="POST" action="/analyze">
                <textarea name="content" placeholder="Enter content to analyze"></textarea><br>
                <select name="model">
                    <option value="gpt">GPT</option>
                    <option value="gemini">Gemini</option>
                    <option value="deepseek">DeepSeek</option>
                </select><br>
                <input type="radio" name="mode" value="quick"> Quick
                <input type="radio" name="mode" value="guided"> Guided
                <input type="radio" name="mode" value="expert"> Expert<br>
                <button type="submit">Analyze</button>
            </form>
        </body>
        </html>
        """

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    """Serve static assets (CSS, JS, images)"""
    return send_from_directory('assets', filename)

@app.route('/analyze', methods=['POST'])
def analyze():
    """Main analysis endpoint"""
    try:
        # Handle both JSON and form data
        if request.is_json:
            data = request.get_json()
            user_input = data.get('user_input') or data.get('input')
            selected_llm = data.get('selected_llm') or data.get('llm') or data.get('model')
            analysis_mode = data.get('analysis_mode') or data.get('mode', 'guided')
        else:
            # Form data from HTML form
            user_input = request.form.get('content')
            selected_llm = request.form.get('model')
            analysis_mode = request.form.get('mode', 'guided')
        
        # Validate required fields
        if not user_input or not selected_llm:
            return jsonify({
                "status": "error",
                "error": "Missing required fields: user_input and selected_llm are required",
                "error_type": "validation"
            }), 400
        
        logger.info(f"Analysis request: {len(user_input)} chars, model={selected_llm}, mode={analysis_mode}")
        
        # Process the analysis request
        result = rai_companion.process_analysis_request(
            user_input=user_input,
            selected_llm=selected_llm,
            analysis_mode=analysis_mode
        )
        
        # Return appropriate status code
        status_code = 200 if result["status"] == "success" else 400
        
        return jsonify(result), status_code
        
    except Exception as e:
        logger.error(f"Analyze endpoint error: {str(e)}")
        logger.error(traceback.format_exc())
        
        return jsonify({
            "status": "error",
            "error": f"Server error: {str(e)}",
            "error_type": "server_error"
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        available_models = rai_companion.get_available_models()
        
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": rai_companion.config.get("app", {}).get("version", "1.0.0"),
            "components_loaded": rai_companion.components_loaded,
            "available_models": list(available_models.keys())
        })
        
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500

@app.route('/config', methods=['GET'])
def get_config():
    """Get public configuration information"""
    try:
        return jsonify({
            "available_models": rai_companion.get_available_models(),
            "analysis_modes": ["quick", "guided", "expert"],
            "max_input_length": rai_companion.config.get("analysis", {}).get("max_input_length", 10000),
            "version": rai_companion.config.get("app", {}).get("version", "1.0.0")
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "status": "error",
        "error": "Endpoint not found",
        "error_type": "not_found"
    }), 404

@app.errorhandler(400)
def bad_request(error):
    """Handle 400 errors"""
    return jsonify({
        "status": "error", 
        "error": "Bad request",
        "error_type": "bad_request"
    }), 400

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        "status": "error",
        "error": "Internal server error",
        "error_type": "server_error"
    }), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large errors"""
    return jsonify({
        "status": "error",
        "error": "Request too large. Maximum size is 16MB.",
        "error_type": "file_too_large"
    }), 413

# Development utilities
@app.route('/debug/test', methods=['POST'])
def debug_test():
    """Debug endpoint for testing components individually"""
    if not app.config.get('DEBUG', False):
        return jsonify({"error": "Debug mode not enabled"}), 403
    
    try:
        data = request.get_json()
        test_type = data.get('test_type', 'full')
        test_input = data.get('input', 'Test input for debugging')
        
        result = {}
        
        if test_type in ['wrapper', 'full']:
            try:
                wrapper_result = rai_companion.rai_wrapper.process_input(test_input) if rai_companion.rai_wrapper else None
                result['wrapper'] = 'success' if wrapper_result and 'error' not in wrapper_result else 'failed'
                result['wrapper_details'] = wrapper_result
            except Exception as e:
                result['wrapper'] = f'error: {str(e)}'
        
        if test_type in ['premises', 'full']:
            try:
                if rai_companion.premise_engine and rai_companion.rai_wrapper:
                    wrapper_result = rai_companion.rai_wrapper.process_input(test_input)
                    if 'error' not in wrapper_result:
                        premise_result = rai_companion.premise_engine.select_premises(wrapper_result['input'])
                        result['premises'] = 'success'
                        result['premise_details'] = {
                            'count': len(premise_result.primary_premises + premise_result.secondary_premises),
                            'primary': premise_result.primary_premises,
                            'secondary': premise_result.secondary_premises
                        }
                    else:
                        result['premises'] = 'wrapper_failed'
                else:
                    result['premises'] = 'unavailable'
            except Exception as e:
                result['premises'] = f'error: {str(e)}'
        
        if test_type in ['modules', 'full']:
            try:
                if rai_companion.module_selector and rai_companion.rai_wrapper:
                    wrapper_result = rai_companion.rai_wrapper.process_input(test_input)
                    if 'error' not in wrapper_result:
                        module_result = rai_companion.module_selector.select_modules(wrapper_result['input'])
                        result['modules'] = 'success'
                        result['module_details'] = {
                            'total': module_result.total_modules,
                            'execution_order': module_result.execution_order,
                            'entry_point': module_result.entry_point.value
                        }
                    else:
                        result['modules'] = 'wrapper_failed'
                else:
                    result['modules'] = 'unavailable'
            except Exception as e:
                result['modules'] = f'error: {str(e)}'
        
        if test_type in ['dispatcher', 'full']:
            try:
                if rai_companion.api_dispatcher:
                    available_models = rai_companion.api_dispatcher.get_available_models()
                    result['dispatcher'] = 'success'
                    result['dispatcher_details'] = {
                        'available_models': available_models,
                        'model_count': len(available_models)
                    }
                else:
                    result['dispatcher'] = 'unavailable'
            except Exception as e:
                result['dispatcher'] = f'error: {str(e)}'
        
        return jsonify({
            "status": "debug_complete",
            "test_type": test_type,
            "results": result,
            "components_loaded": rai_companion.components_loaded
        })
        
    except Exception as e:
        return jsonify({
            "status": "debug_error",
            "error": str(e)
        }), 500

@app.route('/debug/stats', methods=['GET'])
def debug_stats():
    """Get debug statistics and component status"""
    if not app.config.get('DEBUG', False):
        return jsonify({"error": "Debug mode not enabled"}), 403
    
    try:
        stats = {
            "components": {
                "rai_wrapper": rai_companion.rai_wrapper is not None,
                "premise_engine": rai_companion.premise_engine is not None, 
                "module_selector": rai_companion.module_selector is not None,
                "api_dispatcher": rai_companion.api_dispatcher is not None,
                "output_parser": rai_companion.output_parser is not None
            },
            "config_loaded": bool(rai_companion.config),
            "available_models": list(rai_companion.get_available_models().keys()),
            "components_loaded": rai_companion.components_loaded
        }
        
        # Add dispatcher stats if available
        if rai_companion.api_dispatcher:
            try:
                usage_stats = rai_companion.api_dispatcher.get_usage_stats()
                stats["usage_stats"] = usage_stats
            except:
                stats["usage_stats"] = "unavailable"
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# TODO: Add more sophisticated caching for repeated analyses
# TODO: Add rate limiting for production deployment  
# TODO: Add user authentication for multi-user scenarios
# TODO: Add analysis result persistence/history
# TODO: Add real-time analysis status updates via WebSocket
# TODO: Add batch analysis capabilities for multiple inputs

if __name__ == '__main__':
    """Run the Flask application"""
    
    # Load configuration
    config = rai_companion.config
    app_config = config.get("app", {})
    
    # Set debug mode
    debug_mode = app_config.get("debug", True)
    app.config['DEBUG'] = debug_mode
    
    # RENDER.COM FIX - Always use 0.0.0.0 and Render's PORT
    host = "0.0.0.0"
    port = int(os.environ.get("PORT", app_config.get("port", 5000)))
    
    logger.info(f"Starting RAI Companion Flask app on {host}:{port}")
    
    try:
        app.run(
            host=host,
            port=port,
            debug=debug_mode,
            threaded=True
        )
    except Exception as e:
        logger.error(f"Server startup failed: {str(e)}")
        raise
