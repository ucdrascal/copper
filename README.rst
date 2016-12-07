::

     ┌─□─  ┌─□─┐   ┌─□─┐   ┌─□─┐   ┌─□─┐   ┌─□──
    ─┤    ─┤   ├─ ─┤   ├─ ─┤   ├─ ─┼─□─┴─ ─┤
     └─□─  └─□─┘   ├─□─┘   ├─□─┘   └───    │
                   │       │


.. image:: https://api.travis-ci.org/ucdrascal/copper.svg?branch=master
    :target: https://travis-ci.org/ucdrascal/copper
    :alt: Travis CI Status

.. image:: https://codecov.io/gh/ucdrascal/copper/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/ucdrascal/copper
    :alt: Code Coverage Status

.. image:: https://readthedocs.org/projects/copper/badge/?version=latest
   :target: http://copper.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status


``copper`` is a small infrastructure for processing data in a pipeline style.
You create pipeline blocks, then connect them up with an efficient (but still
readable) syntax. It was originally created for flexibly creating pipelines
in real-time signal processing applications.
