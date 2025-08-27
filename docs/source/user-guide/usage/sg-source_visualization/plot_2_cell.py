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
***************
Plotting a cell
***************

This page explains how to use :py:func:`wulfric.PlotlyEngine.plot_cell` on the simple
example of the cubic cell

We use FCC cell as an example.
"""

import wulfric

cell = wulfric.cell.SC_FCC(a=3)


# %%
# To display the cell with the default settings use

pe = wulfric.PlotlyEngine(_sphinx_gallery_fix=True)

pe.plot_cell(cell=cell)

pe.show()

# %%
# Legend and style
# ================

pe = wulfric.PlotlyEngine(_sphinx_gallery_fix=True)

pe.plot_cell(cell=cell, legend_label="Direct cubic cell", color="green")

pe.show()

# %%
# Hiding lattice vectors
# ======================

pe = wulfric.PlotlyEngine(_sphinx_gallery_fix=True)

pe.plot_cell(cell=cell, plot_vectors=False)

pe.show()

# %%
# Shifting origin point
# =====================
#
# By default lattice vectors are plotted from the :math:`(0, 0, 0)` of the global
# of the global reference frame. One can shift this reference point.

pe = wulfric.PlotlyEngine(_sphinx_gallery_fix=True)

# shift is given in the absolute units of the global reference frame
pe.plot_cell(cell=cell, shift=(1, -1, 0.5))

pe.show()

# %%
# Two cells
# =========
# One can plot any number of cells on one instance of :py:class:`wulfric.PlotlyEngine`.
# For example, one can plot direct and reciprocal cell together

pe = wulfric.PlotlyEngine(_sphinx_gallery_fix=True)

# Plot direct cell
pe.plot_cell(cell=cell, legend_label="Direct cell", color="blue")

# Get reciprocal cell
rcell = wulfric.cell.get_reciprocal(cell=cell)

# Plot reciprocal cell
pe.plot_cell(cell=rcell, legend_label="Reciprocal cell", color="red")

pe.show()

# sphinx_gallery_thumbnail_path = 'img/gallery-thumbnails/visualization_plot_cell.png'
