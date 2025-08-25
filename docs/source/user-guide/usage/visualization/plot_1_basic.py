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
"""
*************
Basic objects
*************

This page explains plotting of basic geometric objects with :py:class:`wulfric.PlotlyEngine`.
"""

import wulfric

# %%
# Points
# ======

import numpy as np

pe = wulfric.PlotlyEngine(_sphinx_gallery_fix=True)

pe.plot_points(points=np.random.random((42, 3)))

pe.show()

# %%
# Vector
# ======
#
# Vector is defined by its start and end pints

pe = wulfric.PlotlyEngine(_sphinx_gallery_fix=True)

pe.plot_vector(start_point=(0, 0, 0), end_point=(1, 1, 1))

pe.plot_vector(
    start_point=(0, 0, 0),
    end_point=(1, 0, 0),
    color="red",
    vector_label="x",
)
pe.plot_vector(
    start_point=(0, 0, 0),
    end_point=(0, 1, 0),
    color="green",
    vector_label="y",
)
pe.plot_vector(
    start_point=(0, 0, 0),
    end_point=(0, 0, 1),
    color="blue",
    vector_label="z",
)


pe.show(axes_visible=False)


# %%
# Line
# ====
# Line is defined by two points

pe = wulfric.PlotlyEngine(_sphinx_gallery_fix=True)
pe.plot_line(
    start_point=(0, 0, 0),
    end_point=(1, 0, 0),
    legend_group="square",
    legend_label="square",
)
pe.plot_line(start_point=(1, 0, 0), end_point=(1, 1, 0), legend_group="square")
pe.plot_line(start_point=(1, 1, 0), end_point=(0, 1, 0), legend_group="square")
pe.plot_line(start_point=(0, 1, 0), end_point=(0, 0, 0), legend_group="square")

pe.plot_line(start_point=(0.3, 1, 0.1), end_point=(3, 1, 2), legend_label="single line")

pe.show()

# sphinx_gallery_thumbnail_path = 'img/gallery-thumbnails/visualization_plot_basic.png'
