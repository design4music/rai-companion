"""
RAI API Dispatcher - LLM Provider Integration
Real Artificial Intelligence Framework Implementation

This module dispatches RAI-formatted prompts to various LLM providers
(OpenAI, DeepSeek, Anthropic, Google Gemini) and handles response parsing.
"""

import json
import logging
import time
import os
from typing import Dict, Optional, Tuple, Any, List
from dataclasses import dataclass
from enum import Enum
import requests
import openai
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMProvider(Enum):
    """Supported LLM providers"""
    OPENAI = "openai"
    DEEPSEEK = "deepseek"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"

class ResponseStatus(Enum):
    """Response status codes"""
    SUCCESS = "success"
    ERROR = "error"
    TIMEOUT = "timeout"
    RATE_LIMITED = "rate_limited"
    INVALID_KEY = "invalid_key"

@dataclass
class LLMResponse:
    """Standardized LLM response object"""
    status: ResponseStatus
    content: str
    provider: str
    model: str
    tokens_used: Optional[int]
    response_time: float
    error_message: Optional[str]
    raw_response: Optional[Dict]

@dataclass
class UsageStats:
    """Track usage statistics"""
    total_requests: int
    successful_requests: int
    failed_requests: int
    total_tokens: int
    total_cost_estimate: float
    by_provider: Dict[str, int]

