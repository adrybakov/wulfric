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

try:
    from scipy.spatial import Voronoi

    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def _lattice_points(cell, relative=False):
    r"""
    Compute lattice points

    Parameters
    ----------
    cell : (3,3) |array-like|_
        Primitive unit cell.
    relative : bool, default False
        Whether to return relative or absolute coordinates.

    Returns
    -------
    lattice_points : (N, 3) :numpy:`ndarray`
        N lattice points. Each element is a vector :math:`v = (v_x, v_y, v_z)`.
    """

    lattice_points = np.zeros((27, 3), dtype=float)
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            for k in [-1, 0, 1]:
                point = np.array([i, j, k])
                if not relative:
                    point = point @ cell
                lattice_points[9 * (i + 1) + 3 * (j + 1) + (k + 1)] = point
    return lattice_points


def _get_voronoi_cell(cell):
    r"""
    Computes Voronoi edges around (0,0,0) point.

    Parameters
    ----------
    cell : (3,3) |array-like|_
        Primitive unit cell.

    Returns
    -------
    edges : (N, 2, 3) :numpy:`ndarray`
        N edges of the Voronoi cell around (0,0,0) point.
        Each elements contains two vectors of the points
        of the voronoi vertices forming an edge.
    vertices : (M, 3) :numpy:`ndarray`
        M vertices of the Voronoi cell around (0,0,0) point.
        Each element is a vector :math:`v = (v_x, v_y, v_z)`.
    """

    if not SCIPY_AVAILABLE:
        raise ImportError('SciPy is not available. Install it with "pip install scipy"')
    voronoi = Voronoi(_lattice_points(cell, relative=False))
    edges_index = set()
    # Thanks ase for the idea. 13 - is the index of (0,0,0) point.
    for rv, rp in zip(voronoi.ridge_vertices, voronoi.ridge_points):
        if -1 not in rv and 13 in rp:
            for j in range(0, len(rv)):
                if (rv[j - 1], rv[j]) not in edges_index and (
                    rv[j],
                    rv[j - 1],
                ) not in edges_index:
                    edges_index.add((rv[j - 1], rv[j]))
    edges_index = np.array(list(edges_index))
    edges = np.zeros((edges_index.shape[0], 2, 3), dtype=voronoi.vertices.dtype)
    for i in range(edges_index.shape[0]):
        edges[i][0] = voronoi.vertices[edges_index[i][0]]
        edges[i][1] = voronoi.vertices[edges_index[i][1]]
    return edges, voronoi.vertices[np.unique(edges_index.flatten())]


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
