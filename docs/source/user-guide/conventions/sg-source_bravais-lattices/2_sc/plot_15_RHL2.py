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
RHL2
****

Rhombohedral cell is defined by two parameters by two parameters :math:`a` and
:math:`\alpha`.

RHL lattice has variation RHL2 if :math:`\alpha > 90^{\circ}`.

Cell constructor
================

To get a primitive rhombohedral cell use :py:func:`wulfric.cell.SC_RHL`.

:py:func:`wulfric.cell.get_example_cell` returns an example with :math:`a = \pi` and
:math:`\alpha = 110^{\circ}`
"""

import wulfric

cell = wulfric.cell.sc_get_example_cell("RHL2")
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

assert variation == "RHL2"

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
pe.plot_kpoints(kp=kp, only_from_kpath=True)

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
# In rhombohedral lattice :math:`a = b = c` and :math:`\alpha = \beta = \gamma`,
# thus three edge cases exist:
#
# If :math:`\alpha = 60^{\circ}`, then the lattice is
# :ref:`sphx_glr_user-guide_conventions_bravais-lattices_2_sc_plot_02_FCC.py`.
#
# If :math:`\alpha \approx 109.47122063^{\circ}` (:math:`\cos(\alpha) = -1/3`),
# then the lattice is
# :ref:`sphx_glr_user-guide_conventions_bravais-lattices_2_sc_plot_03_BCC.py`.
#
# If :math:`\alpha = 90^{\circ}`, then the lattice is
# :ref:`sphx_glr_user-guide_conventions_bravais-lattices_2_sc_plot_01_CUB.py`.

# sphinx_gallery_thumbnail_path = 'img/gallery-thumbnails/bl-sc/RHL2.png'
