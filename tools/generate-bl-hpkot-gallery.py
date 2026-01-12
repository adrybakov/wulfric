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


import os


def template(bl_symbol):
    return f'''# ================================== LICENSE ===================================
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
{bl_symbol}
{"*" * len(bl_symbol)}

.. include:: ../../HPKOT-reference-memo.inc

Getting an example
==================

To get an example crystal use :py:func:`wulfric.crystal.hpkot_get_example`.
"""

import wulfric

# For every extended bravais lattice symbol two examples are defined:
# with and without inversion symmetry.
cell, atoms = wulfric.crystal.hpkot_get_example(
    extended_bl_symbol="{bl_symbol}", with_inversion=False
)

# To avoid multiple calls to spglib one can do it once and then pass spglib_data
# to the functions where it is needed
spglib_data = wulfric.get_spglib_data(cell=cell, atoms=atoms)

kp = wulfric.Kpoints.from_crystal(
    cell=cell, atoms=atoms, convention="HPKOT", with_time_reversal=True
)

kp_no_tr = wulfric.Kpoints.from_crystal(
    cell=cell, atoms=atoms, convention="HPKOT", with_time_reversal=False
)

conv_cell, conv_atoms = wulfric.crystal.get_conventional(
    cell=cell, atoms=atoms, convention="HPKOT", spglib_data=spglib_data
)

prim_cell, prim_atoms = wulfric.crystal.get_primitive(
    cell=cell, atoms=atoms, convention="HPKOT", spglib_data=spglib_data
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

pe.plot_brillouin_zone(
    cell=prim_cell, color="red", legend_label="Brillouin zone of the primitive cell"
)
pe.plot_brillouin_zone(
    cell=cell, color="chocolate", legend_label="Brillouin zone of the original cell"
)
pe.plot_kpath(kp=kp, legend_group="with TR", legend_label="With time-reversal")
pe.plot_kpoints(kp=kp, only_from_kpath=True, legend_group="with TR")

pe.plot_kpath(
    kp=kp_no_tr,
    color="#7D7D7D",
    legend_group="without TR",
    legend_label="Without time-reversal",
)
pe.plot_kpoints(
    kp=kp_no_tr, only_from_kpath=True, color="#7D7D7D", legend_group="without TR"
)

pe.show(axes_visible=False)


# %%
# Cells of real space
# ===================
#
# .. hint
#     Click on the legend to hide some of the cells

pe = wulfric.PlotlyEngine(_sphinx_gallery_fix=True)

pe.plot_cell(cell=cell, legend_label="Original cell", color="Chocolate")
pe.plot_cell(cell=prim_cell, legend_label="Primitive cell", color="Black")
pe.plot_cell(cell=conv_cell, legend_label="Conventional cell", color="Blue")
pe.plot_wigner_seitz_cell(
    cell=prim_cell, legend_label="Wigner-Seitz cell", color="green"
)

pe.show(axes_visible=False)

# sphinx_gallery_thumbnail_path = 'img/gallery-thumbnails/bl-hpkot/{bl_symbol}.png'
'''


ORDERED_SYMBOLS = [
    "cP1",
    "cP2",
    "cF1",
    "cF2",
    "cI1",
    "tP1",
    "tI1",
    "tI2",
    "oP1",
    "oF1",
    "oF2",
    "oF3",
    "oI1",
    "oI2",
    "oI3",
    "oC1",
    "oC2",
    "oA1",
    "oA2",
    "hP1",
    "hP2",
    "hR1",
    "hR2",
    "mP1",
    "mC1",
    "mC2",
    "mC3",
    "aP2",
    "aP3",
]


ROOT_DIR = "."

if __name__ == "__main__":
    root_path = os.path.join(
        ROOT_DIR,
        "docs",
        "source",
        "user-guide",
        "conventions",
        "sg-source_bravais-lattices",
        "1_hpkot",
    )
    for s_i, symbol in enumerate(ORDERED_SYMBOLS):
        filename = os.path.join(root_path, f"plot_{s_i + 1:0>2}_{symbol}.py")

        with open(filename, "w") as f:
            f.write(template(bl_symbol=symbol))
