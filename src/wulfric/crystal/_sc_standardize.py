# Wulfric - Crystal, Lattice, Atoms, K-path.
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

from wulfric.cell._basic_manipulation import get_params
from wulfric.cell._lepage import lepage
from wulfric.cell._sc_standardize import get_S_matrix, get_standardized
from wulfric.constants._numerical import EPS_LENGTH, EPS_RELATIVE

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def standardize(cell, atoms, S_matrix=None, rtol=EPS_RELATIVE, atol=EPS_LENGTH):
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
    rtol : float, default ``EPS_RELATIVE``
        Relative tolerance for numerical comparison. Ignored if ``S_matrix`` is provided.
    atol : float, default ``EPS_LENGTH``
        Absolute tolerance for numerical comparison. Ignored if ``S_matrix`` is provided.

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
        lattice_type = lepage(
            *get_params(cell),
            eps_relative=rtol,
            eps_angle=atol,
        )

        S_matrix = get_S_matrix(cell, lattice_type, rtol=rtol, atol=atol)
    else:
        S_matrix = np.array(S_matrix, dtype=float)

    # Standardize cell
    cell = get_standardized(cell=cell, S_matrix=S_matrix)

    # Recalculate atom's relative coordinates.
    atoms["positions"] = [S_matrix @ position for position in atoms["positions"]]

    return cell


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
