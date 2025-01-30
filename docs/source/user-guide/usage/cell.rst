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

  >>> import wulfric as wulf
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

  >>> wulf.cell.get_params(cell)
  (3.55335, 4.744935, 8.760497, 90.0, 90.0, 90.0)

Note that when ``cell`` converted to ``params`` the information about its spacial
orientation is lost.

To create a cell from parameters use

.. doctest::

  >>> # we use np.round to account for the finite precision of float point arithmetic
  >>> np.round(wulf.cell.from_params(3.55335, 4.744935, 8.760497, 90.0, 90.0, 90.0), 6)
  array([[3.55335 , 0.      , 0.      ],
        [0.      , 4.744935, 0.      ],
        [0.      , 0.      , 8.760497]])

The cell is constructed with the first vector oriented along the :math:`x` axis and second
vector in the :math:`xy` plain. The cell can only be constructed from the set of parameters
that can form parallelepiped (see :py:func:`.geometry.parallelepiped_check`).

Note ``wulf.cell.from_params(wulf.cell.get_params(cell))`` is not guaranteed to recover
of the original ``cell``, as the information about the orientation of lattice vectors in
Cartesian reference frame is lost after the call of the first function.


Reciprocal lattice
==================

Any ``cell`` defines a lattice and its reciprocal counterpart. To compute the cell of the
reciprocal lattice use

.. doctest::

  >>> rcell = wulf.cell.get_reciprocal(cell)
  >>> rcell
  array([[1.76824273, 0.        , 0.        ],
        [0.        , 1.32418786, 0.        ],
        [0.        , 0.        , 0.71721791]])


Reciprocal cell is a valid cell as well, therefore, to compute the cell of the real-space
lattice just use the same function again:

.. doctest::

  >>> wulf.cell.get_reciprocal(rcell)
  array([[3.55335 , 0.      , 0.      ],
        [0.      , 4.744935, 0.      ],
        [0.      , 0.      , 8.760497]])

Bravais lattices
================

There is a full description of the :ref:`user-guide_conventions_bravais-lattices` with
their variations, examples, creation functions, details of standardizations. Please
consult it to learn more.

Type of the Bravail lattice might be computed via the :ref:`library_lepage` as

.. doctest::

  >>> # Note wulf.cell.lepage accept lattice parameters as input.
  >>> lattice_type = wulf.cell.lepage(*wulf.cell.get_params(cell))
  >>> lattice_type
  'ORC'

Some of the Bravais lattices have variations, to check the variation of the lattice use

.. doctest::

  >>> # Note there is no variation for the Orthorhombic lattice.
  >>> wulf.cell.get_variation(cell)
  'ORC'

Some of the characteristics of the Bravais lattice can be accessed from its type:

.. doctest::

  >>> # Note lattice_type = "ORC"
  >>> wulf.cell.get_name(lattice_type)
  'Orthorhombic'
  >>> wulf.cell.get_pearson_symbol(lattice_type)
  'oP'

To construct the cell for the one of the :ref:`user-guide_conventions_bravais-lattices`
use dedicated functions:

.. doctest::

  >>> wulf.cell.CUB(a=1)
  array([[1, 0, 0],
         [0, 1, 0],
         [0, 0, 1]])
  >>> mcl = wulf.cell.MCL(a=1, b=4, c=5, alpha=110)
  >>> mcl
  array([[1.        , 0.        , 0.        ],
         [0.        , 4.        , 0.        ],
         [0.        , 1.71010072, 4.6984631 ]])
  >>> # Note that alpha is 70, as the standardized primitive cell is returned
  >>> wulf.cell.get_params(mcl)
  (1.0, 4.0, 5.0, 70.0, 90.0, 90.0)

Required lattice parameters are different for each Bravias lattice type. Wulfric has
functions for all 14 Bravais lattice types, see :ref:`API <api_cell_bravais-lattice>` for
details.

Standardization
===============

An original goal of wulfric was to obtain high symmetry k paths in an automatic fashion
for any given cell. We follow the convention of the Setyawan and Curtarolo [1]_ for the
Bravais lattice types and high symmetry k points, where the definition of high symmetry
points is given for the standardized primitive cells. In wulfric the standardization is
represented by the :ref:`transformation matrix <user-guide_conventions_main_transformation>`
:math:`\boldsymbol{S}`. Actual transformation of the cell rarely needed if the matrix
:math:`\boldsymbol{S}` is knows. It allows to compute the high symmetry points for
arbitrary cell.

To obtain the transformation matrix :math:`\boldsymbol{S}` use

.. doctest::

  >>> wulf.cell.get_S_matrix(cell)
  array([[1., 0., 0.],
         [0., 1., 0.],
         [0., 0., 1.]])

If you need to compute standardized cell use:

.. doctest::

  >>> wulf.cell.get_standardized(cell)
  array([[3.55335 , 0.      , 0.      ],
         [0.      , 4.744935, 0.      ],
         [0.      , 0.      , 8.760497]])

For the example cell the matrix is an identity, indicated that it is already the standard
one.


Conventional cell
=================

If the standardized primitive cell is knows, then standardized convectional cell can be
computed. The transformation is described by the
:ref:`transformation matrix <user-guide_conventions_main_transformation>`
:math:`\boldsymbol{C}`. This matrix is specific to the lattice type and does not depend
on the specific cell

.. doctest::

  >>> wulf.cell.get_C_matrix(lattice_type)
  array([[1., 0., 0.],
         [0., 1., 0.],
         [0., 0., 1.]])

To get the conventional cell from the standardized primitive cell use

.. doctest::

  >>> wulf.cell.get_conventional(cell)
  array([[3.55335 , 0.      , 0.      ],
         [0.      , 4.744935, 0.      ],
         [0.      , 0.      , 8.760497]])

For the Orthorhombic lattice conventional and primitive cells are the same.

Note that wulfric *interprets* the input cell as the standardized primitive one. It is the
responsibility of the user to ensure that it is indeed the standardized primitive cell.



To read more about the conventional cells see :ref:`user-guide_conventions_cell` and
:ref:`user-guide_conventions_bravais-lattices`.



References
==========
.. [1] Setyawan, W. and Curtarolo, S., 2010.
    High-throughput electronic band structure calculations: Challenges and tools.
    Computational materials science, 49(2), pp.299-312.
