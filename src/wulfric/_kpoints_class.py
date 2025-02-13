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


from copy import deepcopy
from typing import Iterable

import numpy as np

from wulfric.cell._basic_manipulation import get_reciprocal
from wulfric.cell._kpoints import get_hs_data
from wulfric.cell._lepage import lepage
from wulfric.geometry._geometry import absolute_to_relative

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


class Kpoints:
    r"""
    Interface for convenient manipulation with the high symmetry kpoints and K-path in
    reciprocal space.

    Parameters
    ----------
    rcell : (3, 3) |array-like|_
        Reciprocal cell. Rows are interpreted as vectors.
    coordinates : list, optional
        Coordinates of high symmetry points given in relative coordinates in reciprocal
        space.
    names: list, optional
        Names of the high symmetry points. Used in ``path``. Has to have the same length
        as ``coordinates``. If ``None``, then use "K1", ... "KN", where
        ``N = len(coordinates)``.
    labels : list, optional
        List of the high symmetry point's labels. Used for plotting. Has to have the same
        length as ``coordinates``. If ``None``, then use "K$_1$", ... "K$_N$", where
        ``N = len(coordinates)``.
    path : str, optional
        K-path. Use elements of ``names`` to specify the path. If no names given, then use
        "K1", ... "KN", where ``N = len(coordinates)``.
    n : int
        Number of intermediate points between each pair of the high symmetry points (high
        symmetry points excluded).

    Attributes
    ----------
    rcell : (3, 3) :numpy:`ndarray`
        Reciprocal cell. Rows are interpreted as vectors.
    hs_names : list
        Names of the high symmetry points. Used for programming, not for plotting.
    hs_coordinates : dict
        Dictionary of the high symmetry points coordinates.

        .. code-block:: python

            {"name": [k_a, k_b, k_c], ... }

    hs_labels : dict
        Dictionary of the high symmetry points labels for plotting.

        .. code-block:: python

            {"name": "label", ... }
    """

    def __init__(
        self, rcell, coordinates=None, names=None, labels=None, path=None, n=100
    ) -> None:
        self.rcell = np.array(rcell)

        if coordinates is None:
            coordinates = []

        # Fill names and labels with defaults
        if names is None:
            names = [f"K{i+1}" for i in range(len(coordinates))]
            if labels is None:
                labels = [f"K$_{i+1}$" for i in range(len(coordinates))]
        if labels is None:
            labels = [name for name in names]
        else:
            if len(labels) != len(coordinates):
                raise ValueError(
                    f"Amount of labels ({len(labels)}) does not match amount of points ({len(coordinates)})."
                )

        # Define high symmetry points attributes
        self.hs_coordinates = dict(
            [(names[i], np.array(coordinates[i])) for i in range(len(coordinates))]
        )
        self.hs_labels = dict([(names[i], labels[i]) for i in range(len(coordinates))])
        self.hs_names = names

        self._n = n

        self._path = None
        if path is None:
            path = "-".join(self.hs_names)
        self.path = path

    @staticmethod
    def from_cell(
        cell,
        lattice_type=None,
        lattice_variation=None,
        S_matrix=None,
        C_matrix=None,
        length_tolerance=1e-8,
        angle_tolerance=1e-4,
        n=100,
    ):
        r"""
        Creates an instance of the :py:class:`wulf.Kpoints` from ``cell``.

        Parameters
        ----------
        cell : (3, 3) |array-like|_
            Matrix of a cell, rows are interpreted as vectors.
        lattice_type : str, optional
            One of the 14 lattice types that correspond to the provided ``cell``,
            case-insensitive. If not provided, then computed automatically from ``cell``.
            If provided, then it user's responsibility to ensure that ``lattice_type`` is
            correct.
        lattice_variation : str, optional
            One of the lattice variations that correspond to the provided ``cell`` and
            ``lattice_type``. If not provided, then computed automatically. Case-insensitive.
        S_matrix : (3, 3) |array-like|_, optional
            Transformation matrix S. If not provided, then computed automatically from
            ``cell``. If provided, then it is user's responsibility to ensure that the matrix
            is the correct one for the given ``cell``.
        C_matrix : (3, 3) |array-like|_, optional
            Transformation matrix C. If not provided, then computed automatically from
            ``cell``. If provided, then it is user's responsibility to ensure that the matrix
            is the correct one for the given ``cell``.
        length_tolerance : float, default :math:`10^{-8}`
            Tolerance for length variables (lengths of the lattice vectors). Default
            value is chosen in the contexts of condense matter physics, assuming that
            length is given in Angstroms. Please choose appropriate tolerance for your
            problem.
        angle_tolerance : float, default :math:`10^{-4}`
            Tolerance for angle variables (angles of the lattice). Default value is chosen
            in the contexts of condense matter physics, assuming that angles are in
            degrees. Please choose appropriate tolerance for your problem.
        n : int, default 100
            Number of points between each pair of the high symmetry points
            (high symmetry points excluded).

        Returns
        -------
        kp : :py:class:`wulf.Kpoints`
        """

        coordinates, names, labels, path = get_hs_data(
            cell,
            lattice_type=lattice_type,
            lattice_variation=lattice_variation,
            S_matrix=S_matrix,
            C_matrix=C_matrix,
            length_tolerance=length_tolerance,
            angle_tolerance=angle_tolerance,
        )

        return Kpoints(
            get_reciprocal(cell),
            coordinates=coordinates,
            names=names,
            labels=labels,
            path=path,
            n=n,
        )

    ################################################################################
    #                            High symmetry points                              #
    ################################################################################
    def add_hs_point(self, name, coordinate, label, relative=True) -> None:
        r"""
        Adds high symmetry point.

        Parameters
        ----------
        name : str
            Name of the high symmetry point.
        coordinate : (3,) array-like
            Coordinate of the high symmetry point.
        label : str
            Label of the high symmetry point, ready to be plotted.
        relative : bool, optional
            Whether to interpret coordinates as relative or absolute.
        """

        if name in self.hs_names:
            raise ValueError(f"Point '{name}' already defined.")

        if not relative:
            coordinate = absolute_to_relative(coordinate, self.rcell)

        self.hs_names.append(name)
        self.hs_coordinates[name] = np.array(coordinate)
        self.hs_labels[name] = label

    def remove_hs_point(self, name) -> None:
        r"""
        Removes high symmetry point.

        Parameters
        ----------
        name : str
            Name of the high symmetry point.
        """

        if name in self.hs_names:
            self.hs_names.remove(name)
            del self.hs_coordinates[name]
            del self.hs_labels[name]

    ################################################################################
    #                                Path attributes                               #
    ################################################################################
    @property
    def path(self) -> list:
        r"""
        K points path.

        Returns
        -------
        path : list of list of str
            K points path. Each subpath is a list of the high symmetry points.
        """

        return self._path

    @path.setter
    def path(self, new_path):
        if isinstance(new_path, str):
            tmp_path = new_path.split("|")
            new_path = []
            for i in range(len(tmp_path)):
                subpath = tmp_path[i].split("-")
                # Each subpath has to contain at least two points.
                if len(subpath) != 1:
                    new_path.append(subpath)
        elif isinstance(new_path, Iterable):
            tmp_path = new_path
            new_path = []
            for subpath in tmp_path:
                if isinstance(subpath, str) and "-" in subpath:
                    subpath = subpath.split("-")
                    # Each subpath has to contain at least two points.
                    if len(subpath) != 1:
                        new_path.append(subpath)
                elif (
                    not isinstance(subpath, str)
                    and isinstance(subpath, Iterable)
                    and len(subpath) != 1
                ):
                    new_path.append(subpath)
                else:
                    new_path = [tmp_path]
                    break
        # Check if all points are defined.
        for subpath in new_path:
            for point in subpath:
                if point not in self.hs_names:
                    message = f"Point '{point}' is not defined. Defined points are:"
                    for defined_name in self.hs_names:
                        message += (
                            f"\n  {defined_name} : {self.hs_coordinates[defined_name]}"
                        )
                    raise ValueError(message)
        self._path = new_path

    @property
    def path_string(self) -> str:
        r"""
        K points path as a string.

        Returns
        -------
        path : str
        """

        result = ""
        for s_i, subpath in enumerate(self.path):
            for i, name in enumerate(subpath):
                if i != 0:
                    result += "-"
                result += name
            if s_i != len(self.path) - 1:
                result += "|"

        return result

    @property
    def n(self) -> int:
        r"""
        Amount of points between each pair of the high symmetry points
        (high symmetry points excluded).

        Returns
        -------
        n : int
        """

        return self._n

    @n.setter
    def n(self, new_n):
        if not isinstance(new_n, int):
            raise ValueError(
                f"n has to be integer. Given: {new_n}, type = {type(new_n)}"
            )
        self._n = new_n

    ################################################################################
    #                         Attributes for the axis ticks                        #
    ################################################################################
    @property
    def labels(self) -> list:
        r"""
        Labels of high symmetry points, ready to be plotted.

        For example for point "Gamma" it returns r"$\Gamma$".

        If there are two high symmetry points following one another in the path,
        it returns "X|Y" where X and Y are the labels of the two high symmetry points.

        Returns
        -------
        labels : list of str
            Labels, ready to be plotted. Same length as :py:attr:`.ticks`.
        """

        labels = []
        for s_i, subpath in enumerate(self.path):
            if s_i != 0:
                labels[-1] += "|" + self.hs_labels[subpath[0]]
            else:
                labels.append(self.hs_labels[subpath[0]])
            for name in subpath[1:]:
                labels.append(self.hs_labels[name])

        return labels

    def ticks(self, relative=False):
        r"""
        Tick's positions of the high symmetry points, ready to be plotted.

        Parameters
        ----------
        relative : bool, optional
            Whether to use relative coordinates instead of the absolute ones.

        Returns
        -------
        ticks : :numpy:`ndarray`
            Tick's positions, ready to be plotted. Same length as :py:attr:`.labels`.
        """

        if relative:
            cell = np.eye(3)
        else:
            cell = self.rcell

        ticks = []
        for s_i, subpath in enumerate(self.path):
            if s_i == 0:
                ticks.append(0)
            for i, name in enumerate(subpath[1:]):
                ticks.append(
                    np.linalg.norm(
                        self.hs_coordinates[name] @ cell
                        - self.hs_coordinates[subpath[i]] @ cell
                    )
                    + ticks[-1]
                )

        return np.array(ticks)

    ################################################################################
    #                   Points of the path with intermediate ones                  #
    ################################################################################
    def points(self, relative=False):
        r"""
        Coordinates of all points with n points between each pair of the high
        symmetry points (high symmetry points excluded).

        Parameters
        ----------
        relative : bool, optional
            Whether to use relative coordinates instead of the absolute ones.

        Returns
        -------
        points : (N, 3) :numpy:`ndarray`
            Coordinates of all points.
        """

        if relative:
            cell = np.eye(3)
        else:
            cell = self.rcell

        points = None
        for subpath in self.path:
            for i in range(len(subpath) - 1):
                name = subpath[i]
                next_name = subpath[i + 1]
                new_points = np.linspace(
                    self.hs_coordinates[name] @ cell,
                    self.hs_coordinates[next_name] @ cell,
                    self._n + 2,
                )
                if points is None:
                    points = new_points
                else:
                    points = np.concatenate((points, new_points))
        return points

    # It can not just call for points and flatten them, because it has to treat "|" as a special case.
    def flatten_points(self, relative=False):
        r"""
        Flatten coordinates of all points with n points between each pair of the high
        symmetry points (high symmetry points excluded).

        Used to plot band structure, dispersion, etc.

        Parameters
        ----------
        relative : bool, optional
            Whether to use relative coordinates instead of the absolute ones.

        Returns
        -------
        flatten_points : (N, 3) :numpy:`ndarray`
            Flatten coordinates of all points.
        """

        if relative:
            cell = np.eye(3)
        else:
            cell = self.rcell

        flatten_points = None
        for s_i, subpath in enumerate(self.path):
            for i in range(len(subpath) - 1):
                name = subpath[i]
                next_name = subpath[i + 1]
                points = (
                    np.linspace(
                        self.hs_coordinates[name] @ cell,
                        self.hs_coordinates[next_name] @ cell,
                        self._n + 2,
                    )
                    - self.hs_coordinates[name] @ cell
                )
                delta = np.linalg.norm(points, axis=1)
                if s_i == 0 and i == 0:
                    flatten_points = delta
                else:
                    delta += flatten_points[-1]
                    flatten_points = np.concatenate((flatten_points, delta))
        return flatten_points

    ################################################################################
    #                                     Copy                                     #
    ################################################################################

    def copy(self):
        r"""
        Creates a copy of the kpoints.

        Returns
        -------
        kpoints : :py:class:`.Kpoints`
            Copy of the kpoints.
        """

        return deepcopy(self)

    ################################################################################
    #                                Human readables                               #
    ################################################################################

    def hs_table(self, decimals=8) -> str:
        r"""
        Table of the high symmetry points.

        Parameters
        ----------
        decimals : int, optional
            Number of decimal places to round the coordinates.

        Returns
        -------
        table : str
            String with N+1 lines, where N is the amount of high symmetry points.
            Each line contains the name of the high symmetry point and its relative and
            absolute coordinates in a reciprocal space, i.e.::

                K1  0.0 0.0 0.0   0.0 0.0 0.0

            First line is a header::

                Name  rel_b1 rel_b2 rel_b3  k_x k_y k_z
        """

        d = decimals
        table = [
            (
                f"{'Name':4}  "
                + f"{'rel_b1':>{d+3}} "
                + f"{'rel_b2':>{d+3}} "
                + f"{'rel_b3':>{d+3}}  "
                + f"{'k_x':>{d+3}} "
                + f"{'k_y':>{d+3}} "
                + f"{'k_z':>{d+3}}"
            )
        ]
        for name in self.hs_names:
            relative = self.hs_coordinates[name]
            i = f"{relative[0]: {d+3}.{d}f}"
            j = f"{relative[1]: {d+3}.{d}f}"
            k = f"{relative[2]: {d+3}.{d}f}"
            absolute = self.hs_coordinates[name] @ self.rcell
            k_x = f"{absolute[0]: {d+3}.{d}f}"
            k_y = f"{absolute[1]: {d+3}.{d}f}"
            k_z = f"{absolute[2]: {d+3}.{d}f}"
            table.append(f"{name:4}  {i} {j} {k}  {k_x} {k_y} {k_z}")
        return "\n".join(table)


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
