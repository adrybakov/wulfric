.. _user-guide_usage_crystal:

**************************
Manipulations with crystal
**************************


For the full technical reference see :ref:`api_crystal`.

On this page we give examples of what can be done with the pair of ``cell`` and ``atoms``
(introduced on the :ref:`key concepts <user-guide_usage_key-concepts_cell>` page), that
define a crystal and reference ``cell``. All functions that deal with atoms or crystal are
available under ``wulfric.crystal`` submodule.

.. doctest::

    >>> import numpy as np
    >>> import wulfric

In the examples below we use crystal with six atoms and orthorhombic cell.

.. doctest::

    >>> cell = np.array([
    ...     [0.000000, 4.744935, 0.000000],
    ...     [3.553350, 0.000000, 0.000000],
    ...     [0.000000, 0.000000, 8.760497],
    ... ])
    >>> atoms = {
    ...     "names": ["Cr1", "Br1", "S1", "Cr2", "Br2", "S2"],
    ...     "positions": np.array([
    ...         [0.000000, -0.500000,  0.882382],
    ...         [0.000000, 0.000000,  0.677322],
    ...         [-0.500000, -0.500000,  0.935321],
    ...         [0.500000, 0.000000,  0.117618],
    ...         [0.500000, 0.500000,  0.322678],
    ...         [0.000000, 0.000000,  0.064679],
    ...     ]),
    ... }

Choice of the cell
==================

Please read :ref:`user-guide_conventions_which-cell_choice` first.

Conventional cell
-----------------

To choose conventional cell use :py:func:`wulfric.crystal.get_conventional`

.. doctest::

    # Default convention is HPKOT
    >>> conv_cell, conv_atoms = wulfric.crystal.get_conventional(cell, atoms)

Note that the first two lattice vectors are changed.

.. doctest::

    >>> conv_cell
    array([[3.55335 , 0.      , 0.      ],
           [0.      , 4.744935, 0.      ],
           [0.      , 0.      , 8.760497]])

Atom's positions are modified to account for the new cell. In that way the crystal is not
modified and stays in the same spatial orientation.

.. doctest::

    >>> conv_atoms["positions"]
    array([[0.5     , 0.      , 0.882382],
           [0.      , 0.      , 0.677322],
           [0.5     , 0.5     , 0.935321],
           [0.      , 0.5     , 0.117618],
           [0.5     , 0.5     , 0.322678],
           [0.      , 0.      , 0.064679]])

Conventional atoms are either the same ones as in the original crystal ("Br1", "Cr2",
"Br2", "S2") or translationally equivalent ones ("Cr1", "S1")

.. doctest::

    >>> atoms["positions"] @ cell
    array([[-1.776675  ,  0.        ,  7.73010486],
           [ 0.        ,  0.        ,  5.93367735],
           [-1.776675  , -2.3724675 ,  8.19387681],
           [ 0.        ,  2.3724675 ,  1.03039214],
           [ 1.776675  ,  2.3724675 ,  2.82681965],
           [ 0.        ,  0.        ,  0.56662019]])
    >>> # Cr1 (index 0) Shifted by cell[1]
    >>> # Br1 (index 1) Same
    >>> # S1  (index 2) Shifted by cell[0] + cell[1]
    >>> # Cr2 (index 3) Same
    >>> # Br2 (index 4) Same
    >>> # S2  (index 5) Same
    >>> conv_atoms["positions"] @ conv_cell
    array([[1.776675  , 0.        , 7.73010486],
           [0.        , 0.        , 5.93367735],
           [1.776675  , 2.3724675 , 8.19387681],
           [0.        , 2.3724675 , 1.03039214],
           [1.776675  , 2.3724675 , 2.82681965],
           [0.        , 0.        , 0.56662019]])

Primitive cell
--------------

To choose primitive cell use :py:func:`wulfric.crystal.get_primitive`.

.. doctest::

    >>> prim_cell, prim_atoms = wulfric.crystal.get_primitive(cell, atoms)


Atom's names
============

Wulfric does not impose any rule on atom's names. Any non-empty string is a valid name.

To get a set of unique names for your atoms you can use
:py:func:`wulfric.crystal.get_unique_names`, that supports two strategies for modification
of names

*   (default) "all"

    Adds an index of the atom to the end of each name. First atom gets an index ``1``.

*   "repeated-only"

    Adds an indices only to the atoms that have the same name. The count is separate for
    each group of atoms.

.. doctest::

    >>> import wulfric
    >>> atoms1 = {"names" : ["Cr1", "Cr2", "Br", "Br", "S", "S"]}
    >>> # Default strategy is "all"
    >>> wulfric.crystal.get_unique_names(atoms1)
    ['Cr11', 'Cr22', 'Br3', 'Br4', 'S5', 'S6']
    >>> wulfric.crystal.get_unique_names(atoms1, strategy="repeated-only")
    ['Cr1', 'Cr2', 'Br1', 'Br2', 'S1', 'S2']

