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

from wulfric.cell._basic_manipulation import get_reciprocal
from wulfric.constants._sc_notation import DEFAULT_K_PATHS, HS_PLOT_NAMES

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def get_hs_data(
    cell,
    return_relative=True,
):
    r"""
    Return information about high symmetry points. An interface to |seek-kpath|_.

    Parameters
    ----------
    cell : (3, 3) |array-like|_
        Matrix of a cell, rows are interpreted as vectors.
    return_relative : bool, default True
        Whether to return coordinates as relative to the reciprocal cell or in absolute
        coordinates in the reciprocal Cartesian space.

    Returns
    -------
    coordinates : list of (3, 3) :numpy:`ndarray`
        Coordinates of the high symmetry points in reciprocal space. Relative to the
        reciprocal cell.
    names: list of str
        Names of the high symmetry points. Used for programming, not for plotting. Have
        the same length as ``coordinates``.
    labels : list of str
        List of the high symmetry points labels for plotting. Have the same length as
        ``coordinates``. Labels are not necessary equal to the names.
    path : str
        K path. High symmetry points are referenced by elements of ``names``.

    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp. 299-312.

    See Also
    --------
    wulfric.Kpoints : Class with a convenient interface for the same information.

    """

    cell = np.array(cell, dtype=float)

    names = []
    labels = []
    coordinates = []

    for point in hs_points:
        names.append(point)
        # Compute relative coordinates with respect to the
        # non-standardized primitive cell
        # here hs_points[point] <- \tilde{g} and coordinates <- g
        coordinates.append(np.linalg.inv(S_matrix).T @ hs_points[point])

        labels.append(HS_PLOT_NAMES[point])

    if not return_relative:

        rcell = get_reciprocal(cell)

        for i in range(len(coordinates)):
            coordinates[i] = coordinates[i] @ rcell

    return coordinates, names, labels, DEFAULT_K_PATHS[lattice_variation]


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
