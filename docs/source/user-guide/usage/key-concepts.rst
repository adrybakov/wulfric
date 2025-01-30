.. _user-guide_usage_key-concepts:

************
Key concepts
************

Several concepts and data structures are essential for understanding of wulfric's scope.

.. _user-guide_usage_key-concepts_cell:

Cell
====

``cell`` is a two-dimensianal :math:`3\times3` matrix, that describe three lattice vectors.
The rows of the ``cell`` are the vectors, while the columns give the cartesian coordinates.
Here is an example of a simple orthorhombic cell

.. doctest::

    >>> cell = [
    ...     [3.553350, 0.000000, 0.000000],
    ...     [0.000000, 4.744935, 0.000000],
    ...     [0.000000, 0.000000, 8.760497],
    ... ]

The functions of wulfric assume that the cell is |array-like|_, i.e. can be converted to
the |NumPy|_ array.

.. doctest::

    >>> import numpy as np
    >>> cell = np.array(cell, dtype=float)

There is a lot of things that one can do with ``cell``. All functions are implemented
under :ref:`api_cell`.

For the given cell one can compute a set of lattice parameters: lengths of the lattice
vectors and pair-wise angles between them as

.. doctest::

    >>> import wulfric as wulf
    >>> wulf.cell.get_params(cell)
    (3.55335, 4.744935, 8.760497, 90.0, 90.0, 90.0)

This function returns six numbers ``(a, b, c, alpha, beta, gamma)``.

Another typical task is to find a reciprocal cell

.. doctest::

    >>> wulf.cell.get_reciprocal(cell)
    array([[6.28318531, 0.        , 0.        ],
           [0.        , 6.28318531, 0.        ],
           [0.        , 0.        , 6.28318531]])

For more examples of what can be done with cell see :ref:`user-guide_usage_cell`.

.. _user-guide_usage_key-concepts_atoms:

Atoms
=====

.. doctest::

    >>> atoms = {
    ...     "names": ["Cr1", "Br1", "S1", "Cr2", "Br2", "S2"],
    ...     "species": ["Cr", "Br", "S", "Cr", "Br", "S"],
    ...     "positions": [
    ...         [0.500000, 0.000000, 0.882382],
    ...         [0.000000, 0.000000, 0.677322],
    ...         [0.500000, 0.500000, 0.935321],
    ...         [0.000000, 0.500000, 0.117618],
    ...         [0.500000, 0.500000, 0.322678],
    ...         [0.000000, 0.000000, 0.064679],
    ...     ],
    ... }

Atoms in wulfric are stored as a plain python dictionary. Keys of the ``atoms`` are
properties of atoms. Values are the lists of :math:`N` elements each, where :math:`N` is
an amount of atoms.

Keys recognized by wulfric:

*   "names" :
    ``list`` of ``str``
*   "species" :
    ``list`` of ``str``.
*   "positions" :
    ``list`` of *relative* coordinates of atoms. Each element is an |array-like|_ of the
    length :math:`3`.

As you can see wulfric recognize only a few of the keys, however, we invite you to extend
the ``atoms`` to your needs. Below we list a few of the potential keys that are not used
by any of wulfric's functions, but might be useful or might be used by wulfric in the
future.


* "spin_vectors"
* "g_factors"
* "charges"
* ...

``atoms`` dictionary allows to use wulfric's functions on the user-extendend ``atoms``.
Functions of wulfric will only modify the key-values that are recognized by it and leave
the user-defined ones intact.

.. _user-guide_usage_key-concepts_crystal:

Crystal
=======

Crystal is a just a pairt of ``cell`` and ``atoms``. We do not introduce any new structure
for the crystal (not even a tuple ``(cell, atoms)``). When necessary the user must provide
two variables: ``cell`` and ``atoms``. ``atoms["positions"]`` are interpreted as relative
with respect to ``cell``.

For example, ``cell`` and ``atoms`` from the two sections above describe a crystal of
|CrSBr-materials-cloud|_.

.. _user-guide_usage_key-concepts_kpath:

K-path
======

We use a specific format in the package: "G-K-X|R-S":

* ``-`` separates high symmetry points in each subpath.
* ``|`` separates subpaths.
* K-points are identified by their names (elements of :py:attr:`.Kpoints.hs_names`).

In the example below n points are generated between "G" and "K", between "K" ans "X",
between "R" and "S", but not between "X" and "R".
