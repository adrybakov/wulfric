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
from math import atan, pi

import matplotlib.pyplot as plt
import numpy as np

ROOT_DIR = "."


def bidirectional_arrow(
    ax, x, y, u, v, text_1=None, text_2=None, quiver_kwargs=None, text_kwargs=None
):
    if quiver_kwargs is None:
        quiver_kwargs = {}
    if text_kwargs is None:
        text_kwargs = {}

    center = np.array((x + u / 2, y + v / 2), dtype=float)

    if u != 0:
        normal = (-v / u, 1)
        angle = atan(v / u) / pi * 180
    else:
        normal = (1, -u / v)
        if v > 0:
            angle = 90
        else:
            angle = 270

    normal = np.array(normal, dtype=float)
    normal /= np.linalg.norm(normal)

    if angle <= 90:
        pass
    elif angle <= 180:
        angle = -(180 - angle)
    elif angle <= 270:
        angle -= 180
    else:
        angle = -(360 - angle)

    if text_1 is not None or text_2 is not None:
        ax.quiver(x + normal[0], y + normal[1], u, v, **quiver_kwargs)
        ax.quiver(x + u - normal[0], y + v - normal[1], -u, -v, **quiver_kwargs)
    else:
        ax.quiver(*center, u / 2, v / 2, **quiver_kwargs)
        ax.quiver(*center, -u / 2, -v / 2, **quiver_kwargs)

    ax.text(
        *(center + 3 * normal),
        text_1,
        **text_kwargs,
        rotation=angle,
        ha="center",
        va="center",
        rotation_mode="anchor",
    )
    ax.text(
        *(center - 3 * normal),
        text_2,
        **text_kwargs,
        rotation=angle,
        ha="center",
        va="center",
        rotation_mode="anchor",
    )


def main():
    fig, ax = plt.subplots(figsize=(7, 5))
    bbox = dict(
        boxstyle="round",
        ec=(64 / 255, 176 / 255, 166 / 255, 1),
        fc=(64 / 255, 176 / 255, 166 / 255, 0.5),
    )
    bbox_root = dict(
        boxstyle="round",
        ec=(225 / 255, 190 / 255, 106 / 255, 1),
        fc=(225 / 255, 190 / 255, 106 / 255, 0.5),
    )
    text_style = dict(bbox=bbox, size=15, va="center", ha="center")
    text_style_2 = dict(bbox=bbox_root, size=15, va="center", ha="center")
    arrow_style = dict(
        angles="xy", scale_units="xy", scale=1, headlength=3, headaxislength=2.7
    )

    parent_color = "#EBAE29"
    used_in_color = "#728EFC"
    base_for_color = "#BD2A7B"

    ax.text(
        35,
        25,
        "_spin_vector\n$(S_x, S_y, S_z)$",
        **text_style_2,
    )
    ax.text(
        30,
        45,
        "spin\n$S$",
        **text_style,
    )
    ax.text(
        15,
        5,
        "spin_direction\n$(S_x/S, S_y/S, S_z/S)$",
        **text_style,
    )
    ax.text(
        57,
        5,
        "spin_vector\n$(S_x, S_y, S_z)$",
        **text_style,
    )
    ax.text(
        57,
        45,
        "magmom\n$(m_x, m_y, m_z)$",
        **text_style,
    )
    ax.text(
        10,
        37,
        "spin_angles\n" R"$\theta, \varphi$",
        **text_style,
    )

    bidirectional_arrow(ax, 25, 25, -15, 7, quiver_kwargs=arrow_style)

    bidirectional_arrow(ax, 35, 30, -5, 10, quiver_kwargs=arrow_style)
    bidirectional_arrow(ax, 25, 20, -10, -10, quiver_kwargs=arrow_style)

    bidirectional_arrow(ax, 45, 20, 12, -10, quiver_kwargs=arrow_style)
    bidirectional_arrow(
        ax,
        45,
        30,
        10,
        8,
        text_1="g_factor",
        text_2="1/g_factor",
        quiver_kwargs=arrow_style,
        text_kwargs=dict(fontsize=15),
    )

    ax.set_xlim(0, 70)
    ax.set_ylim(0, 50)

    # ax.vlines([i for i in range(0, 71)], 0, 50, color="grey", lw=0.1)
    # ax.hlines([i for i in range(0, 51)], 0, 70, color="grey", lw=0.1)
    # ax.vlines([10 * i for i in range(0, 8)], 0, 50, ls="--", color="black", lw=0.5)
    # ax.hlines([10 * i for i in range(0, 5)], 0, 70, ls="--", color="black", lw=0.5)

    ax.axis("off")
    filename = os.path.join(
        ROOT_DIR, "docs", "source", "img", "atom-magnetic-properties.png"
    )
    plt.savefig(filename, dpi=600, bbox_inches="tight")
    print(f"File is saved in {os.path.abspath(filename)}")


if __name__ == "__main__":
    main()
