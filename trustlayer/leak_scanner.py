import re
from typing import Any, Dict
from .models import BaseDetector, DetectionResult

class LeakScanner(BaseDetector):
    """Scans for sensitive data exposure such as API keys, emails, and PII."""

    def __init__(self):
        # Patterns for sensitive data leakage
        self.patterns: Dict[str, str] = {
            "api_key": r"(?i)(?:key|password|secret|token|api_?key)(?:.*?)[\s:=]+['\"]?([a-zA-Z0-9-_{}]{16,})['\"]?",
            "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            "credit_card": r"\b(?:\d[ -]*?){13,16}\b",
            "ipv4": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
        }

    def detect(self, text: str, **kwargs: Any) -> DetectionResult:
        """Analyzes text for sensitive data leaks.

        Args:
            text: The text to analyze.
            **kwargs: Unused.

        Returns:
            DetectionResult mapping found leaks.
        """
        found_leaks = []
        for leak_type, pattern in self.patterns.items():
            if re.search(pattern, text):
                found_leaks.append(leak_type)

        risk_score = min(len(found_leaks) * 0.3, 1.0)
        is_safe = risk_score < 0.2  # Very strict on leaks
        
        return DetectionResult(
            is_safe=is_safe,
            risk_score=risk_score,
            threat_type="data_leak" if not is_safe else None,
            confidence=0.95 if found_leaks else 1.0,
            metadata={"leak_types": found_leaks}
        )
