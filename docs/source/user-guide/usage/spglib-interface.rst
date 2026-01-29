.. _user-guide_usage_spglib-interface:

*******************
Interface to Spglib
*******************

Wulfric relies on |spglib|_ in all its functions that need any information about
crystal's (``cell`` + ``atoms``) symmetry.

.. doctest::

    >>> import numpy as np
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

As wulfric is primarily designed as a set of well-defined functions, we face the problem
of multiple calls to |spglib|_, when more than one property is desired by user.

For example, is the user want to know both conventional and primitive cells, they can
be computed as

.. doctest::

    >>> import wulfric
    >>> conv_cell, conv_atoms = wulfric.crystal.get_conventional(cell, atoms)
    >>> prim_cell, prim_atoms = wulfric.crystal.get_primitive(cell, atoms)

But, to know the primitive cell one needs to know the conventional cell, therefore
function :py:func:`wulfric.crystal.get_conventional` is called twice - one time by the
user and one time within the :py:func:`wulfric.crystal.get_primitive`.

To solve this problem of executing the code twice (or at least of calling |spglib|_ twice,
which might be expensive), we isolate the interaction of wulfric with |spglib|_ into a
single function :py:func:`wulfric.get_spglib_data`. Then, the same code as above can be
rewritten as

.. doctest::

    >>> import wulfric
    >>> spglib_data = wulfric.get_spglib_data(cell, atoms)
    >>> conv_cell, conv_atoms = wulfric.crystal.get_conventional(cell, atoms, spglib_data=spglib_data)
    >>> prim_cell, prim_atoms = wulfric.crystal.get_primitive(cell, atoms, spglib_data=spglib_data)

In that way |spglib|_ is called only once and the data are re-used.

All functions that accept ``cell`` and ``atoms`` and rely on |spglib|_ have optional
argument ``spglib_data`` that can be passed to them.

Moreover, ``spglib_data`` object by itself (which is just a dictionary with dot access)
can be used by the user for access to additional information derived from spglib:

.. doctest::

    # Fancy dot access
    >>> spglib_data.space_group_number
    59
    >>> # is actually the same as
    >>> spglib_data["space_group_number"]
    59
    >>> spglib_data.crystal_family
    'o'
    >>> spglib_data.centring_type
    'P'

All properties of ``spglib_data`` are documented in :py:func:`wulfric.get_spglib_data`.
