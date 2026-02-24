import pytest
from trustlayer.hallucination import HallucinationDetector

def test_hallucination_confident_text():
    detector = HallucinationDetector()
    result = detector.detect("The capital of France is Paris.")
    assert result.is_safe is True
    assert result.risk_score == 0.0

def test_hallucination_hedge_words():
    detector = HallucinationDetector()
    result = detector.detect("I think maybe the answer is 42.")
    assert result.risk_score > 0.1
    assert "hedge_words" in result.metadata
    assert len(result.metadata["hedge_words"]) >= 2

def test_hallucination_short_text():
    detector = HallucinationDetector()
    result = detector.detect("Ok.")
    assert result.metadata["is_short"] is True
    assert result.risk_score >= 0.1

def test_hallucination_unsafe_combination():
    detector = HallucinationDetector()
    result = detector.detect("I think maybe I'm not sure.")
    assert result.risk_score >= 0.2
    assert result.is_safe is True

def test_hallucination_metadata_accuracy():
    detector = HallucinationDetector()
    result = detector.detect("As an AI, I'm not sure.")
    assert "As an AI" in result.metadata["hedge_words"]
    assert "I'm not sure" in result.metadata["hedge_words"]
