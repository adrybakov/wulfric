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
    import plotly.graph_objects as go

    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


class PlotlyBackend(AbstractBackend):
    r"""
    Plotting engine based on |plotly|_.

    Parameters
    ----------
    fig : plotly graph object
        Figure to plot on. If not provided, a new figure is created.

    Attributes
    ----------
    fig : plotly graph object
        Figure to plot on.

    Notes
    -----
    This class is a part of ``wulfric[visual]``
    """

    def __init__(self, fig=None):
        if not PLOTLY_AVAILABLE:
            raise ImportError(
                'Plotly is not available. Install it with "pip install plotly"'
            )
        super().__init__()
        if fig is None:
            fig = go.Figure()
        self.fig = fig

    def show(self, axes_visible=True, **kwargs):
        r"""
        Shows the figure in the interactive mode.

        Parameters
        ----------
        axes_visible : bool, default True
            Whether to show axes.
        **kwargs
            Passed directly to the |plotly-update-layout|_.
        """

        if not axes_visible:
            self.fig.update_scenes(
                xaxis_visible=False, yaxis_visible=False, zaxis_visible=False
            )

        # Set up defaults
        if "width" not in kwargs:
            kwargs["width"] = 800
        if "height" not in kwargs:
            kwargs["height"] = 700
        if "yaxis_scaleanchor" not in kwargs:
            kwargs["yaxis_scaleanchor"] = "x"
        if "showlegend" not in kwargs:
            kwargs["showlegend"] = False
        if "autosize" not in kwargs:
            kwargs["autosize"] = False

        self.fig.update_layout(**kwargs)
        self.fig.show()

    def save(
        self,
        output_name="lattice_graph.png",
        kwargs_update_layout=None,
        kwargs_write_html=None,
        axes_visible=True,
    ):
        r"""
        Saves the figure in the html file.

        Parameters
        ----------
        output_name : str, default "lattice_graph.png"
            Name of the file to be saved. With extension.
        kwargs_update_layout : dict, optional
            Passed directly to the |plotly-update-layout|_.
        kwargs_write_html : dict, optional
            Passed directly to the |plotly-write-html|_.
        axes_visible : bool, default True
            Whether to show axes.
        """

        if kwargs_update_layout is None:
            kwargs_update_layout = {}
        if kwargs_write_html is None:
            kwargs_write_html = {}

        self.fig.update_scenes(aspectmode="data")
        if not axes_visible:
            self.fig.update_scenes(
                xaxis_visible=False, yaxis_visible=False, zaxis_visible=False
            )

        self.fig.update_layout(**kwargs_update_layout)

        self.fig.write_html(output_name, **kwargs_write_html)

    def plot_unit_cell(
        self,
        cell,
        vectors=True,
        color="#274DD1",
        label=None,
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
            Colour for the plot. Any value supported Plotly.
        label : str, optional
            Label for the plot.
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

        if conventional:
            cell = get_conventional(cell)
        elif reciprocal:
            cell = get_reciprocal(cell)

        if normalize:
            cell /= abs(get_volume(cell) ** (1 / 3.0))

        legendgroup = "".join(choices(ascii_lowercase, k=10))

        if vectors:
            labels = [f"{vector_label}{i+1}" for i in range(3)]
            for i in range(3):
                x = [0, cell[i][0]]
                y = [0, cell[i][1]]
                z = [0, cell[i][2]]
                self.fig.add_traces(
                    data=[
                        {
                            "x": x,
                            "y": y,
                            "z": z,
                            "mode": "lines",
                            "type": "scatter3d",
                            "hoverinfo": "none",
                            "line": {"color": color, "width": 3},
                            "showlegend": False,
                            "legendgroup": legendgroup,
                        },
                        {
                            "type": "cone",
                            "x": [x[1]],
                            "y": [y[1]],
                            "z": [z[1]],
                            "u": [0.2 * (x[1] - x[0])],
                            "v": [0.2 * (y[1] - y[0])],
                            "w": [0.2 * (z[1] - z[0])],
                            "anchor": "tip",
                            "hoverinfo": "none",
                            "colorscale": [[0, color], [1, color]],
                            "showscale": False,
                            "showlegend": False,
                            "legendgroup": legendgroup,
                        },
                    ]
                )
                self.fig.add_traces(
                    data=go.Scatter3d(
                        mode="text",
                        x=[1.2 * x[1]],
                        y=[1.2 * y[1]],
                        z=[1.2 * z[1]],
                        marker=dict(size=0, color=color),
                        text=labels[i],
                        hoverinfo="none",
                        textposition="top center",
                        textfont=dict(size=12),
                        showlegend=False,
                        legendgroup=legendgroup,
                    )
                )

        def plot_line(line, shift, showlegend=False):
            self.fig.add_traces(
                data=go.Scatter3d(
                    mode="lines",
                    x=[shift[0], shift[0] + line[0]],
                    y=[shift[1], shift[1] + line[1]],
                    z=[shift[2], shift[2] + line[2]],
                    line=dict(color=color),
                    hoverinfo="none",
                    legendgroup=legendgroup,
                    name=label,
                    showlegend=showlegend,
                ),
            )

        showlegend = label is not None
        for i in range(0, 3):
            j = (i + 1) % 3
            k = (i + 2) % 3
            plot_line(cell[i], np.zeros(3), showlegend=showlegend)
            if showlegend:
                showlegend = False
            plot_line(cell[i], cell[j])
            plot_line(cell[i], cell[k])
            plot_line(cell[i], cell[j] + cell[k])

    def plot_wigner_seitz(
        self,
        cell,
        vectors=True,
        label=None,
        color="black",
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
        label : str, optional
            Label for the plot.
        color : str, default "black" or "#FF4D67"
            Colour for the plot. Any value supported Plotly.
        reciprocal : bool, default False
            Whether to plot reciprocal or real Wigner-Seitz cell.
        normalize : bool, default False
            Whether to normalize volume of the cell to one.
        """

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

        legendgroup = "".join(choices(ascii_lowercase, k=10))

        if vectors:
            labels = [f"{vector_label}{i+1}" for i in range(3)]
            for i in range(3):
                x = [0, vs[i][0]]
                y = [0, vs[i][1]]
                z = [0, vs[i][2]]
                self.fig.add_traces(
                    data=[
                        {
                            "x": x,
                            "y": y,
                            "z": z,
                            "mode": "lines",
                            "type": "scatter3d",
                            "hoverinfo": "none",
                            "line": {"color": color, "width": 3},
                            "showlegend": False,
                            "legendgroup": legendgroup,
                        },
                        {
                            "type": "cone",
                            "x": [x[1]],
                            "y": [y[1]],
                            "z": [z[1]],
                            "u": [0.2 * (x[1] - x[0])],
                            "v": [0.2 * (y[1] - y[0])],
                            "w": [0.2 * (z[1] - z[0])],
                            "anchor": "tip",
                            "hoverinfo": "none",
                            "colorscale": [[0, color], [1, color]],
                            "showscale": False,
                            "showlegend": False,
                            "legendgroup": legendgroup,
                        },
                    ]
                )
                self.fig.add_traces(
                    data=go.Scatter3d(
                        mode="text",
                        x=[1.2 * x[1]],
                        y=[1.2 * y[1]],
                        z=[1.2 * z[1]],
                        marker=dict(size=0, color=color),
                        text=labels[i],
                        hoverinfo="none",
                        textposition="top center",
                        textfont=dict(size=12),
                        showlegend=False,
                        legendgroup=legendgroup,
                    )
                )

        edges, _ = _get_voronoi_cell(cell)
        showlegend = label is not None
        for p1, p2 in edges:
            xyz = np.array([p1, p2]).T
            self.fig.add_traces(
                data=go.Scatter3d(
                    mode="lines",
                    x=xyz[0],
                    y=xyz[1],
                    z=xyz[2],
                    line=dict(color=color),
                    hoverinfo="none",
                    showlegend=showlegend,
                    legendgroup=legendgroup,
                    name=label,
                ),
            )
            if showlegend:
                showlegend = False

    def plot_kpath(self, cell, color="#000000", label=None, normalize=False, **kwargs):
        r"""
        Plots k path in the reciprocal space.

        Parameters
        ----------
        cell : (3, 3) |array-like|_
            Matrix of a cell, rows are interpreted as vectors.
        color : str, default "#000000"
            Colour for the plot. Any value supported Plotly.
        label : str, optional
            Label for the plot.
        normalize : bool, default False
            Whether to normalize volume of the cell to one.
        """

        if normalize:
            cell /= get_volume(cell) ** (1 / 3.0)

        kp = Kpoints.from_cell(cell=cell)

        cell = get_reciprocal(cell)

        p_abs = []
        p_rel = []
        labels = []
        for point in kp.hs_names:
            p_abs.append(tuple(kp.hs_coordinates[point] @ cell))
            p_rel.append(kp.hs_coordinates[point])

            labels.append(kp.hs_labels[point])

        p_abs = np.array(p_abs).T

        self.fig.add_traces(
            data=go.Scatter3d(
                mode="markers+text",
                x=p_abs[0],
                y=p_abs[1],
                z=p_abs[2],
                marker=dict(size=6, color=color),
                text=labels,
                hoverinfo="text",
                hovertext=p_rel,
                textposition="top center",
                textfont=dict(size=16),
                showlegend=False,
            )
        )

        for subpath in kp.path:
            xyz = []
            for i in range(len(subpath)):
                xyz.append(kp.hs_coordinates[subpath[i]] @ cell)

            xyz = np.array(xyz).T
            self.fig.add_traces(
                data=go.Scatter3d(
                    mode="lines",
                    x=xyz[0],
                    y=xyz[1],
                    z=xyz[2],
                    line=dict(color=color),
                    hoverinfo="none",
                    showlegend=False,
                ),
            )

    def plot_lattice(self, cell, label=None, repetitions=(1, 1, 1)):
        r"""
        TODO
        """

        points = []
        for i in range(-repetitions[0], repetitions[0] + 1):
            for j in range(-repetitions[1], repetitions[1] + 1):
                for k in range(-repetitions[2], repetitions[2] + 1):
                    points.append(i * cell[0] + j * cell[1] + k * cell[2])

        points = np.array(points).T
        self.fig.add_traces(
            data=go.Scatter3d(
                mode="markers",
                x=points[0],
                y=points[1],
                z=points[2],
                marker=dict(size=2, color="Black"),
                hoverinfo="none",
                showlegend=label is not None,
                legendgroup=label,
                name=label,
            ),
        )


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
