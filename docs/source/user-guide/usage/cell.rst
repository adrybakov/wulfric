.. _user-guide_usage_cell:

***********************
Manipulations with cell
***********************


For the full technical reference see :ref:`api_cell`.

On this page we give examples of what can be done with the ``cell`` introduced on the
:ref:`key concepts <user-guide_usage_key-concepts_cell>` page. Cell-related functions are
available under ``wulfric.cell`` submodule. For the examples of this page we assume the
imports and an example cell of the form

.. doctest::

  >>> import wulfric
  >>> import numpy as np
  >>> cell = [
  ...     [3.553350, 0.000000, 0.000000],
  ...     [0.000000, 4.744935, 0.000000],
  ...     [0.000000, 0.000000, 8.760497],
  ... ]


Cell parameters
===============

A valid cell can be characterized by the set of six parameters

============== ==========================================================================
============== ==========================================================================
:math:`a`      Length of the first lattice vector :math:`\boldsymbol{a}_1` (``cell[0]``)
:math:`b`      Length of the second lattice vector :math:`\boldsymbol{a}_2` (``cell[1]``)
:math:`c`      Length of the third lattice vector :math:`\boldsymbol{a}_3` (``cell[2]``)
:math:`\alpha` Angel between :math:`\boldsymbol{a}_2` and :math:`\boldsymbol{a}_3`
:math:`\beta`  Angel between :math:`\boldsymbol{a}_1` and :math:`\boldsymbol{a}_3`
:math:`\gamma` Angel between :math:`\boldsymbol{a}_1` and :math:`\boldsymbol{a}_2`
============== ==========================================================================

To compute parameters from the cell use

.. doctest::

  >>> wulfric.cell.get_params(cell)
  (3.55335, 4.744935, 8.760497, 90.0, 90.0, 90.0)

Note that when ``cell`` converted to ``params`` the information about its spacial
orientation is lost.

To create a cell from parameters use

.. doctest::

  >>> # we use np.round to account for the finite precision of float point arithmetic
  >>> np.round(wulfric.cell.from_params(3.55335, 4.744935, 8.760497, 90.0, 90.0, 90.0), 6)
  array([[3.55335 , 0.      , 0.      ],
         [0.      , 4.744935, 0.      ],
         [0.      , 0.      , 8.760497]])

The cell is constructed with the first vector oriented along the :math:`x` axis and second
vector in the :math:`xy` plain. The cell can only be constructed from the set of parameters
that can form parallelepiped (see :py:func:`.geometry.parallelepiped_check`).

Note ``wulfric.cell.from_params(wulfric.cell.get_params(cell))`` is not guaranteed to recover
the original ``cell``, as the information about the orientation of lattice vectors in
Cartesian reference frame is lost after the call of the first function.


Reciprocal lattice
==================

Any ``cell`` defines a lattice and its reciprocal counterpart. To compute the cell of the
reciprocal lattice use

.. doctest::

  >>> rcell = wulfric.cell.get_reciprocal(cell)
  >>> rcell
  array([[1.76824273, 0.        , 0.        ],
         [0.        , 1.32418786, 0.        ],
         [0.        , 0.        , 0.71721791]])


Reciprocal cell is a valid cell as well, therefore, to compute the cell of the real-space
lattice just use the same function again:

.. doctest::

  >>> wulfric.cell.get_reciprocal(rcell)
  array([[3.55335 , 0.      , 0.      ],
         [0.      , 4.744935, 0.      ],
         [0.      , 0.      , 8.760497]])

To construct the cell for the one of the :ref:`user-guide_conventions_bravais-lattices`
use dedicated functions:

.. doctest::

  >>> wulfric.cell.SC_CUB(a=1)
  array([[1, 0, 0],
         [0, 1, 0],
         [0, 0, 1]])
  >>> mcl = wulfric.cell.SC_MCL(a=1, b=4, c=5, alpha=70)
  >>> mcl
  array([[1.        , 0.        , 0.        ],
         [0.        , 4.        , 0.        ],
         [0.        , 1.71010072, 4.6984631 ]])

Required lattice parameters are different for each Bravias lattice type. Wulfric has
functions for all 14 Bravais lattice types, see :ref:`API <api_cell_bravais-lattice>` for
details.
