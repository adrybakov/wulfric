# ================================== LICENSE ===================================
# Wulfric - Cell, Atoms, K-path, visualization.
# Copyright (C) 2023-2025 Andrey Rybakov
#
# e-mail: anry@uv.es, web: adrybakov.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ================================ END LICENSE =================================
import spglib
from copy import deepcopy
import numpy as np
from wulfric._syntactic_sugar import SyntacticSugar, add_sugar
from wulfric.crystal._crystal_validation import validate_atoms
from wulfric._exceptions import _raise_with_message, _SUPPORT_FOOTER
from wulfric.crystal._atoms import get_atom_species

from wulfric.constants._space_groups import CRYSTAL_FAMILY, CENTRING_TYPE

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def validate_spglib_data(cell, atoms, spglib_data) -> None:
    r"""
    Validate that ``cell`` and ``atoms["positions"]`` match the ones on which
    ``spglib_data`` was created.

    In details, it check that

    * ``cell`` is the same as ``spglib_data.original_cell``
    * ``atoms["positions"]`` are the same as ``spglib_data.original_positions``
    * ``wulfric.crystal.get_spglib_types(atoms=atoms)`` is the same as
      ``spglib_data.original_types``.

    Parameters
    ==========
    cell : (3, 3) |array-like|_
        Matrix of a cell, rows are interpreted as vectors. In the language of |spglib|_
        the same concept is usually called "basis vectors" or "lattice".
    atoms : dict
        Dictionary with N atoms. Expected keys:

        *   "positions" : (N, 3) |array-like|_

            Positions of the atoms in the basis of lattice vectors (``cell``). In other
            words - relative coordinates of atoms.
        *   "names" : (N, ) list of str, optional
        *   "species" : (N, ) list of str, optional
        *   "spglib_types" : (N, ) list of int, optional
    spglib_data : dict
        A dictionary with the added syntactic sugar (i.e. with the dot access to the keys),
        that is produced via call to :py:func:`.get_spglib_data`.

    Raises
    ======
    ValueError
        If ``cell`` and ``atoms`` do not match ``spglib_data``.
    """

    if not np.allclose(cell, spglib_data.original_cell):
        raise ValueError(
            "Validation of spglib_data against cell and atoms: cell mismatch."
        )

    if not np.allclose(atoms["positions"], spglib_data.original_positions):
        raise ValueError(
            "Validation of spglib_data against cell and atoms: atom's positions mismatch."
        )

    if get_spglib_types(atoms=atoms) != spglib_data.original_types:
        raise ValueError(
            "Validation of spglib_data against cell and atoms: atom's types mismatch."
        )


def get_spglib_types(atoms):
    r"""
    Constructs spglib_types for the given atoms.

    First satisfied rule is applied

    1.  "spglib_types" in atoms

        Return ``atoms["spglib_types"]``.

    2.  "species" in atoms.

        ``spglib_types`` are deduced from ``atoms["species"]``. If two atoms have the same
        species, then they will have the same integer assigned to them in
        ``spglib_types``.

    3.  "names" in ``atoms``

        Species are automatically deduced based on atom's names (via
        :py:func:`wulfric.crystal.get_atom_species`), and then the second rule is
        applied.

    Parameters
    ==========
    atoms : dict
        Dictionary with N atoms. At least one of the following keys is expected

        *   "names" : (N, ) list of str, optional
        *   "species" : (N, ) list of str, optional
        *   "spglib_types" : (N, ) list of int, optional

    Returns
    =======
    spglib_types : (N, ) list of int
        List of integer indices ready to be passed to |spglib|_.
    """

    validate_atoms(atoms=atoms, raise_errors=True)

    if "spglib_types" in atoms:
        spglib_types = atoms["spglib_types"]
    else:
        if "species" not in atoms and "names" in atoms:
            species = [
                get_atom_species(name=name, raise_on_fail=False)
                for name in atoms["names"]
            ]
        elif "species" in atoms:
            species = atoms["species"]
        else:
            raise ValueError(
                'Expected at least one of "spglib_types", "species" or "names" keys in ""atoms, found none.'
            )

        mapping = {
            name: index + 1 for index, name in enumerate(sorted(list(set(species))))
        }
        spglib_types = [mapping[name] for name in species]

    return spglib_types


