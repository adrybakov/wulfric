# ================================== LICENSE ===================================
# Wulfric - Cell, Atoms, K-path, visualization.
# Copyright (C) 2023 Andrey Rybakov
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
import numpy as np
from wulfric._package_info import BINARY_LOGO


def plot_logo(output_file, cmap):
    fig = plt.figure(figsize=(len(BINARY_LOGO[0]), len(BINARY_LOGO)))
    ax = fig.add_axes((0, 0, 1, 1))

    image = np.array(BINARY_LOGO, dtype=float)
    image[image == 0] = np.nan

    ax.imshow(
        image,
        interpolation=None,
        vmin=0,
        vmax=1,
        cmap=cmap,
    )

    ax.axis("off")

    fig.savefig(output_file, transparent=True, dpi=16)
    plt.close()


if __name__ == "__main__":
    plot_logo(
        output_file=os.path.join("docs", "source", "_static", "wulfric-logo-black.png"),
        cmap="binary",
    )
    plot_logo(
        output_file=os.path.join("docs", "source", "_static", "wulfric-logo-white.png"),
        cmap="binary_r",
    )
