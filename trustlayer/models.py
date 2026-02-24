from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, List, Any

@dataclass
class DetectionResult:
    """Result of a single security check."""
    is_safe: bool
    risk_score: float
    threat_type: Optional[str] = None
    confidence: float = 1.0
    metadata: dict = field(default_factory=dict)

@dataclass
class GuardResponse:
    """Aggregated response from the TrustLayer Guard."""
    safe_output: str
    risk_score: float
    threat_type: Optional[str]
    confidence: float
    results: List[DetectionResult]

    def __repr__(self) -> str:
        return (f"GuardResponse(risk={self.risk_score}, threat={self.threat_type}, "
                f"safe={self.risk_score < 0.5})")

class BaseDetector(ABC):
    """Interface for implementing custom risk detectors."""

    @abstractmethod
    def detect(self, text: str, **kwargs: Any) -> DetectionResult:
        """Analyze text and return a DetectionResult."""
        pass
