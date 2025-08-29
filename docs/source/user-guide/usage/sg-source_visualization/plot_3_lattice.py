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
"""
**************
Lattice points
**************

This page explains how to display lattice points associated with the given ``cell``.

We use FCC cell as an example.
"""

import wulfric

cell = wulfric.cell.SC_FCC(a=3)


# %%
# Wulfric assumes that ``cell`` contains one lattice point.

pe = wulfric.PlotlyEngine(_sphinx_gallery_fix=True)

pe.plot_cell(cell=cell, legend_label="Original cell", color="green")
pe.plot_lattice(cell=cell, range=(4, 4, 4), legend_label="Associated lattice")

pe.show()


# sphinx_gallery_thumbnail_path = 'img/gallery-thumbnails/visualization/lattice.png'
