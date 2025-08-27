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
from copy import deepcopy
from typing import Iterable

import numpy as np

from wulfric.cell._basic_manipulation import get_reciprocal
from wulfric.constants._kpoints import HS_PLOT_NAMES
from wulfric.kpoints._path_and_points import (
    get_path_as_string,
    get_path_as_list,
    get_path_and_points,
)

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


class Kpoints:
    r"""
    Interface for convenient manipulations with the high symmetry k-points and k-path in
    reciprocal space.

    Parameters
    ----------
    rcell : (3, 3) |array-like|_
        Reciprocal cell. Rows are interpreted as vectors.
    coordinates : list, optional
        Coordinates of high symmetry points given in relative coordinates in reciprocal
        space (in the basis of ``rcell``).
    names: list, optional
        Names of the high symmetry points. Used in ``path``. Has to have the same length
        as ``coordinates``. If ``None``, then use "K1", ... "KN", where
        ``N = len(coordinates)``.
    labels : list, optional
        List of the high symmetry point's labels. Used for plotting. Has to have the same
        length as ``coordinates``. If ``None`` and ``names is None, then use "K$_1$", ...
        "K$_N$", where ``N = len(coordinates)``. If ``None`` but ``names are given, then
        ``labels = names``.
    path : str, optional
        K-path. Use elements of ``names`` to specify the path. If no names given, then use
        "K1-K2-...-KN", where ``N = len(coordinates)``.
    n : int
        Number of intermediate points between each pair of the high symmetry points (high
        symmetry points excluded).

    Attributes
    ----------
    rcell : (3, 3) :numpy:`ndarray`
        Reciprocal cell. Rows are interpreted as vectors.
    hs_names : list
        Names of the high symmetry points. Used in k-path and as main identifier of the
        point.
    hs_coordinates : dict
        Dictionary of the high symmetry points coordinates. Coordinates are relative (in
        the basis of ``rcell``)

        .. code-block:: python

            {"name": [k_a, k_b, k_c], ... }

    hs_labels : dict
        Dictionary of labels for plotting.

        .. code-block:: python

            {"name": "label", ... }
    """

    def __init__(
        self, rcell, coordinates=None, names=None, labels=None, path=None, n=100
    ) -> None:
        self.rcell = np.array(rcell)

        if coordinates is None:
            coordinates = []

        if labels is None:
            if names is None:
                labels = [f"K$_{i + 1}$" for i in range(len(coordinates))]
            else:
                labels = [name for name in names]
        elif len(labels) != len(coordinates):
            raise ValueError(
                f"Amount of labels ({len(labels)}) does not match amount of points ({len(coordinates)})."
            )

        if names is None:
            names = [f"K{i + 1}" for i in range(len(coordinates))]
        elif len(names) != len(coordinates):
            raise ValueError(
                f"Amount of names ({len(names)}) does not match amount of points ({len(coordinates)})."
            )

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
    def from_crystal(cell, atoms, convention="HPKOT", n=100, spglib_data=None):
        r"""

        Parameters
        ----------
        cell : (3, 3) |array-like|_
            Matrix of a cell, rows are interpreted as vectors.
        atoms : dict
            Dictionary with N atoms. Expected keys:

            *   "positions" : (N, 3) |array-like|_

                Positions of the atoms in the basis of lattice vectors (``cell``). In other
                words - relative coordinates of atoms.
            *   "names" : (N, ) list of str, optional

                See Notes
            *   "species" : (N, ) list of str, optional

                See Notes
            *   "spglib_types" : (N, ) list of int, optional

                See Notes

            .. hint::
                Pass ``atoms = dict(positions=[[0, 0, 0]], spglib_types=[1])`` if you would
                like to interpret the ``cell`` alone (effectively assuming that the ``cell``
                is a primitive one).

        convention : str, default "HPKOT"
            Convention for the definition of the conventional cell. Case-insensitive.
            Supported:

            * "HPKOT" for [1]_
            * "SC" for [2]_
            * "spglib" for |spglib|_

        n : int, default 100
            Number of intermediate points between each pair of the high symmetry points
            (high symmetry points excluded).
        spglib_data : :py:class:`.SyntacticSugar`, optional
            If you need more control on the parameters passed to the spglib, then
            you can get ``spglib_data`` manually and pass it to this function.
            Use wulfric's interface to |spglib|_ as

            .. code-block:: python

                spglib_data = wulfric.get_spglib_data(...)

            using the same ``cell`` and ``atoms["positions"]`` that you are passing to this
            function.


        Notes
        -----
        |spglib|_ uses ``types`` to distinguish the atoms. To see how wulfric deduces the
        ``types`` for given atoms see :py:func:`wulfric.get_spglib_types`.

        If two atoms ``i`` and ``j`` have the same spglib_type (i.e.
        ``atoms["spglib_types"][i] == atoms["spglib_types"][j]``), but they have different
        property that is stored in ``atoms[key]`` (i.e ``atoms[key][i] != atoms[key][j]``),
        then those two atoms are considered equal. In the returned ``conventional_atoms``
        the value of the ``conventional_atoms[key]`` are populated based on the *last* found
        atom in ``atoms`` with each for spglib_type. This rule do not apply to the "positions"
        key.


        References
        ----------
        .. [1] Hinuma, Y., Pizzi, G., Kumagai, Y., Oba, F. and Tanaka, I., 2017.
            Band structure diagram paths based on crystallography.
            Computational Materials Science, 128, pp.140-184.
        .. [2] Setyawan, W. and Curtarolo, S., 2010.
            High-throughput electronic band structure calculations: Challenges and tools.
            Computational materials science, 49(2), pp. 299-312.
        """

        path, points = get_path_and_points(
            cell=cell,
            atoms=atoms,
            spglib_data=spglib_data,
            convention=convention,
            relative=True,
        )

        names = list(points.keys())
        coordinates = list(points.values())
        labels = [HS_PLOT_NAMES[name] for name in names]

        return Kpoints(
            rcell=get_reciprocal(cell=cell),
            coordinates=coordinates,
            names=names,
            labels=labels,
            path=path,
            n=n,
        )

    ################################################################################
    #                            High symmetry points                              #
    ################################################################################
    def add_hs_point(self, name, coordinate, label=None, relative=True) -> None:
        r"""
        Adds high symmetry point.

        Parameters
        ----------
        name : str
            Name of the high symmetry point.
        coordinate : (3,) array-like
            Coordinate of the high symmetry point.
        label : str, optional
            Label of the high symmetry point, ready to be plotted. If ``None``, then
            ``label = name``.
        relative : bool, optional
            Whether to interpret coordinates as relative or absolute.
        """

        if label is None:
            label = name

        if name in self.hs_names:
            raise ValueError(f'Point "{name}" already defined.')

        if not relative:
            # Transform from Cartesian coordinates to relative coordinates.
            coordinate = coordinate @ np.linalg.inv(self.rcell)

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

            .. code-block:: python

                path = [[K1, ..., KN], ...]
        """

        return self._path

    @path.setter
    def path(self, new_path):
        if isinstance(new_path, str):
            new_path = get_path_as_list(path_as_string=new_path)
        elif isinstance(new_path, Iterable):
            tmp_path = new_path
            new_path = []
            for subpath in tmp_path:
                if not isinstance(subpath, Iterable) or len(subpath) < 2:
                    raise ValueError(
                        f'Expected at least two points in each subpath, got "{subpath}"'
                    )

                subpath = [str(name) for name in subpath]
                new_path.append(subpath)

        # Check if all points are defined.
        for subpath in new_path:
            for point in subpath:
                if point not in self.hs_names:
                    raise ValueError(
                        (
                            f"Point '{point}' is not defined. Defined points are:\n  "
                            + "\n  ".join(
                                [
                                    f"{name} : {self.hs_coordinates[name]}"
                                    for name in self.hs_names
                                ]
                            )
                        )
                    )
        self._path = new_path

    @property
    def path_string(self) -> str:
        r"""
        K points path as a string.

        Returns
        -------
        path : str
        """

        return get_path_as_string(path_as_list=self._path)

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
                f'n has to be integer. Given: {new_n} of type "{type(new_n)}"'
            )
        self._n = new_n

    ################################################################################
    #                         Attributes for the axis ticks                        #
    ################################################################################
    @property
    def labels(self) -> list:
        r"""
        Labels of high symmetry points, ready to be plotted.

        For example for point "GAMMA" it returns R"$\Gamma$".

        If there are two high symmetry points following one another in the path,
        it returns "X|Y" where X and Y are the labels of the two high symmetry points.

        Returns
        -------
        labels : (N, ) list of str
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

        Same coordinated as in :py:meth:`.flat_points`.

        Parameters
        ----------
        relative : bool, default False
            Whether to use relative coordinates instead of the absolute ones.

        Returns
        -------
        ticks : (N, ) :numpy:`ndarray`
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
        relative : bool, default False
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

    # It can not just call for points and flatten them,
    # because it has to treat "|" as a special case.
    def flat_points(self, relative=False):
        r"""
        Flatten coordinates of all points with n points between each pair of the high
        symmetry points (high symmetry points excluded).

        Used to plot band structure, dispersion, etc.

        Parameters
        ----------
        relative : bool, default False
            Whether to use relative coordinates instead of the absolute ones.

        Returns
        -------
        flat_points : (N, 3) :numpy:`ndarray`
            Flatten coordinates of all points.
        """

        if relative:
            cell = np.eye(3)
        else:
            cell = self.rcell

        flat_points = None
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
                    flat_points = delta
                else:
                    delta += flat_points[-1]
                    flat_points = np.concatenate((flat_points, delta))
        return flat_points

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
                + f"{'rel_b1':>{d + 3}} "
                + f"{'rel_b2':>{d + 3}} "
                + f"{'rel_b3':>{d + 3}}  "
                + f"{'k_x':>{d + 3}} "
                + f"{'k_y':>{d + 3}} "
                + f"{'k_z':>{d + 3}}"
            )
        ]
        for name in self.hs_names:
            relative = self.hs_coordinates[name]
            i = f"{relative[0]: {d + 3}.{d}f}"
            j = f"{relative[1]: {d + 3}.{d}f}"
            k = f"{relative[2]: {d + 3}.{d}f}"
            absolute = self.hs_coordinates[name] @ self.rcell
            k_x = f"{absolute[0]: {d + 3}.{d}f}"
            k_y = f"{absolute[1]: {d + 3}.{d}f}"
            k_z = f"{absolute[2]: {d + 3}.{d}f}"
            table.append(f"{name:4}  {i} {j} {k}  {k_x} {k_y} {k_z}")
        return "\n".join(table)


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
