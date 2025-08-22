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
import numpy as np

from wulfric.cell._basic_manipulation import get_reciprocal

try:
    from scipy.spatial import Voronoi

    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def get_lattice_points(cell, range=(1, 1, 1), relative=False, flat=True):
    r"""
    Compute lattice points for the given cell.

    Assumes that ``cell`` contains one lattice point.

    Parameters
    ----------
    cell : (3, 3) |array-like|_
        Matrix of a cell, rows are interpreted as vectors.
    range : (3, ) list or tuple of int, default (1, 1, 1)
        How many lattice points to return. All lattice points with relative coordinates
        ``r_1``, ``r_2``, ``r_3``, that fulfil

        * ``-range[0] <= r_1 <= range[0]``
        * ``-range[1] <= r_2 <= range[1]``
        * ``-range[2] <= r_3 <= range[2]``
    relative : bool, default False
        Whether to return relative coordinates.
    flat : bool, default False

    Returns
    -------
    lattice_points : (N1, N2, N3, 3) or (N, 3) :numpy:`ndarray`
        N lattice points. Each element is a vector :math:`v = (v_x, v_y, v_z)`.

        * ``N = N1 * N2 * N3``
        * ``N1 = 2 * range[0] + 1``
        * ``N2 = 2 * range[1] + 1``
        * ``N3 = 2 * range[2] + 1``

        The shape of the returned array is

        * (N, 3) if ``flat=True``
        * (N1, N2, N3, 3) if ``flat=False``
    """

    N1 = 2 * range[0] + 1
    N2 = 2 * range[1] + 1
    N3 = 2 * range[2] + 1

    lp1 = np.arange(-range[0], range[0] + 1)
    lp2 = np.arange(-range[1], range[1] + 1)
    lp3 = np.arange(-range[2], range[2] + 1)

    lattice_points = np.array(np.meshgrid(lp1, lp2, lp3, indexing="ij")).transpose(
        (1, 2, 3, 0)
    )

    if not relative:
        lattice_points = lattice_points @ cell

    if flat:
        lattice_points = np.reshape(lattice_points, shape=(N1 * N2 * N3, 3))

    return lattice_points


def _get_voronoi_cell(cell):
    r"""
    Computes Voronoi edges around (0,0,0) point.

    Parameters
    ----------
    cell : (3, 3) |array-like|_
        Matrix of a cell, rows are interpreted as vectors.

    Returns
    -------
    vertices : (M, 3) :numpy:`ndarray`
        M vertices of the Voronoi cell around (0,0,0) point. Each element is a vector
        :math:`v = (v_x, v_y, v_z)`.
    edges : (N, 2) :numpy:`ndarray`
        N edges of the Voronoi cell around (0,0,0) point. Each elements contains two
        indices of the ``vertices`` forming an edge. Edge ``i`` is between points
        ``vertices[edges[i][0]]`` and ``vertices[edges[i][1]]``.
    """

    n = 10
    index_000 = ((2 * n + 1) ** 3 - 1) // 2

    if not SCIPY_AVAILABLE:
        raise ImportError(
            'SciPy is not available. Please install it with "pip install scipy"'
        )
    voronoi = Voronoi(get_lattice_points(cell, relative=False, range=(n, n, n)))
    edges_index = set()
    # Thanks ASE for the general idea
    # Note that more than -10 0 10 range is required for the lattice points to correctly
    # produce the Voronoi decomposition of the lattice in most cases
    # In general bigger span might be required
    for rv, rp in zip(voronoi.ridge_vertices, voronoi.ridge_points):
        if -1 not in rv and index_000 in rp:
            for j in range(0, len(rv)):
                if (rv[j - 1], rv[j]) not in edges_index and (
                    rv[j],
                    rv[j - 1],
                ) not in edges_index:
                    edges_index.add((rv[j - 1], rv[j]))
    edges_index = np.array(list(edges_index))
    edges = np.zeros((edges_index.shape[0], 2, 3), dtype=voronoi.vertices.dtype)
    for i in range(edges_index.shape[0]):
        edges[i][0] = edges_index[i][0]
        edges[i][1] = edges_index[i][1]
    return voronoi.vertices[np.unique(edges_index.flatten())], edges


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir


def get_wigner_seitz_cell(cell):
    r"""
    Computes |Wigner-Seitz|_ cell.

    It assumes that given ``cell`` contains one lattice point.

    Parameters
    ----------
    cell : (3, 3) |array-like|_
        Matrix of a cell, rows are interpreted as vectors.

    Returns
    -------
    vertices : (M, 3) :numpy:`ndarray`
        M vertices of the |Wigner-Seitz|_ cell. Each element is a vector
        :math:`v = (v_x, v_y, v_z)` in absolute (Cartesian) coordinates.
    edges : (N, 2) :numpy:`ndarray`
        N edges of the |Wigner-Seitz|_ cell. Each elements contains two indices of the
        ``vertices`` forming an edge. Edge ``i`` is between points
        ``vertices[edges[i][0]]`` and ``vertices[edges[i][1]]``.
    """

    return _get_voronoi_cell(cell=cell)


def get_brillouin_zone(cell):
    r"""
    Computes Brillouin_zone.

    It assumes that given ``cell`` contains one lattice point.

    Parameters
    ----------
    cell : (3, 3) |array-like|_
        Matrix of a cell, rows are interpreted as vectors.

    Returns
    -------
    vertices : (M, 3) :numpy:`ndarray`
        M vertices of the Brillouin_zone. Each element is a vector
        :math:`v = (v_x, v_y, v_z)` in absolute (Cartesian) coordinates.
    edges : (N, 2) :numpy:`ndarray`
        N edges of the Brillouin_zone. Each elements contains two indices of the
        ``vertices`` forming an edge. Edge ``i`` is between points
        ``vertices[edges[i][0]]`` and ``vertices[edges[i][1]]``.
    """

    return _get_voronoi_cell(cell=get_reciprocal(cell=cell))
