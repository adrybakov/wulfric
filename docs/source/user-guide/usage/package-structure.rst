.. _user-guide_usage_package-scheme:

*****************
Package structure
*****************

Wulfric is a collection of functions, that are implemented in the submodules, grouped by
some concept (i.e. ``cell``, ``io``, ...).

Firs of all one need to import the package

.. doctest::

  >>> import wulfric as wulf
  >>> # or
  >>> import wulfric

Throughout this documentation we will import wulfric as mentioned above or assume that it
was imported in that way. If the package is imported in that way, then through the ``wulf``
one can access all submodules of wulfric as well as the top-level functions.

Package scheme
==============

Wulfric consists of several submodules and top-level functions. Each submodule expose
access to a number of constants and/or functions and/or classes. The majority of Wulfric
is as functions.

We invite you to explore the package structure in the interactive python console.
Alternatively public part of the package is documented in :ref:`api`.

In the next pages we describe how to use wulfric for the particular tasks and introduce
the key concepts.
