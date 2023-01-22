import random
import pytest


@pytest.fixture
def random_seed():
    random.seed(42)
