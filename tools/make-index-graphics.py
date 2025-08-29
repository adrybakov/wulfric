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
import wulfric
import numpy as np
import os

ROOT_DIR = "."


def main():
    index_file = os.path.join(ROOT_DIR, "docs", "source", "index.rst")
    lines = []
    target_line = "Example of some of the wulfric's capabilities"

    with open(index_file, "r") as f:
        break_next = False
        for line in f:
            lines.append(line)
            if target_line in line:
                break_next = True
            elif break_next:
                break

    lines = "".join(lines)
    if target_line not in lines:
        raise ValueError(f'Target line "{target_line}" not in "docs/source/index.rst.')

    lines = lines.split("\n")

    lines += [
        "",
        ".. hint::",
        "    Click on the legend to hide the data",
        "",
        """.. raw:: html""",
        "",
        """    <div class="output_subarea output_html rendered_html output_result">""",
        """        <div>""",
        """            <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-AMS-MML_SVG"></script>""",
        """            <script type="text/javascript">if (window.MathJax && window.MathJax.Hub && window.MathJax.Hub.Config) {window.MathJax.Hub.Config({SVG: {font: "STIX-Web"}});}</script>""",
        """            <script type="text/javascript">window.PlotlyConfig = {MathJaxConfig: 'local'};</script>""",
        """            <script charset="utf-8" src="https://cdn.plot.ly/plotly-3.0.1.min.js" integrity="sha256-oy6Be7Eh6eiQFs5M7oXuPxxm9qbJXEtTpfSI93dW16Q=" crossorigin="anonymous"></script>""",
    ]

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

    prim_cell_sc, prim_atoms_sc = wulfric.crystal.get_primitive(
        cell, atoms, spglib_data=spglib_data, convention="SC"
    )
    prim_cell_hpkot, prim_atoms_hpkot = wulfric.crystal.get_primitive(
        cell, atoms, spglib_data=spglib_data, convention="HPKOT"
    )

    conv_cell_sc, conv_atoms_sc = wulfric.crystal.get_conventional(
        cell, atoms, spglib_data=spglib_data, convention="SC"
    )
    conv_cell_hpkot, conv_atoms_hpkot = wulfric.crystal.get_conventional(
        cell, atoms, spglib_data=spglib_data, convention="HPKOT"
    )

    kp_sc = wulfric.Kpoints.from_crystal(
        cell, atoms, convention="SC", spglib_data=spglib_data
    )

    kp_hpkot = wulfric.Kpoints.from_crystal(
        cell, atoms, convention="HPKOT", spglib_data=spglib_data
    )

    pe = wulfric.PlotlyEngine(rows=3, cols=2)

    # Original cell and atoms
    pe.plot_cell(
        cell,
        row=1,
        col=1,
        legend_label="Original cell and atoms",
        legend_group="Original cell and atoms",
    )
    pe.plot_atoms(cell, atoms, row=1, col=1, legend_group="Original cell and atoms")

    # Wigner Seitz cell
    pe.plot_wigner_seitz_cell(
        prim_cell_hpkot,
        color="green",
        legend_label="Wigner-Seitz cell",
        legend_group="WS",
        row=1,
        col=2,
    )

    # Two conventional cells
    pe.plot_cell(
        conv_cell_sc,
        color="darkslategrey",
        legend_label="Conventional cell (SC)",
        legend_group="conv_cell_sc",
        row=2,
        col=1,
    )
    pe.plot_cell(
        conv_cell_hpkot,
        color="black",
        legend_label="Conventional cell (HPKOT)",
        legend_group="conv_cell_hpkot",
        row=2,
        col=2,
    )

    # Two primitive cells
    pe.plot_cell(
        prim_cell_sc,
        color="darkseagreen",
        legend_label="Primitive cell and atoms (SC)",
        legend_group="prim_cell_sc",
        row=2,
        col=1,
    )
    pe.plot_atoms(
        prim_cell_sc, prim_atoms_sc, row=2, col=1, legend_group="prim_cell_sc"
    )
    pe.plot_cell(
        prim_cell_hpkot,
        color="blue",
        legend_label="Primitive cell and atoms (HPKOT)",
        legend_group="prim_cell_hpkot",
        row=2,
        col=2,
    )
    pe.plot_atoms(
        prim_cell_hpkot, prim_atoms_hpkot, row=2, col=2, legend_group="prim_cell_hpkot"
    )

    # Two Brillouine zones
    pe.plot_brillouin_zone(
        prim_cell_sc,
        color="chocolate",
        row=3,
        col=1,
        legend_label="Brillouin zone of primitive cell (SC)",
        legend_group="BZ SC",
    )
    pe.plot_brillouin_zone(
        prim_cell_hpkot,
        color="red",
        row=3,
        col=2,
        legend_label="Brillouin zone of primitive cell (HPKOT)",
        legend_group="BZ HPKOT",
    )

    # Two kpaths
    pe.plot_kpath(
        kp=kp_sc,
        row=3,
        col=1,
        color="darkslategrey",
        legend_label="k-path and k-points (SC)",
        legend_group="KP SC",
    )
    pe.plot_kpoints(kp=kp_sc, row=3, col=1, color="darkslategrey", legend_group="KP SC")
    pe.plot_kpath(
        kp=kp_hpkot,
        row=3,
        col=2,
        legend_label="k-path and k-points (HPKOT)",
        legend_group="KP HPKOT",
    )
    pe.plot_kpoints(kp=kp_hpkot, row=3, col=2, legend_group="KP HPKOT")

    # Plot lattice
    pe.plot_lattice(
        prim_cell_hpkot, range=(2, 2, 2), legend_label="Lattice points", row=1, col=2
    )

    # Plot complementary cells
    pe.plot_wigner_seitz_cell(
        prim_cell_sc,
        color="green",
        legend_group="WS",
        row=1,
        col=1,
        plot_vectors=False,
    )
    pe.plot_wigner_seitz_cell(
        prim_cell_sc,
        color="green",
        legend_group="WS",
        row=2,
        col=1,
        plot_vectors=False,
    )
    pe.plot_wigner_seitz_cell(
        prim_cell_hpkot,
        color="green",
        legend_group="WS",
        row=2,
        col=2,
        plot_vectors=False,
    )

    pe.plot_cell(
        cell,
        row=1,
        col=2,
        legend_group="Original cell and atoms",
    )

    # Save the figure
    pe.fig.update_layout(
        height=1500,
        legend=dict(
            yanchor="bottom",
            y=1.0,
            xanchor="center",
            x=0.5,
            orientation="h",
            entrywidthmode="fraction",
            entrywidth=0.4,
        ),
    )

    graph_text = pe.fig.to_html(full_html=False, include_plotlyjs=False)

    graph_text = graph_text.split("<div>")[1].split("</div>")

    graph_div = (graph_text[0] + "</div>").strip()
    graph_script = graph_text[1].strip()

    lines += [
        " " * 12 + graph_div,
        " " * 12 + graph_script,
        " " * 8 + "</div>",
        " " * 4 + "</div>",
        "",
    ]

    with open(index_file, "w") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
