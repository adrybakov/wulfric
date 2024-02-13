# WULFRIC - Crystal, Lattice, Atoms, K-path.
# Copyright (C) 2023-2024 Andrey Rybakov
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

import os

import matplotlib.pyplot as plt

ROOT_DIR = "."


def class_structure():
    fig, ax = plt.subplots(figsize=(10, 5))
    bbox = dict(
        boxstyle="round",
        ec=(64 / 255, 176 / 255, 166 / 255, 1),
        fc=(64 / 255, 176 / 255, 166 / 255, 0.5),
    )
    bbox_visual = dict(
        boxstyle="round",
        ec=(225 / 255, 190 / 255, 106 / 255, 1),
        fc=(225 / 255, 190 / 255, 106 / 255, 0.5),
    )
    text_style = dict(
        ha="center",
        va="center",
        bbox=bbox,
        size=25,
    )
    arrow_style = dict(
        angles="xy", scale_units="xy", scale=1, headlength=3, headaxislength=2.7
    )

    def legend(x, y, text, color):
        ax.quiver(x, y, 20, 0, color=color, **arrow_style)
        ax.text(x + 21, y, text, ha="left", va="center", fontsize=15)

    parent_color = "#EBAE29"
    used_in_color = "#728EFC"
    base_for_color = "#BD2A7B"
    ax.text(30, 15, "Lattice", **text_style)
    ax.text(30, 75, "Kpoints", **text_style)
    ax.text(90, 15, "Crystal", **text_style)
    ax.text(90, 75, "Atom", **text_style)
    ax.text(150, 25, "Cell$^*$", **text_style)
    ax.text(
        150,
        65,
        "[visual]\nPlotlyBackend\nMatplotlibBackend",
        ha="center",
        va="center",
        bbox=bbox_visual,
        size=15,
    )

    ax.quiver(48, 15, 24, 0, color=parent_color, **arrow_style)
    ax.quiver(90, 65, 0, -40, color=used_in_color, **arrow_style)
    ax.quiver(30, 25, 0, 40, color=base_for_color, **arrow_style)
    ax.set_xlim(0, 170)
    ax.set_ylim(-10, 87)
    ax.axis("off")
    legend(5, -5, "is a parent of", parent_color)
    legend(65, -5, "is used in", used_in_color)
    legend(125, -5, "is a base for", base_for_color)
    filename = os.path.join(ROOT_DIR, "docs", "source", "img", "package-scheme.png")
    plt.savefig(filename, dpi=600, bbox_inches="tight")
    print(f"File is save in {os.path.abspath(filename)}")


if __name__ == "__main__":
    class_structure()
