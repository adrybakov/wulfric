.. _contribute_tests:

*******
Testing
*******

In Wulfric we rely on |pytest|_, |hypothesis|_ and |doctest|_ for testing.

Unit tests
==========

All unit tests are located in the "src/wulfric/_tests" directory.  To run the
tests, use (on Linux and macOS)

.. code-block:: bash

  wulfric test

The structure of the "_tests" directory loosely follows the structure of the
"src/wulfric" directory.

Documentation tests
===================

Across the documentation there are many examples of how to use Wulfric.  These
code snippets are tested using |doctest|_ and ensure that the documentation
correctly reflects actual behavior of the code. To run doctests you need to
build the :ref:`documentation <contribute_docs>` and then run the doctests

.. code-block:: bash

  make doctest