def get_spglib_data(
    cell,
    atoms,
    spglib_symprec=1e-5,
    spglib_angle_tolerance=-1,
):
    r"""
    Interface to |spglib|_.

    The idea is that this is the only way to access the data from |spglib|_. In that way
    one can associate a dataset with a given ``cell`` and ``atoms`` and re-use it when necessary.

    Parameters
    ==========
    cell : (3, 3) |array-like|_
        Matrix of a cell, rows are interpreted as vectors. In the language of |spglib|_
        the same concept is usually called "basis vectors" or "lattice".
    atoms : dict
        Dictionary with N atoms. Expected keys:

        *   "positions" : (N, 3) |array-like|_
            Positions of the atoms in the basis of lattice vectors (``cell``). In other
            words - relative coordinates of atoms.
        *   "names" : (N, ) list of str, optional
            See Notes
        *   "species" : (N, ) list of str, optional
            See Notes
        *   "spglib_types" (N, ) list of int, optional
            See Notes

        .. hint::
            Pass ``atoms = dict(positions=[[0, 0, 0]], spglib_types=[1])`` if you would
            like to interpret the ``cell`` alone (effectively assuming that the ``cell``
            is a primitive one).
    spglib_symprec : float, default 1e-5
        Directly passed to |spglib|_. Tolerance parameter for the symmetry search.
    spglib_angle_tolerance : float, default -1
        Directly passed to |spglib|_. Tolerance parameter for the symmetry search.

    Returns
    =======
    spglib_data : dict
        A dictionary with the added syntactic sugar (i.e. with the dot access to the keys).

        Data that are included:

        * ``spglib_data.original_cell``

          Same as the given ``cell``

        * ``spglib_data.original_positions``

          Same as the given ``atoms["positions"]``

        * ``spglib_data.original_types``

          Same as ``wulfric.crystal.get_spglib_types(atoms=atoms)`` for given ``atoms``.

        * ``spglib_data.space_group_number``

          Number of the space group. ``1 <= spglib_data.space_group_number <= 230``.

        * ``spglib_data.crystal_family``

          Crystal family.

          * "c" for cubic
          * "h" for hexagonal
          * "t" for tetragonal
          * "o" for orhorhombic
          * "m" for monoclinic
          * "a" for triclinic

        * ``spglib_data.centring_type``

          Centring type.

          * "P" for primitive
          * "A" for side centered
          * "C" for side centered
          * "I" for body-centered
          * "R" for rhombohedral centring
          * "F" for all faces centered

        * ``spglib_data.conventional_cell``

          Conventional cell associated with the given structure in the same spatial
          orientation. In other words, it is a choice of the cell for the same crystal.
          It can contain more than one lattice point.

        * ``spglib_data.conventional_positions``

          N relative positions of the atoms in the basis of
          ``spglib_data.conventional_cell``.

        * ``spglib_data.conventional_types``

          N types of the atoms.

        * ``spglib_data.primitive_cell``

          Primitive cell associated with the given structure in the same spatial
          orientation. In other words, it is a choice of the cell for the same crystal.
          It contains exactly one lattice point.

        * ``spglib_data.primitive_positions``

          M relative positions of the atoms in the basis of
          ``spglib_data.primitive_cell``.

        * ``spglib_data.primitive_types``

          M types of the atoms.

    Raises
    ======
    ValueError
        If some input data are not what is expected.
    TypeError
        If some input data are not what is expected.
    RuntimeError
        If spglib fail to detect symmetry.

    Notes
    =====
    |spglib|_ uses ``types`` to distinguish the atoms. To see how wulfric deduces
    ``types`` from given ``atoms`` see :py:func:`wulfric.crystal.get_spglib_types`.
    """

    try:
        # Validate input data
        # # Validate that the atoms dictionary is what expected of it
        validate_atoms(atoms=atoms, required_keys=["positions"], raise_errors=True)

        # Validate cell TODO: write _cell_validation.py,
        # perhaps check if it can form a parallelepiped
        try:
            cell = np.array(cell, dtype=float)
        except Exception as e:
            _raise_with_message(e=e, message=f"cell is not array-like, got\n{cell}")

        if cell.shape != (3, 3):
            raise ValueError(f"Expected shape of (3, 3) for cell, got {cell.shape}.")

        # Just a dictionary with dot-like access to its keys
        spglib_data = SyntacticSugar()

        # Populate with the input data
        spglib_data.original_cell = deepcopy(cell)
        spglib_data.original_positions = deepcopy(atoms["positions"])
        spglib_data.original_types = deepcopy(get_spglib_types(atoms=atoms))

        dataset = spglib.get_symmetry_dataset(
            (cell, spglib_data.original_positions, spglib_data.original_types),
            symprec=spglib_symprec,
            angle_tolerance=spglib_angle_tolerance,
        )

        if dataset is None:
            raise RuntimeError(
                f"spglib failed to detect symmetry for the given structure with spglib_symprec = {spglib_symprec} and spglib_angle_tolerance = {spglib_angle_tolerance}."
            )

        # For spglib <= 2.4.0
        if isinstance(dataset, dict):
            dataset = add_sugar(dataset)

        spglib_data.space_group_number = dataset.number
        spglib_data.crystal_family = CRYSTAL_FAMILY[dataset.number]
        spglib_data.centring_type = CENTRING_TYPE[dataset.number]
        # Rotate conventional cell back to the orientation of the given cell and atoms
        spglib_data.conventional_cell = (
            dataset.std_lattice @ dataset.std_rotation_matrix
        )
        spglib_data.conventional_positions = dataset.std_positions
        spglib_data.conventional_types = dataset.std_types

        primitive_cell, primitive_positions, primitive_types = spglib.find_primitive(
            (cell, spglib_data.original_positions, spglib_data.original_types),
            symprec=spglib_symprec,
            angle_tolerance=spglib_angle_tolerance,
        )

        # Rotate primitive cell back to the orientation of the given cell and atoms
        spglib_data.primitive_cell = primitive_cell @ dataset.std_rotation_matrix
        spglib_data.primitive_positions = primitive_positions
        spglib_data.primitive_types = primitive_types

        return spglib_data

    except Exception as e:
        _raise_with_message(
            e=e,
            message=f"Call to spglib failed with spglib version {spglib.__version__}."
            + _SUPPORT_FOOTER,
        )


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
