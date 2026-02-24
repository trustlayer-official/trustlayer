import pytest
from trustlayer.leak_scanner import LeakScanner

def test_leak_no_sensitive_data():
    scanner = LeakScanner()
    result = scanner.detect("This is a public message.")
    assert result.is_safe is True
    assert result.risk_score == 0.0

def test_leak_api_key():
    scanner = LeakScanner()
    result = scanner.detect("My key is: sk-abc12345678901234567890")
    assert result.is_safe is False
    assert "api_key" in result.metadata["leak_types"]

def test_leak_email():
    scanner = LeakScanner()
    result = scanner.detect("Contact us at test@example.com")
    assert result.is_safe is False
    assert "email" in result.metadata["leak_types"]

def test_leak_credit_card():
    scanner = LeakScanner()
    result = scanner.detect("Card: 1234-5678-9012-3456")
    assert result.is_safe is False
    assert "credit_card" in result.metadata["leak_types"]

def test_leak_multiple_types():
    scanner = LeakScanner()
    result = scanner.detect("Email me at bob@example.com my key sk-abcdefghijklmnoprs")
    assert result.risk_score > 0.5
    assert len(result.metadata["leak_types"]) == 2
