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

from wulfric.constants._space_groups import CRYSTAL_FAMILY, CENTRING_TYPE
from wulfric._exceptions import ConventionNotSupported
from wulfric.crystal._crystal_validation import validate_atoms
from wulfric.crystal._atoms import get_spglib_types
from wulfric.crystal._basic_manipulation import get_spatial_mapping

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def get_C_matrix(
    cell,
    atoms,
    convention="hpkot",
    spglib_symprec=1e-5,
    spglib_angle_tolerance=-1,
):
    r"""
    Return a matrix that converts the given cell into the conventional one

    .. code-block:: python

        conventional_cell = C.T @ cell

    Parameters
    ==========
    cell : (3, 3) |array-like|_
        Matrix of a cell, rows are interpreted as vectors.
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

    convention : str, default "hpkot"
        Convention for the definition of the conventional cell. Case-insensitive.
        Supported:

        * "HPKOT" for [1]_
        * "SC" for [2]_
        * "spglib* for |spglib|_

    spglib_symprec : float, default 1e-5
        Tolerance parameter for the symmetry search, that is passed to |spglib|_. Quote
        from its documentation: "Symmetry search tolerance in the unit of length".
    spglib_angle_tolerance : float, default -1
        Tolerance parameter for the symmetry search, that is passed to |spglib|_. Quote
        from its documentation: "Symmetry search tolerance in the unit of angle deg.
        Normally it is not recommended to use this argument. If the value is
        negative, an internally optimized routine is used to judge symmetry.

    Returns
    =======
    C_matrix : (3, 3) :numpy:`ndarray`
        Transformation matrix from the given cell into the conventional one.

    See Also
    ========
    :ref:`user-guide_conventions_which-cell`
    wulfric.crystal.get_conventional
    wulfric.cell.get_conventional
    wulfric.cell.get_C_matrix

    Notes
    =====
    |spglib|_ uses ``types`` to distinguish the atoms. To see how wulfric defines the
    ``types`` see :ref:`wulfric.crystal.get_spglib_types()`.

    References
    ==========
    .. [1] Hinuma, Y., Pizzi, G., Kumagai, Y., Oba, F. and Tanaka, I., 2017.
           Band structure diagram paths based on crystallography.
           Computational Materials Science, 128, pp.140-184.
    .. [2] Setyawan, W. and Curtarolo, S., 2010.
           High-throughput electronic band structure calculations: Challenges and tools.
           Computational materials science, 49(2), pp. 299-312.
    """

    conventional_cell, _ = get_conventional(
        cell=cell,
        atoms=atoms,
        convention=convention,
        spglib_symprec=spglib_symprec,
        spglib_angle_tolerance=spglib_angle_tolerance,
    )

    return np.linalg.inv(cell).T @ conventional_cell


def get_conventional(
    cell,
    atoms,
    convention="hpkot",
    spglib_symprec=1e-5,
    spglib_angle_tolerance=-1,
):
    r"""
    Return conventional cell associated with the given ``cell``.

    Parameters
    ==========
    cell : (3, 3) |array-like|_
        Matrix of a cell, rows are interpreted as vectors.
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

    convention : str, default "hpkot"
        Convention for the definition of the conventional cell. Case-insensitive.
        Supported:

        * "HPKOT" for [1]_
        * "SC" for [2]_
        * "spglib* for |spglib|_

    spglib_symprec : float, default 1e-5
        Tolerance parameter for the symmetry search, that is passed to |spglib|_. Quote
        from its documentation: "Symmetry search tolerance in the unit of length".
    spglib_angle_tolerance : float, default -1
        Tolerance parameter for the symmetry search, that is passed to |spglib|_. Quote
        from its documentation: "Symmetry search tolerance in the unit of angle deg.
        Normally it is not recommended to use this argument. If the value is
        negative, an internally optimized routine is used to judge symmetry.

    Returns
    =======
    conventional_cell : (3, 3) :numpy:`ndarray`
        Conventional cell.
    conventional_atoms : dict
        Dictionary of atoms of the conventional cell. Has all the same keys as the
        original ``atoms``. The values of each key are updated in such a way that
        ``conventional_cell`` with ``conventional_atoms`` describe the same crystal (and
        in the same spatial orientation) as ``cell with ``atoms``.

    See Also
    ========
    :ref:`user-guide_conventions_which-cell`
    wulfric.crystal.get_C_matrix
    wulfric.cell.get_C_matrix
    wulfric.cell.get_conventional

    Notes
    =====
    |spglib|_ uses ``types`` to distinguish the atoms. To see how wulfric defines the
    ``types`` see :ref:`wulfric.crystal.get_spglib_types()`.


    References
    ==========
    .. [1] Hinuma, Y., Pizzi, G., Kumagai, Y., Oba, F. and Tanaka, I., 2017.
           Band structure diagram paths based on crystallography.
           Computational Materials Science, 128, pp.140-184.
    .. [2] Setyawan, W. and Curtarolo, S., 2010.
           High-throughput electronic band structure calculations: Challenges and tools.
           Computational materials science, 49(2), pp. 299-312.
    """

    # Validate that the atoms dictionary is what expected of it
    validate_atoms(atoms=atoms, required_keys=["positions"], raise_errors=True)

    dataset = spglib.get_symmetry_dataset(
        (cell, atoms["positions"], get_spglib_types(atoms=atoms)),
        symprec=spglib_symprec,
        angle_tolerance=spglib_angle_tolerance,
    )

    conv_cell = dataset.std_lattice @ dataset.std_rotation_matrix
    conv_positions = dataset.std_positions
    bravais_lattice = CRYSTAL_FAMILY[dataset.number] + CENTRING_TYPE[dataset.number]

    convention = convention.lower()
    if convention == "spglib" or convention == "hpkot" and bravais_lattice != "aP":
        # dataset.std_types might be more uniform that actual properties of atoms.
        # Therefor, wulfric need to match the cartesian coordinates of the atoms
        # of the conventional lattice with the cartesian coordinates of the atoms
        # of the original original lattice.
        mapping = get_spatial_mapping(
            old_cell=cell,
            old_positions=atoms["positions"],
            new_cell=conv_cell,
            new_positions=conv_positions,
        )

        conv_atoms = dict(positions=conv_positions)

        # Populate conv_atoms with all keys that have been defined in the original atoms.
        for key in atoms:
            if key != "positions":
                conv_atoms[key] = []
                for index in mapping:
                    conv_atoms[key].append(atoms[key][index])

        return conv_cell, conv_atoms

    if convention == "hpkot" and bravais_lattice == "aP":
        raise NotImplementedError

    if convention == "sc":
        raise NotImplementedError

    raise ConventionNotSupported(convention, with_spglib=True)


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
