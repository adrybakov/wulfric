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


def template(
    lattice_type, variation, header, example_spec, footer=None, variation_condition=None
):
    if variation_condition is None:
        variation_string = ""
        variation_prog_test = ""
    else:
        variation_string = f"{lattice_type} lattice has variation {variation} when {variation_condition}."
        variation_prog_test = f"""\nvariation = wulfric.crystal.sc_get_variation(
    cell=cell, atoms=atoms, spglib_data=spglib_data
)

assert variation == "{variation}"

print(variation)"""
    if footer is None:
        footer = ""
    if example_spec is None:
        example_spec = ""
    else:
        example_spec = f":py:func:`wulfric.cell.sc_get_example` returns an example where\n{example_spec}."
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
{variation}
{"*" * len(variation)}

{header}

{variation_string}

Cell constructor
================

To get an example of the cell use :py:func:`wulfric.cell.SC_{lattice_type}`.

{example_spec}
"""

import wulfric

cell = wulfric.cell.sc_get_example("{variation}")
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
{variation_prog_test}

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

pe.plot_cell(cell=cell, legend_label="Original cell", color="Chocolate")
pe.plot_cell(cell=prim_cell, legend_label="Primitive cell", color="Black")
pe.plot_cell(cell=conv_cell, legend_label="Conventional cell", color="Blue")
pe.plot_wigner_seitz_cell(
    cell=prim_cell, legend_label="Wigner-Seitz cell", color="green"
)

pe.show(axes_visible=False)

{footer}
# sphinx_gallery_thumbnail_path = 'img/gallery-thumbnails/bl-sc/{variation}.png'
'''


ORDERED_VARIATIONS = [
    "CUB",
    "FCC",
    "BCC",
    "TET",
    "BCT1",
    "BCT2",
    "ORC",
    "ORCF1",
    "ORCF2",
    "ORCF3",
    "ORCI",
    "ORCC",
    "HEX",
    "RHL1",
    "RHL2",
    "MCL",
    "MCLC1",
    "MCLC2",
    "MCLC3",
    "MCLC4",
    "MCLC5",
    "TRI1a",
    "TRI2a",
    "TRI1b",
    "TRI2b",
]

LATTICE_TYPES = {
    "CUB": "CUB",
    "FCC": "FCC",
    "BCC": "BCC",
    "TET": "TET",
    "BCT1": "BCT",
    "BCT2": "BCT",
    "ORC": "ORC",
    "ORCF1": "ORCF",
    "ORCF2": "ORCF",
    "ORCF3": "ORCF",
    "ORCI": "ORCI",
    "ORCC": "ORCC",
    "HEX": "HEX",
    "RHL1": "RHL",
    "RHL2": "RHL",
    "MCL": "MCL",
    "MCLC1": "MCLC",
    "MCLC2": "MCLC",
    "MCLC3": "MCLC",
    "MCLC4": "MCLC",
    "MCLC5": "MCLC",
    "TRI1a": "TRI",
    "TRI2a": "TRI",
    "TRI1b": "TRI",
    "TRI2b": "TRI",
}

HEADERS = {
    "CUB": R"Cubic cell is defined by single parameter :math:`a`.",
    "FCC": R"Face-centered cubic cell is defined by single parameter :math:`a`.",
    "BCC": R"Body-centered cubic cell is defined by single parameter :math:`a`.",
    "TET": R"Tetragonal cell is defined by two parameters :math:`a` and :math:`c`.",
    "BCT1": R"Body-centered tetragonal cell is defined by two parameters :math:`a` and :math:`c`.",
    "BCT2": R"Body-centered tetragonal cell is defined by two parameters :math:`a` and :math:`c`.",
    "ORC": R"Orthorhombic cell is defined by three parameters :math:`a`, :math:`b` and :math:`c` with :math:`a < b < c`.",
    "ORCF1": R"Face-centred orthorhombic cell is defined by three parameters :math:`a`, :math:`b` and :math:`c` with :math:`a < b < c`.",
    "ORCF2": R"Face-centred orthorhombic cell is defined by three parameters :math:`a`, :math:`b` and :math:`c` with :math:`a < b < c`.",
    "ORCF3": R"Face-centred orthorhombic cell is defined by three parameters :math:`a`, :math:`b` and :math:`c` with :math:`a < b < c`.",
    "ORCI": R"Body-centered orthorhombic cell is defined by three parameters :math:`a`, :math:`b` and :math:`c` with :math:`a < b < c`.",
    "ORCC": R"Base-centered orthorhombic cell is defined by three parameters :math:`a`, :math:`b` and :math:`c` with :math:`a < b < c`.",
    "HEX": R"Hexagonal cell is defined by two parameters :math:`a` and :math:`c`.",
    "RHL1": R"Rhombohedral cell is defined by two parameters :math:`a` and :math:`\alpha`.",
    "RHL2": R"Rhombohedral cell is defined by two parameters :math:`a` and :math:`\alpha`.",
    "MCL": R"Monoclinic cell is defined by four parameters :math:`a`, :math:`b`, :math:`c` and :math:`\alpha` with :math:`b \le c`, :math:`\alpha < 90^{\circ}`.",
    "MCLC1": R"Base-centered monoclinic cell is defined by four parameters :math:`a`, :math:`b`, :math:`c` and :math:`\alpha` with :math:`b \le c`, :math:`\alpha < 90^{\circ}`.",
    "MCLC2": R"Base-centered monoclinic cell is defined by four parameters :math:`a`, :math:`b`, :math:`c` and :math:`\alpha` with :math:`b \le c`, :math:`\alpha < 90^{\circ}`.",
    "MCLC3": R"Base-centered monoclinic cell is defined by four parameters :math:`a`, :math:`b`, :math:`c` and :math:`\alpha` with :math:`b \le c`, :math:`\alpha < 90^{\circ}`.",
    "MCLC4": R"Base-centered monoclinic cell is defined by four parameters :math:`a`, :math:`b`, :math:`c` and :math:`\alpha` with :math:`b \le c`, :math:`\alpha < 90^{\circ}`.",
    "MCLC5": R"Base-centered monoclinic cell is defined by four parameters :math:`a`, :math:`b`, :math:`c` and :math:`\alpha` with :math:`b \le c`, :math:`\alpha < 90^{\circ}`.",
    "TRI1a": R"Triclinic cell is defined by six parameters :math:`a`, :math:`b`, :math:`c` and :math:`\alpha`, :math:`\beta`, :math:`\gamma`.",
    "TRI2a": R"Triclinic cell is defined by six parameters :math:`a`, :math:`b`, :math:`c` and :math:`\alpha`, :math:`\beta`, :math:`\gamma`.",
    "TRI1b": R"Triclinic cell is defined by six parameters :math:`a`, :math:`b`, :math:`c` and :math:`\alpha`, :math:`\beta`, :math:`\gamma`.",
    "TRI2b": R"Triclinic cell is defined by six parameters :math:`a`, :math:`b`, :math:`c` and :math:`\alpha`, :math:`\beta`, :math:`\gamma`.",
}

VARIATION_CONDITIONS = {
    "CUB": None,
    "FCC": None,
    "BCC": None,
    "TET": None,
    "BCT1": R":math:`c < a`",
    "BCT2": R":math:`c > a`",
    "ORC": None,
    "ORCF1": R":math:`\dfrac{1}{a^2} > \dfrac{1}{b^2} + \dfrac{1}{c^2}`",
    "ORCF2": R":math:`\dfrac{1}{a^2} < \dfrac{1}{b^2} + \dfrac{1}{c^2}`",
    "ORCF3": R":math:`\dfrac{1}{a^2} = \dfrac{1}{b^2} + \dfrac{1}{c^2}`",
    "ORCI": None,
    "ORCC": None,
    "HEX": None,
    "RHL1": R":math:`\alpha < 90^{\circ}`",
    "RHL2": R":math:`\alpha > 90^{\circ}`",
    "MCL": None,
    "MCLC1": R":math:`k_{\gamma} > 90^{\circ}`",
    "MCLC2": R":math:`k_{\gamma} = 90^{\circ}`",
    "MCLC3": R":math:`k_{\gamma} < 90^{\circ}` and :math:`\dfrac{b\cos(\alpha)}{c} + \dfrac{b^2\sin(\alpha)^2}{a^2} < 1`",
    "MCLC4": R":math:`k_{\gamma} < 90^{\circ}` and :math:`\dfrac{b\cos(\alpha)}{c} + \dfrac{b^2\sin(\alpha)^2}{a^2} = 1`",
    "MCLC5": R":math:`k_{\gamma} < 90^{\circ}` and :math:`\dfrac{b\cos(\alpha)}{c} + \dfrac{b^2\sin(\alpha)^2}{a^2} > 1`",
    "TRI1a": R":math:`k_{\alpha} > 90^{\circ}, k_{\beta} > 90^{\circ}, k_{\gamma} > 90^{\circ}` and :math:`k_{\gamma} = \min(k_{\alpha}, k_{\beta}, k_{\gamma})`",
    "TRI2a": R":math:`k_{\alpha} > 90^{\circ}, k_{\beta} > 90^{\circ}, k_{\gamma} = 90^{\circ}`",
    "TRI1b": R":math:`k_{\alpha} < 90^{\circ}, k_{\beta} < 90^{\circ}, k_{\gamma} < 90^{\circ}` and :math:`k_{\gamma} = \max(k_{\alpha}, k_{\beta}, k_{\gamma})`",
    "TRI2b": R":math:`k_{\alpha} < 90^{\circ}, k_{\beta} < 90^{\circ}, k_{\gamma} = 90^{\circ}`",
}

EXAMPLE_SPECS = {
    "CUB": R":math:`a = \pi`",
    "FCC": R":math:`a = \pi`",
    "BCC": R":math:`a = \pi`",
    "TET": R":math:`a = \pi` and :math:`c = 1.5\pi`",
    "BCT1": R":math:`a = 1.5\pi` and :math:`c = \pi`",
    "BCT2": R":math:`a = \pi` and :math:`c = 1.5\pi`",
    "ORC": R":math:`a = \pi` and :math:`c = 1.5\pi` and :math:`c = 2\pi`",
    "ORCF1": R":math:`a = 0.7\pi`, :math:`b = 5\pi/4` and :math:`c = 5\pi/3`",
    "ORCF2": R":math:`a = 1.2\pi`, :math:`b = 5\pi/4` and :math:`c = 5\pi/3`",
    "ORCF3": R":math:`a = \pi`, :math:`b = 5\pi/4` and :math:`c = 5\pi/3`",
    "ORCI": R":math:`a = \pi`, :math:`b  = 1.3\pi` and :math:`c = 1.7\pi`",
    "ORCC": R":math:`a = \pi`, :math:`b  = 1.3\pi` and :math:`c = 1.7\pi`",
    "HEX": R":math:`a = \pi` and :math:`c = 2\pi`",
    "RHL1": R":math:`a = \pi` and :math:`\alpha = 70^{\circ}`",
    "RHL2": R":math:`a = \pi` and :math:`\alpha = 110^{\circ}`",
    "MCL": R":math:`a = \pi`, :math:`b = 1.3 \pi` :math:`c = 1.6 \pi` and :math:`\alpha = 75^{\circ}`",
    "MCLC1": R":math:`a = \pi`, :math:`b = 1.4\cdot\pi`, :math:`c = 1.7\cdot\pi` and :math:`\alpha = 80^{\circ}`",
    "MCLC2": R":math:`a = 1.4\cdot\pi\cdot\sin(75^{\circ})`, :math:`b = 1.4\cdot\pi`, :math:`c = 1.7\cdot\pi` and :math:`\alpha=75^{\circ}`",
    "MCLC3": R":math:`a = 1.1\cdot\sin(78)\cdot\pi`, :math:`b = \pi`, :math:`c = 1.8\cdot 121\cdot\cos(65)\cdot\pi/21` and :math:`\alpha = 78^{\circ}`",
    "MCLC4": R":math:`a = 1.2\sin(65)\pi`, :math:`b = \pi`, :math:`c = 36\cos(65)\pi/11` and :math:`\alpha = 65^{\circ}`",
    "MCLC5": R":math:`a = 1.4\cdot\sin(53)\cdot\pi`, :math:`b = \pi`, :math:`c = 0.9\cdot 11\cdot\cos(53)\cdot\pi/6` and :math:`\alpha = 53^{\circ}`",
    "TRI1a": None,
    "TRI2a": None,
    "TRI1b": None,
    "TRI2b": None,
}

FOOTERS = {
    "CUB": None,
    "FCC": None,
    "BCC": None,
    "TET": R"""# %%
