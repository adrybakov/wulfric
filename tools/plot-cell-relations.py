# Wulfric - Crystal, Lattice, Atoms, K-path.
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

import os

import matplotlib.pyplot as plt

ROOT_DIR = "."


def quiver(ax, pos, width, height):

    ax.quiver(
        pos[0],
        pos[1],
        width / 2,
        height / 2,
        angles="xy",
        scale_units="xy",
        scale=1,
        headlength=3,
        headaxislength=2.7,
        color="#728EFC",
    )
    ax.quiver(
        pos[0],
        pos[1],
        -width / 2,
        -height / 2,
        angles="xy",
        scale_units="xy",
        scale=1,
        headlength=3,
        headaxislength=2.7,
        color="#728EFC",
    )


def cells():
    fig, ax = plt.subplots(figsize=(10, 6))
    bbox = dict(
        boxstyle="round",
        ec=(64 / 255, 176 / 255, 166 / 255, 1),
        fc=(64 / 255, 176 / 255, 166 / 255, 0.5),
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

    ax.text(
        40,
        95,
        "Primitive cell\n" R"$\boldsymbol{A}$",
        **text_style,
    )
    ax.text(
        40,
        40,
        "Reciprocal cell\n" R"$\boldsymbol{B}$",
        **text_style,
    )
    ax.text(
        140,
        95,
        "Standardized\nprimitive cell\n" R"$\boldsymbol{A^s}$",
        **text_style,
    )
    ax.text(
        140,
        30,
        "Standardized\nconventional cell\n" R"$\boldsymbol{A^{cs}}$",
        **text_style,
    )

    quiver(ax, (89, 95), 26, 0)
    quiver(ax, (140, 63), 0, 20)
    ax.text(143, 63, R"$\boldsymbol{C}$", ha="left", va="center", size=25)
    ax.text(89, 98, R"$\boldsymbol{S}$", ha="center", va="bottom", size=25)

    ax.quiver(
        40,
        76,
        0,
        -16,
        angles="xy",
        scale_units="xy",
        scale=1,
        headlength=3,
        headaxislength=2.7,
        color="#BD2A7B",
    )

    ax.set_xlim(0, 200)
    ax.set_ylim(0, 120)
    ax.axis("off")

    filename = os.path.join(ROOT_DIR, "docs", "source", "img", "cell-relations.png")
    plt.savefig(filename, dpi=600, bbox_inches="tight")
    print(f"File is saved in {os.path.abspath(filename)}")


if __name__ == "__main__":
    cells()
