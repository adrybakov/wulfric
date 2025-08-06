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
import numpy as np

from wulfric.geometry._geometry import absolute_to_relative

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def shift_atoms(
    atoms, gravity_point=(0.5, 0.5, 0.5), cell=None, gp_is_relative=True
) -> None:
    R"""
    Shifts all atoms with the same vector in a way
    that the ``gravity_point`` is located in the middle between minimum and maximum
    relative coordinates of the atoms, individually for each lattice vector.

    I.e. if there is one atom in the cell, then it is placed in the center of the cell
    for ``gravity_point`` = (0.5, 0.5, 0.5).

    Modifies given ``atoms`` dictionary.

    Parameters
    ----------
    atoms : dict
        Dictionary with atoms. Must have a ``"positions"`` with value of (N,3) |array-like|_.
    gravity_point : (3,) |array-like|_, default (0.5, 0.5, 0.5)
        Relative coordinates of the gravity point.
    cell : (3, 3) |array-like|_, optional
        Matrix of a cell, rows are interpreted as vectors. Required if
        ``gp_is_relative = False``.
    gp_is_relative : bool, default True
        Whether the ``gravity_point`` is given in relative coordinates.

    Examples
    --------

    .. doctest::

        >>> import wulfric as wulf
        >>> cell = [[2, 0, 0], [0, 2, 0], [0, 0, 2]]
        >>> atoms = {
        ...     "names": ["Cr1", "Cr2"],
        ...     "positions": [[0.0, 0.0, 0.0], [0.5, 0.5, 1.0]],
        ... }
        >>> wulf.crystal.shift_atoms(atoms=atoms, gravity_point=(0.5, 0.5, 0.5))
        >>> for i in range(len(atoms["names"])):
        ...     print(atoms["names"][i], atoms["positions"][i])
        Cr1 [0.25 0.25 0.  ]
        Cr2 [0.75 0.75 1.  ]
        >>> wulf.crystal.shift_atoms(
        ...     atoms, gravity_point=(1, 1, 1), cell=cell, gp_is_relative=False
        ... )
        >>> for i in range(len(atoms["names"])):
        ...     print(atoms["names"][i], atoms["positions"][i])
        Cr1 [0.25 0.25 0.  ]
        Cr2 [0.75 0.75 1.  ]
    """

    if not gp_is_relative:
        if cell is None:
            raise ValueError("cell is required if gp_is_relative False")

        gravity_point = absolute_to_relative(gravity_point, cell)

    min_coord = np.min(atoms["positions"], axis=0)
    max_coord = np.max(atoms["positions"], axis=0)
    shift = (max_coord + min_coord) / 2

    atoms["positions"] = [
        position - shift + gravity_point for position in atoms["positions"]
    ]


def cure_negative(atoms) -> None:
    R"""
    Shifts all atoms with the same vector in a way
    that all relative coordinates becomes non-negative.

    Modifies given ``atoms`` dictionary.

    Parameters
    ----------
    atoms : dict
        Dictionary with atoms. Must have a ``"positions"`` with value of (N,3) |array-like|_.

    Examples
    --------

    .. doctest::

        >>> import wulfric as wulf
        >>> cell = [[2, 0, 0], [0, 2, 0], [0, 0, 2]]
        >>> atoms = {
        ...     "names": ["Cr1", "Cr2"],
        ...     "positions": [[-0.5, 0.5, 0.0], [0.1, 0.5, 0.0]],
        ... }
        >>> wulf.crystal.cure_negative(atoms)
        >>> for i in range(len(atoms["names"])):
        ...     print(atoms["names"][i], atoms["positions"][i])
        Cr1 [0.  0.5 0. ]
        Cr2 [0.6 0.5 0. ]
    """

    min_values = atoms["positions"][0]
    for position in atoms["positions"][1:]:
        min_values = np.minimum(min_values, position)

    shift = np.where(min_values < 0, -min_values, 0)

    atoms["positions"] = [position + shift for position in atoms["positions"]]


def ensure_000(atoms) -> None:
    r"""
    Ensures that all atoms are from (0,0,0) unit cell.

    In other word ensures that all relative coordinates of all atoms are :math:`\in [0,1]`.input

    Parameters
    ----------
    atoms : dict
        Dictionary with atoms. Must have a ``"positions"`` with value of (N,3) |array-like|_.

    Examples
    --------

    .. doctest::

        >>> import wulfric as wulf
        >>> atoms = {"positions": [[0, 0.5, 0], [1.25, 0, -0.52], [0.25, -0.65, 2.375]]}
        >>> for p in atoms["positions"]:
        ...     print(p)
        [0, 0.5, 0]
        [1.25, 0, -0.52]
        [0.25, -0.65, 2.375]
        >>> wulf.crystal.ensure_000(atoms)
        >>> for p in atoms["positions"]:
        ...     print(p)
        [0, 0.5, 0]
        [0.25, 0, 0.48]
        [0.25, 0.35, 0.375]
    """

    for i in range(len(atoms["positions"])):
        for j in range(3):
            poscomp = atoms["positions"][i][j]

            # Ensure -1 < poscomp < 1
            poscomp -= int(poscomp)

            # Ensure 0 <= poscomp <= 1
            if poscomp < 0:
                poscomp += 1

            atoms["positions"][i][j] = poscomp


