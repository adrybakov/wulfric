.. _user-guide_usage_crystal:

*********************************
Manipulations with atoms and cell
*********************************


For the full technical reference see :ref:`api_crystal`.

On this page we give examples of what can be done with the ``atoms`` and reference ``cell``
introduced on the :ref:`key concepts <user-guide_usage_key-concepts_cell>` page. Functions
from the examples are available under ``wulfric.crystal`` submodule.

In the examples on this page we assume that wulfric and |NumPy|_ are imported as

.. doctest::

  >>> import numpy as np
  >>> import wulfric

In the examples we use crystall with six atoms and orthorhombic cell.

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

Atom's names
============

There are no rules specified by wulfric for the atom names. Any non-empty string is a
valid name. Wulfric can modify names to ensure their uniqueness with
:py:func:`wulfric.crystal.ensure_unique_names`

.. doctest::

  >>> import wulfric
  >>> atoms1 = {"names" : ["Cr1", "Cr2", "Br", "Br", "S", "S"]}
  >>> # Default strategy is "all"
  >>> wulfric.crystal.ensure_unique_names(atoms1)
  >>> atoms1
  {'names': ['Cr11', 'Cr22', 'Br3', 'Br4', 'S5', 'S6']}
  >>> atoms1 = {"names" : ["Cr1", "Cr2", "Br", "Br", "S", "S"]}
  >>> wulfric.crystal.ensure_unique_names(atoms1, strategy="repeated-only")
  >>> atoms1
  {'names': ['Cr1', 'Cr2', 'Br1', 'Br2', 'S1', 'S2']}

Atom's species
==============

Wulfric recognizes two keywords in the ``atoms`` dictionary: "names" and "species".
Both are lists of strings. Names of atoms are not restricted in any way and user is free
to name atoms as they please (however, it is a common practice to include atom's species
in the name). On contrary the "species" are interpreted having a set of special values in
mind. Correct strings for possible species are hard-coded and available under the
:py:const:`wulfric.constants.ATOM_SPECIES` constant.

Wulfric implements two functions to automatically guess the atom's species from its name

.. doctest::

  >>> wulfric.crystal.get_atom_species("Cr1")
  'Cr'

If it is unable to guess the atom species, then it issues a ``RuntimeWarning`` and return
``"X"`` as a species.

.. doctest::

  >>> wulfric.crystal.get_atom_species("124")
  ...
  'X'
  >>> # It is possible to raise an error instead of the warning
  wulfric.crystal.get_atom_species("124", raise_on_fail=True)
  ...
  wulfric._exceptions.FailedToDeduceAtomSpecies: Tried to deduce name from '124'. Failed.

To guess the names for the dictionary of ``atoms`` use

.. doctest::

  >>> # Note: this function modifies the dictionary on which it is called
  >>> wulfric.crystal.populate_atom_species(atoms)
  >>> atoms["species"]
  ['Cr', 'Br', 'S', 'Cr', 'Br', 'S']

Pair of atoms
=============

Often a distance between a pair of atoms is required. Wulfric has two functions for that.
It assumes that first atom is located in the reference unit cell with indices
:math:`(0, 0, 0)` and second atom is located in any unit cell of the crystal with indices
:math:`(i, j, k)`.

To get the vector from atom 1 to atom 2 and distance between them use

.. doctest::

  >>> wulfric.crystal.get_vector(cell, atoms, atom1=0, atom2=0, R=(0,1,0))
  array([3.55335, 0.     , 0.     ])
  >>> wulfric.crystal.get_distance(cell, atoms, atom1=0, atom2=0, R=(0,1,0))
  3.55335

Translation equivalence
=======================

After standardization relative coordinates of atoms may become negative. It means that the
atoms are located outside of the unit cell in real space. The crystal that is defined by
the new part of cell and atoms is still the same as before standardization.

One may want to ensure that all atoms are located within the volume of :math:`(0, 0, 0)`
unit cell. In that way the atoms would be changed to their translational equivalent images.
To do so use

.. doctest::

  >>> for p in atoms["positions"]:
  ...     print(p)
  ...
  [ 0.       -0.5       0.882382]
  [0.       0.       0.677322]
  [-0.5      -0.5       0.935321]
  [0.5      0.       0.117618]
  [0.5      0.5      0.322678]
  [0.       0.       0.064679]
  >>> wulfric.crystal.ensure_000(atoms)
  >>> for p in atoms["positions"]:
  ...     print(p)
  ...
  [0.       0.5      0.882382]
  [0.       0.       0.677322]
  [0.5      0.5      0.935321]
  [0.5      0.       0.117618]
  [0.5      0.5      0.322678]
  [0.       0.       0.064679]

Resulting pair of atoms and cell still describe the same crystal as at the beginning.
