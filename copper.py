class PipelineBlock(object):

    def process(self, data):
        out = data
        return out

    def clear(self):
        pass

    def __repr__(self):
        return "%s.%s()" % (
            self.__class__.__module__,
            self.__class__.__name__
        )


class Pipeline(PipelineBlock):
    """
    Container for processing a set of PipelineBlock objects arranged in a
    block diagram structure.

    To create a pipeline, the following two rules are needed: blocks in a list
    processed in series, and blocks in a tuple are processed in parallel.

    For example, the following feeds incoming data first to block `a`, and the
    output of block `a` is passed to both blocks `b` and `c`. The output of
    blocks `b` and `c` are then both passed to block `d`.

    >>> from pygesture import pipeline
    >>> a = pipeline.PipelineBlock()
    >>> b = pipeline.PipelineBlock()
    >>> c = pipeline.PipelineBlock()
    >>> d = pipeline.PipelineBlock()
    >>> p = pipeline.Pipeline([a, (b, c), d])

    Blocks that are arranged to take multiple inputs (such as block `d` in the
    above example) should expect to take the corresponding number of inputs in
    the order they are given. It is up to the user constructing the pipeline to
    make sure that the arrangement of blocks makes sense.

    Parameters
    ----------
    blocks : nested lists/tuples of objects derived from PiplineBlock
        The blocks in the pipline, with lists processed in series and tuples
        processed in parallel.
    """

    def __init__(self, blocks):
        self.blocks = blocks

    def process(self, data):
        """
        Calls the `process` method of each block in the pipeline, passing the
        outputs around as specified in the block structure.

        Parameters
        ----------
        data : object
            The input to the first block(s) in the pipeline. The type/format
            doesn't matter to copper, as long as the blocks you define accept
            it.

        Returns
        -------
        out : object
            The data output by the `process` method of the last block(s) in the
            pipeline.
        """
        out = _call_block('process', self.blocks, data)
        return out

    def clear(self):
        """
        Calls the `clear` method on each block in the pipeline. The effect
        depends on the blocks themselves.
        """
        _call_block('clear', self.blocks)


class PassthroughPipeline(Pipeline):

    def __init__(self, blocks, expand_output=True):
        super(PassthroughPipeline, self).__init__(blocks)
        self.expand_output = expand_output

    def process(self, data):
        out = Pipeline.process(self, data)
        if self.expand_output:
            l = [data]
            l.extend(out)
            return l
        else:
            return data, out


def _call_block(fname, block, data=None):
    if type(block) is list:
        out = _call_list(fname, block, data)
    elif type(block) is tuple:
        out = _call_tuple(fname, block, data)
    else:
        f = getattr(block, fname)
        if data is not None:
            out = f(data)
        else:
            out = f()

    return out


def _call_list(fname, block, data=None):
    out = data
    for b in block:
        out = _call_block(fname, b, out)

    return out


def _call_tuple(fname, block, data=None):
    out = []
    for b in block:
        out.append(_call_block(fname, b, data))

    return out
