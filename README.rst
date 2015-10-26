::

     ┌─□─  ┌─□─┐   ┌─□─┐   ┌─□─┐   ┌─□─┐   ┌─□──
    ─┤    ─┤   ├─ ─┤   ├─ ─┤   ├─ ─┼─□─┴─ ─┤
     └─□─  └─□─┘   ├─□─┘   ├─□─┘   └───    │
                   │       │

``copper`` is a small infrastructure for processing data in a pipeline style.
You create pipeline blocks, then connect them up with an efficient (but still
readable) syntax. It was originally created for flexibly creating pipelines
in real-time signal processing applications.

The syntax for expressing pipeline structure is based on lists and tuples.
Lists hold elements that are connected in series::

    [a, b]:

        ─a─b─

The input is whatever ``a`` takes, and the output is whatever ``b`` outputs.
Tuples hold elements that are connected in parallel::

    (a, b):

         ┌─a─┐
        ─┤   ┝━
         └─b─┘

The input goes to *both* ``a`` and ``b``, and the output is whatever ``a`` and
``b`` output in a list. If we connect another element in series with a parallel
block, it must be a block that handles multiple inputs::

    [(a, b), c]:

         ┌─a─┐
        ─┤   ┝━c─
         └─b─┘

The bottom line is: pipeline blocks **accept** input types and they **specify**
the output types. You are responsible for ensuring that pipeline blocks can be
connected as specified.

Sometimes, you might want to pass the output of a block to some block structure
*and* somewhere downstream. To handle this case, ``copper`` has
a "pass-through" pipeline that you can use as a block within another pipeline::

    passthrough pipeline p ← (b, c):

         ┌─────┐
         ├─b─┐ │
        ─┤   ┝━┷━
         └─c─┘

    [a, p, d]:

        ─a─p━d─

The pass-through pipeline places its own output(s) after its input, so the
input is accesible on the other side. There are cases where this type of
structure is possible with a list/tuple expression, but sometimes the
pass-through pipeline as a block is needed. The above example is one of those
cases.


Implementing Pipelines
----------------------

Pipeline blocks are simple to implement. It is only expected that you implement
a ``process()`` method which takes one argument (``data``) and returns
something. For multi-input blocks, you'll probably want to just expand the
inputs right off the bat (e.g. ``in_a, in_b = data``). Usually, the output is
some processed form of the input data::

    import copper

    class FooBlock(copper.PipelineBlock):
        def process(self, data):
            return data + 1

    class BarBlock(copper.PipelineBlock):
        def process(self, data):
            return 2 * data

With some blocks implemented, the list/tuple syntax described above is used for
specifying how they are connected::

    a = FooBlock()
    b = BarBlock()
    p = copper.Pipeline([a, b])

Now, you just give the pipeline input and get its output::

    input = 3
    result = p.process(input)

In this case, the result would be ``2 * (input + 1) == 8``.
