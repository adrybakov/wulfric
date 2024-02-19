.. _user-guide_module_bravais-lattices:

****************
Bravais lattices
****************

.. currentmodule:: wulfric

For the full technical reference see :ref:`api_bravais-lattices`

For the description of each Bravais lattice type see :ref:`library_bravais-lattices`.

Bravais lattice notation and standardization follows Setyawan and Curtarolo [1]_.

Each Bravais lattice is an instance of :py:class:`.Lattice` class.


For each Bravais lattice system there is a function defined, which constructs
the instance of :py:class:`.Lattice` class from the parameters. For the names of the
constructors and corresponding parameters see the :ref:`dedicated page <library_bravais-lattices>`
(for full reference see :ref:`Api reference <api_bravais-lattices>`).

Import
======

.. doctest::

    >>> # Exact import
    >>> from wulfric.bravais_lattice.constructor import CUB
    >>> # Explicit import
    >>> from wulfric.bravais_lattice import CUB
    >>> # Recommended import
    >>> from wulfric import CUB

Creation
========

.. doctest::

    >>> lattice = CUB(1)
    >>> lattice.parameters
    (1.0, 1.0, 1.0, 90.0, 90.0, 90.0)

Constructor can be used to get the cell instead of the lattice:

    >>> cell = CUB(1, return_cell=True)
    >>> cell
    array([[1, 0, 0],
           [0, 1, 0],
           [0, 0, 1]])

Predefined examples
===================

For each type and variation a predefined example of the lattice is available.
It could be accessed in a following way:

.. doctest::

    >>> import wulfric as wulf
    >>> cubic_example = wulf.lattice_example("cub")
    >>> cubic_example.variation
    'CUB'

.. hint::

    Capitalization of the name of the lattice example is not important:
    ``CUB``, ``CUb``, ``CuB``, ``cUB``, ``Cub``, ``cUb``, ``cuB``, and ``cub`` are equivalent.


References
==========
.. [1] Setyawan, W. and Curtarolo, S., 2010.
    High-throughput electronic band structure calculations: Challenges and tools.
    Computational materials science, 49(2), pp.299-312.
