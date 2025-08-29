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
Plotting atoms
**************

This page explains how to plot a set of atoms.

"""

import wulfric
import numpy as np

cell = np.array(
    [
        [0.000000, 4.744935, 0.000000],
        [3.553350, 0.000000, 0.000000],
        [0.000000, 0.000000, 8.760497],
    ]
)
atoms = {
    "names": ["Cr1", "Br1", "S1", "Cr2", "Br2", "S2"],
    "positions": np.array(
        [
            [0.000000, -0.500000, 0.882382],
            [0.000000, 0.000000, 0.677322],
            [-0.500000, -0.500000, 0.935321],
            [0.500000, 0.000000, 0.117618],
            [0.500000, 0.500000, 0.322678],
            [0.000000, 0.000000, 0.064679],
        ]
    ),
}


pe = wulfric.PlotlyEngine(_sphinx_gallery_fix=True)

pe.plot_atoms(cell=cell, atoms=atoms, scale=0.7)
pe.plot_cell(cell=cell)

pe.show()

# %%
# Atoms'labels are deduced based on ``atoms["names"]``.
#
# Atom's colors are deduced based on atom's species, but can be directly passed to the
# function as well.


atoms = dict(positions=atoms["positions"])

pe = wulfric.PlotlyEngine(_sphinx_gallery_fix=True)

pe.plot_atoms(cell=cell, atoms=atoms, scale=0.7)
pe.plot_cell(cell=cell)

pe.show()

# sphinx_gallery_thumbnail_path = 'img/gallery-thumbnails/visualization/atoms.png'
