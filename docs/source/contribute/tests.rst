.. _contribute_tests:

*******
Testing
*******

In wulfric we rely on |pytest|_, |hypothesis|_ and |doctest|_ for testing.

Unit tests
==========

All unit tests are located in the "utest" directory.
To run the tests use (on Linux and MacOS)::

    make test

Structure of the "utest" directory loosely follows the structure of the "src/wulfric"
directory.

Documentation tests
===================

Across the documentation there are many examples of how to use wulfric with code snippets.
These code snippets are tested using |doctest|_ and ensure that the documentation
correctly reflects an actual behavior of the code. To run doctests you need to build the
:ref:`documentation <contribute_docs>` and then run the doctests::

    make doctest
