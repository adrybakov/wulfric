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
from random import choices
from string import ascii_lowercase as ASCII_LOWERCASE

import numpy as np

from wulfric._kpoints_class import Kpoints
from wulfric.cell._basic_manipulation import get_reciprocal
from wulfric.cell._voronoi import get_wigner_seitz_cell

try:
    import plotly.graph_objects as go

    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


class PlotlyEngine:
    r"""
    Plotting engine based on |plotly|_.

    Parameters
    ----------
    fig : plotly graph object, optional
        Figure to plot on. If not provided, then a new one is created as
        ``fig = go.Figure()``.

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
                'Plotly is not available. Please install it with "pip install plotly"'
            )

        if fig is None:
            fig = go.Figure(layout=go.Layout(scene=dict(aspectmode="data")))
        self.fig = fig

        self.fig.update_layout(template="none")

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

        self.fig.update_layout(**kwargs)
        self.fig.show()

    def save(
        self,
        output_name="wulfric-plot.html",
        axes_visible=True,
        kwargs_write_html=None,
        **kwargs,
    ):
        r"""
        Saves the figure in the html file.

        Parameters
        ----------
        output_name : str, default "lattice_graph.html"
            Name of the file to be saved. With extension.
        axes_visible : bool, default True
            Whether to show axes.
        kwargs_write_html : dict, optional
            Passed directly to the |plotly-write-html|_.
        **kwargs
            Passed directly to the |plotly-update-layout|_.
        """

        if kwargs_write_html is None:
            kwargs_write_html = {}

        if not axes_visible:
            self.fig.update_scenes(
                xaxis_visible=False, yaxis_visible=False, zaxis_visible=False
            )

        self.fig.update_layout(**kwargs)

        self.fig.write_html(output_name, **kwargs_write_html)

    def plot_line(
        self,
        start_point,
        end_point,
        color="#000000",
        legend_label=None,
        legend_group=None,
    ):
        r"""
        Plots a single line between ``start_point`` to ``end_point``.

        Parameters
        ----------
        start_point : (3, ) |array-like|_
            First end of the line.
        end_point : (3, ) |array-like|_
            Second point of the line.
        color : str, default "#000000"
            Color of the line. Any value that is supported by |plotly|_.
        legend_label : str, optional
            Label of the line that is displayed in the figure.
        legend_group : str, optional
            Legend's group. If ``None``, then defaults to the random string of 10
            characters.
        """

        if legend_group is None:
            legend_group = "".join(choices(ASCII_LOWERCASE, k=10))

        x, y, z = np.array([start_point, end_point]).T

        self.fig.add_traces(
            data=dict(
                type="scatter3d",
                mode="lines",
                legendgroup=legend_group,
                name=legend_label,
                showlegend=legend_label is not None,
                x=x,
                y=y,
                z=z,
                line=dict(color=color),
                hoverinfo="none",
            )
        )

    def plot_vector(
        self,
        start_point,
        end_point,
        color="#000000",
        vector_label=None,
        legend_label=None,
        legend_group=None,
    ):
        r"""
        Plots a single vector pointing from ``start_point`` to ``end_point``.

        Parameters
        ----------
        start_point : (3, ) |array-like|_
            Start point of the vector.
        end_point : (3, ) |array-like|_
            End point of the vector.
        color : str, default "#000000"
            Color of the vector and its label. Any value that is supported by |plotly|_.
        vector_label : str, optional
            Label of the vector that is displayed in the figure.
        legend_label : str, optional
            Label for the legend. Entry in legend only showed if
            ``legend_label is not None``.
        legend_group : str, optional
            Legend's group. If ``None``, then defaults to the random string of 10
            characters.
        """

        if legend_group is None:
            legend_group = "".join(choices(ASCII_LOWERCASE, k=10))

        x, y, z = np.array([start_point, end_point]).T

        self.fig.add_traces(
            data=[
                dict(
                    type="scatter3d",
                    mode="lines",
                    legendgroup=legend_group,
                    name=legend_label,
                    showlegend=legend_label is not None,
                    x=x,
                    y=y,
                    z=z,
                    line=dict(color=color, width=3),
                    hoverinfo="none",
                ),
                dict(
                    type="cone",
                    legendgroup=legend_group,
                    showlegend=False,
                    x=[x[1]],
                    y=[y[1]],
                    z=[z[1]],
                    u=[0.4 * (x[1] - x[0])],
                    v=[0.4 * (y[1] - y[0])],
                    w=[0.4 * (z[1] - z[0])],
                    anchor="tip",
                    colorscale=[[0, color], [1, color]],
                    showscale=False,
                    hoverinfo="none",
                ),
            ]
        )
        if vector_label is not None:
            self.fig.add_traces(
                data=dict(
                    type="scatter3d",
                    mode="text",
                    legendgroup=legend_group,
                    showlegend=False,
                    x=[1.2 * (x[1] - x[0]) + x[0]],
                    y=[1.2 * (y[1] - y[0]) + y[0]],
                    z=[1.2 * (z[1] - z[0]) + z[0]],
                    marker=dict(size=0),
                    text=vector_label,
                    textfont=dict(size=12, color=color),
                    textposition="top center",
                    hoverinfo="none",
                )
            )

    def plot_cell(
        self,
        cell,
        color="#000000",
        plot_vectors=True,
        vector_label="a",
        shift=(0, 0, 0),
        legend_label=None,
        legend_group=None,
    ):
        r"""
        Plots given ``cell`` as is.

        Parameters
        ----------
        cell : (3, 3) |array-like|_
            Matrix of a cell, rows are interpreted as vectors.
        color : str, default "#000000"
            Colour for the cell and the labels. Any value that is supported by |plotly|_.
        plot_vectors : bool, default True
            Whether to plot lattice vectors.
        vector_label : str, default "a"
            Vector's label, ignored if ``plot_vectors = False``.
        shift : (3, ) |array-like|_, default (0.0, 0.0, 0.0)
            Absolute coordinates of the corner of the cell, from which the three lattice
            vectors are plotted.
        legend_label : str, optional
            Label for the legend. Entry in legend only showed if
            ``legend_label is not None``.
        legend_group : str, optional
            Legend's group. If ``None``, then defaults to the random string of 10
            characters.
        """

        cell = np.array(cell)

        if legend_group is None:
            legend_group = "".join(choices(ASCII_LOWERCASE, k=10))

        shift = np.array(shift)

        # Plot vectors
        if plot_vectors:
            for i in range(3):
                self.plot_vector(
                    start_point=shift,
                    end_point=shift + cell[i],
                    color=color,
                    vector_label=f"{vector_label}{i + 1}",
                    legend_group=legend_group,
                )

        # Plot the cell borders
        for i in range(0, 3):
            j = (i + 1) % 3
            k = (i + 2) % 3
            self.plot_line(
                start_point=shift,
                end_point=shift + cell[i],
                color=color,
                legend_label=legend_label,
                legend_group=legend_group,
            )
            if legend_label is not None:
                legend_label = None
            self.plot_line(
                start_point=shift + cell[i],
                end_point=shift + cell[i] + cell[j],
                color=color,
                legend_group=legend_group,
            )
            self.plot_line(
                start_point=shift + cell[i],
                end_point=shift + cell[i] + cell[k],
                color=color,
                legend_group=legend_group,
            )
            self.plot_line(
                start_point=shift + cell[i] + cell[j],
                end_point=shift + cell[i] + cell[j] + cell[k],
                color=color,
                legend_group=legend_group,
            )

    def plot_wigner_seitz_cell(
        self,
        cell,
        plot_vectors=True,
        vector_label="a",
        color="#000000",
        shift=(0.0, 0.0, 0.0),
        legend_label=None,
        legend_group=None,
    ):
        r"""
        Plots Wigner-Seitz cell of the lattice spawned by the given ``cell``.

        Parameters
        ----------
        cell : (3, 3) |array-like|_
            Matrix of a cell, rows are interpreted as vectors.
        plot_vectors : bool, default True
            Whether to plot lattice vectors.
        vector_label : str, default "a"
            Vector's label, ignored if ``plot_vectors = False``.
        color : str, default "#000000"
            Colour for the cell and labels. Any value that is supported by |plotly|_.
        shift : (3, ) |array-like|_, default (0.0, 0.0, 0.0)
            Absolute coordinates of the center of the Wigner-Seitz cell.
        legend_label : str, optional
            Label for the legend. Entry in legend only showed if
            ``legend_label is not None``.
        legend_group : str, optional
            Legend's group. If ``None``, then defaults to the random string of 10
            characters.
        """

        cell = np.array(cell)

        if legend_group is None:
            legend_group = "".join(choices(ASCII_LOWERCASE, k=10))

        # Plot vectors
        if plot_vectors:
            for i in range(3):
                self.plot_vector(
                    start_point=shift,
                    end_point=shift + cell[i],
                    color=color,
                    vector_label=f"{vector_label}{i + 1}",
                    legend_group=legend_group,
                )

        vertices, edges = get_wigner_seitz_cell(cell=cell)
        for start_index, end_index in edges:
            self.plot_line(
                start_point=shift + vertices[start_index],
                end_point=shift + vertices[end_index],
                color=color,
                legend_label=legend_label,
                legend_group=legend_group,
            )
            if legend_label is not None:
                legend_label = None

    def plot_brillouin_zone(
        self,
        cell,
        plot_vectors=True,
        vector_label="b",
        color="#FF4D67",
        shift=(0.0, 0.0, 0.0),
        legend_label=None,
        legend_group=None,
    ):
        r"""

        Plots Brillouin zone.

        Parameters
        ----------
        cell : (3, 3) |array-like|_
            Matrix of a cell, rows are interpreted as vectors.
        plot_vectors : bool, default True
            Whether to plot lattice vectors.
        vector_label : str, default "b"
            Vector's label, ignored if ``plot_vectors = False``.
        color : str, default "#FF4D67"
            Colour for the Brillouin zone and labels. Any value that is supported by |plotly|_.
        shift : (3, ) |array-like|_, default (0.0, 0.0, 0.0)
            Absolute coordinates of the center of the Brillouin zone.
        legend_label : str, optional
            Label for the legend. Entry in legend only showed if
            ``legend_label is not None``.
        legend_group : str, optional
            Legend's group. If ``None``, then defaults to the random string of 10
            characters.
        """

        self.plot_wigner_seitz_cell(
            cell=get_reciprocal(cell),
            plot_vectors=plot_vectors,
            vector_label=vector_label,
            color=color,
            shift=shift,
            legend_label=legend_label,
            legend_group=legend_group,
        )

    def plot_kpath(
        self,
        cell,
        color="#000000",
        shift=(0.0, 0.0, 0.0),
        legend_label=None,
        legend_group=None,
    ):
        r"""
        Plots k path in the reciprocal space.

        Parameters
        ----------
        cell : (3, 3) |array-like|_
            Matrix of a cell, rows are interpreted as vectors.
        color : str, default "#000000"
            Colour for the plot. Any value that is supported by |plotly|_.
        shift : (3, ) |array-like|_, default (0, 0, 0)
            Absolute coordinates of the center of the Brillouin zone.
        legend_label : str, optional
            Label for the legend. Entry in legend only showed if
            ``legend_label is not None``.
        legend_group : str, optional
            Legend's group. If ``None``, then defaults to the random string of 10
            characters.
        """

        if legend_group is None:
            legend_group = "".join(choices(ASCII_LOWERCASE, k=10))

        rcell = get_reciprocal(cell)

        kp = Kpoints.from_cell(cell=cell)

        p_abs = []
        p_rel = []
        labels = []
        for point in kp.hs_names:
            p_abs.append(shift + tuple(kp.hs_coordinates[point] @ rcell))
            p_rel.append(kp.hs_coordinates[point])

            labels.append(point)

        p_abs = np.array(p_abs).T

        self.fig.add_traces(
            data=dict(
                type="scatter3d",
                mode="markers+text",
                legendgroup=legend_group,
                name=legend_label,
                showlegend=legend_label is not None,
                x=p_abs[0],
                y=p_abs[1],
                z=p_abs[2],
                marker=dict(size=6, color=color),
                text=labels,
                textposition="top center",
                textfont=dict(size=16, color=color),
                hovertext=p_rel,
                hoverinfo="text",
            )
        )

        for subpath in kp.path:
            xyz = []
            for i in range(len(subpath)):
                xyz.append(shift + kp.hs_coordinates[subpath[i]] @ rcell)

            xyz = np.array(xyz).T
            self.fig.add_traces(
                data=dict(
                    type="scatter3d",
                    mode="lines",
                    legendgroup=legend_group,
                    showlegend=False,
                    x=xyz[0],
                    y=xyz[1],
                    z=xyz[2],
                    line=dict(color=color),
                    hoverinfo="none",
                ),
            )

    def plot_lattice(
        self,
        cell,
        color="#000000",
        repetitions=(1, 1, 1),
        shift=(0, 0, 0),
        legend_label=None,
        legend_group=None,
    ):
        r"""
        Plots lattice points spawned by the given ``cell``.

        Parameters
        ----------
        cell : (3, 3) |array-like|_
            Matrix of a cell, rows are interpreted as vectors.
        color : str, default "#000000"
            Color of the points. Any value that is supported by |plotly|_.
        repetitions : (3, ) tuple of int, default (1, 1, 1)
            How many lattice points to plot. All lattice points with relative coordinates
            ``r_1``, ``r_2``, ``r_3``, that fulfil

            * ``-repetitions[0] <= r_1 <= repetitions[0]``
            * ``-repetitions[1] <= r_2 <= repetitions[1]``
            * ``-repetitions[2] <= r_3 <= repetitions[2]``

            are plotted.
        shift : (3, ) |array-like|_, default (0, 0, 0)
            Absolute coordinates of the corner of the cell, from which the three lattice
            vectors are plotted.
        legend_label : str, optional
            Label for the legend. Entry in legend only showed if
            ``legend_label is not None``.
        legend_group : str, optional
            Legend's group. If ``None``, then defaults to the random string of 10
            characters.
        """

        cell = np.array(cell)

        if legend_group is None:
            legend_group = "".join(choices(ASCII_LOWERCASE, k=10))

        points = []
        for i in range(-repetitions[0], repetitions[0] + 1):
            for j in range(-repetitions[1], repetitions[1] + 1):
                for k in range(-repetitions[2], repetitions[2] + 1):
                    points.append(shift + i * cell[0] + j * cell[1] + k * cell[2])

        points = np.array(points).T
        self.fig.add_traces(
            data=dict(
                type="scatter3d",
                mode="markers",
                legendgroup=legend_group,
                name=legend_label,
                showlegend=legend_label is not None,
                x=points[0],
                y=points[1],
                z=points[2],
                marker=dict(size=2, color=color),
                hoverinfo="none",
            ),
        )


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
