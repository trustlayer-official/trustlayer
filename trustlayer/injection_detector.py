import re
from typing import Any
from .models import BaseDetector, DetectionResult

class InjectionDetector(BaseDetector):
    """Detects adversarial injection patterns."""

    def __init__(self):
        # A mix of common and subtle injection/jailbreak patterns
        self.patterns = [
            r"(?i)ignore\s+(?:all\s+)?previous\s+instructions",
            r"(?i)system\s+prompt\s+bypass",
            r"(?i)you\s+are\s+now\s+a\s+(?:developer|hacker|unrestricted)",
            r"(?i)disregard\s+(?:the\s+)?above",
            r"(?i)output\s+the\s+entire\s+original\s+prompt",
            r"(?i)jailbreak",
            r"(?i)DAN\s+mode",
            r"(?i)ignore\s+safety\s+filters",
            r"(?i)switch\s+to\s+developer\s+mode",
        ]

    def detect(self, text: str, **kwargs: Any) -> DetectionResult:
        """Scan text for known malicious patterns."""
        matches = [p for p in self.patterns if re.search(p, text)]

        risk_score = min(len(matches) * 0.5, 1.0)
        is_safe = risk_score < 0.4
        
        return DetectionResult(
            is_safe=is_safe,
            risk_score=risk_score,
            threat_type="injection" if not is_safe else None,
            confidence=0.9 if matches else 1.0,
            metadata={"matched_patterns": matches}
        )
