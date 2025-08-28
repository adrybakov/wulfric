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

from wulfric.cell._voronoi import _get_voronoi_cell


def test_voronoi_get_lattice_points_range():
    cell = np.array(
        [
            [2.8480, 0.0000, 0.0000],
            [0.0000, 2.8480, 0.0000],
            [1.4240, 1.4240, 1.4240],
        ]
    )
    vertices, edges = _get_voronoi_cell(cell)
    assert len(edges) == 36
    assert len(vertices) == 24
