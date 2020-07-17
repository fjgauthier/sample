import numpy

import pytest

from sample import Sample, SampleError, Shape


@pytest.fixture
def numbers():
    return numpy.array([1.0, 2.0, 3.0, 4.0, 5.0])


@pytest.fixture
def empty_shape():
    test_sample = Sample(':memory:')
    test_sample.create_empty_database()
    return test_sample


def test_simple(numbers):
    assert len(numbers) == 5


def test_empty_database(empty_shape):
    assert len(empty_shape) == 0


def test_add_shape(empty_shape):
    shape = Shape(1, 'Polygon')
    shape.add_point(0.0, 0.0, 0.0)
    empty_shape.add_shape(shape)
    assert len(empty_shape) == 1


def test_centroid():
    shape = Shape(1, 'Polygon')
    shape.add_point(0.0, 0.0, 0.0)
    shape.add_point(0.0, 2.0, 0.0)
    shape.add_point(2.0, 2.0, 0.0)
    shape.add_point(2.0, 0.0, 0.0)

    assert numpy.array_equal(shape.centroid(), numpy.array([1.0, 1.0, 0.0]))


@pytest.mark.xfail(raises=ZeroDivisionError)
def test_centroid_empty():
    shape = Shape(1, 'Polygon')
    shape.centroid()


@pytest.mark.xfail(raises=SampleError)
def test_add_shape_incorrect(empty_shape):
    empty_shape.add_shape('foo')
