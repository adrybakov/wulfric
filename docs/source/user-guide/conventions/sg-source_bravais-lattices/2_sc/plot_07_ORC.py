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
r"""
ORC
***

Orthorhombic cell is defined by two parameters by three parameters :math:`a`, :math:`b`
and :math:`c` with :math:`a < b < c`.

Cell constructor
================

To get a primitive orthorhombic cell use :py:func:`wulfric.cell.SC_ORC`.

:py:func:`wulfric.cell.get_example_cell` returns an example with :math:`a = \pi` and
:math:`c = 1.5\pi` and :math:`c = 2\pi`.
"""

import wulfric

cell = wulfric.cell.sc_get_example_cell("ORC")
atoms = dict(positions=[[0, 0, 0]], spglib_types=[1])

# To avoid multiple calls to spglib one can do it once and then pass spglib_data
# to the functions where it is needed
spglib_data = wulfric.get_spglib_data(cell=cell, atoms=atoms)

kp = wulfric.Kpoints.from_crystal(cell=cell, atoms=atoms, convention="SC")

conv_cell, conv_atoms = wulfric.crystal.get_conventional(
    cell=cell, atoms=atoms, convention="SC", spglib_data=spglib_data
)

prim_cell, prim_atoms = wulfric.crystal.get_primitive(
    cell=cell, atoms=atoms, convention="SC", spglib_data=spglib_data
)

# %%
# K-path
# ======

print(kp.path_string)

# %%
# High-symmetry points
# ====================

print(kp.hs_table(decimals=4))

# %%
# Brillouin zone and default k-path
# =================================

pe = wulfric.PlotlyEngine(_sphinx_gallery_fix=True)

pe.plot_brillouin_zone(cell=cell, color="red")
pe.plot_kpath(kp=kp)

pe.show(axes_visible=False)


# %%
# Primitive and Wigner-Seitz cells
# ================================
#
# .. hint
#     Click on the legend to hide some of the cells

pe = wulfric.PlotlyEngine(_sphinx_gallery_fix=True)

pe.plot_cell(cell=prim_cell, legend_label="Primitive cell", color="black")
pe.plot_cell(cell=conv_cell, legend_label="Conventional cell", color="blue")
pe.plot_wigner_seitz_cell(
    cell=prim_cell, legend_label="Wigner-Seitz cell", color="green"
)

pe.show(axes_visible=False)

# %%
# Edge cases
# ==========
#
# If :math:`a = b \ne c` or :math:`a = c \ne b` or :math:`b = c \ne a`,
# then the lattice is
# :ref:`sphx_glr_user-guide_conventions_bravais-lattices_2_sc_plot_04_TET.py`.
#
# If :math:`a = b = c`, then the lattice is
# :ref:`sphx_glr_user-guide_conventions_bravais-lattices_2_sc_plot_01_CUB.py`.

# sphinx_gallery_thumbnail_path = 'img/gallery-thumbnails/bl-sc/ORC.png'