def get_vector(
    cell, atoms, atom1, atom2, R=(0, 0, 0), return_relative=False
) -> np.ndarray:
    r"""
    Computes a vector from atom1 (from (0,0,0)) to atom2 (from (i,j,k)).

    Parameters
    ----------
    cell : (3, 3) |array-like|_,
        Matrix of a cell, rows are interpreted as vectors.
    atoms : dict
        Dictionary with atoms. Must have a ``"positions"`` with value of (N,3) |array-like|_.
    atom1 : int
        Index of the first atom in ``atoms["positions"]``.
    atom2 : int
        Index of the second atom in ``atoms["positions"]``.
    R : (3,) tuple of int, default (0, 0, 0)
        Radius vector of the unit cell for atom2 (i,j,k).
    return_relative : bool, default False
        Whether to return vector relative to the ``cell``.

    Returns
    -------
    v : (3,) :numpy:`ndarray`
        Vector from atom1 in (0,0,0) cell to atom2 in R cell.

    Examples
    --------

    .. doctest::

        >>> import wulfric as wulf
        >>> cell = [[1, 0, 0], [0, 2, 0], [0, 0, 3]]
        >>> atoms = {"positions": [[0.5, 0, 0], [0, 0, 0.5]]}
        >>> wulf.crystal.get_vector(cell, atoms, atom1=0, atom2=1, R=(0, 0, 0))
        array([-0.5,  0. ,  1.5])
        >>> wulf.crystal.get_vector(cell, atoms, atom1=0, atom2=1, R=(1, 0, 0))
        array([0.5, 0. , 1.5])
        >>> wulf.crystal.get_vector(cell, atoms, atom1=0, atom2=1, R=(1, 0, -3))
        array([ 0.5,  0. , -7.5])
        >>> wulf.crystal.get_vector(
        ...     cell, atoms, atom1=0, atom2=1, R=(1, 0, -3), return_relative=True
        ... )
        array([ 0.5,  0. , -2.5])
    """

    relative_vector = (
        np.array(R, dtype=float) + atoms["positions"][atom2] - atoms["positions"][atom1]
    )

    if return_relative:
        return relative_vector

    return relative_vector @ cell


def get_distance(cell, atoms, atom1, atom2, R=(0, 0, 0)) -> float:
    r"""
    Computes distance between atom1 (from (0,0,0)) and atom2 (from (i,j,k)).

    Parameters
    ----------
    cell : (3, 3) |array-like|_,
        Matrix of a cell, rows are interpreted as vectors.
    atoms : dict
        Dictionary with atoms. Must have a ``"positions"`` with value of (N,3) |array-like|_.
    atom1 : int
        Index of the first atom in ``atoms["positions"]``.
    atom2 : int
        Index of the second atom in ``atoms["positions"]``.
    R : (3,) tuple of int, default (0, 0, 0)
        Radius vector of the unit cell for atom2 (i,j,k).

    Returns
    -------
    distance : float
        Distance between atom1 in (0,0,0) cell and atom2 in R cell.

    Examples
    --------

    .. doctest::

        >>> import wulfric as wulf
        >>> cell = [[1, 0, 0], [0, 2, 0], [0, 0, 3]]
        >>> atoms = {"positions": [[0.5, 0, 0], [0, 0, 0.5]]}
        >>> round(
        ...     wulf.crystal.get_distance(cell, atoms, atom1=0, atom2=1, R=(0, 0, 0)), 8
        ... )
        1.58113883
        >>> round(
        ...     wulf.crystal.get_distance(cell, atoms, atom1=0, atom2=1, R=(1, 0, 0)), 8
        ... )
        1.58113883
        >>> round(
        ...     wulf.crystal.get_distance(cell, atoms, atom1=0, atom2=1, R=(1, 0, -3)),
        ...     8,
        ... )
        7.51664819
    """

    return float(
        np.linalg.norm(
            get_vector(
                cell=cell,
                atoms=atoms,
                atom1=atom1,
                atom2=atom2,
                R=R,
                return_relative=False,
            )
        )
    )


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
