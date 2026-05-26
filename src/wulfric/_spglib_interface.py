# ================================== LICENSE ===================================
# Wulfric - Cell, Atoms, K-path, visualization.
# Copyright (C) 2023 Andrey Rybakov
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
from dataclasses import dataclass

import spglib
from copy import deepcopy
import numpy as np
from wulfric._syntactic_sugar import add_sugar
from wulfric.crystal._crystal_validation import validate_atoms
from wulfric._exceptions import _raise_with_message, _SUPPORT_FOOTER
from wulfric.crystal._atoms import get_atom_species

from wulfric.constants._space_groups import CRYSTAL_FAMILY, CENTRING_TYPE

__all__ = ["SpglibData", "validate_spglib_data", "get_spglib_types", "get_spglib_data"]


@dataclass(eq=False, frozen=True)
class SpglibData:
    r"""
    Data from spglib.

    .. versionadded:: 0.7.0

    Parameters
    ==========
    cell : (3, 3) |array-like|_
        See :py:func:`.get_spglib_data`.
    atoms : dict
        See :py:func:`.get_spglib_data`.
    spglib_symprec : float, default :math:`10^{-5}`
        See :py:func:`.get_spglib_data`.
    spglib_angle_tolerance : float, default -1
        See :py:func:`.get_spglib_data`.
    """

    def __init__(self, cell, atoms, spglib_symprec=1e-5, spglib_angle_tolerance=-1):
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
                raise ValueError(
                    f"Expected shape of (3, 3) for cell, got {cell.shape}."
                )

            # Populate with the input data

            object.__setattr__(self, "original_cell", deepcopy(cell))
            object.__setattr__(
                self,
                "original_positions",
                np.array(deepcopy(atoms["positions"]), dtype=float),
            )
            object.__setattr__(
                self, "original_types", deepcopy(get_spglib_types(atoms=atoms))
            )
            object.__setattr__(self, "symprec", spglib_symprec)
            object.__setattr__(self, "angle_tolerance", spglib_angle_tolerance)

            # Populate with the version of the spglib
            object.__setattr__(self, "spglib_version", spglib.__version__)

            dataset = spglib.get_symmetry_dataset(
                (cell, self.original_positions, self.original_types),
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

            object.__setattr__(self, "space_group_number", dataset.number)
            object.__setattr__(self, "crystal_family", CRYSTAL_FAMILY[dataset.number])
            object.__setattr__(self, "centring_type", CENTRING_TYPE[dataset.number])
            # Rotate conventional cell back to the orientation of the given cell and atoms
            object.__setattr__(
                self,
                "conventional_cell",
                dataset.std_lattice @ dataset.std_rotation_matrix,
            )
            object.__setattr__(
                self,
                "conventional_positions",
                np.array(dataset.std_positions, dtype=float),
            )
            object.__setattr__(self, "conventional_types", dataset.std_types)

            primitive_cell, primitive_positions, primitive_types = (
                spglib.find_primitive(
                    (cell, self.original_positions, self.original_types),
                    symprec=spglib_symprec,
                    angle_tolerance=spglib_angle_tolerance,
                )
            )

            # Rotate primitive cell back to the orientation of the given cell and atoms
            object.__setattr__(
                self, "primitive_cell", primitive_cell @ dataset.std_rotation_matrix
            )
            object.__setattr__(
                self, "primitive_positions", np.array(primitive_positions, dtype=float)
            )
            object.__setattr__(self, "primitive_types", primitive_types)

        except Exception as e:
            _raise_with_message(
                e=e,
                message=f"Call to spglib failed. Spglib version {spglib.__version__}."
                + _SUPPORT_FOOTER,
            )

    original_cell: np.ndarray
    r"""
    Same as the given ``cell``.
    """

    original_positions: np.ndarray
    r"""
    Same as the given ``atoms["positions"]``.
    """

    original_types: list
    r"""
    Same as ``wulfric.get_spglib_types(atoms=atoms)`` for given ``atoms``.
    """

    spglib_version: str
    r"""
    Version of spglib that was used to create this dataset.
    """

    space_group_number: int
    r"""
    Number of the space group. ``1 <= spglib_data.space_group_number <= 230``.
    """

    crystal_family: str
    r"""
    Crystal family.

    * "c" for cubic
    * "h" for hexagonal
    * "t" for tetragonal
    * "o" for orhorhombic
    * "m" for monoclinic
    * "a" for triclinic
    """

    centring_type: str
    r"""
    Centring type.

    * "P" for primitive
    * "A" for side centered
    * "C" for side centered
    * "I" for body-centered
    * "R" for rhombohedral centring
    * "F" for all faces centered
    """

    conventional_cell: np.ndarray
    r"""
    Conventional cell associated with the given structure in the same spatial
    orientation. In other words, it is a choice of the cell for the same crystal.
    It can contain more than one lattice point. Same as ``std_lattice`` of
    |spglib-dataset|_ but rotated back with the ``std_rotation_matrix`` of
    |spglib-dataset|_.
    """

    conventional_positions: np.ndarray
    r"""
    N relative positions of the atoms in the basis of
    ``spglib_data.conventional_cell``. Same as ``std_positions`` of
    |spglib-dataset|_.
    """

    conventional_types: list
    r"""
    N types of the atoms. Same as ``std_types`` of |spglib-dataset|_.
    """

    primitive_cell: np.ndarray
    r"""
    Primitive cell associated with the given structure in the same spatial
    orientation. In other words, it is a choice of the cell for the same crystal.
    It contains exactly one lattice point. Same as ``primitive_lattice``
    returned by |spglib-find-primitive|_, but rotated back with the
    ``std_rotation_matrix`` of |spglib-dataset|_.
    """

    primitive_positions: np.ndarray
    r"""
    M relative positions of the atoms in the basis of
    ``spglib_data.primitive_cell``. Same as ``primitive_positions``
    returned by |spglib-find-primitive|_.
    """

    primitive_types: list
    r"""
    M types of the atoms. Same as ``primitive_types``
    returned by |spglib-find-primitive|_.
    """

    symprec: float
    r"""
    Tolerance parameter that was used to call |spglib|_.
    """

    angle_tolerance: float
    r"""
    Tolerance parameter that was used to call |spglib|_.
    """


def validate_spglib_data(cell, atoms, spglib_data) -> None:
    r"""
    Validate that ``cell`` and ``atoms["positions"]`` match the ones on which
    ``spglib_data`` was created.

    In details, it check that

    * ``cell`` is the same as ``spglib_data.original_cell``
    * ``atoms["positions"]`` are the same as ``spglib_data.original_positions``
    * ``wulfric.get_spglib_types(atoms=atoms)`` is the same as
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

    .. versionchanged:: 0.7.0 Rule 3 modified to account for failed deduction of species from names.

    First satisfied rule is applied

    1.  "spglib_types" in atoms

        Return ``atoms["spglib_types"]``.

    2.  "species" in atoms.

        ``spglib_types`` are deduced from ``atoms["species"]``. If two atoms have the same
        species, then they will have the same integer assigned to them in
        ``spglib_types``.

    3.  "names" in ``atoms``.

        Species are automatically deduced based on atom's names (via
        :py:func:`wulfric.crystal.get_atom_species`). Then the new list is constructed as:

        a.  If the deduced species is "X", then the atom's name is used.
        b.  If the deduced species is not "X", then the deduced species is used.

        If the two atoms have the same entry in that new list, then they have the
        same integer assigned to them in ``spglib_types``.

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

    Raises
    ======
    ValueError
        If neither "spglib_types" nor "species" nor "names" are present in ``atoms``.
    """

    validate_atoms(atoms=atoms, raise_errors=True)

    if "spglib_types" in atoms:
        spglib_types = atoms["spglib_types"]
    else:
        if "species" not in atoms and "names" in atoms:
            # Try to deduce species automatically from names
            identifiers = [
                get_atom_species(name=name, raise_on_fail=False)
                for name in atoms["names"]
            ]

            # When detection fails, fallback to using name as an identifier.
            identifiers = [
                atoms["names"][i] if identifier == "X" else identifier
                for i, identifier in enumerate(identifiers)
            ]
        elif "species" in atoms:
            identifiers = atoms["species"]
        else:
            raise ValueError(
                'Expected at least one of "spglib_types", "species" or "names" keys in "atoms", found none.'
            )

        mapping = {
            name: index + 1 for index, name in enumerate(sorted(list(set(identifiers))))
        }
        spglib_types = [mapping[name] for name in identifiers]

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
            Pass ``atoms = dict(positions=[[0, 0, 0]], spglib_types=[1])`` to interpret
            the ``cell`` alone (effectively assuming that the ``cell`` is a primitive
            one).
    spglib_symprec : float, default :math:`10^{-5}`
        Directly passed to |spglib|_. Tolerance parameter for the symmetry search.
    spglib_angle_tolerance : float, default -1
        Directly passed to |spglib|_. Tolerance parameter for the symmetry search.

    Returns
    =======
    spglib_data : :py:class:`.SpglibData`

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
    ``types`` from given ``atoms`` see :py:func:`wulfric.get_spglib_types`.
    """

    return SpglibData(
        cell=cell,
        atoms=atoms,
        spglib_symprec=spglib_symprec,
        spglib_angle_tolerance=spglib_angle_tolerance,
    )
