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
*****************
Wigner-Seitz cell
*****************

This page explains how to plot Wigner-Seitz cell of the direct lattice and Brillouin zone.

We use FCC cell as an example.
"""

import wulfric

cell = wulfric.cell.SC_FCC(a=3)


# %%
# When wulfric plots |Wigner-Seitz|_ cell for any given ``cell``, it assumes that ``cell``
# contains exactly one lattice point.

pe = wulfric.PlotlyEngine(_sphinx_gallery_fix=True)

pe.plot_cell(cell=cell, legend_label="Original cell")
pe.plot_wigner_seitz_cell(
    cell=cell, plot_vectors=False, color="green", legend_label="Wigner-Seitz cell"
)

pe.show()

# %%
# Brillouin zone
# ==============
# Brillouin zone is simply a |Wigner-Seitz|_ cell of the reciprocal ``cell``.
# Therefore, Brillouin zone can be plotted in two equivalent ways.

rcell = wulfric.cell.get_reciprocal(cell=cell)

pe = wulfric.PlotlyEngine(_sphinx_gallery_fix=True)

# Brillouin zone from direct cell
pe.plot_brillouin_zone(cell=cell, legend_label="Brillouin zone: method 1", color="red")
# Brillouin zone from reciprocal cell
pe.plot_wigner_seitz_cell(
    cell=rcell,
    legend_label="Brillouin zone: method 2",
    color="blue",
    shift=(-6, 0, 0),
    vector_label="b",
)

pe.show()

# %%
# Other Brillouin zones
# =====================
#
# By default wulfric plots first Brillouin zone. If you need to plot other ones, use
# ``shift``.

pe = wulfric.PlotlyEngine(_sphinx_gallery_fix=True)

pe.plot_brillouin_zone(cell=cell, legend_label="First Brillouin zone", color="green")

# Compute shift along the first reciprocal lattice vector in absolute coordinates
shift = (1, 0, 0) @ rcell
pe.plot_brillouin_zone(
    cell=cell,
    legend_label="Second Brillouin zone along +b1",
    color="red",
    shift=shift,
    plot_vectors=False,
)
pe.plot_brillouin_zone(
    cell=cell,
    legend_label="Second Brillouin zone along -b1",
    color="blue",
    shift=-shift,
    plot_vectors=False,
)
pe.show()


# sphinx_gallery_thumbnail_path = 'img/gallery-thumbnails/visualization_plot_wigner-seitz.png'
