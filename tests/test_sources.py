import pytest
import numpy as np
from numpy.testing import assert_equal
import copper


def test_segment_simple():
    x = np.arange(6)
    segs = list(copper.segment(x, 2))
    assert_equal(segs[0], np.array([[0, 1]]))
    assert_equal(segs[1], np.array([[2, 3]]))
    assert len(segs) == 3


def test_segment_overlap():
    x = np.random.randn(100)
    segs = list(copper.segment(x, 10, overlap=5))
    assert_equal(segs[0][:, -5:], segs[1][:, :5])


def test_segment_indices_simple():
    segs = list(copper.segment_indices(8, 2))
    assert segs == [(0, 2), (2, 4), (4, 6), (6, 8)]


def test_segment_indices_overlap():
    segs = list(copper.segment_indices(9, 3, overlap=2))
    assert segs == [(0, 3), (1, 4), (2, 5), (3, 6), (4, 7), (5, 8), (6, 9)]


def test_segment_indices_bad_length():
    with pytest.warns(UserWarning):
        list(copper.segment_indices(11, 5))

    with pytest.warns(UserWarning):
        list(copper.segment_indices(12, 5, overlap=2))