class APIDispatcher:
    """
    RAI API Dispatcher
    
    Handles communication with multiple LLM providers:
    - OpenAI (GPT-4, GPT-3.5)
    - DeepSeek 
    - Anthropic Claude
    - Google Gemini
    
    Features:
    - Automatic failover between providers
    - Response parsing and standardization
    - Usage tracking and logging
    - Error handling and retries
    """
    
    def __init__(self, config_path: str = "config.json"):
        """Initialize dispatcher with configuration"""
        self.config = self._load_config(config_path)
        self.usage_stats = UsageStats(0, 0, 0, 0, 0.0, {})
        self.model_aliases = self._build_model_aliases()
        self._setup_clients()
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                logger.info(f"Loaded configuration from {config_path}")
                return config
        except FileNotFoundError:
            logger.warning(f"Config file {config_path} not found, using environment variables")
            return self._load_from_env()
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file: {e}")
            return self._load_from_env()
    
    def _load_from_env(self) -> Dict:
        """Load configuration from environment variables"""
        return {
            "openai": {
                "api_key": os.getenv("OPENAI_API_KEY"),
                "model": "gpt-4",
                "max_tokens": 4000,
                "temperature": 0.3
            },
            "deepseek": {
                "api_key": os.getenv("DEEPSEEK_API_KEY"),
                "model": "deepseek-chat",
                "base_url": "https://api.deepseek.com/v1",
                "max_tokens": 4000,
                "temperature": 0.3
            },
            "anthropic": {
                "api_key": os.getenv("ANTHROPIC_API_KEY"),
                "model": "claude-3-sonnet-20240229",
                "max_tokens": 4000,
                "temperature": 0.3
            },
            "gemini": {
                "api_key": os.getenv("GEMINI_API_KEY"),
                "model": "gemini-pro",
                "max_tokens": 4000,
                "temperature": 0.3
            }
        }
    
    def _build_model_aliases(self) -> Dict[str, Tuple[str, str]]:
        """Build model alias mapping: alias -> (provider, model_name)"""
        return {
            # OpenAI aliases
            "gpt-4": ("openai", "gpt-4"),
            "gpt-4-turbo": ("openai", "gpt-4-turbo-preview"),
            "gpt-3.5": ("openai", "gpt-3.5-turbo"),
            "gpt-3.5-turbo": ("openai", "gpt-3.5-turbo"),
            
            # DeepSeek aliases
            "deepseek": ("deepseek", "deepseek-chat"),
            "deepseek-chat": ("deepseek", "deepseek-chat"),
            
            # Anthropic aliases
            "claude": ("anthropic", "claude-3-sonnet-20240229"),
            "claude-3": ("anthropic", "claude-3-sonnet-20240229"),
            "claude-sonnet": ("anthropic", "claude-3-sonnet-20240229"),
            
            # Gemini aliases
            "gemini": ("gemini", "gemini-pro"),
            "gemini-pro": ("gemini", "gemini-pro"),
            "gemini-1.5": ("gemini", "gemini-1.5-pro-latest")
        }
    
    def _setup_clients(self):
        """Setup API clients for each provider"""
        self.clients = {}
        
        # OpenAI client
        if self.config.get("openai", {}).get("api_key"):
            openai.api_key = self.config["openai"]["api_key"]
            self.clients["openai"] = openai
            logger.info("OpenAI client configured")
        
        # DeepSeek client (OpenAI-compatible)
        if self.config.get("deepseek", {}).get("api_key"):
            self.clients["deepseek"] = "configured"
            logger.info("DeepSeek client configured")
        
        # Anthropic client
        if self.config.get("anthropic", {}).get("api_key"):
            try:
                import anthropic
                self.clients["anthropic"] = anthropic.Anthropic(
                    api_key=self.config["anthropic"]["api_key"]
                )
                logger.info("Anthropic client configured")
            except ImportError:
                logger.warning("Anthropic library not installed")
        
        # Gemini client
        if self.config.get("gemini", {}).get("api_key"):
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.config["gemini"]["api_key"])
                self.clients["gemini"] = genai
                logger.info("Gemini client configured")
            except ImportError:
                logger.warning("Google GenerativeAI library not installed")
    
    def dispatch_to_llm(self, prompt: str, model_alias: str, 
                       max_retries: int = 3, timeout: int = 120) -> LLMResponse:
        """
        Main dispatch function - sends prompt to specified LLM
        
        Args:
            prompt: RAI-formatted prompt
            model_alias: Model alias (e.g., 'gpt-4', 'deepseek', 'claude')
            max_retries: Maximum retry attempts
            timeout: Request timeout in seconds
            
        Returns:
            LLMResponse object with standardized response data
        """
        start_time = time.time()
        
        # Resolve model alias
        if model_alias not in self.model_aliases:
            return LLMResponse(
                status=ResponseStatus.ERROR,
                content="",
                provider="unknown",
                model=model_alias,
                tokens_used=None,
                response_time=0.0,
                error_message=f"Unknown model alias: {model_alias}",
                raw_response=None
            )
        
        provider, model_name = self.model_aliases[model_alias]
        
        # Check if provider is configured
        if provider not in self.clients:
            return LLMResponse(
                status=ResponseStatus.ERROR,
                content="",
                provider=provider,
                model=model_name,
                tokens_used=None,
                response_time=0.0,
                error_message=f"Provider {provider} not configured",
                raw_response=None
            )
        
        # Dispatch to appropriate provider
        for attempt in range(max_retries):
            try:
                if provider == "openai":
                    response = self._call_openai(prompt, model_name, timeout)
                elif provider == "deepseek":
                    response = self._call_deepseek(prompt, model_name, timeout)
                elif provider == "anthropic":
                    response = self._call_anthropic(prompt, model_name, timeout)
                elif provider == "gemini":
                    response = self._call_gemini(prompt, model_name, timeout)
                else:
                    raise ValueError(f"Unsupported provider: {provider}")
                
                # Calculate response time
                response.response_time = time.time() - start_time
                
                # Log usage
                self._log_usage(response)
                
                return response
                
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed for {provider}: {str(e)}")
                if attempt == max_retries - 1:
                    return LLMResponse(
                        status=ResponseStatus.ERROR,
                        content="",
                        provider=provider,
                        model=model_name,
                        tokens_used=None,
                        response_time=time.time() - start_time,
                        error_message=str(e),
                        raw_response=None
                    )
                time.sleep(2 ** attempt)  # Exponential backoff
    
    def _call_openai(self, prompt: str, model: str, timeout: int) -> LLMResponse:
        """Call OpenAI API"""
        config = self.config["openai"]
        
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=config.get("max_tokens", 4000),
                temperature=config.get("temperature", 0.3),
                request_timeout=timeout
            )
            
            return LLMResponse(
                status=ResponseStatus.SUCCESS,
                content=response.choices[0].message.content,
                provider="openai",
                model=model,
                tokens_used=response.usage.total_tokens,
                response_time=0.0,  # Will be set by caller
                error_message=None,
                raw_response=response.to_dict()
            )
            
        except openai.error.RateLimitError:
            raise Exception("OpenAI rate limit exceeded")
        except openai.error.InvalidRequestError as e:
            raise Exception(f"OpenAI invalid request: {str(e)}")
        except openai.error.AuthenticationError:
            raise Exception("OpenAI authentication failed")
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def _call_deepseek(self, prompt: str, model: str, timeout: int) -> LLMResponse:
        """Call DeepSeek API (OpenAI-compatible)"""
        config = self.config["deepseek"]
        
        headers = {
            "Authorization": f"Bearer {config['api_key']}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": config.get("max_tokens", 4000),
            "temperature": config.get("temperature", 0.3)
        }
        
        try:
            response = requests.post(
                f"{config.get('base_url', 'https://api.deepseek.com/v1')}/chat/completions",
                headers=headers,
                json=data,
                timeout=timeout
            )
            response.raise_for_status()
            
            result = response.json()
            
            return LLMResponse(
                status=ResponseStatus.SUCCESS,
                content=result["choices"][0]["message"]["content"],
                provider="deepseek",
                model=model,
                tokens_used=result.get("usage", {}).get("total_tokens"),
                response_time=0.0,
                error_message=None,
                raw_response=result
            )
            
        except requests.exceptions.Timeout:
            raise Exception("DeepSeek request timeout")
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                raise Exception("DeepSeek rate limit exceeded")
            elif response.status_code == 401:
                raise Exception("DeepSeek authentication failed")
            else:
                raise Exception(f"DeepSeek HTTP error: {response.status_code}")
        except Exception as e:
            raise Exception(f"DeepSeek API error: {str(e)}")
    
    def _call_anthropic(self, prompt: str, model: str, timeout: int) -> LLMResponse:
        """Call Anthropic Claude API"""
        if "anthropic" not in self.clients:
            raise Exception("Anthropic client not configured")
        
        config = self.config["anthropic"]
        client = self.clients["anthropic"]
        
        try:
            response = client.messages.create(
                model=model,
                max_tokens=config.get("max_tokens", 4000),
                temperature=config.get("temperature", 0.3),
                messages=[{"role": "user", "content": prompt}],
                timeout=timeout
            )
            
            return LLMResponse(
                status=ResponseStatus.SUCCESS,
                content=response.content[0].text,
                provider="anthropic",
                model=model,
                tokens_used=response.usage.input_tokens + response.usage.output_tokens,
                response_time=0.0,
                error_message=None,
                raw_response=response.to_dict() if hasattr(response, 'to_dict') else None
            )
            
        except Exception as e:
            if "rate_limit" in str(e).lower():
                raise Exception("Anthropic rate limit exceeded")
            elif "authentication" in str(e).lower():
                raise Exception("Anthropic authentication failed")
            else:
                raise Exception(f"Anthropic API error: {str(e)}")
    
    def _call_gemini(self, prompt: str, model: str, timeout: int) -> LLMResponse:
        """Call Google Gemini API"""
        if "gemini" not in self.clients:
            raise Exception("Gemini client not configured")
        
        config = self.config["gemini"]
        genai = self.clients["gemini"]
        
        try:
            model_instance = genai.GenerativeModel(model)
            
            generation_config = genai.types.GenerationConfig(
                max_output_tokens=config.get("max_tokens", 4000),
                temperature=config.get("temperature", 0.3)
            )
            
            response = model_instance.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            return LLMResponse(
                status=ResponseStatus.SUCCESS,
                content=response.text,
                provider="gemini",
                model=model,
                tokens_used=None,  # Gemini doesn't always provide token counts
                response_time=0.0,
                error_message=None,
                raw_response=None
            )
            
        except Exception as e:
            if "quota" in str(e).lower() or "rate" in str(e).lower():
                raise Exception("Gemini rate limit exceeded")
            elif "api_key" in str(e).lower():
                raise Exception("Gemini authentication failed")
            else:
                raise Exception(f"Gemini API error: {str(e)}")
    
    def _log_usage(self, response: LLMResponse):
        """Log usage statistics"""
        self.usage_stats.total_requests += 1
        
        if response.status == ResponseStatus.SUCCESS:
            self.usage_stats.successful_requests += 1
            if response.tokens_used:
                self.usage_stats.total_tokens += response.tokens_used
        else:
            self.usage_stats.failed_requests += 1
        
        # Track by provider
        provider = response.provider
        if provider not in self.usage_stats.by_provider:
            self.usage_stats.by_provider[provider] = 0
        self.usage_stats.by_provider[provider] += 1
        
        # Log to file
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "provider": response.provider,
            "model": response.model,
            "status": response.status.value,
            "tokens_used": response.tokens_used,
            "response_time": response.response_time,
            "error": response.error_message
        }
        
        logger.info(f"LLM Request: {json.dumps(log_entry)}")
    
    def parse_rai_response(self, llm_response: LLMResponse) -> Dict[str, str]:
        """
        Parse LLM response into structured RAI components
        
        Returns:
            Dict with fact_level, narrative_level, system_level, final_synthesis
        """
        if llm_response.status != ResponseStatus.SUCCESS:
            return {
                "fact_level": "",
                "narrative_level": "",
                "system_level": "",
                "final_synthesis": f"Error: {llm_response.error_message}",
                "raw_response": llm_response.content
            }
        
        content = llm_response.content
        
        # Try to parse structured sections
        try:
            parsed = self._extract_rai_sections(content)
            parsed["raw_response"] = content
            return parsed
        except Exception as e:
            logger.warning(f"Failed to parse RAI sections: {e}")
            # Fallback to raw content
            return {
                "fact_level": "Parsing failed - see raw response",
                "narrative_level": "",
                "system_level": "",
                "final_synthesis": content[:500] + "..." if len(content) > 500 else content,
                "raw_response": content
            }
    
    def _extract_rai_sections(self, content: str) -> Dict[str, str]:
        """Extract RAI sections from LLM response"""
        
        # Common section markers
        section_markers = {
            "fact_level": [
                "**Fact-Level", "**FACT-LEVEL", "**FL-", "**Factual Analysis",
                "## Fact-Level", "### Fact-Level", "# Fact-Level"
            ],
            "narrative_level": [
                "**Narrative-Level", "**NARRATIVE-LEVEL", "**NL-", "**Narrative Analysis",
                "## Narrative-Level", "### Narrative-Level", "# Narrative-Level"
            ],
            "system_level": [
                "**System-Level", "**SYSTEM-LEVEL", "**SL-", "**System Analysis",
                "## System-Level", "### System-Level", "# System-Level"
            ],
            "final_synthesis": [
                "**Final Synthesis", "**FINAL SYNTHESIS", "**Synthesis", "**Conclusion",
                "## Final Synthesis", "### Final Synthesis", "# Final Synthesis"
            ]
        }
        
        sections = {
            "fact_level": "",
            "narrative_level": "",
            "system_level": "",
            "final_synthesis": ""
        }
        
        lines = content.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            line_stripped = line.strip()
            
            # Check if this line starts a new section
            new_section = None
            for section_name, markers in section_markers.items():
                if any(marker in line for marker in markers):
                    new_section = section_name
                    break
            
            if new_section:
                # Save previous section
                if current_section and current_content:
                    sections[current_section] = '\n'.join(current_content).strip()
                
                # Start new section
                current_section = new_section
                current_content = []
            elif current_section:
                # Add to current section
                current_content.append(line)
        
        # Save final section
        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content).strip()
        
        # If no structured sections found, try simpler fallback
        if not any(sections.values()):
            # Split by major headings or just use full content
            sections["final_synthesis"] = content.strip()
        
        return sections
    
    def get_available_models(self) -> List[str]:
        """Get list of available model aliases"""
        available = []
        for alias, (provider, _) in self.model_aliases.items():
            if provider in self.clients:
                available.append(alias)
        return sorted(available)
    
    def get_usage_stats(self) -> Dict:
        """Get current usage statistics"""
        return {
            "total_requests": self.usage_stats.total_requests,
            "successful_requests": self.usage_stats.successful_requests,
            "failed_requests": self.usage_stats.failed_requests,
            "success_rate": (
                self.usage_stats.successful_requests / max(self.usage_stats.total_requests, 1)
            ) * 100,
            "total_tokens": self.usage_stats.total_tokens,
            "by_provider": self.usage_stats.by_provider
        }
    
    def test_connection(self, model_alias: str) -> bool:
        """Test connection to specified model"""
        test_prompt = "Hello, this is a connection test. Please respond with 'Connection successful.'"
        
        response = self.dispatch_to_llm(test_prompt, model_alias, max_retries=1, timeout=30)
        return response.status == ResponseStatus.SUCCESS


