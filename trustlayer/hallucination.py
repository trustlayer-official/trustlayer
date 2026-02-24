from typing import Any
from .models import BaseDetector, DetectionResult

class HallucinationDetector(BaseDetector):
    """Heuristic-based detector for potential hallucinations in model outputs."""

    def detect(self, text: str, **kwargs: Any) -> DetectionResult:
        """Analyzes text for indicators of hallucinations.

        Args:
            text: The text to analyze.
            **kwargs: Can include 'reference_context' to check against.

        Returns:
            DetectionResult mapping potential hallucination risk.
        """
        # Basic heuristic: Check for hedge words and high-uncertainty phrases
        hedge_words = ["I think", "maybe", "possibly", "I'm not sure", "As an AI", "it is likely"]
        found_hedges = [word for word in hedge_words if word.lower() in text.lower()]
        
        # Simple length-based heuristic
        is_suspiciously_short = len(text.split()) < 2
        
        risk_score = 0.0
        if found_hedges:
            risk_score += 0.2
        if is_suspiciously_short:
            risk_score += 0.1
            
        return DetectionResult(
            is_safe=risk_score < 0.3,
            risk_score=risk_score,
            threat_type="hallucination" if risk_score >= 0.4 else None,
            confidence=0.7,
            metadata={"hedge_words": found_hedges, "is_short": is_suspiciously_short}
        )
