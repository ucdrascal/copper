import pytest
import numpy as np
from scipy import signal

from numpy.testing import assert_array_equal, assert_array_almost_equal

import copper

np.random.seed(12345)

rand_data_1d = np.random.rand(100)
rand_data_2d1 = np.random.rand(1, 100)
rand_data_2d = np.random.rand(5, 100)

b, a = signal.butter(2, (10/1000, 450/1000), btype='bandpass')


class _NthSampleFeature(object):
    def __init__(self, ind, channel=None):
        self.ind = ind
        self.channel = channel

    def compute(self, data):
        if self.channel is None:
            return data[:, self.ind]
        else:
            return data[self.channel, self.ind]


def _window_generator(data, length):
    for i in range(0, data.shape[-1], length):
        yield data[:, i:i+length]


def test_windower_no_overlap():
    # make sure windower handles data the same length as the window
    data = rand_data_2d
    windower = copper.Windower(10)

    for samp in _window_generator(data, 10):
        win = windower.process(samp)

    assert_array_equal(win, data[:, -10:])


def test_windower_overlap():
    # make sure window overlap works correctly
    data = rand_data_2d
    windower = copper.Windower(13)

    for samp in _window_generator(data, 10):
        win = windower.process(samp)

    assert_array_equal(win, data[:, -13:])


def test_windower_1d():
    # make sure a 1D array raises an error
    data = np.array([1, 2, 3, 4])
    windower = copper.Windower(10)

    with pytest.raises(ValueError):
        windower.process(data)


def test_windower_short():
    # make sure an exception is raised if the window length is too short
    data = rand_data_2d
    windower = copper.Windower(data.shape[1]-1)

    with pytest.raises(ValueError):
        windower.process(data)


def test_windower_clear():
    # make sure clearing the windower allows for changing number of channels
    data = rand_data_2d
    windower = copper.Windower(data.shape[1]+1)
    windower.process(data)

    with pytest.raises(ValueError):
        windower.process(rand_data_2d1)

    windower.clear()

    windower.process(rand_data_2d1)


def test_filter_overlap():
    # make sure output is continuous when filtering overlapped data
    data = rand_data_2d
    win_length = 10
    overlap = 5
    block = copper.Filter(b, a, overlap=overlap)

    data1 = data[:, 0:win_length]
    data2 = data[:, win_length-overlap:win_length-overlap+win_length]
    out1 = block.process(data1)
    out2 = block.process(data2)

    assert_array_almost_equal(out1[:, -overlap:], out2[:, :overlap])


def test_fextractor_simple():
    f0 = _NthSampleFeature(0)
    ex = copper.FeatureExtractor([('0', f0),
                                  ('1', _NthSampleFeature(1))])
    data = np.array([[0, 1, 2, 3, 4],
                     [5, 6, 7, 8, 9]])

    assert_array_equal(np.array([0, 5, 1, 6]), ex.process(data))
    assert_array_equal(np.array([0, 5, 1, 6]), ex.process(data))

    assert ex.feature_indices['0'] == (0, 2)
    assert ex.feature_indices['1'] == (2, 4)

    assert ex.named_features['0'] is f0


def test_fextractor_unequal_feature_sizes():
    ex = copper.FeatureExtractor([('0', _NthSampleFeature(0)),
                                  ('1', _NthSampleFeature(2, channel=1))])
    data = np.array([[0, 1, 2, 3, 4],
                     [5, 6, 7, 8, 9]])
    assert_array_equal(np.array([0, 5, 7]), ex.process(data))


def test_fextractor_clear():
    ex = copper.FeatureExtractor([('0', _NthSampleFeature(0)),
                                  ('1', _NthSampleFeature(2))])
    data_2ch = np.array([[0, 1, 2, 3, 4],
                         [5, 6, 7, 8, 9]])
    data_1ch = np.array([[0, 1, 2, 3, 4]])

    assert_array_equal(np.array([0, 5, 2, 7]), ex.process(data_2ch))
    ex.clear()
    assert_array_equal(np.array([0, 2]), ex.process(data_1ch))


def test_ensure2d_row():
    data = rand_data_1d
    b = copper.Ensure2D()
    b_exp = copper.Ensure2D(orientation='row')

    truth = data[np.newaxis, :]
    assert_array_equal(truth, b.process(data))
    assert_array_equal(truth, b_exp.process(data))


def test_ensure2d_col():
    data = rand_data_1d
    b = copper.Ensure2D(orientation='col')

    truth = data[:, np.newaxis]
    assert_array_equal(truth, b.process(data))
