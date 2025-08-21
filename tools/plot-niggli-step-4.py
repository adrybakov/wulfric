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


def plot():
    s = 3
    space = 1
    margin = 1.5

    fx = (s + space) * 6 + margin + space
    fy = (s + space) * 3 + margin
    fig = plt.figure(figsize=(fx, fy))

    fig.text(
        margin / 2 / fx,
        (space + 0.5 * s) / fy,
        R"$\xi > 0$",
        fontsize=25,
        ha="left",
        va="center",
    )
    fig.text(
        margin / 2 / fx,
        (2 * space + 1.5 * s) / fy,
        R"$\xi = 0$",
        fontsize=25,
        ha="left",
        va="center",
    )
    fig.text(
        margin / 2 / fx,
        (3 * space + 2.5 * s) / fy,
        R"$\xi < 0$",
        fontsize=25,
        ha="left",
        va="center",
    )

    fig.text(
        (margin + 0.5 * space) / fx,
        (fy - margin / 2) / fy,
        R"Step 1 $\rightarrow$",
        fontsize=25,
        ha="center",
        va="center",
    )
    fig.text(
        (margin + 1.5 * space + 1 * s) / fx,
        (fy - margin / 2) / fy,
        R"$\rightarrow$ Step 2 $\rightarrow$",
        fontsize=25,
        ha="center",
        va="center",
    )
    fig.text(
        (margin + 2.5 * space + 2 * s) / fx,
        (fy - margin / 2) / fy,
        R"$\rightarrow$ Step 3 $\rightarrow$",
        fontsize=25,
        ha="center",
        va="center",
    )
    fig.text(
        (margin + 3.5 * space + 3 * s) / fx,
        (fy - margin / 2) / fy,
        R"$\rightarrow$ Step 4 $\rightarrow$",
        fontsize=25,
        ha="center",
        va="center",
    )
    fig.text(
        (margin + 4.5 * space + 4 * s) / fx,
        (fy - margin / 2) / fy,
        R"$\rightarrow$ Step 5 $\rightarrow$",
        fontsize=25,
        ha="center",
        va="center",
    )

    fig.text(
        (margin + 6 * space + 5.5 * s) / fx,
        (fy - margin / 2) / fy,
        "Acceptable\nvariants",
        fontsize=25,
        ha="center",
        va="center",
    )

    axs = []

    for i in range(3):
        axs.append([])
        for j in range(6):
            axs[-1].append(
                fig.add_axes(
                    (
                        (margin + space + j * (space + s)) / fx,
                        (fy - margin - s - i * (s + space)) / fy,
                        s / fx,
                        s / fy,
                    )
                )
            )

    for i in range(3):
        for j in range(6):
            axs[i][j].set_yticks(
                [5, 15, 25],
                [R"$\zeta < 0$", R"$\zeta = 0$", R"$\zeta > 0$"],
                fontsize=15,
            )
            axs[i][j].set_xticks(
                [5, 15, 25], [R"$\eta < 0$", R"$\eta = 0$", R"$\eta > 0$"], fontsize=15
            )

            axs[i][j].set_xlim(0, 30)
            axs[i][j].set_ylim(0, 30)

            axs[i][j].set_aspect(1)

            axs[i][j].vlines(
                [10, 20],
                0,
                1,
                transform=axs[i][j].get_xaxis_transform(),
                lw=1,
                color="black",
            )
            axs[i][j].hlines(
                [10, 20],
                0,
                1,
                transform=axs[i][j].get_yaxis_transform(),
                lw=1,
                color="black",
            )

    def plot_info(step, ijk, p, xi, eta, zeta):
        xi += 1
        eta += 1
        zeta += 1

        ax = axs[xi][step]

        posx = 5 + eta * 10
        posy = 5 + zeta * 10

        text1 = f" i  j  k\n{ijk[0]} {ijk[1]} {ijk[2]}"
        if p is not None:
            text1 += f"\n$p " R"\rightarrow" f" {'ijk'[p]}$"

        ax.text(posx, posy, text1, ha="center", va="center", fontsize=15)

    for xi in [-1, 0, 1]:
        for eta in [-1, 0, 1]:
            for zeta in [-1, 0, 1]:
                if xi * eta * zeta > 0:
                    continue

                p = None

                # step 1
                ijk = [1, 1, 1]

                plot_info(0, ijk, p, xi, eta, zeta)

                # step 2
                if xi > 0:
                    ijk[0] = -1
                elif not xi < 0:
                    p = 0

                plot_info(1, ijk, p, xi, eta, zeta)

                # step 3
                if eta > 0:
                    ijk[1] = -1
                elif not eta < 0:
                    p = 1

                plot_info(2, ijk, p, xi, eta, zeta)

                # step 4
                if zeta > 0:
                    ijk[2] = -1
                elif not zeta < 0:
                    p = 2

                plot_info(3, ijk, p, xi, eta, zeta)

                # step 5
                if ijk[0] * ijk[1] * ijk[2] < 0 and p is not None:
                    ijk[p] = -1

                p = None
                plot_info(4, ijk, p, xi, eta, zeta)

                text = []
                for i in [-1, 1]:
                    for j in [-1, 1]:
                        for k in [-1, 1]:
                            xi_new = xi * j * k
                            eta_new = eta * i * k
                            zeta_new = zeta * i * j
                            if xi_new <= 0 and eta_new <= 0 and zeta_new <= 0:
                                text.append([i, j, k])

                if len(text) == 8:
                    text = "any"
                else:
                    text = [f"{e[0]:2.0f} {e[1]:2.0f} {e[2]:2.0f}" for e in text]
                    text = "\n".join(text)

                if text == "any":
                    color = "green"
                else:
                    trial_set = f"{ijk[0]:2.0f} {ijk[1]:2.0f} {ijk[2]:2.0f}"

                    good_sets = text.split("\n")

                    if trial_set in good_sets:
                        color = "green"
                    else:
                        color = "red"

                ax = axs[xi + 1][5]

                ax.fill_between(
                    [10 * (eta + 1), (eta + 2) * 10],
                    [10 * (zeta + 1), (zeta + 1) * 10],
                    [10 * (zeta + 2), (zeta + 2) * 10],
                    zorder=0,
                    alpha=0.3,
                    color=color,
                )

                posx = 5 + (eta + 1) * 10
                posy = 5 + (zeta + 1) * 10

                ax.text(posx, posy, text, ha="center", va="center", fontsize=15)

    filename = os.path.join(ROOT_DIR, "docs", "source", "img", "niggli-step-4.png")
    plt.savefig(filename, dpi=600, bbox_inches="tight")
    plt.close()
    print(f"File is saved in {os.path.abspath(filename)}")


if __name__ == "__main__":
    plot()
