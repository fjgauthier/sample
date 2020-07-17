import numpy

import pytest


@pytest.fixture
def numbers():
    return numpy.array([1.0, 2.0, 3.0, 4.0, 5.0])


def test_simple(numbers):
    assert len(numbers) == 5
    
