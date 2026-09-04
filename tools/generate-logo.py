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
