"""
RAI API Dispatcher v2 - Streamlined LLM Communication
Real Artificial Intelligence Framework Implementation

Focused on LLM communication only - parsing handled by output_parser.py
Removed redundant response parsing and over-engineering.
"""

import json
import logging
import time
import os
from typing import Dict, Optional, Tuple, List
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
    """Streamlined LLM response object"""
    status: ResponseStatus
    content: str
    provider: str
    model: str
    tokens_used: Optional[int]
    response_time: float
    error_message: Optional[str]

class APIDispatcher:
    """
    Streamlined API Dispatcher
    
    Handles communication with multiple LLM providers.
    Parsing is handled by output_parser.py - this focuses purely on LLM communication.
    """
    
    def __init__(self, config_path: str = "config.json"):
        """Initialize dispatcher with configuration"""
        self.config = self._load_config(config_path)
        self.model_aliases = self._build_model_aliases()
        self._setup_clients()
        
        # Simple usage tracking
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file or environment"""
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
            LLMResponse object with response content
        """
        start_time = time.time()
        self.total_requests += 1
        
        # Resolve model alias
        if model_alias not in self.model_aliases:
            self.failed_requests += 1
            return LLMResponse(
                status=ResponseStatus.ERROR,
                content="",
                provider="unknown",
                model=model_alias,
                tokens_used=None,
                response_time=0.0,
                error_message=f"Unknown model alias: {model_alias}"
            )
        
        provider, model_name = self.model_aliases[model_alias]
        
        # Check if provider is configured
        if provider not in self.clients:
            self.failed_requests += 1
            return LLMResponse(
                status=ResponseStatus.ERROR,
                content="",
                provider=provider,
                model=model_name,
                tokens_used=None,
                response_time=0.0,
                error_message=f"Provider {provider} not configured"
            )
        
        # Dispatch to appropriate provider with retries
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
                
                # Calculate response time and log success
                response.response_time = time.time() - start_time
                self.successful_requests += 1
                
                logger.info(f"LLM success: {provider}/{model_name} - {response.tokens_used} tokens - {response.response_time:.2f}s")
                return response
                
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed for {provider}: {str(e)}")
                if attempt == max_retries - 1:
                    self.failed_requests += 1
                    return LLMResponse(
                        status=ResponseStatus.ERROR,
                        content="",
                        provider=provider,
                        model=model_name,
                        tokens_used=None,
                        response_time=time.time() - start_time,
                        error_message=str(e)
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
                response_time=0.0,
                error_message=None
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
                error_message=None
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
                error_message=None
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
                error_message=None
            )
            
        except Exception as e:
            if "quota" in str(e).lower() or "rate" in str(e).lower():
                raise Exception("Gemini rate limit exceeded")
            elif "api_key" in str(e).lower():
                raise Exception("Gemini authentication failed")
            else:
                raise Exception(f"Gemini API error: {str(e)}")
    
    def get_available_models(self) -> List[str]:
        """Get list of available model aliases"""
        available = []
        for alias, (provider, _) in self.model_aliases.items():
            if provider in self.clients:
                available.append(alias)
        return sorted(available)
    
    def get_usage_stats(self) -> Dict:
        """Get simple usage statistics"""
        return {
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "success_rate": (
                self.successful_requests / max(self.total_requests, 1)
            ) * 100 if self.total_requests > 0 else 0
        }
    
    def test_connection(self, model_alias: str) -> bool:
        """Test connection to specified model"""
        test_prompt = "Hello, this is a connection test. Please respond with 'Connection successful.'"
        
        response = self.dispatch_to_llm(test_prompt, model_alias, max_retries=1, timeout=30)
        return response.status == ResponseStatus.SUCCESS


# Example usage
if __name__ == "__main__":
    dispatcher = APIDispatcher()
    
    available_models = dispatcher.get_available_models()
    print(f"Available models: {available_models}")
    
    if available_models:
        # Quick test
        model = available_models[0]
        print(f"\nTesting {model}...")
        
        test_prompt = "Please respond with 'RAI test successful' if you can read this."
        response = dispatcher.dispatch_to_llm(test_prompt, model)
        
        print(f"Status: {response.status.value}")
        if response.status.value == "success":
            print(f"Response: {response.content}")
            print(f"Tokens: {response.tokens_used}")
            print(f"Time: {response.response_time:.2f}s")
        else:
            print(f"Error: {response.error_message}")
        
        print(f"\nUsage stats: {dispatcher.get_usage_stats()}")