# Example usage and testing
if __name__ == "__main__":
    # Initialize dispatcher
    dispatcher = APIDispatcher()
    
    # Test prompt
    test_prompt = """
    You are operating under the Real Artificial Intelligence (RAI) Framework.
    
    Please analyze this claim: "The media is biased against certain political figures."
    
    **Execute the following RAI modules:**
    - FL-1: Claim Clarity and Anchoring
    - NL-1: Cause-Effect Chain Analysis
    - SL-1: Power and Incentive Mapping
    
    Provide structured output with clear sections for Fact-Level, Narrative-Level, System-Level, and Final Synthesis.
    """
    
    # Test available models
    available_models = dispatcher.get_available_models()
    print(f"Available models: {available_models}")
    
    if available_models:
        # Test first available model
        model = available_models[0]
        print(f"\nTesting with {model}...")
        
        response = dispatcher.dispatch_to_llm(test_prompt, model)
        
        print(f"Status: {response.status.value}")
        print(f"Provider: {response.provider}")
        print(f"Model: {response.model}")
        print(f"Tokens: {response.tokens_used}")
        print(f"Response time: {response.response_time:.2f}s")
        
        if response.status == ResponseStatus.SUCCESS:
            # Parse response
            parsed = dispatcher.parse_rai_response(response)
            print("\n=== PARSED RESPONSE ===")
            for section, content in parsed.items():
                if content and section != "raw_response":
                    print(f"\n**{section.upper()}:**")
                    print(content[:200] + "..." if len(content) > 200 else content)
        else:
            print(f"Error: {response.error_message}")
        
        # Show usage stats
        print(f"\n=== USAGE STATS ===")
        stats = dispatcher.get_usage_stats()
        print(json.dumps(stats, indent=2))
    else:
        print("No models available. Check your configuration.")
