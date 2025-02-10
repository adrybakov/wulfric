# Wulfric - Cell, Atoms, K-path.
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


import numpy as np

from wulfric.cell._lepage import lepage
from wulfric.cell._sc_standardize import get_S_matrix, get_standardized

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def standardize(
    cell, atoms, S_matrix=None, length_tolerance=1e-8, angle_tolerance=1e-4
):
    R"""
    Standardize cell with respect to the Bravais lattice type as defined in [1]_.

    ``atoms`` are not returned, but rather updated.

    Parameters
    ----------
    cell : (3,3) |array-like|_
        Primitive unit cell.
    atoms : dict
        Dictionary with atoms. Must have a ``positions`` with value of (N,3) |array-like|_.
    S_matrix : (3,3) |array-like|_, optional
        Transformation matrix S.
    length_tolerance : float, default :math:`10^{-8}`
        Tolerance for length variables (lengths of the lattice vectors). Default values
        are chosen for the contexts of condense matter physics, where Angstroms are used.
        Please choose appropriate tolerance for your problem.
    angle_tolerance : float, default :math:`10^{-4}`
        Tolerance for angle variables (angles of the lattice). Default values are chosen
        for the contexts of condense matter physics, where Angstroms are used. Please
        choose appropriate tolerance for your problem.

    Returns
    -------
    cell : (3,3) :numpy:`ndarray`
        Standardized cell. Rows are lattice vectors. Independent from the initial cell,
        safe to modify.

    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp.299-312.
    """

    cell = np.array(cell, dtype=float)

    # Get S matrix before cell standardization
    if S_matrix is None:
        lattice_type = lepage(cell, angle_tolerance=angle_tolerance)

        S_matrix = get_S_matrix(
            cell,
            lattice_type,
            length_tolerance=length_tolerance,
            angle_tolerance=angle_tolerance,
        )
    else:
        S_matrix = np.array(S_matrix, dtype=float)

    # Standardize cell
    cell = get_standardized(cell=cell, S_matrix=S_matrix)

    # Recalculate atom's relative coordinates.
    atoms["positions"] = [
        np.linalg.inv(S_matrix) @ position for position in atoms["positions"]
    ]

    return cell


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