# Edge cases
# ==========
#
# If :math:`a = c`, then the lattice is
# :ref:`sphx_glr_user-guide_conventions_bravais-lattices_2_sc_plot_01_CUB.py`.
""",
    "BCT1": R"""# %%
# Edge cases
# ==========
#
# If :math:`a = c`, then the lattice is
# :ref:`sphx_glr_user-guide_conventions_bravais-lattices_2_sc_plot_01_CUB.py`.
""",
    "BCT2": R"""# %%
# Edge cases
# ==========
#
# If :math:`a = c`, then the lattice is
# :ref:`sphx_glr_user-guide_conventions_bravais-lattices_2_sc_plot_01_CUB.py`.
""",
    "ORC": R"""# %%
# Edge cases
# ==========
#
# If :math:`a = b \ne c` or :math:`a = c \ne b` or :math:`b = c \ne a`,
# then the lattice is
# :ref:`sphx_glr_user-guide_conventions_bravais-lattices_2_sc_plot_04_TET.py`.
#
# If :math:`a = b = c`, then the lattice is
# :ref:`sphx_glr_user-guide_conventions_bravais-lattices_2_sc_plot_01_CUB.py`.
""",
    "ORCF1": R"""# %%
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
""",
    "ORCF2": R"""# %%
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
""",
    "ORCF3": R"""# %%
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
""",
    "ORCI": R"""# %%