Atom's species
==============

Names of atoms are not restricted in any way and user is free to name atoms as they please
(however, it is a common practice to include atom's species in the name).

On contrary, the "species" are one of the 118 pre-defined strings
(see :ref:`api_constants_ATOM_SPECIES`).

Wulfric implements two functions to automatically guess the atom's species from its name

.. doctest::

    >>> wulfric.crystal.get_atom_species("Cr1")
    'Cr'

If it is unable to the atom species from its name, then it issues a ``RuntimeWarning``
and returns ``"X"`` as a species.

.. doctest::

    >>> wulfric.crystal.get_atom_species("124")
    ...
    'X'
    >>> # You can raise an error instead of the warning
    wulfric.crystal.get_atom_species("124", raise_on_fail=True)
    ...
    wulfric._exceptions.FailedToDeduceAtomSpecies: Tried to deduce name from '124'. Failed.

To guess the names for all ``atoms`` at once use :py:func:`wulfric.crystal.get_atoms_species`

.. doctest::

    >>> wulfric.crystal.get_atoms_species(atoms)
    ['Cr', 'Br', 'S', 'Cr', 'Br', 'S']

Atom's positions
================

Wulfric implements a couple of routines to perform common operations on atom's positions,
that do not change orientation of the crystal. Those functions return ``None`` and modify
the same ``atoms``, that was passed to them.

*   :py:func:`wulfric.crystal.ensure_000`

    Ensures that relative coordinates of all atoms are within :math:`[0,1]`

    .. doctest::

        >>> import wulfric
        >>> atoms = {"positions": [[0, 0.5, 0], [1.25, 0, -0.52], [0.25, -0.65, 2.375]]}
        >>> for p in atoms["positions"]:
        ...     print(p)
        [0, 0.5, 0]
        [1.25, 0, -0.52]
        [0.25, -0.65, 2.375]
        >>> wulfric.crystal.ensure_000(atoms)
        >>> for p in atoms["positions"]:
        ...     print(p)
        [0, 0.5, 0]
        [0.25, 0, 0.48]
        [0.25, 0.35, 0.375]

*   :py:func:`wulfric.crystal.cure_negative`

    Ensures that all relative coordinates of all atoms are positive

    .. doctest::

        >>> import wulfric
        >>> atoms = {
        ...     "names": ["Cr1", "Cr2"],
        ...     "positions": [[-0.5, 0.5, 0.0], [0.1, 0.5, 0.0]],
        ... }
        >>> wulfric.crystal.cure_negative(atoms)
        >>> for i in range(len(atoms["names"])):
        ...     print(atoms["names"][i], atoms["positions"][i])
        Cr1 [0.  0.5 0. ]
        Cr2 [0.6 0.5 0. ]

*   :py:func:`wulfric.crystal.shift_atoms`

    Shifts al atoms at once in a special way.

    .. doctest::

        >>> import wulfric
        >>> cell = [[2, 0, 0], [0, 2, 0], [0, 0, 2]]
        >>> atoms = {
        ...     "names": ["Cr1", "Cr2"],
        ...     "positions": [[0.0, 0.0, 0.0], [0.5, 0.5, 1.0]],
        ... }
        >>> wulfric.crystal.shift_atoms(atoms=atoms, gravity_point=(0.5, 0.5, 0.5))
        >>> for i in range(len(atoms["names"])):
        ...     print(atoms["names"][i], atoms["positions"][i])
        Cr1 [0.25 0.25 0.  ]
        Cr2 [0.75 0.75 1.  ]
        >>> wulfric.crystal.shift_atoms(
        ...     atoms, gravity_point=(1, 1, 1), cell=cell, gp_is_relative=False
        ... )
        >>> for i in range(len(atoms["names"])):
        ...     print(atoms["names"][i], atoms["positions"][i])
        Cr1 [0.25 0.25 0.  ]
        Cr2 [0.75 0.75 1.  ]

Pair of atoms
=============

Often a distance or a vector between a pair of atoms is required. Wulfric has two
functions for that. It assumes that first atom is located in the reference unit cell with
indices :math:`(0, 0, 0)` and second atom is located in any unit cell of the crystal with
indices :math:`(i, j, k)`.

To get the vector from atom 1 to atom 2 or distance between them use
:py:func:`wulfric.crystal.get_vector` or :py:func:`wulfric.crystal.get_distance`

.. doctest::

    >>> wulfric.crystal.get_vector(cell, atoms, atom1=0, atom2=0, R=(0,1,0))
    array([3.55335, 0.     , 0.     ])
    >>> wulfric.crystal.get_distance(cell, atoms, atom1=0, atom2=0, R=(0,1,0))
    3.55335
