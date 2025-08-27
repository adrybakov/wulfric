.. _user-guide_usage_key-concepts:

************
Key concepts
************

On this page we list concepts and data structures, that are essential for understanding of
wulfric's scope. And give some some code examples for each.

.. _user-guide_usage_key-concepts_cell:

Cell
====

``cell`` is a two-dimensianal :math:`3\times3` matrix, that defines three lattice
vectors. The rows of the ``cell`` are vectors, while the columns are cartesian
coordinates. Here is an example of a simple orthorhombic cell

.. doctest::

    >>> cell = [
    ... [3.553350, 0.000000, 0.000000],
    ... [0.000000, 4.744935, 0.000000],
    ... [0.000000, 0.000000, 8.760497],
    ... ]

The functions of wulfric assume that the cell is |array-like|_, i. e. that it can be
converted to the |NumPy|_ array.

.. doctest::

    >>> import numpy as np
    >>> cell = np.array(cell, dtype=float)

There is a lot of things that one can do with ``cell``. All functions that deal with the
cell alone (i.e. do not require any ``atoms``) are implemented in the :ref:`api_cell`
submodule. For more detailed examples of what can be done with the cell see
:ref:`user-guide_usage_cell`.

.. _user-guide_usage_key-concepts_atoms:

Atoms
=====

Atoms in wulfric are stored as a plain python dictionary. Keys of the ``atoms`` are
properties of atoms. Values are the lists of :math:`N` elements each, where :math:`N` is
an amount of atoms.

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


Keys recognized by wulfric:

*   "names" :
    ``list`` of ``str``.
*   "species" :
    ``list`` of ``str``.
*   "positions" :
    ``list`` of *relative* positions of atoms. Each element is an |array-like|_ of the
    length :math:`3`.
*   "spglib_types" :
    ``list`` of ``int``. Each element is ``>=1``.

Wulfric uses only those four keys, however, we invite you to extend the ``atoms`` to your
needs and store any properties in the same dictionary. Any function of wulfric that reads
``atoms`` dictionary and returns ``new_atoms`` dictionary will transfer the values of each
atom in  ``atoms`` to the corresponding atom of ``new_atoms`` for **every** key, not only
for ones that wulfric recognizes. ``atoms`` dictionary allows to use wulfric's functions
on the user-extendend ``atoms``. Functions of wulfric will only ever modify the key-values
that are recognized by it and leave the user-defined ones intact.

.. hint::

    If you want to have an attribute-like access to the ``atoms`` properties, then you can
    add some |Syntactic-sugar|_ to any dictionary with

    .. doctest::

        >>> import wulfric
        >>> atoms = wulfric.add_sugar(atoms)
        >>> atoms.names
        ['Cr1', 'Br1', 'S1', 'Cr2', 'Br2', 'S2']

    See :py:func:`wulfric.add_sugar` and :py:func:`wulfric.remove_sugar` for
    more.

.. _user-guide_usage_key-concepts_crystal:

Crystal
=======

Crystal is simply a pair of ``cell`` and ``atoms``. There is no dedicated data structure
for crystal in wulfric (not even a tuple ``(cell, atoms)``). If necessary the user must
provide two variables: ``cell`` and ``atoms``. ``atoms["positions"]`` are always
interpreted by wulfric as relative with respect to ``cell``. Therefore, user is
responsible for providing appropriate ``cell`` for any given ``atoms``.

For example, ``cell`` and ``atoms`` from the above two sections describe a crystal of
|CrSBr-materials-cloud|_.

.. _user-guide_usage_key-concepts_k-path:

K-path
======

Wulfric understands kpath of the format like "G-K-X|R-S".

* K-points are identified by their names. Name can not contain "-".
* ``|`` separates subpaths. Each subpath has to contain at least two points. Path has to
  have at least one subpath.
* ``-`` separates high-symmetry points in each subpath.

Almost every function of wulfric expects k-path to be given as a string in that format.

The concept of subpaths allows to "jump" from one k-point to another, without following a
path in between. For instance, in the path "G-K-X|R-S" for the band structure
calculation/plots some amount of intermediate points is implied between "G" and "K",
between "K" and "X" and between "R" and "S". However, there is no intermediate points
between "X" and "R".

Internally the path is stored as ``list`` of ``list`` of ``str``, i.e. as list of
subpaths, where each subpath is a list of names of high-symmetry points. Functions
:py:func:`wulfric.kpoints.get_path_as_string` and
:py:func:`wulfric.kpoints.get_path_as_list` can be used for conversion between
representations if necessary.

Here are some examples

========= ==================================
As string As ``list`` of ``list`` of ``str``
========= ==================================
G-K       ``[["G", "K"]]``
G-K-X|R-S ``[["G","K","X",],["R","S"]]``
S1-K-G    ``[["S1", "K", "G"]]``
========= ==================================
