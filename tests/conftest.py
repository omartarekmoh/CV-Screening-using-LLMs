# This file ensures pytest recognizes the tests directory
# You can add shared fixtures here if needed

import pytest


@pytest.fixture(scope="session")
def base_url():
    return "http://localhost:8000"