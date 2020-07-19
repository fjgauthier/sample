from unittest import mock

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


@pytest.fixture
def bypass_db_sample():
    with mock.patch("sqlite3.connect"):
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


def test_shortTest(bypass_db_sample):
    bypass_db_sample.connection.fetchall.return_value = [
        {'shape_id': 1, 'shape_name': 'triangle', 'x': 0.0, 'y': 0.0, 'z': 0.0},
        {'shape_id': 1, 'shape_name': 'triangle', 'x': 2.0, 'y': 2.0, 'z': 0.0},
        {'shape_id': 1, 'shape_name': 'triangle', 'x': 2.0, 'y': 0.0, 'z': 0.0},
        {'shape_id': 2, 'shape_name': 'rectangle', 'x': 0.0, 'y': 0.0, 'z': 0.0},
        {'shape_id': 2, 'shape_name': 'rectangle', 'x': 4.0, 'y': 0.0, 'z': 0.0},
        {'shape_id': 2, 'shape_name': 'rectangle', 'x': 4.0, 'y': 2.0, 'z': 0.0},
        {'shape_id': 2, 'shape_name': 'rectangle', 'x': 0.0, 'y': 2.0, 'z': 0.0},
    ]
    bypass_db_sample.load_database()
    assert len(bypass_db_sample) == 2
    assert len(bypass_db_sample.shapes[1]) == 3
    assert bypass_db_sample.shapes[1].shape_name == 'triangle'
    assert len(bypass_db_sample.shapes[2]) == 4
    assert bypass_db_sample.shapes[2].shape_name == 'rectangle'
