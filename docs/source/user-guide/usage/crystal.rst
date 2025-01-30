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
  >>> import wulfric as wulf

In the examples we use crystall with six atoms and orthorhombic cell.

.. doctest::

  >>> cell = np.array([
  ...     [0.000000, 0.000000, 8.760497],
  ...     [3.553350, 0.000000, 0.000000],
  ...     [0.000000, 4.744935, 0.000000],
  ... ])
  >>> atoms = {
  ...     "names": ["Cr1", "Br1", "S1", "Cr2", "Br2", "S2"],
  ...     "positions": [
  ...         [0.882382, 0.500000, 0.000000],
  ...         [0.677322, 0.000000, 0.000000],
  ...         [0.935321, 0.500000, 0.500000],
  ...         [0.117618, 0.000000, 0.500000],
  ...         [0.322678, 0.500000, 0.500000],
  ...         [0.064679, 0.000000, 0.000000],
  ...     ],
  ... }


Atom's species
==============

Wulfric recognizes two keywords in the ``atoms`` dictionary: "names" and "species".
Both are lists of strings. Names of atoms are not restricted in any way and user is free
to name atoms as they please (however, it is a common practice to include atom's species
in the name). On contrary the "species" are interpreted having a set of special values in
mind. Correct strings for possible species are hard-coded and available in the
``wulf.constants.ATOM_SPECIES`` constant.

Wulfric implements two functions to automatically guess the atom's species from its name

.. doctest::

  >>> wulf.crystal.get_atom_species("Cr1")
  'Cr'

If it is unable to guess the atom species, then it issues a ``RuntimeWarning`` and return
``"X"`` as a species.

.. doctest::

  >>> wulf.crystal.get_atom_species("124")
  ...
  'X'
  >>> # It is possible to raise an error instead of the warning
  wulf.crystal.get_atom_species("124", raise_on_fail=True)
  ...
  wulfric._exceptions.FailedToDeduceAtomSpecies: Tried to deduce name from '124'. Failed.

To guess the names for the dictionary of ``atoms`` use

.. doctest::

  >>> # Note: this function modifies the dictionary on which it is called
  >>> wulf.crystal.populate_atom_species(atoms)
  >>> atoms["species"]
  ['Cr', 'Br', 'S', 'Cr', 'Br', 'S']

Pair of atoms
=============

Often a distance between a pair of atoms is required. Wulfric has two functions for that.
It assumed that first atom is located in the reference unit cell with indices
:math:`(0, 0, 0)` and second atom is located in any unit cell of the crystal with indices
:math:`(i, j, k)`.

To get the vector from atom 1 to atom 2 and distance between them use

.. doctest::

  >>> wulf.crystal.get_vector(cell, atoms, atom1=0, atom2=0, R=(0,1,0))
  array([3.55335, 0.     , 0.     ])
  >>> wulf.crystal.get_distance(cell, atoms, atom1=0, atom2=0, R=(0,1,0))
  3.55335

Standardization
===============

Please read :ref:`similar section for the cell <user-guide_usage_cell_standardization>`
first.

When ``cell`` is standardized. Standardization of the cell does not change neither the
lattice defined by this cell nor absolute coordinates of atoms. Therefore, *relative*
coordinates, stored in ``atoms["positions"]`` should change. Wulfric defines a function,
which standardize the cell and update relative coordinated of atoms.

.. doctest::

  >>> # Position of the first atom relative to the non-standardized cell
  >>> atoms["positions"][0]
  [0.882382, 0.5, 0.0]
  >>> # Position of the same atom in the real space, in absolute coordinates
  >>> atoms["positions"][0] @ cell
  array([1.776675  , 0.        , 7.73010486])
  >>> # This function return new cell, but update passes atoms dictionary
  >>> cell = wulf.crystal.standardize(cell=cell, atoms=atoms)
  >>> # Note how the relative positions changed
  >>> atoms["positions"][0]
  array([0.5     , 0.      , 0.882382])
  >>> # But absolute position is the same
  >>> atoms["positions"][0] @ cell
  array([1.776675  , 0.        , 7.73010486])
  >>> # It reflects a reordering of the lattice vectors
  >>> # For ORC lattice a < b < c
  >>> cell
  array([[3.55335 , 0.      , 0.      ],
         [0.      , 4.744935, 0.      ],
         [0.      , 0.      , 8.760497]])
