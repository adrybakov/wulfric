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

    with open(index_file, "r") as f:
        break_next = False
        for line in f:
            lines.append(line)
            if "Example of wulfric's visualization" in line:
                break_next = True
            elif break_next:
                break

    lines = "".join(lines).split("\n")

    lines += [
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

    kp = wulfric.Kpoints.from_crystal(cell, atoms, convention="SC")
    pe = wulfric.PlotlyEngine(rows=2, cols=2)

    pe.plot_cell(
        cell,
        row=1,
        col=1,
        legend_label="Original cell and atoms",
        legend_group="Original cell and atoms",
    )
    pe.plot_atoms(cell, atoms, row=1, col=1, legend_group="Original cell and atoms")

    pe.plot_brillouin_zone(
        cell, color="red", row=1, col=2, legend_label="Brillouin zone"
    )
    pe.plot_kpath(kp=kp, row=1, col=2, legend_label="k-path and k-points")

    pe.plot_wigner_seitz_cell(
        cell, color="green", legend_label="Wigner-Seitz cell", row=2, col=1
    )

    pe.plot_lattice(
        cell,
        range=(2, 2, 2),
        row=2,
        col=2,
        legend_group="Lattice",
        color="blue",
    )
    pe.plot_cell(
        cell,
        row=2,
        col=2,
        legend_group="Lattice",
        color="blue",
        legend_label="Lattice",
    )

    pe.fig.update_layout(
        height=1000, legend=dict(yanchor="bottom", y=1.0, xanchor="center", x=0.5)
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
