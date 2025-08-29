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
ORCF1
*****

Face-centred orthorhombic cell is defined by two parameters by three parameters :math:`a`, :math:`b`
and :math:`c` with :math:`a < b < c`.

ORCF lattice has variation ORCF1 if
:math:`\dfrac{1}{a^2} > \dfrac{1}{b^2} + \dfrac{1}{c^2}`.

Cell constructor
================

To get a primitive face-centered orthorhombic cell use :py:func:`wulfric.cell.SC_ORCF`.

:py:func:`wulfric.cell.get_example_cell` returns an example with :math:`a = 0.7\pi`,
:math:`b = 5\pi/4` and :math:`c = 5\pi/3`.
"""

import wulfric

cell = wulfric.cell.sc_get_example_cell("ORCF1")
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

assert variation == "ORCF1"

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

# %%
# Edge cases
# ==========
# If :math:`a = b \ne c` or :math:`a = c \ne b` or :math:`b = c \ne a`,
# then the lattice is
# :ref:`sphx_glr_user-guide_conventions_bravais-lattices_2_sc_plot_05_BCT1.py`
# or
# :ref:`sphx_glr_user-guide_conventions_bravais-lattices_2_sc_plot_06_BCT2.py`.
#
# If :math:`a = b = c`, then the lattice is
# :ref:`sphx_glr_user-guide_conventions_bravais-lattices_2_sc_plot_02_FCC.py`.

# sphinx_gallery_thumbnail_path = 'img/gallery-thumbnails/bl-sc/ORCF1.png'
