"""
OpenAI integration for Troll-Tove app.

Handles AI-powered prediction generation with:
- Nordnorsk tone preservation
- Cost control (configurable model, max tokens, temperature)
- Anti-repeat mechanism (lightweight in-memory cache)
- Fallback to file-based predictions on errors
"""
import os
import logging
from typing import Optional, List, Callable
from collections import deque

logger = logging.getLogger(__name__)


class OpenAIGenerator:
    """
    Generates AI-powered predictions using OpenAI API.
    
    Features:
    - Configurable model, tokens, and temperature for cost control
    - Anti-repeat mechanism to avoid repetitive answers
    - Graceful fallback on API errors
    - Nordnorsk tone enforcement in prompts
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        timeout: Optional[int] = None,
        anti_repeat_size: int = 10
    ):
        """
        Initialize OpenAI generator with configuration.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            model: Model to use (defaults to OPENAI_MODEL env var or gpt-4o-mini)
            max_tokens: Max tokens for response (defaults to OPENAI_MAX_TOKENS or 220)
            temperature: Randomness level (defaults to OPENAI_TEMPERATURE or 0.8)
            timeout: API timeout in seconds (defaults to OPENAI_TIMEOUT or 30)
            anti_repeat_size: Number of recent answers to track per mode
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        
        # Parse numeric environment variables with fallbacks
        try:
            self.max_tokens = max_tokens or int(os.getenv("OPENAI_MAX_TOKENS", "220"))
        except (ValueError, TypeError):
            self.max_tokens = 220
            
        try:
            self.temperature = temperature or float(os.getenv("OPENAI_TEMPERATURE", "0.8"))
        except (ValueError, TypeError):
            self.temperature = 0.8
            
        try:
            self.timeout = timeout or int(os.getenv("OPENAI_TIMEOUT", "30"))
        except (ValueError, TypeError):
            self.timeout = 30
        
        # Anti-repeat cache: stores last N answers per mode
        self.recent_answers = {
            "standard": deque(maxlen=anti_repeat_size),
            "glimt": deque(maxlen=anti_repeat_size),
            "dark": deque(maxlen=anti_repeat_size)
        }
        
        # Initialize OpenAI client if API key is available
        self.client = None
        if self.api_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key, timeout=self.timeout)
                logger.info(f"OpenAI client initialized with model: {self.model}")
            except ImportError:
                logger.error("OpenAI package not installed. Install with: pip install openai")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
    
    def is_enabled(self) -> bool:
        """Check if OpenAI integration is enabled and ready."""
        return self.client is not None and self.api_key is not None
    
    def generate_prediction(
        self,
        mode: str,
        user_name: str,
        user_question: str,
        fallback: Callable[[], str]
    ) -> str:
        """
        Generate an AI-powered prediction or fall back to file-based.
        
        Args:
            mode: Prediction mode ("standard", "glimt", or "dark")
            user_name: User's name for personalization
            user_question: User's question (if any)
            fallback: Callable that returns a fallback prediction
            
        Returns:
            Generated prediction text or fallback
        """
        if not self.is_enabled():
            logger.debug("OpenAI not enabled, using fallback")
            return fallback()
        
        try:
            prompt = self._build_prompt(mode, user_name, user_question)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Du er Troll-Tove, en humoristisk nordnorsk spåkone som gir korte, morsomme spådommer."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            prediction = response.choices[0].message.content.strip()
            
            # Handle None or empty content
            if not prediction:
                logger.warning("OpenAI returned empty content, using fallback")
                return fallback()
            
            # Store in anti-repeat cache
            self.recent_answers[mode].append(prediction)
            
            logger.info(f"Generated prediction for mode={mode}, tokens={response.usage.total_tokens}")
            return prediction
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}, falling back to file-based prediction")
            return fallback()
    
    def _build_prompt(self, mode: str, user_name: str, user_question: str) -> str:
        """
        Build prompt based on mode with anti-repeat instructions.
        
        Args:
            mode: Prediction mode
            user_name: User's name
            user_question: User's question
            
        Returns:
            Formatted prompt string
        """
        # Get recent answers to avoid repetition
        recent = list(self.recent_answers[mode])
        anti_repeat_text = ""
        if recent:
            # Filter and format valid strings only
            valid_recent = [str(ans)[:100] for ans in recent[-5:] if ans]
            if valid_recent:
                anti_repeat_text = f"\n\nUnngå å gjenta disse nylige spådommene:\n" + "\n".join(f"- {ans}..." for ans in valid_recent)
        
        if mode == "glimt":
            return (
                f"Gi en kort, humoristisk spådom om FK Bodø/Glimt på nordnorsk dialekt. "
                f"Bruk 2-4 setninger. Vær kreativ, morsom og litt frekk. "
                f"Spådommen skal være om fotball og Glimt."
                f"{anti_repeat_text}"
            )
        elif mode == "dark":
            return (
                f"Gi en kort, mørk og eksistensiell spådom på nordnorsk dialekt. "
                f"Bruk 2-4 setninger. Vær dyster, filosofisk og litt mystisk. "
                f"Spådommen skal handle om livet, skjebnen eller fremtiden."
                f"{anti_repeat_text}"
            )
        else:  # standard
            question_text = f" Spørsmålet er: '{user_question}'." if user_question else ""
            return (
                f"Gi en kort, humoristisk spådom til {user_name} på nordnorsk dialekt. "
                f"Bruk 2-4 setninger. Vær kreativ, morsom og overraskende.{question_text}"
                f"{anti_repeat_text}"
            )