# Edge cases
# ==========
# If :math:`a = b \ne c` or :math:`a = c \ne b` or :math:`b = c \ne a`,
# then the lattice is
# :ref:`sphx_glr_user-guide_conventions_bravais-lattices_2_sc_plot_05_BCT1.py`
# or
# :ref:`sphx_glr_user-guide_conventions_bravais-lattices_2_sc_plot_06_BCT2.py`.
#
# If :math:`a = b = c`, then the lattice is
# :ref:`sphx_glr_user-guide_conventions_bravais-lattices_2_sc_plot_03_BCC.py`.
""",
    "ORCC": R"""# %%
# Edge cases
# ==========
# If :math:`a = b`, then the lattice is
# :ref:`sphx_glr_user-guide_conventions_bravais-lattices_2_sc_plot_04_TET.py`.
#
# If :math:`a = b = \sqrt{2} c`, then the lattice is
# :ref:`sphx_glr_user-guide_conventions_bravais-lattices_2_sc_plot_01_CUB.py`.
""",
    "HEX": None,
    "RHL1": R"""# %%
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
""",
    "RHL2": R"""# %%
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
""",
    "MCL": R"""# %%
# If (:math:`\alpha = 60^{\circ}` or :math:`\alpha = 120^{\circ}`) and :math:`b = c`,
# then the lattice is
# :ref:`sphx_glr_user-guide_conventions_bravais-lattices_2_sc_plot_13_HEX.py`.
#
# If (:math:`\alpha = 30^{\circ}` or :math:`\alpha = 150^{\circ}`
# or :math:`\alpha = 45^{\circ}` or :math:`\alpha = 145^{\circ}`) and :math:`b = c`,
# then the lattice is
# :ref:`sphx_glr_user-guide_conventions_bravais-lattices_2_sc_plot_12_ORCC.py`.
#
# If (:math:`\alpha = 60^{\circ}` or :math:`\alpha = 120^{\circ}`) and :math:`a \ne b = c/2`,
# then the lattice is
# :ref:`sphx_glr_user-guide_conventions_bravais-lattices_2_sc_plot_07_ORC.py`.
#
# If :math:`a \ne b \ne c` and :math:`\alpha = 90^{\circ}`, then the lattice is
# :ref:`sphx_glr_user-guide_conventions_bravais-lattices_2_sc_plot_07_ORC.py`.
#
# If (:math:`\alpha = 60^{\circ}` or :math:`\alpha = 120^{\circ}`) and :math:`a = b = c/2`,
# then the lattice is
# :ref:`sphx_glr_user-guide_conventions_bravais-lattices_2_sc_plot_04_TET.py`.
#
# If (:math:`a = b \ne c` or :math:`a = c \ne b` or :math:`b = c \ne a`) and
# :math:`\alpha = 90^{\circ}`, then the lattice is
# :ref:`sphx_glr_user-guide_conventions_bravais-lattices_2_sc_plot_04_TET.py`.
#
# If :math:`a = b = c` and :math:`\alpha = 90^{\circ}`, then the lattice is
# :ref:`sphx_glr_user-guide_conventions_bravais-lattices_2_sc_plot_01_CUB.py`.
""",
    "MCLC1": None,
    "MCLC2": None,
    "MCLC3": None,
    "MCLC4": None,
    "MCLC5": None,
    "TRI1a": None,
    "TRI2a": None,
    "TRI1b": None,
    "TRI2b": None,
}


ROOT_DIR = "."

if __name__ == "__main__":
    root_path = os.path.join(
        ROOT_DIR,
        "docs",
        "source",
        "user-guide",
        "conventions",
        "sg-source_bravais-lattices",
        "2_sc",
    )
    for v_i, variation in enumerate(ORDERED_VARIATIONS):
        filename = os.path.join(root_path, f"plot_{v_i + 1:0>2}_{variation}.py")

        with open(filename, "w") as f:
            f.write(
                template(
                    lattice_type=LATTICE_TYPES[variation],
                    variation=variation,
                    header=HEADERS[variation],
                    example_spec=EXAMPLE_SPECS[variation],
                    footer=FOOTERS[variation],
                    variation_condition=VARIATION_CONDITIONS[variation],
                )
            )
