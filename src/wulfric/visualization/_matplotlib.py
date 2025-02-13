# Wulfric - Cell, Atoms, K-path.
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


from random import choices
from string import ascii_lowercase
from typing import Iterable

import numpy as np

from wulfric._kpoints_class import Kpoints
from wulfric.cell._basic_manipulation import get_reciprocal
from wulfric.cell._sc_standardize import get_conventional
from wulfric.cell._voronoi import _get_voronoi_cell
from wulfric.geometry._geometry import get_volume
from wulfric.visualization._interface import AbstractBackend

try:
    import matplotlib.pyplot as plt
    from matplotlib import rcParams
    from matplotlib.patches import FancyArrowPatch
    from mpl_toolkits.mplot3d import Axes3D, proj3d

    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


if MATPLOTLIB_AVAILABLE:
    # Better 3D arrows, see: https://stackoverflow.com/questions/22867620/putting-arrowheads-on-vectors-in-a-3d-plot
    class Arrow3D(FancyArrowPatch):
        def __init__(self, ax, xs, ys, zs, *args, **kwargs):
            FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
            self._verts3d = xs, ys, zs
            self.ax = ax

        def draw(self, renderer):
            xs3d, ys3d, zs3d = self._verts3d
            xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.ax.axes.M)
            self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
            FancyArrowPatch.draw(self, renderer)

        def do_3d_projection(self, *_, **__):
            return 0


# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


