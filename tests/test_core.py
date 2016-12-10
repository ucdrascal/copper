import pytest
import copper

data = 4.3


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
        super(_Stateful, self).__init__()
        self.initial = initial
        self.clear()

    def clear(self):
        self.data = self.initial

    def process(self, data):
        self.data = _f(data)
        return self.data


class _NamedBlock(copper.PipelineBlock):

    def __init__(self, name=None):
        super(_NamedBlock, self).__init__(name=name)


class _HookEnabledBlock(copper.PipelineBlock):

    def __init__(self, hooks=None):
        super(_HookEnabledBlock, self).__init__(hooks=hooks)

    def process(self, data):
        return _f(data)


def test_series():
    """
    Simple series test:

        -- a - b --
    """
    a = _FBlock()
    b = _GBlock()
    p = copper.Pipeline([a, b])
    result = p.process(data)

    assert result == _g(_f(data))


def test_parallel():
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

    assert result == [_f(data), _g(data)]


def test_parallel_series():
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

    assert result == _twoin(_f(data), _g(data))


def test_composite():
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

    assert result == _twoin(_g(_f(data)), _f(data))


def test_passthrough():
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
    assert result == _threein(ares, _f(ares), _g(ares))


def test_passthrough_noexpand():
    # test passthrough block without expanding output
    a = _FBlock()
    b = _GBlock()
    c = copper.PassthroughPipeline((a, b), expand_output=False)
    assert c.process(data) == (data, [_f(data), _g(data)])


def test_clear():
    # clearing a stateful block.
    init = 4
    b = _Stateful(init)
    p = copper.Pipeline([b])
    p.process(data)

    assert b.data == _f(data)
    b.clear()
    assert b.data == init


def test_clear_pass():
    # make sure clear passes
    a = copper.PipelineBlock()
    a.clear()

    f = _FBlock()
    f.clear()


def test_clear_pipeline():
    init = 4
    b = _Stateful(init)
    p = copper.Pipeline([b])
    p.process(data)

    p.clear()
    assert b.data == init


def test_block_repr():
    b = copper.PipelineBlock()
    assert repr(b) == 'copper.core.PipelineBlock()'


def test_process_unimplemented():
    # unimplemented process method should raise error
    a = copper.PipelineBlock()
    with pytest.raises(NotImplementedError):
        a.process(0)

    class BadPipelineBlock(copper.PipelineBlock):
        pass

    a = BadPipelineBlock()
    with pytest.raises(NotImplementedError):
        a.process(0)


def test_named_block():
    # make sure block naming works.
    b = _NamedBlock()
    assert b.name == '_NamedBlock'

    b2 = _NamedBlock('blockname')
    assert b2.name == 'blockname'


def test_hooks():
    # test hooks for intermediate blocks.
    def hook1(out):
        assert out == _f(data)

    def hook2(out):
        assert out == _f(data)

    # first test just one hook
    a = _HookEnabledBlock(hooks=[hook1])
    b = _GBlock()

    p = copper.Pipeline([a, b])
    result = p.process(data)

    assert result == _g(_f(data))

    # test multiple hooks
    a = _HookEnabledBlock(hooks=[hook1, hook2])
    p = copper.Pipeline([a, b])

    result = p.process(data)

    assert result == _g(_f(data))


def test_block_access():
    # test access to blocks in a pipeline using `named_blocks`.
    a = _NamedBlock(name='a')
    b = _NamedBlock(name='b')

    p = copper.Pipeline([a, b])

    assert p.named_blocks['a'] is a
    assert p.named_blocks['b'] is b
    assert p.named_blocks['a'] is not b
    assert p.named_blocks['b'] is not a


def test_callable_block():
    # test block creation from function
    a = _FBlock()
    b = copper.CallablePipelineBlock(_g)
    p = copper.Pipeline([a, b])
    result = p.process(data)
    assert result == _g(_f(data))

    a = copper.CallablePipelineBlock(lambda x: x + 2)
    assert a.process(3) == 5
