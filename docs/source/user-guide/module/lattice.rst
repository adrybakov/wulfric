.. _user-guide_module_lattice:

.. currentmodule:: wulfric

*******
Lattice
*******

For the full technical reference see :ref:`api_lattice`

Every Bravais lattice is an instance of the :py:class:`.Lattice` class.
For the guide about Bravais lattices see :ref:`user-guide_module_bravais-lattices`.
This page describes the :py:class:`.Lattice` class and its methods.

Import
======

  >>> # Exact import
  >>> from wulfric.lattice import Lattice
  >>> # Recommended import
  >>> from wulfric import Lattice

For the examples in this page we need additional import and some predefined variables:

.. doctest::

  >>> from wulfric import lattice_example

Creation
========

Lattice can be created in three different ways:

* From ``cell`` matrix:

  .. doctest::

    >>> cell = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    >>> lattice = Lattice(cell)
    >>> lattice.cell
    array([[1, 0, 0],
           [0, 1, 0],
           [0, 0, 1]])

* From three lattice vectors :math:`\vec{a}_1`, :math:`\vec{a}_2`, :math:`\vec{a}_3`:

  .. doctest::

    >>> a1 = [1, 0, 0]
    >>> a2 = [0, 1, 0]
    >>> a3 = [0, 0, 1]
    >>> lattice = Lattice(a1, a2, a3)
    >>> lattice.cell
    array([[1, 0, 0],
           [0, 1, 0],
           [0, 0, 1]])

* From lattice parameters :math:`a`, :math:`b`, :math:`c`, :math:`\alpha`, :math:`\beta`, :math:`\gamma`:

  .. doctest::

    >>> lattice = Lattice(1, 1, 1, 90, 90, 90)
    >>> import numpy as np
    >>> np.round(lattice.cell, decimals=1)
    array([[1., 0., 0.],
           [0., 1., 0.],
           [0., 0., 1.]])


Numerical tolerance
===================

As in the a package itself the :py:class:`.Lattice` class has two attributes, that control the
numerical tolerance

* For the distance: :py:attr:`.Lattice.eps_rel` and :py:attr:`.Lattice.eps`

  .. doctest::

    >>> l = Lattice()
    >>> l.eps_rel
    0.0001
    >>> l.eps
    0.0001

* For the angle: :py:attr:`.Lattice.angle_tol`

  .. doctest::

    >>> l = Lattice()
    >>> l.angle_tol
    0.0001

.. hint::

  The numerical tolerance is used in the lattice standardization and in the
  identification of the lattice type. If :py:meth:`.Lattice.type` does not return an
  expected type, then you can try to reduce the numerical tolerance.

Lattice type
============

Bravais lattice type is lazily identified when it is needed:

.. doctest::

  >>> lattice = Lattice(1, 1, 1, 90, 90, 90)
  >>> lattice.type()
  'CUB'

Identification procedure is implemented in the :py:func:`.lepage` function.
For the brief algorithm description see :ref:`library_lepage`.

.. note::

  Lattice identification is not a trivial task and may be time consuming.
  The algorithm is based on the assumption that the lattice`s unit cell is primitive.
  As a rule of thumb, Wulfric will identify the lattice type only if it is explicitly
  required for the task.

Variation of the lattice
========================
Some Bravais lattice types have several variations. The lattice variation requires
the lattice to be standardized. For the standardization of the lattice just call
:py:meth:`.Lattice.standardize` method:

To check the variation of the lattice use :py:attr:`.Lattice.variation` attribute:

.. doctest::

    >>> lattice = lattice_example("BCT")
    >>> lattice.variation
    'BCT1'
    >>> lattice = Lattice(1, 1, 1, 90, 90, 90)
    >>> lattice.variation
    'CUB'

Reference attributes
====================

You can use the following attributes for the information about the lattice
based on the Bravais type:

.. doctest::

    >>> lattice = Lattice([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    >>> lattice.pearson_symbol
    'cP'
    >>> lattice.crystal_family
    'c'
    >>> lattice.centring_type
    'P'

Lattice parameters
==================

All lattice parameters can be accessed as attributes:

* Real space

.. doctest::

    >>> lattice = Lattice([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    >>> lattice.a1
    array([1, 0, 0])
    >>> lattice.a2
    array([0, 1, 0])
    >>> lattice.a3
    array([0, 0, 1])
    >>> lattice.cell
    array([[1, 0, 0],
           [0, 1, 0],
           [0, 0, 1]])
    >>> lattice.a
    1.0
    >>> lattice.b
    1.0
    >>> lattice.c
    1.0
    >>> lattice.alpha
    90.0
    >>> lattice.beta
    90.0
    >>> lattice.gamma
    90.0
    >>> lattice.unit_cell_volume
    1.0
    >>> lattice.parameters
    (1.0, 1.0, 1.0, 90.0, 90.0, 90.0)

* Reciprocal space

.. doctest::

    >>> from math import pi
    >>> lattice = Lattice([[2*pi, 0, 0], [0, 2*pi, 0], [0, 0, 2*pi]])
    >>> lattice.b1
    array([1., 0., 0.])
    >>> lattice.b2
    array([0., 1., 0.])
    >>> lattice.b3
    array([0., 0., 1.])
    >>> lattice.reciprocal_cell
    array([[1., 0., 0.],
           [0., 1., 0.],
           [0., 0., 1.]])
    >>> # Since 0.4.0 there is a shortcut in place
    >>> lattice.rcell
    array([[1., 0., 0.],
           [0., 1., 0.],
           [0., 0., 1.]])
    >>> round(lattice.k_a, 4)
    1.0
    >>> round(lattice.k_b, 4)
    1.0
    >>> round(lattice.k_c, 4)
    1.0
    >>> lattice.k_alpha
    90.0
    >>> lattice.k_beta
    90.0
    >>> lattice.k_gamma
    90.0

.. hint::

    Not all properties of the lattice are listed here (for examples the one of the
    conventional cell are not even mentioned). See :ref:`api_lattice` for the full list
    of properties.

K points
========

Path in reciprocal space and k points for plotting and calculation are
implemented in a separate class :py:class:`.Kpoints`. It is expected to be accessed
through the :py:attr:`.Lattice.kpoints` attribute. Note that you can work with
kpoints from the instance of the :py:class:`.Lattice`, since the instance of the
:py:class:`.Kpoints` class is created when the property is accessed for the first
time and stored internally for later use:

.. doctest::

    >>> lattice = Lattice(1, 1, 1, 90, 90, 90)
    >>> lattice.kpoints.add_hs_point("CP", [0.5, 0.5, 0.5], label="Custom label")
    >>> lattice.kpoints.path = "G-X|M-CP-X"
    >>> lattice.kpoints.path_string
    'G-X|M-CP-X'
    >>> kp = lattice.kpoints
    >>> kp.path_string
    'G-X|M-CP-X'
    >>> kp.path = "G-X|M-X"
    >>> kp.path_string
    'G-X|M-X'
    >>> lattice.kpoints.path_string
    'G-X|M-X'

.. note::

    For each Bravais lattice type there is a predefined path and set of
    kpoints in reciprocal space. See :ref:`user-guide_conventions_bravais-lattices` for
    more details. Standardization of the unit cell is required prior to the v0.4.0. As of
    version 0.4.0 and later standardization is not required and high symmetry kpoints are
    computed with respect to any given cell.

For the full guide on how to use :py:class:`.Kpoints` class see
:ref:`user-guide_module_kpoints`.