class MatplotlibBackend(AbstractBackend):
    r"""
    Plotting engine based on |matplotlib|_.

    Parameters
    ----------
    fig : matplotlib figure, optional
        Figure to plot on. If not provided, a new figure and ``ax`` is created.
    ax : matplotlib axis, optional
        Axis to plot on. If not provided, a new axis is created.
    background : bool, default True
        Whether to keep the axis in the plot.
    focal_length : float, default 0.2
        See: |matplotlibFocalLength|_

    Attributes
    ----------
    fig : matplotlib figure
        Figure to plot on.
    ax : matplotlib axis
        Axis to plot on.
    artists : dict
        Dictionary of the artists. Keys are the plot kinds, values are the lists of artists.

    Notes
    -----
    This class is a part of ``wulfric[visual]``
    """

    def __init__(self, fig=None, ax=None, background=True, focal_length=0.2):
        if not MATPLOTLIB_AVAILABLE:
            raise ImportError(
                'Matplotlib is not available. Install it with "pip install matplotlib"'
            )
        super().__init__()
        if fig is None:
            fig = plt.figure(figsize=(6, 6))
            ax = fig.add_subplot(projection="3d")
        elif ax is None:
            ax = fig.add_subplot(projection="3d")

        rcParams["axes.linewidth"] = 0
        rcParams["xtick.color"] = "#B3B3B3"
        ax.set_proj_type("persp", focal_length=focal_length)
        if background:
            ax.axes.linewidth = 0
            ax.xaxis._axinfo["grid"]["color"] = (1, 1, 1, 1)
            ax.yaxis._axinfo["grid"]["color"] = (1, 1, 1, 1)
            ax.zaxis._axinfo["grid"]["color"] = (1, 1, 1, 1)
            ax.set_xlabel("x", fontsize=15, alpha=0.5)
            ax.set_ylabel("y", fontsize=15, alpha=0.5)
            ax.set_zlabel("z", fontsize=15, alpha=0.5)
            ax.tick_params(axis="both", zorder=0, color="#B3B3B3")
        else:
            ax.axis("off")
        self.fig = fig
        self.ax = ax
        self.artists = {}

    def remove(self, kind="primitive"):
        r"""
        Removes a set of artists from the plot.

        Parameters
        ----------
        kind : str or list of str
            Type of the plot to be removed. Supported kinds:

            * "conventional"
            * "primitive"
            * "brillouin"
            * "kpath"
            * "brillouin_kpath"
            * "wigner_seitz"
        """

        if kind == "brillouin_kpath":
            kinds = ["brillouin", "kpath"]
        else:
            kinds = [kind]

        for kind in kinds:
            if kind not in self.artists:
                raise ValueError(f"No artists for the {kind} kind.")
            for artist in self.artists[kind]:
                if isinstance(artist, list):
                    for i in artist:
                        i.remove()
                else:
                    artist.remove()
            del self.artists[kind]
        self.ax.relim(visible_only=True)
        self.ax.set_aspect("equal")

    def plot(self, cell, kind="primitive", **kwargs):
        r"""
        Main plotting method.

        Actual list of supported kinds can be check with:

        .. doctest::

            >>> self.kinds.keys() # doctest: +SKIP

        Parameters
        ----------
        cell : (3, 3) |array-like|_
            Matrix of a cell, rows are interpreted as vectors.
        kind : str or list od str
            Type of the plot to be plotted. Supported plots:

            * "conventional"
            * "primitive"
            * "brillouin"
            * "kpath"
            * "brillouin-kpath"
            * "wigner-seitz"
            * "unit-cell"

        **kwargs
            Parameters to be passed to the specialized plotting function.
            See each function for the list of supported parameters.

        Raises
        ------
        ValueError
            If the plot kind is not supported.

        See Also
        --------
        plot_conventional : "conventional" plot.
        plot_primitive : "primitive" plot.
        plot_brillouin : "brillouin" plot.
        plot_kpath : "kpath" plot.
        plot_brillouin_kpath : "brillouin_kpath" plot.
        plot_wigner_seitz : "wigner-seitz" plot.
        plot_unit_cell : "unit-cell" plot.
        show : Shows the plot.
        save : Save the figure in the file.
        """

        super().plot(cell, kind=kind, **kwargs)
        self.ax.relim()
        self.ax.set_aspect("equal")

    def show(self, elev=30, azim=-60):
        r"""
        Shows the figure in the interactive mode.

        Parameters
        ----------
        elev : float, default 30
            Passed directly to matplotlib. See |matplotlibViewInit|_.
        azim : float, default -60
            Passed directly to matplotlib. See |matplotlibViewInit|_.
        """
        self.ax.set_aspect("equal")
        self.ax.view_init(elev=elev, azim=azim)
        plt.show()
        self.fig = None
        self.ax = None
        plt.close()

    def save(self, output_name="cell_graph.png", elev=30, azim=-60, **kwargs):
        r"""
        Saves the figure in the file.

        Parameters
        ----------
        output_name : str, default "cell_graph.png"
            Name of the file to be saved. With extension.
        elev : float, default 30
            Passed directly to matplotlib. See |matplotlibViewInit|_.
        azim : float, default -60
            Passed directly to matplotlib. See |matplotlibViewInit|_.
        **kwargs
            Parameters to be passed to the |matplotlibSavefig|_.
        """

        self.ax.set_aspect("equal")
        self.ax.view_init(elev=elev, azim=azim)
        self.fig.savefig(output_name, **kwargs)

    def clear(self):
        r"""
        Clears the axis.
        """

        if self.ax is not None:
            self.ax.cla()

    def legend(self, **kwargs):
        r"""
        Adds legend to the figure.

        Parameters
        ----------
        **kwargs :
            Directly passed to the |matplotlibLegend|_.
        """

        self.ax.legend(**kwargs)

    def plot_unit_cell(
        self,
        cell,
        vectors=True,
        color="#274DD1",
        label=None,
        vector_pad=1.1,
        conventional=False,
        reciprocal=False,
        normalize=False,
    ):
        r"""
        Plots real or reciprocal unit cell.

        Parameters
        ----------
        cell : (3, 3) |array-like|_
            Matrix of a cell, rows are interpreted as vectors.
        vectors : bool, default True
            Whether to plot lattice vectors.
        color : str, default "#274DD1"
            Colour for the plot. Any format supported by matplotlib (see |matplotlibColor|_).
        label : str, optional
            Label for the plot.
        vector_pad : float, default 1.1
            Multiplier for the position of the vectors labels. 1 = position of the vector.
        conventional : bool, default False
            Whether to plot conventional cell.
            Only primitive unit cell is supported for reciprocal space.
        reciprocal : bool, default False
            Whether to plot reciprocal or real unit cell.
        normalize : bool, default False
            Whether to normalize volume of the cell to one.
        """
        if reciprocal and conventional:
            raise ValueError("Conventional cell is not supported in reciprocal space.")
        if conventional:
            artist_group = "conventional"
        else:
            artist_group = "primitive"

        if reciprocal:
            artist_group += "_reciprocal"
            vector_label = "b"
        else:
            artist_group += "_real"
            vector_label = "a"

        self.artists[artist_group] = []

        if conventional:
            cell = get_conventional(cell)
        elif reciprocal:
            cell = get_reciprocal(cell)

        if normalize:
            cell /= abs(get_volume(cell) ** (1 / 3.0))

        if label is not None:
            self.artists[artist_group].append(
                self.ax.scatter(0, 0, 0, color=color, label=label)
            )
        if vectors:
            if not isinstance(vector_pad, Iterable):
                vector_pad = [vector_pad, vector_pad, vector_pad]
            for i in range(3):
                self.artists[artist_group].append(
                    self.ax.text(
                        cell[i][0] * vector_pad[i],
                        cell[i][1] * vector_pad[i],
                        cell[i][2] * vector_pad[i],
                        f"${vector_label}_{i+1}$",
                        fontsize=20,
                        color=color,
                        ha="center",
                        va="center",
                    )
                )
                # Try beautiful arrows
                try:
                    self.artists[artist_group].append(
                        self.ax.add_artist(
                            Arrow3D(
                                self.ax,
                                [0, cell[i][0]],
                                [0, cell[i][1]],
                                [0, cell[i][2]],
                                mutation_scale=20,
                                arrowstyle="-|>",
                                color=color,
                                lw=2,
                                alpha=0.7,
                            )
                        )
                    )
                # Go to default
                except:
                    self.artists[artist_group].append(
                        self.ax.quiver(
                            0,
                            0,
                            0,
                            *tuple(cell[i]),
                            arrow_length_ratio=0.2,
                            color=color,
                            alpha=0.7,
                            linewidth=2,
                        )
                    )
                # Ghost point to account for the plot range
                self.artists[artist_group].append(self.ax.scatter(*tuple(cell[i]), s=0))

        def plot_line(line, shift):
            self.artists[artist_group].append(
                self.ax.plot(
                    [shift[0], shift[0] + line[0]],
                    [shift[1], shift[1] + line[1]],
                    [shift[2], shift[2] + line[2]],
                    color=color,
                )
            )

        for i in range(0, 3):
            j = (i + 1) % 3
            k = (i + 2) % 3
            plot_line(cell[i], np.zeros(3))
            plot_line(cell[i], cell[j])
            plot_line(cell[i], cell[k])
            plot_line(cell[i], cell[j] + cell[k])

    def plot_wigner_seitz(
        self,
        cell,
        vectors=True,
        color="black",
        label=None,
        vector_pad=1.1,
        reciprocal=False,
        normalize=False,
    ):
        r"""
        Plots Wigner-Seitz cell.

        Parameters
        ----------
        cell : (3, 3) |array-like|_
            Matrix of a cell, rows are interpreted as vectors.
        vectors : bool, default True
            Whether to plot lattice vectors.
        color : str, default "black"
            Colour for the plot. Any format supported by matplotlib (see |matplotlibColor|_).
        label : str, optional
            Label for the plot.
        vector_pad : float, default 1.1
            Multiplier for the position of the vectors labels. 1 = position of the vector.
        reciprocal : bool, default False
            Whether to plot reciprocal or real Wigner-Seitz cell.
        normalize : bool, default False
            Whether to normalize volume of the cell to one.
        """

        if reciprocal:
            artist_group = "brillouin"
        else:
            artist_group = "wigner_seitz"

        self.artists[artist_group] = []

        if reciprocal:
            cell = get_reciprocal(cell)
            vector_label = "b"
        else:
            vector_label = "a"

        if color is None:
            color = "black"

        if normalize:
            cell /= abs(get_volume(cell) ** (1 / 3.0))

        v1, v2, v3 = cell[0], cell[1], cell[2]

        vs = [v1, v2, v3]

        if label is not None:
            self.artists[artist_group].append(
                self.ax.scatter(0, 0, 0, color=color, label=label)
            )
        if vectors:
            if not isinstance(vector_pad, Iterable):
                vector_pad = [vector_pad, vector_pad, vector_pad]
            for i in range(3):
                self.artists[artist_group].append(
                    self.ax.text(
                        vs[i][0] * vector_pad[i],
                        vs[i][1] * vector_pad[i],
                        vs[i][2] * vector_pad[i],
                        f"${vector_label}_{i+1}$",
                        fontsize=20,
                        color=color,
                        ha="center",
                        va="center",
                    )
                )
                # Try beautiful arrows
                try:
                    self.artists[artist_group].append(
                        self.ax.add_artist(
                            Arrow3D(
                                self.ax,
                                [0, vs[i][0]],
                                [0, vs[i][1]],
                                [0, vs[i][2]],
                                mutation_scale=20,
                                arrowstyle="-|>",
                                color=color,
                                lw=2,
                                alpha=0.8,
                            )
                        )
                    )
                # Go to default
                except:
                    self.artists[artist_group].append(
                        self.ax.quiver(
                            0,
                            0,
                            0,
                            *tuple(vs[i]),
                            arrow_length_ratio=0.2,
                            color=color,
                            alpha=0.5,
                        )
                    )
                # Ghost point to account for the plot range
                self.artists[artist_group].append(self.ax.scatter(*tuple(vs[i]), s=0))

        edges, _ = _get_voronoi_cell(cell)
        for p1, p2 in edges:
            self.artists[artist_group].append(
                self.ax.plot(
                    [p1[0], p2[0]],
                    [p1[1], p2[1]],
                    [p1[2], p2[2]],
                    color=color,
                )
            )

    def plot_kpath(self, cell, color="black", label=None, normalize=False):
        r"""
        Plots k path in the reciprocal space.

        Parameters
        ----------
        cell : (3, 3) |array-like|_
            Matrix of a cell, rows are interpreted as vectors.
        color : str, default "black"
            Colour for the plot. Any format supported by matplotlib (see |matplotlibColor|_).
        label : str, optional
            Label for the plot.
        normalize : bool, default False
            Whether to normalize volume of the cell to one.
        """

        artist_group = "kpath"

        self.artists[artist_group] = []

        if normalize:
            cell /= get_volume(cell) ** (1 / 3.0)

        kp = Kpoints.from_cell(cell)

        cell = get_reciprocal(cell)

        for point in kp.hs_names:
            self.artists[artist_group].append(
                self.ax.scatter(
                    *tuple(kp.hs_coordinates[point] @ cell),
                    s=36,
                    color=color,
                )
            )

            self.artists[artist_group].append(
                self.ax.text(
                    *tuple(
                        kp.hs_coordinates[point] @ cell
                        + 0.025 * cell[0]
                        + +0.025 * cell[1]
                        + 0.025 * cell[2]
                    ),
                    kp.hs_labels[point],
                    fontsize=20,
                    color=color,
                )
            )
        if label is not None:
            self.artists[artist_group].append(
                self.ax.scatter(
                    0,
                    0,
                    0,
                    s=36,
                    color=color,
                    label=label,
                )
            )

        for subpath in kp.path:
            for i in range(len(subpath) - 1):
                self.artists[artist_group].append(
                    self.ax.plot(
                        *tuple(
                            np.concatenate(
                                (
                                    kp.hs_coordinates[subpath[i]] @ cell,
                                    kp.hs_coordinates[subpath[i + 1]] @ cell,
                                )
                            )
                            .reshape(2, 3)
                            .T
                        ),
                        color=color,
                        alpha=0.5,
                        linewidth=3,
                    )
                )


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
