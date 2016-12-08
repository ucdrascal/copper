import pytest
import numpy as np
import copper


@pytest.fixture
def array_2d():
    return np.array([[1, 2, 3, 4], [5, 6, 7, 8]])


@pytest.fixture
def array_1d():
    return np.array([1, 2, 3, 4, 5])


def test_ensure_2d(array_1d, array_2d):
    np.testing.assert_equal(copper.util.ensure_2d(array_2d), array_2d)
    assert copper.util.ensure_2d(array_1d).ndim == 2


def test_rolling_window_1d(array_1d):
    out = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])
    np.testing.assert_equal(copper.util.rolling_window(array_1d, 2), out)


def test_rolling_window_2d(array_2d):
    out = np.array([[[1, 2], [2, 3], [3, 4]], [[5, 6], [6, 7], [7, 8]]])
    np.testing.assert_equal(copper.util.rolling_window(array_2d, 2), out)
