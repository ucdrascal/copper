class PipelineBlock(object):

    def process(self, data):
        out = data
        return out

    def __repr__(self):
        return "%s.%s()" % (
            self.__class__.__module__,
            self.__class__.__name__
        )


class Pipeline(PipelineBlock):

    def __init__(self, blocks):
        self.blocks = blocks

    def process(self, data):
        out = _process_block(self.blocks, data)
        return out


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


def _process_block(block, data):
    if type(block) is list:
        out = _process_series(block, data)
    elif type(block) is tuple:
        out = _process_parallel(block, data)
    else:
        out = block.process(data)

    return out


def _process_series(block, data):
    out = data
    for b in block:
        out = _process_block(b, out)

    return out


def _process_parallel(block, data):
    out = []
    for b in block:
        out.append(_process_block(b, data))

    return out
