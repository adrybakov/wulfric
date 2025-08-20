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
import numpy as np
from wulfric._syntactic_sugar import SyntacticSugar, add_sugar
from wulfric._exceptions import _raise_with_message, _SUPPORT_FOOTER

from wulfric.constants._space_groups import CRYSTAL_FAMILY, CENTRING_TYPE

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def get_spglib_data(
    cell,
    atom_positions,
    atom_types,
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
    atom_positions : (N, 3) |array-like|_
        Relative positions of N atoms with respect to the given ``cell``. In the
        language of |spglib|_ it is usually called "positions" or "atomic points".
    atom_types : (N, ) list of int
        Directly passed to |spglib|_. All elements are >= 1. Used to distinguish atoms.
        In the language of |spglib|_ it is usually called "types".
    spglib_symprec : float, default 1e-5
        Directly passed to |spglib|_. Tolerance parameter for the symmetry search.
    spglib_angle_tolerance : float, default -1
        Directly passed to |spglib|_. Tolerance parameter for the symmetry search.

    Returns
    =======
    spglib_data : dict
        A dictionary with the added syntactic sugar (i.e. with the dot access to the keys).

        Data that are included:

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
    """

    try:
        # Validate input data
        if len(atom_types) != len(atom_positions):
            raise ValueError(
                f"Length of atom_types ({len(atom_types)}) do not match the length of atom_positions ({len(atom_positions)})."
            )

        for i in range(len(atom_types)):
            if not isinstance(atom_types[i], int):
                raise TypeError(
                    f"Element {i} of atom_types is not an integer, got {type(atom_types[i])}."
                )
            if atom_types < 1:
                raise ValueError(
                    f"Element {i} of atom_types is lower than 1, got {atom_types[i]}."
                )

        try:
            atom_positions = np.array(atom_positions, dtype=float)
        except Exception as e:
            _raise_with_message(
                e=e, message=f"atom_positions is not array-like, got\n{atom_positions}"
            )

        if len(atom_positions.shape) != 2 or atom_positions.shape[1] != 3:
            raise ValueError(
                f"Expected shape of (N, 3) for atom_positions, got {atom_positions.shape}."
            )

        try:
            cell = np.array(cell, dtype=float)
        except Exception as e:
            _raise_with_message(e=e, message=f"cell is not array-like, got\n{cell}")

        if cell.shape != (3, 3):
            raise ValueError(f"Expected shape of (3, 3) for cell, got {cell.shape}.")

        # Just a dictionary with dot-like access to its keys
        spglib_data = SyntacticSugar()

        dataset = spglib.get_symmetry_dataset(
            (cell, atom_positions, atom_types),
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
            (cell, atom_positions, atom_types),
            symprec=spglib_symprec,
            angle_tolerance=spglib_angle_tolerance,
        )

        # Rotate primitive cell back to the orientation of the given cell and atoms
        spglib_data.primitive_cell = primitive_cell @ dataset.std_rotation_matrix
        spglib_data.primitive_positions = primitive_positions
        spglib_data.primitive_types = primitive_types

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
