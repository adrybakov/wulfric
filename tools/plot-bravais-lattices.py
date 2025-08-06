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
import os

import wulfric as wulf

ROOT_DIR = "."
OUTPUT_PATH = os.path.join(
    ROOT_DIR, "docs", "source", "user-guide", "conventions", "bravais-lattices"
)


def plot():
    wtps = {
        "CUB": [["brillouin-kpath"], ["primitive", "wigner-seitz", "lattice"]],
        "FCC": [
            ["brillouin-kpath"],
            ["primitive", "conventional", "wigner-seitz", "lattice"],
        ],
        "BCC": [
            ["brillouin-kpath"],
            ["primitive", "conventional", "wigner-seitz", "lattice"],
        ],
        "TET": [["brillouin-kpath"], ["primitive", "wigner-seitz", "lattice"]],
        "BCT1": [
            ["brillouin-kpath"],
            ["primitive", "conventional", "wigner-seitz", "lattice"],
        ],
        "BCT2": [
            ["brillouin-kpath"],
            ["primitive", "conventional", "wigner-seitz", "lattice"],
        ],
        "ORC": [["brillouin-kpath"], ["primitive", "wigner-seitz", "lattice"]],
        "ORCF1": [
            ["brillouin-kpath"],
            ["primitive", "conventional", "wigner-seitz", "lattice"],
        ],
        "ORCF2": [
            ["brillouin-kpath"],
            ["primitive", "conventional", "wigner-seitz", "lattice"],
        ],
        "ORCF3": [
            ["brillouin-kpath"],
            ["primitive", "conventional", "wigner-seitz", "lattice"],
        ],
        "ORCI": [
            ["brillouin-kpath"],
            ["primitive", "conventional", "wigner-seitz", "lattice"],
        ],
        "ORCC": [
            ["brillouin-kpath"],
            ["primitive", "conventional", "wigner-seitz", "lattice"],
        ],
        "HEX": [["brillouin-kpath"], ["primitive", "wigner-seitz", "lattice"]],
        "RHL1": [["brillouin-kpath"], ["primitive", "wigner-seitz", "lattice"]],
        "RHL2": [["brillouin-kpath"], ["primitive", "wigner-seitz", "lattice"]],
        "MCL": [["brillouin-kpath"], ["primitive", "wigner-seitz", "lattice"]],
        "MCLC1": [
            ["brillouin-kpath"],
            ["primitive", "conventional", "wigner-seitz", "lattice"],
        ],
        "MCLC2": [
            ["brillouin-kpath"],
            ["primitive", "conventional", "wigner-seitz", "lattice"],
        ],
        "MCLC3": [
            ["brillouin-kpath"],
            ["primitive", "conventional", "wigner-seitz", "lattice"],
        ],
        "MCLC4": [
            ["brillouin-kpath"],
            ["primitive", "conventional", "wigner-seitz", "lattice"],
        ],
        "MCLC5": [
            ["brillouin-kpath"],
            ["primitive", "conventional", "wigner-seitz", "lattice"],
        ],
        "TRI1a": [["brillouin-kpath"], ["primitive", "wigner-seitz", "lattice"]],
        "TRI2a": [["brillouin-kpath"], ["primitive", "wigner-seitz", "lattice"]],
        "TRI1b": [["brillouin-kpath"], ["primitive", "wigner-seitz", "lattice"]],
        "TRI2b": [["brillouin-kpath"], ["primitive", "wigner-seitz", "lattice"]],
    }
    names = {
        "CUB": ["reciprocal", "real"],
        "FCC": ["reciprocal", "real"],
        "BCC": ["reciprocal", "real"],
        "TET": ["reciprocal", "real"],
        "BCT1": ["reciprocal", "real"],
        "BCT2": ["reciprocal", "real"],
        "ORC": ["reciprocal", "real"],
        "ORCF1": ["reciprocal", "real"],
        "ORCF2": ["reciprocal", "real"],
        "ORCF3": ["reciprocal", "real"],
        "ORCI": ["reciprocal", "real"],
        "ORCC": ["reciprocal", "real"],
        "HEX": ["reciprocal", "real"],
        "RHL1": ["reciprocal", "real"],
        "RHL2": ["reciprocal", "real"],
        "MCL": ["reciprocal", "real"],
        "MCLC1": ["reciprocal", "real"],
        "MCLC2": ["reciprocal", "real"],
        "MCLC3": ["reciprocal", "real"],
        "MCLC4": ["reciprocal", "real"],
        "MCLC5": ["reciprocal", "real"],
        "TRI1a": ["reciprocal", "real"],
        "TRI2a": ["reciprocal", "real"],
        "TRI1b": ["reciprocal", "real"],
        "TRI2b": ["reciprocal", "real"],
    }

    for i, name in enumerate(names):
        print(f"Start to plot {name} ", end="")
        output_subname = (name.translate(str.maketrans("", "", "12345ab"))).lower()
        cell = wulf.cell.get_cell_example(name)
        for j, wtp in enumerate(wtps[name]):
            py_file = open(
                os.path.join(
                    OUTPUT_PATH, output_subname, f"{name.lower()}_{names[name][j]}.py"
                ),
                "w",
                encoding="utf-8",
            )
            py_file.write(
                "\n".join(
                    [
                        "import wulfric as wulf\n",
                        f'cell = wulf.cell.get_cell_example("{name}")',
                        "backend = wulf.visualization.PlotlyBackend()\n",
                    ]
                )
            )
            backend = wulf.visualization.PlotlyBackend()
            for data in wtp:
                print(data, end=" ", flush=True)
                if len(wtp) == 1:
                    backend.plot(cell, kind=data)
                    py_file.write(f'backend.plot(cell, kind="{data}")\n')
                else:
                    if data == "conventional":
                        backend.plot(cell, kind=data, label=data, color="blue")
                        py_file.write(
                            f'backend.plot(cell, kind="{data}", label="{data}", color="blue")\n'
                        )
                    elif data == "wigner-seitz":
                        backend.plot(cell, kind=data, label=data, color="green")
                        py_file.write(
                            f'backend.plot(cell, kind="{data}", label="{data}", color="green")\n'
                        )
                    elif data == "primitive":
                        backend.plot(cell, kind=data, label=data, color="black")
                        py_file.write(
                            f'backend.plot(cell, kind="{data}", label="{data}", color="black")\n'
                        )
                    elif data == "lattice":
                        backend.plot(cell, kind=data, label=data, repetitions=(1, 1, 1))
                        py_file.write(
                            f'backend.plot(cell, kind="{data}", label="{data}", repetitions=(1, 1, 1))\n'
                        )
                    else:
                        backend.plot(cell, kind=data, label=data)
                        py_file.write(
                            f'backend.plot(cell, kind="{data}", label="{data}")\n'
                        )

            backend.save(
                os.path.join(
                    OUTPUT_PATH, output_subname, f"{name.lower()}_{names[name][j]}.html"
                ),
                kwargs_write_html=dict(full_html=False, include_plotlyjs=False),
                # kwargs_update_layout=dict(
                #     width=600,
                #     height=600,
                # ),
                axes_visible=False,
            )

            py_file.write(
                "# Save an image:\n"
                + f'backend.save("{name.lower()}_{names[name][j]}.png")\n'
            )
            py_file.write("# Interactive plot:\n" + "backend.show()\n")
            py_file.close()
            del backend
        print(" done")


if __name__ == "__main__":
    plot()
