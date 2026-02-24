import pytest
from trustlayer.risk_scoring import RiskScoring
from trustlayer.models import DetectionResult

def test_risk_scoring_empty():
    assert RiskScoring.aggregate([]) == 0.0

def test_risk_scoring_single_high():
    results = [DetectionResult(is_safe=False, risk_score=0.8)]
    assert RiskScoring.aggregate(results) == 0.8

def test_risk_scoring_all_low():
    results = [
        DetectionResult(is_safe=True, risk_score=0.1),
        DetectionResult(is_safe=True, risk_score=0.1)
    ]
    assert RiskScoring.aggregate(results) == 0.1

def test_risk_scoring_multiple_medium():
    results = [
        DetectionResult(is_safe=False, risk_score=0.4),
        DetectionResult(is_safe=False, risk_score=0.4)
    ]
    # 0.4 + (0.1 * (2-1)) = 0.5
    assert RiskScoring.aggregate(results) == 0.5

def test_risk_scoring_max_cap():
    results = [
        DetectionResult(is_safe=False, risk_score=0.9),
        DetectionResult(is_safe=False, risk_score=0.8),
        DetectionResult(is_safe=False, risk_score=0.8)
    ]
    assert RiskScoring.aggregate(results) == 1.0
