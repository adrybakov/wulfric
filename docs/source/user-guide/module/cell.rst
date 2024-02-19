.. _user-guide_module_cell:

****
Cell
****

.. currentmodule:: wulfric

For the full technical reference see :ref:`api_cell`.

The :py:mod:`.Cell` combines a set of functions that are used for manipulations with unit cells.

It could have been a class with a number of ``@classmethods``, but we decided to write it as a
separate module. It is deliberately not included in the :py:class:`.Lattice`-:py:class:`.Crystall`
hierarchy, because it unites the methods that use only concepts of lattice vector (i.e.
:py:func:`.reciprocal` and :py:func:`.params`) as well as the ones that use the concept
of lattice and atoms (i.e. :py:func:`.primitive`).


Import
======

A number of import scenarios is possible:

* Import of the needed functions:

.. doctest::

  >>> # Explicit import
  >>> from wulfric.cell import params, reciprocal

* Import of the interface in the class-style syntax

.. doctest::

  >>> # Recommended import
  >>> from wulfric import Cell
  >>> # it is equivalent to
  >>> from wulfric import cell as Cell


Cell parameters
===============

Two functions that convert the cell parameters to the matrix of lattice vectors and vice versa.

* :py:func:`.Cell.params`: Cell -> parameters

.. doctest::

  >>> from wulfric import Cell
  >>> Cell.params([[ 1.,  0.,  0.],
  ...              [ 0.,  1.,  0.],
  ...              [ 0.,  0.,  1.]])
  (1.0, 1.0, 1.0, 90.0, 90.0, 90.0)

* :py:func:`.Cell.from_params`: Parameters -> cell

.. doctest::

  >>> from wulfric import Cell
  >>> # Rounding is used because of the floating point errors
  >>> import numpy as np
  >>> np.around(Cell.from_params(1, 1, 1, 90, 90, 90), 2)
  array([[1., 0., 0.],
         [0., 1., 0.],
         [0., 0., 1.]])

Reciprocal lattice
==================

.. math::

  \begin{matrix}
    \boldsymbol{b}_1 = \dfrac{2\pi}{V}\boldsymbol{a}_2\times\boldsymbol{a}_3 \\
    \boldsymbol{b}_2 = \dfrac{2\pi}{V}\boldsymbol{a}_3\times\boldsymbol{a}_1 \\
    \boldsymbol{b}_3 = \dfrac{2\pi}{V}\boldsymbol{a}_1\times\boldsymbol{a}_2 \\
  \end{matrix}

where :math:`V` is the volume of the unit cell.

.. doctest::

  >>> from wulfric import Cell
  >>> # Rounding is used because of the floating point errors
  >>> import numpy as np
  >>> np.around(Cell.reciprocal([[ 1.,  0.,  0.],
  ...                            [ 0.,  1.,  0.],
  ...                            [ 0.,  0.,  1.]]), 2)
  array([[6.28, 0.  , 0.  ],
         [0.  , 6.28, 0.  ],
         [0.  , 0.  , 6.28]])


Primitive cell
==============

Sometimes we are given some supercell and we want to find the primitive cell. The primitive cell
is the smallest cell that can reproduce the crystalline structure (:py:class:`.Lattice`
and set of :py:class:`.Atom`\ s).

.. warning::

  The function that computes the primitive cell is not implemented yet.
