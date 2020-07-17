import numpy

import pytest

from sample import Sample


@pytest.fixture
def numbers():
    return numpy.array([1.0, 2.0, 3.0, 4.0, 5.0])


def test_simple(numbers):
    assert len(numbers) == 5


def test_empty_database():
    test_sample = Sample(':memory:')
    test_sample.create_empty_database()
    assert len(test_sample) == 0
