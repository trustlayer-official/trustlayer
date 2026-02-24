from typing import List
from .models import DetectionResult

class RiskScoring:
    """Aggregates multiple detection results into a single risk score."""

    @staticmethod
    def aggregate(results: List[DetectionResult]) -> float:
        """Calculates a normalized risk score from multiple results.

        Uses a weighted maximum approach: high-risk detections dominate.

        Args:
            results: List of DetectionResult objects.

        Returns:
            A normalized risk score between 0.0 and 1.0.
        """
        if not results:
            return 0.0
            
        # Prioritize the highest risk score detected
        max_risk = max(r.risk_score for r in results)
        
        # Penalize multiple medium risks
        count_risks = sum(1 for r in results if r.risk_score > 0.3)
        if count_risks > 1:
            max_risk = min(max_risk + (0.1 * (count_risks - 1)), 1.0)
            
        return round(max_risk, 2)
