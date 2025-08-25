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
import pytest
import numpy as np

from wulfric.cell._basic_manipulation import get_reciprocal
from wulfric.cell._sc_examples import sc_get_example_cell
from wulfric.cell._voronoi import _get_voronoi_cell, get_lattice_points
from wulfric.constants._sc_convention import SC_BRAVAIS_LATTICE_VARIATIONS


def test_get_lattice_points():
    cell = np.array([[0.2, 0.5, 0.9], [3, 6, 0], [0.8, 5, 1]])

    lp_reference_relative_not_flat = np.array(
        [
            [
                [
                    [-1, -2, -3],
                    [-1, -2, -2],
                    [-1, -2, -1],
                    [-1, -2, 0],
                    [-1, -2, 1],
                    [-1, -2, 2],
                    [-1, -2, 3],
                ],
                [
                    [-1, -1, -3],
                    [-1, -1, -2],
                    [-1, -1, -1],
                    [-1, -1, 0],
                    [-1, -1, 1],
                    [-1, -1, 2],
                    [-1, -1, 3],
                ],
                [
                    [-1, 0, -3],
                    [-1, 0, -2],
                    [-1, 0, -1],
                    [-1, 0, 0],
                    [-1, 0, 1],
                    [-1, 0, 2],
                    [-1, 0, 3],
                ],
                [
                    [-1, 1, -3],
                    [-1, 1, -2],
                    [-1, 1, -1],
                    [-1, 1, 0],
                    [-1, 1, 1],
                    [-1, 1, 2],
                    [-1, 1, 3],
                ],
                [
                    [-1, 2, -3],
                    [-1, 2, -2],
                    [-1, 2, -1],
                    [-1, 2, 0],
                    [-1, 2, 1],
                    [-1, 2, 2],
                    [-1, 2, 3],
                ],
            ],
            [
                [
                    [0, -2, -3],
                    [0, -2, -2],
                    [0, -2, -1],
                    [0, -2, 0],
                    [0, -2, 1],
                    [0, -2, 2],
                    [0, -2, 3],
                ],
                [
                    [0, -1, -3],
                    [0, -1, -2],
                    [0, -1, -1],
                    [0, -1, 0],
                    [0, -1, 1],
                    [0, -1, 2],
                    [0, -1, 3],
                ],
                [
                    [0, 0, -3],
                    [0, 0, -2],
                    [0, 0, -1],
                    [0, 0, 0],
                    [0, 0, 1],
                    [0, 0, 2],
                    [0, 0, 3],
                ],
                [
                    [0, 1, -3],
                    [0, 1, -2],
                    [0, 1, -1],
                    [0, 1, 0],
                    [0, 1, 1],
                    [0, 1, 2],
                    [0, 1, 3],
                ],
                [
                    [0, 2, -3],
                    [0, 2, -2],
                    [0, 2, -1],
                    [0, 2, 0],
                    [0, 2, 1],
                    [0, 2, 2],
                    [0, 2, 3],
                ],
            ],
            [
                [
                    [1, -2, -3],
                    [1, -2, -2],
                    [1, -2, -1],
                    [1, -2, 0],
                    [1, -2, 1],
                    [1, -2, 2],
                    [1, -2, 3],
                ],
                [
                    [1, -1, -3],
                    [1, -1, -2],
                    [1, -1, -1],
                    [1, -1, 0],
                    [1, -1, 1],
                    [1, -1, 2],
                    [1, -1, 3],
                ],
                [
                    [1, 0, -3],
                    [1, 0, -2],
                    [1, 0, -1],
                    [1, 0, 0],
                    [1, 0, 1],
                    [1, 0, 2],
                    [1, 0, 3],
                ],
                [
                    [1, 1, -3],
                    [1, 1, -2],
                    [1, 1, -1],
                    [1, 1, 0],
                    [1, 1, 1],
                    [1, 1, 2],
                    [1, 1, 3],
                ],
                [
                    [1, 2, -3],
                    [1, 2, -2],
                    [1, 2, -1],
                    [1, 2, 0],
                    [1, 2, 1],
                    [1, 2, 2],
                    [1, 2, 3],
                ],
            ],
        ]
    )

    lp_reference_relative_flat = lp_reference_relative_not_flat.reshape((105, 3))

    lp_reference_absolute_not_flat = lp_reference_relative_not_flat @ cell

    lp_reference_absolute_flat = lp_reference_relative_flat @ cell

    assert np.allclose(
        get_lattice_points(cell=cell, range=(1, 2, 3), flat=False, relative=True),
        lp_reference_relative_not_flat,
    )
    assert np.allclose(
        get_lattice_points(cell=cell, range=(1, 2, 3), flat=True, relative=True),
        lp_reference_relative_flat,
    )
    assert np.allclose(
        get_lattice_points(cell=cell, range=(1, 2, 3), flat=False, relative=False),
        lp_reference_absolute_not_flat,
    )
    assert np.allclose(
        get_lattice_points(cell=cell, range=(1, 2, 3), flat=True, relative=False),
        lp_reference_absolute_flat,
    )


def test_get_lattice_points_negative_range():
    lattice_points = get_lattice_points(cell=np.eye(3), range=(-1, 1, 1), flat=False)

    assert lattice_points.shape == (0, 3, 3, 3)


def test_get_lattice_points_zero_range():
    lattice_points = get_lattice_points(cell=np.eye(3), range=(0, 1, 1), flat=False)

    assert lattice_points.shape == (1, 3, 3, 3)

    assert np.allclose(
        lattice_points,
        np.array(
            [
                [
                    [
                        [0.0, -1.0, -1.0],
                        [0.0, -1.0, 0.0],
                        [0.0, -1.0, 1.0],
                    ],
                    [
                        [0.0, 0.0, -1.0],
                        [0.0, 0.0, 0.0],
                        [0.0, 0.0, 1.0],
                    ],
                    [
                        [0.0, 1.0, -1.0],
                        [0.0, 1.0, 0.0],
                        [0.0, 1.0, 1.0],
                    ],
                ]
            ]
        ),
    )


CELLS = [sc_get_example_cell(i) for i in SC_BRAVAIS_LATTICE_VARIATIONS]
N_EDGES = [
    12,
    36,
    24,
    12,
    28,
    36,
    12,
    28,
    36,
    24,
    36,
    18,
    18,
    36,
    24,
    18,
    36,
    28,
    28,
    24,
    36,
    36,
    28,
    36,
    28,
]

N_VERSTICES = [
    8,
    24,
    14,
    8,
    18,
    24,
    8,
    18,
    24,
    14,
    24,
    12,
    12,
    24,
    14,
    12,
    24,
    18,
    18,
    14,
    24,
    24,
    18,
    24,
    18,
]


@pytest.mark.parametrize(
    "cell, n_edge",
    list(zip(CELLS, N_EDGES)),
    ids=SC_BRAVAIS_LATTICE_VARIATIONS,
)
def test_edges(cell, n_edge):
    edges, vertices = _get_voronoi_cell(cell=get_reciprocal(cell))
    assert len(edges) == n_edge


@pytest.mark.parametrize(
    "cell, n_vertex",
    list(zip(CELLS, N_VERSTICES)),
    ids=SC_BRAVAIS_LATTICE_VARIATIONS,
)
def test_vertices(cell, n_vertex):
    edges, vertices = _get_voronoi_cell(cell=get_reciprocal(cell))
    assert len(vertices) == n_vertex
