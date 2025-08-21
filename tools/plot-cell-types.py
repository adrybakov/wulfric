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

    ax.text(50, 75, '"The"\ncell', fontsize=30, va="center", ha="center")

    ax.text(25, 25, "Conventional\ncell", fontsize=30, va="center", ha="center")
    ax.text(75, 25, "Primitive\ncell", fontsize=30, va="center", ha="center")

    arrow_style = dict(
        angles="xy",
        scale_units="xy",
        scale=1,
        headlength=3,
        headaxislength=2.7,
        color="#728EFC",
    )
    ax.quiver(40, 60, -15, -20, **arrow_style)
    ax.quiver(60, 60, 15, -20, **arrow_style)

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    filename = os.path.join(ROOT_DIR, "docs", "source", "img", "cell-types.png")
    plt.savefig(filename, dpi=600, bbox_inches="tight")
    plt.close()
    print(f"File is saved in {os.path.abspath(filename)}")


if __name__ == "__main__":
    cells()
