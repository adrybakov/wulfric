.. _api_crystal:

*******
Crystal
*******

.. currentmodule:: wulfric

Class
=====

.. autosummary::
    :toctree: generated/

    Crystal

.. hint::
    All properties and methods of :ref:`api_lattice`
    are accessible directly from the crystal instance:

    .. doctest::

        >>> import wulfric as wulf
        >>> c = wulf.Crystal()
        >>> c.a
        1.0
        >>> c.b
        1.0
        >>> c.c
        1.0


Atom methods
============
* Crystal.atoms

.. autosummary::

    Crystal.add_atom
    Crystal.remove_atom
    Crystal.get_atom

Positioning of atoms
====================

.. autosummary::

    Crystal.get_atom_coordinates
    Crystal.get_distance
    Crystal.get_vector

Primitive cell
==============

.. autosummary::

    Crystal.find_primitive_cell

Lattice getter
==============

.. autosummary::

    Crystal.lattice
