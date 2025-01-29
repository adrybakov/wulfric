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

import pytest

from wulfric.cell._sc_examples import cell_example
from wulfric.cell._sc_standardize import get_standardized
from wulfric.cell._sc_variation import variation as get_variation
from wulfric.cell._voronoi import voronoi_cell
from wulfric.constants._sc_notation import (
    BRAVAIS_LATTICE_VARIATIONS as lattice_variations,
)


@pytest.mark.parametrize("name", lattice_variations, ids=lattice_variations)
def test_examples(name):
    cell = cell_example(name)


cells = [cell_example(i) for i in lattice_variations]
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
    "cell, variation",
    list(zip(cells, lattice_variations)),
    ids=lattice_variations,
)
def test_variants(cell, variation):
    cell = get_standardized(cell)
    assert get_variation(cell) == variation


@pytest.mark.parametrize(
    "cell, n_edge",
    list(zip(cells, n_edges)),
    ids=lattice_variations,
)
def test_edges(cell, n_edge):
    edges, vertices = voronoi_cell(cell=cell, reciprocal=True)
    assert len(edges) == n_edge


@pytest.mark.parametrize(
    "cell, n_vertex",
    list(zip(cells, n_vertices)),
    ids=lattice_variations,
)
def test_vertices(cell, n_vertex):
    edges, vertices = voronoi_cell(cell=cell, reciprocal=True)
    assert len(vertices) == n_vertex
