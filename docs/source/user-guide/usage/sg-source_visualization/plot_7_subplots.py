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
********
Subplots
********

This page explains how to make subplots.

"""

import wulfric
import numpy as np

cell = np.array(
    [
        [5.64, 0.00, 0.00],
        [0.00, 5.64, 0.00],
        [0.00, 0.00, 5.64],
    ]
)
atoms = {
    "names": ["Cl1", "Cl2", "Cl3", "Cl4", "Na1", "Na2", "Na3", "Na4"],
    "positions": np.array(
        [
            (0, 0, 0),
            (1 / 2, 1 / 2, 0),
            (1 / 2, 0, 1 / 2),
            (0, 1 / 2, 1 / 2),
            (1 / 2, 1 / 2, 1 / 2),
            (1 / 2, 0, 0),
            (0, 1 / 2, 0),
            (0, 0, 1 / 2),
        ]
    ),
}
spglib_data = wulfric.get_spglib_data(cell, atoms)

# %% For this example we will plot a figure with two subplots - original cell and atoms on
# one and brillouin zone and k-path on another.
#
# First difference from usual plot is at the moment of engine creation. One needs to
# specify the grid of the subplots

pe = wulfric.PlotlyEngine(_sphinx_gallery_fix=True, rows=1, cols=2)

# %%
# Second change is at the moment of plotting. Every ``plot_...`` function can take two
# optional arguments ``row`` and ``col``. They specify on which subplot to plot the data.
# Both start from ``1``. ``row=1, col=1`` is top left subplot.
#
# Plot original cell and atoms on the first row an first column

pe.plot_atoms(cell=cell, atoms=atoms, row=1, col=1, legend_label="original atoms")
pe.plot_cell(cell=cell, row=1, col=1, legend_label="original cell")

# %%
# Then plot brillouin zone, k-path and k-points on the first row and second column

kp = wulfric.Kpoints.from_crystal(
    cell, atoms, spglib_data=spglib_data, convention="HPKOT"
)
prim_cell, _ = wulfric.crystal.get_primitive(cell, atoms, spglib_data=spglib_data)

pe.plot_brillouin_zone(
    cell=prim_cell,
    color="red",
    legend_label="Brillouin zone of the primitive cell",
    row=1,
    col=2,
)
pe.plot_kpath(kp=kp, legend_label="K-path", row=1, col=2)
pe.plot_kpoints(kp=kp, legend_label="K-points", row=1, col=2)

pe.show()

# sphinx_gallery_thumbnail_path = 'img/gallery-thumbnails/visualization/subplots.png'
