from unittest import TestCase
import copper

data = 4.3


class TestCopper(TestCase):

    def test_series(self):
        """
        Simple series test:

            -- a - b --
        """
        a = _FBlock()
        b = _GBlock()
        p = copper.Pipeline([a, b])
        result = p.process(data)

        self.assertEqual(result, _g(_f(data)))

    def test_parallel(self):
        """
        Simple parallel structure:

              .- a -.
              |     |
            --+     +==
              |     |
              '- b -'
        """
        a = _FBlock()
        b = _GBlock()
        p = copper.Pipeline((a, b))
        result = p.process(data)

        self.assertEqual(result, [_f(data), _g(data)])

    def test_parallel_series(self):
        """
        Simple parallel to series structure:

              .- a -.
              |     |
            --+     += c --
              |     |
              '- b -'
        """
        a = _FBlock()
        b = _GBlock()
        c = _TwoIn()
        p = copper.Pipeline([(a, b), c])
        result = p.process(data)

        self.assertEqual(result, _twoin(_f(data), _g(data)))

    def test_composite(self):
        """
        Composite pipeline (pipeline within a pipeline):

            m:
                -- a - b --
            p:
                  .- m -.
                  |     |
                --+     += d --
                  |     |
                  '- c -'
        """
        a = _FBlock()
        b = _GBlock()
        m = copper.Pipeline([a, b])
        c = _FBlock()
        d = _TwoIn()
        p = copper.Pipeline([(m, c), d])
        result = p.process(data)

        self.assertEqual(result, _twoin(_g(_f(data)), _f(data)))

    def test_passthrough(self):
        """
        Pass-through pipeline test

            m:
                  .--------.
                  |        |
                  +- b -.  |
                  |     |  |
                --+     +==+==
                  |     |
                  '- c -'
            p:
                -- a - m = d --
        """
        b = _FBlock()
        c = _GBlock()
        m = copper.PassthroughPipeline((b, c))
        a = _FBlock()
        d = _ThreeIn()
        p = copper.Pipeline([a, m, d])
        result = p.process(data)

        ares = _f(data)
        self.assertEqual(result, _threein(ares, _f(ares), _g(ares)))

    def test_clear(self):
        """
        Clearing a stateful block.
        """
        init = 4
        b = _Stateful(init)
        p = copper.Pipeline([b])
        p.process(data)

        self.assertEqual(b.data, _f(data))
        b.clear()
        self.assertEqual(b.data, init)


def _f(x):
    return 2 * x + 1


def _g(x):
    return (x + 3) / (3 - x)


def _twoin(x, y):
    return (4 * x) + y + 3


def _threein(x, y, z):
    return (x * y) + z


class _FBlock(copper.PipelineBlock):

    def process(self, data):
        return _f(data)


class _GBlock(copper.PipelineBlock):

    def process(self, data):
        return _g(data)


class _TwoIn(copper.PipelineBlock):

    def process(self, data):
        a, b = data
        return _twoin(a, b)


class _ThreeIn(copper.PipelineBlock):

    def process(self, data):
        a, b, c = data
        return _threein(a, b, c)


class _Stateful(copper.PipelineBlock):

    def __init__(self, initial):
        self.initial = initial
        self.clear()

    def clear(self):
        self.data = self.initial

    def process(self, data):
        self.data = _f(data)
        return self.data
