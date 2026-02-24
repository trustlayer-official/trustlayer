from typing import List, Optional, Any
from .models import BaseDetector, GuardResponse, DetectionResult
from .injection_detector import InjectionDetector
from .leak_scanner import LeakScanner
from .hallucination import HallucinationDetector
from .risk_scoring import RiskScoring
from .utils import logger

class Guard:
    """Core engine for validating text against security policies."""

    def __init__(self, custom_detectors: Optional[List[BaseDetector]] = None):
        """Setup guard with default and optional custom detectors."""
        self.detectors: List[BaseDetector] = [
            InjectionDetector(),
            LeakScanner(),
            HallucinationDetector(),
        ]
        
        if custom_detectors:
            self.detectors.extend(custom_detectors)
            
        logger.info(f"Guard initialized with {len(self.detectors)} detectors.")

    def validate(self, text: str, **kwargs: Any) -> GuardResponse:
        """Run validation checks on the provided text."""
        results: List[DetectionResult] = []
        
        for detector in self.detectors:
            try:
                results.append(detector.detect(text, **kwargs))
            except Exception as e:
                logger.error(f"Detector {detector.__class__.__name__} failed: {e}")
                results.append(DetectionResult(
                    is_safe=False, 
                    risk_score=1.0, 
                    threat_type="detector_error",
                    metadata={"error": str(e)}
                ))

        risk_score = RiskScoring.aggregate(results)
        
        # Determine the primary threat based on highest risk
        primary_threat = None
        highest_risk = 0.0
        for r in results:
            if r.risk_score > highest_risk and r.threat_type:
                highest_risk = r.risk_score
                primary_threat = r.threat_type

        # Redact the output if the risk exceeds our threshold
        safe_output = text
        if risk_score >= 0.5:
            safe_output = "[REDACTED DUE TO SECURITY RISK]"

        avg_confidence = (sum(r.confidence for r in results) / len(results)) if results else 1.0

        return GuardResponse(
            safe_output=safe_output,
            risk_score=risk_score,
            threat_type=primary_threat,
            confidence=round(avg_confidence, 2),
            results=results
        )
