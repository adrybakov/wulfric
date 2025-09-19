.. _user-guide_usage_cell:

***********************
Manipulations with cell
***********************


For the full technical reference see :ref:`api_cell`.

On this page we give examples of what can be done with the ``cell`` introduced on the
:ref:`key concepts <user-guide_usage_key-concepts_cell>` page. Cell-related functions,
that do not require ``atoms`` are available under the ``wulfric.cell`` submodule.

.. doctest::

    >>> import wulfric
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

To compute parameters of any cell use :py:func:`wulfric.cell.get_params`

.. doctest::

    >>> wulfric.cell.get_params(cell)
    (3.55335, 4.744935, 8.760497, 90.0, 90.0, 90.0)

.. note::
    When ``cell`` converted to ``params`` the information about its spacial orientation is
    lost.

To create a cell from parameters use

.. doctest::

    >>> # we use np.round to account for the finite precision of float point arithmetic
    >>> import numpy as np
    >>> np.round(wulfric.cell.from_params(3.55335, 4.744935, 8.760497, 90.0, 90.0, 90.0), 6)
    array([[3.55335 , 0.      , 0.      ],
           [0.      , 4.744935, 0.      ],
           [0.      , 0.      , 8.760497]])

:py:func`wulfric.cell.from_params` constructs the cell with the first vector oriented
along the :math:`x` axis and second vector in the :math:`xy` plain. The cell can only be
constructed from the set of parameters that can form parallelepiped (see
:py:func:`wulfric.geometry.parallelepiped_check`).

.. note::
    ``wulfric.cell.from_params(wulfric.cell.get_params(cell))`` is not guaranteed to
    recover the same ``cell`` matrix, as the information about the orientation of lattice
    vectors in Cartesian reference frame is lost after the call of the first function.


Reciprocal lattice
==================

Any ``cell`` defines a direct lattice and its reciprocal counterpart. To compute the cell
of the reciprocal lattice use

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

Examples of Bravais lattices
============================

Wulfric implement constructors for the 14 Bravais lattice types as described in [1]_.

You can use one of the 14 functions to construct cell of each Bravais lattice with
user-provided parameters

.. doctest::

    >>> wulfric.cell.SC_CUB(a=1)
    array([[1, 0, 0],
           [0, 1, 0],
           [0, 0, 1]])
    >>> wulfric.cell.SC_MCL(a=1, b=4, c=5, alpha=70)
    array([[1.        , 0.        , 0.        ],
           [0.        , 4.        , 0.        ],
           [0.        , 1.71010072, 4.6984631 ]])

Or you can get a pre-defined examples with the parameter that are chosen by wulfric

.. doctest::

    >>> wulfric.cell.sc_get_example("FCC")
    array([[0.        , 1.57079633, 1.57079633],
           [1.57079633, 0.        , 1.57079633],
           [1.57079633, 1.57079633, 0.        ]])

In the latter case you can get an example for each lattice type and for each lattice
variation as defined in [1]_.

.. doctest::

    >>> wulfric.cell.sc_get_example("BCT1")
    array([[-2.35619449,  2.35619449,  1.57079633],
           [ 2.35619449, -2.35619449,  1.57079633],
           [ 2.35619449,  2.35619449, -1.57079633]])
    >>> wulfric.cell.sc_get_example("BCT2")
    array([[-1.57079633,  1.57079633,  2.35619449],
           [ 1.57079633, -1.57079633,  2.35619449],
           [ 1.57079633,  1.57079633, -2.35619449]])


References
==========
.. [1] Setyawan, W. and Curtarolo, S., 2010.
    High-throughput electronic band structure calculations: Challenges and tools.
    Computational materials science, 49(2), pp. 299-312.
