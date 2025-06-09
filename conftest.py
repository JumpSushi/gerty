#!/usr/bin/env python3
"""
pytest configuration for GERTY Display tests
"""

import pytest
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure pytest
def pytest_configure(config):
    """Configure pytest settings"""
    config.addinivalue_line(
        "markers", 
        "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers",
        "integration: marks tests as integration tests"
    )

# Fixtures available to all tests
@pytest.fixture(scope="session")
def project_root():
    """Get the project root directory"""
    return Path(__file__).parent
