::

     ┌─□─  ┌─□─┐   ┌─□─┐   ┌─□─┐   ┌─□─┐   ┌─□──
    ─┤    ─┤   ├─ ─┤   ├─ ─┤   ├─ ─┼─□─┴─ ─┤
     └─□─  └─□─┘   ├─□─┘   ├─□─┘   └───    │
                   │       │


``copper`` is a small infrastructure for processing data in a pipeline style.
You create pipeline blocks, then connect them up with an efficient (but still
readable) syntax. It was originally created for flexibly creating pipelines in
real-time signal processing applications, but it can be useful in offline
applications as well.


.. toctree::
   :maxdepth: 2

   guide
   api
