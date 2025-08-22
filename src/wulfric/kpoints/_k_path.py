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
from typing import Iterable

old_dir = set(dir())
old_dir.add("old_dir")


def get_path_as_list(path_as_string) -> list:
    r"""
    Converts k=path from string to list representation.

    .. code-block:: python

        path_as_list = [["G", "X", "Y", "S"], ["G", "Z"]]
        path_as_string = "G-X-Y-S|G-Z"

    Parameters
    ----------
    path_as_string : str
        K-path as a single string.

    Returns
    -------
    path_as_list : list of list of str
        K-path as list of subpaths, where each subpath is a list of k-points.

    Raises
    ------
    ValueError
        If ``path_as_string`` is not ``str``
    Valueerror
        If any subpath contains less than two points.

    See Also
    --------
    :ref:`user-guide_usage_key-concepts_kpath`
    """
    if not isinstance(path_as_string, str):
        raise ValueError(f"path_as_string is not a string: {path_as_string}")

    subpaths_as_str = path_as_string.split("|")
    path_as_list = []
    for s_i, subpath_as_str in subpaths_as_str:
        subpath_as_list = subpath_as_str.split("-")
        # Each subpath has to contain at least two points.
        # If subpath is empty, then no action required
        if len(subpath_as_list) == 1:
            raise ValueError(
                f"Subpath {s_i + 1} has less than two points: {subpath_as_str}"
            )

        if len(subpath_as_list) >= 2:
            path_as_list.append(subpath_as_list)


def get_path_as_string(path_as_list) -> str:
    r"""
    Converts k=path from list to string representation.

    .. code-block:: python

        path_as_string = "G-X-Y-S|G-Z"
        path_as_list = [["G", "X", "Y", "S"], ["G", "Z"]]

    Parameters
    ----------
    path_as_list : list of list of str
        K-path as list of subpaths, where each subpath is a list of k-points.


    Returns
    -------
    path_as_string : str
        K-path as a single string.

    Raises
    ------
    ValueError
        If ``path_as_list`` is not a ``list`` of ``list``.

    See Also
    --------
    :ref:`user-guide_usage_key-concepts_kpath`
    """

    if not isinstance(path_as_list, Iterable):
        raise ValueError(
            f"path_as_list is not Iterable, can not convert to string:\n{path_as_list}"
        )

    subpaths_as_str = []
    for s_i, subpath_as_list in enumerate(path_as_list):
        if not isinstance(subpath_as_list, Iterable):
            raise ValueError(
                f"Subpath {s_i + 1} is not Iterable, can not convert to string:\n{subpath_as_list}"
            )
        subpaths_as_str.append("-".join(subpath_as_list))

    return "|".join(subpaths_as_str)


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
