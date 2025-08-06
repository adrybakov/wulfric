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

from wulfric.cell._basic_manipulation import get_reciprocal
from wulfric.cell._sc_examples import get_example_cell_SC
from wulfric.cell._voronoi import _get_voronoi_cell
from wulfric.constants._sc_notation import (
    BRAVAIS_LATTICE_VARIATIONS as lattice_variations,
)

cells = [get_example_cell_SC(i) for i in lattice_variations]
n_edges = [
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

n_vertices = [
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
    list(zip(cells, n_edges)),
    ids=lattice_variations,
)
def test_edges(cell, n_edge):
    edges, vertices = _get_voronoi_cell(cell=get_reciprocal(cell))
    assert len(edges) == n_edge


@pytest.mark.parametrize(
    "cell, n_vertex",
    list(zip(cells, n_vertices)),
    ids=lattice_variations,
)
def test_vertices(cell, n_vertex):
    edges, vertices = _get_voronoi_cell(cell=get_reciprocal(cell))
    assert len(vertices) == n_vertex
