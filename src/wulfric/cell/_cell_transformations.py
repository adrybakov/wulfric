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

from wulfric.constants._space_groups import crystal_family, centring_type
from wulfric._exceptions import ConventionNotSupported

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def get_C_matrix(
    cell,
    convention="hpkot",
    spglib_symprec=1e-5,
    spglib_angle_tolerance=-1,
):
    r"""
    Return a matrix that converts the given cell into the conventional one, that acts as

    .. code-block:: python

        conventional_cell = C.T @ cell

    Parameters
    ==========
    cell : (3, 3) |array-like|_
        Matrix of a cell, rows are interpreted as vectors.
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
    wulfric.cell.get_conventional
    wulfric.crystal.get_C_matrix
    wulfric.crystal.get_conventional

    Notes
    =====
    This method treats the given cell as primitive one (on contrary with
    :py:func:`wulfric.crystal.get_C_martix`). Internally wulfric populates the cell with
    one fictitious atom at ``[0, 0, 0]`` before passing info to |spglib|_.

    References
    ==========
    .. [1] Hinuma, Y., Pizzi, G., Kumagai, Y., Oba, F. and Tanaka, I., 2017.
           Band structure diagram paths based on crystallography.
           Computational Materials Science, 128, pp.140-184.
    .. [2] Setyawan, W. and Curtarolo, S., 2010.
           High-throughput electronic band structure calculations: Challenges and tools.
           Computational materials science, 49(2), pp. 299-312.
    """

    C_matrix = np.linalg.inv(cell).T @ get_conventional(
        cell=cell,
        convention=convention,
        spglib_symprec=spglib_symprec,
        spglib_angle_tolerance=spglib_angle_tolerance,
    )

    return C_matrix


def get_conventional(
    cell,
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

    See Also
    ========
    wulfric.cell.get_C_matrix
    wulfric.crystal.get_C_matrix
    wulfric.crystal.get_conventional

    Notes
    =====
    This method treats the given cell as primitive one (on contrary with
    :py:func:`wulfric.crystal.get_conventional`). Internally wulfric populates the cell
    with one fictitious atom at ``[0, 0, 0]`` before passing info to |spglib|_.

    References
    ==========
    .. [1] Hinuma, Y., Pizzi, G., Kumagai, Y., Oba, F. and Tanaka, I., 2017.
           Band structure diagram paths based on crystallography.
           Computational Materials Science, 128, pp.140-184.
    .. [2] Setyawan, W. and Curtarolo, S., 2010.
           High-throughput electronic band structure calculations: Challenges and tools.
           Computational materials science, 49(2), pp. 299-312.
    """

    # IDEA point to the same function of the crystal
    # The functions of the crystal are the most general ones.
    # Same goes for niggli cell, keep the method, but default to spglib:
    # niggli(..., implementation="spglib"/"wulfric")

    convention = convention.lower()

    fictitious_atomic_points = [[0, 0, 0]]
    fictitious_types = [1]

    dataset = spglib.get_symmetry_dataset(
        (cell, fictitious_atomic_points, fictitious_types),
        symprec=spglib_symprec,
        angle_tolerance=spglib_angle_tolerance,
    )

    conventional_cell = dataset.std_lattice @ dataset.std_rotation_matrix

    if convention == "spglib":
        return conventional_cell

    bravais_lattice = crystal_family[dataset.number] + centring_type[dataset.number]

    if convention == "hpkot":
        if bravais_lattice == "aP":
            raise NotImplementedError

        return conventional_cell

    if convention == "sc":
        raise NotImplementedError

    raise ConventionNotSupported(convention, with_spglib=True)


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
