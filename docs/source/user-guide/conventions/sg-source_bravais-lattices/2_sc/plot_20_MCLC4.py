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
MCLC4
*****

Base-centered monoclinic cell is defined by two parameters by four parameters :math:`a`,
:math:`b`, :math:`c` and :math:`\alpha` with :math:`b \le c`, :math:`\alpha < 90^{\circ}`.

MCLC lattice has variation MCLC4 if :math:`k_{\gamma} < 90^{\circ}` and
:math:`\dfrac{b\cos(\alpha)}{c} + \dfrac{b^2\sin(\alpha)^2}{a^2} = 1`.

Cell constructor
================

To get a primitive base-centered monoclinic cell use :py:func:`wulfric.cell.SC_MCLC`.

:py:func:`wulfric.cell.get_example_cell` returns an example with
:math:`a = 1.2\sin(65)\pi`, :math:`b = \pi`,
:math:`c = 36\cos(65)\pi/11` and :math:`\alpha = 65^{\circ}`
"""

import wulfric

cell = wulfric.cell.sc_get_example_cell("MCLC4")
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

variation = wulfric.crystal.sc_get_variation(
    cell=cell, atoms=atoms, spglib_data=spglib_data
)

assert variation == "MCLC4"

print(variation)

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

pe.plot_brillouin_zone(
    cell=prim_cell, color="red", legend_label="Brillouin zone of the primitive cell"
)
pe.plot_brillouin_zone(
    cell=cell, color="chocolate", legend_label="Brillouin zone of the original cell"
)
pe.plot_kpath(kp=kp)

pe.show(axes_visible=False)


# %%
# Cells of real space
# ===================
#
# .. hint
#     Click on the legend to hide some of the cells

pe = wulfric.PlotlyEngine(_sphinx_gallery_fix=True)

pe.plot_cell(cell=cell, legend_label="Original cell", color="black")
pe.plot_cell(cell=prim_cell, legend_label="Primitive cell", color="indigo")
pe.plot_cell(cell=conv_cell, legend_label="Conventional cell", color="blue")
pe.plot_wigner_seitz_cell(
    cell=prim_cell, legend_label="Wigner-Seitz cell", color="green"
)

pe.show(axes_visible=False)

# sphinx_gallery_thumbnail_path = 'img/gallery-thumbnails/bl-sc/MCLC4.png'
