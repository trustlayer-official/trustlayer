# Contributing to TrustLayer

We love contributions! Whether it's a new detector, a bug fix, or a typo, feel free to open a PR.

## Development Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/your-org/trustlayer.git
   ```
2. Install dev dependencies:
   ```bash
   pip install pytest
   ```
3. Run tests:
   ```bash
   pytest tests/
   ```

## Creating a Custom Detector

Just inherit from `BaseDetector` and implement the `detect` method. Make sure to return a `DetectionResult` object.

```python
from trustlayer import BaseDetector, DetectionResult

class MyDetector(BaseDetector):
    def detect(self, text, **kwargs):
        # logic here
        return DetectionResult(...)
```

## Pull Request Process

1. Create a new branch.
2. Ensure all tests pass.
3. Update documentation if needed.
4. Submit the PR!
