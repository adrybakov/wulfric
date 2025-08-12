.. _user-guide_usage_package-scheme:

*****************
Package structure
*****************

Wulfric is a collection of functions, that are implemented in the submodules and grouped
by some concept (i.e. ``cell``, ``io``, ...).

Firs of all, one need to import the package

.. doctest::

  >>> import wulfric
  >>> # or
  >>> import wulfric

Through the ``wulf`` one can access all submodules and the top-level functions of wulfric.

Each submodule expose access to a number of constants and/or functions and/or classes.

We invite you to explore the package structure in the interactive python console.
Alternatively, public part of the package is documented in :ref:`api`.
