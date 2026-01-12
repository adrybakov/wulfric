# ================================== LICENSE ===================================
# Wulfric - Cell, Atoms, K-path, visualization.
# Copyright (C) 2023-2026 Andrey Rybakov
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
*******************
K-path and k-points
*******************

This page explains how to plot a set of atoms.

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


# %%
# Best way to interact with high-symmetry points and k-path is trough the
# :py:class:`wulfric.Kpoints`. First, we create one

kp = wulfric.Kpoints.from_crystal(
    cell, atoms, spglib_data=spglib_data, convention="HPKOT"
)

# %%
# Now one can check the recommended k-path and pre-defined high-symmetry points

print(kp.path_string)

print(kp.hs_table())

# %%
# High-symmetry points are given by relative coordinates with respect to the reciprocal
# cell of the original cell. However, the points correspond to the Brillouin zone of the
# **primitive** cell, which may or may not be the one that have k-path and high symmetry
# points lying on its edges

prim_cell, _ = wulfric.crystal.get_primitive(cell, atoms, spglib_data=spglib_data)

pe = wulfric.PlotlyEngine(_sphinx_gallery_fix=True)

pe.plot_brillouin_zone(
    cell=prim_cell, color="red", legend_label="Brillouin zone of primitive cell"
)
pe.plot_kpath(kp=kp, legend_label="K-path")
pe.plot_kpoints(kp=kp, legend_label="K-points")


pe.plot_brillouin_zone(
    cell=cell, color="chocolate", legend_label="Brillouin zone of original cell"
)

pe.show()

# sphinx_gallery_thumbnail_path = 'img/gallery-thumbnails/visualization/kpath.png'
