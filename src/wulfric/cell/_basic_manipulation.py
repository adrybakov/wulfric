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


from math import cos
from math import pi as PI
from math import sin, sqrt

import numpy as np

from wulfric.constants._numerical import TORADIANS
from wulfric.geometry._geometry import get_angle, get_volume, parallelepiped_check

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def get_reciprocal(cell):
    r"""
    Computes reciprocal cell.

    Parameters
    ----------
    cell : (3, 3) |array-like|_
        Cell matrix, rows are interpreted as vectors.

    Returns
    -------
    reciprocal_cell : (3, 3) :numpy:`ndarray`
        Reciprocal cell matrix, rows are interpreted as vectors.
        :math:`cell = (\boldsymbol{v}_1, \boldsymbol{v}_2, \boldsymbol{v}_3)^T`, where

        .. math::

            \begin{matrix}
                \boldsymbol{b}_1 = \dfrac{2\pi}{V}\boldsymbol{a}_2\times\boldsymbol{a}_3 \\
                \boldsymbol{b}_2 = \dfrac{2\pi}{V}\boldsymbol{a}_3\times\boldsymbol{a}_1 \\
                \boldsymbol{b}_3 = \dfrac{2\pi}{V}\boldsymbol{a}_1\times\boldsymbol{a}_2 \\
            \end{matrix}

    """

    return 2 * PI * np.linalg.inv(cell).T


def from_params(a=1.0, b=1.0, c=1.0, alpha=90.0, beta=90.0, gamma=90.0):
    r"""
    Constructs cell from lattice parameters.

    *   Lattice vector :math:`\boldsymbol{a_1}` has the length ``a`` and oriented along
        :math:`{\cal x}` axis.
    *   Lattice vector :math:`\boldsymbol{a_2}` has the length ``b`` and is placed in
        :math:`{\cal xy}` plane and form an angle ``gamma`` with vector
        :math:`\boldsymbol{a_1}`, positive in a mathematical sense.
    *   Lattice vector :math:`\boldsymbol{a_3}` has the length ``c`` and form an angle
        ``alpha`` with the vector :math:`\boldsymbol{a_2}` and an angle ``beta`` with
        the vector :math:`\boldsymbol{a_1}`.

    Parameters
    ----------
    a : float, default 1
        Length of the :math:`\boldsymbol{a_1}` vector.
    b : float, default 1
        Length of the :math:`\boldsymbol{a_2}` vector.
    c : float, default 1
        Length of the :math:`\boldsymbol{a_3}` vector.
    alpha : float, default 90
        Angle between vectors :math:`\boldsymbol{a_2}` and :math:`\boldsymbol{a_3}`. In degrees.
    beta : float, default 90
        Angle between vectors :math:`\boldsymbol{a_1}` and :math:`\boldsymbol{a_3}`. In degrees.
    gamma : float, default 90
        Angle between vectors :math:`\boldsymbol{a_1}` and :math:`\boldsymbol{a_2}`. In degrees.

    Returns
    -------
    cell : (3, 3) :numpy:`ndarray`
        Cell matrix.

        .. code-block:: python

            cell = [[a1_x, a1_y, a1_z],
                    [a2_x, a2_y, a2_z],
                    [a3_x, a3_y, a3_z]]

    Raises
    ------
    ValueError
        If parameters could not form a parallelepiped.

    See Also
    --------
    parallelepiped_check : Check if parameters could form a parallelepiped.
    """
    parallelepiped_check(a, b, c, alpha, beta, gamma, raise_error=True)
    alpha = alpha * TORADIANS
    beta = beta * TORADIANS
    gamma = gamma * TORADIANS
    return np.array(
        [
            [a, 0, 0],
            [b * cos(gamma), b * sin(gamma), 0],
            [
                c * cos(beta),
                c / sin(gamma) * (cos(alpha) - cos(beta) * cos(gamma)),
                c
                / sin(gamma)
                * sqrt(
                    1
                    + 2 * cos(alpha) * cos(beta) * cos(gamma)
                    - cos(alpha) ** 2
                    - cos(beta) ** 2
                    - cos(gamma) ** 2
                ),
            ],
        ],
        dtype=float,
    )


def get_params(cell):
    r"""
    Computes lattice parameters of the cell.

    Parameters
    ----------
    cell : (3,3) |array-like|_
        Cell matrix, rows are interpreted as vectors.

        .. code-block:: python

            cell = [[a1x, a1y, a1z],
                    [a2x, a2y, a2z],
                    [a3x, a3y, a3z]]

    Returns
    -------
    a : float
        Length of the :math:`\boldsymbol{a_1}` vector.
    b : float
        Length of the :math:`\boldsymbol{a_2}` vector.
    c : float
        Length of the :math:`\boldsymbol{a_3}` vector.
    alpha : float
        Angle between vectors :math:`\boldsymbol{a_2}` and :math:`\boldsymbol{a_3}`. In degrees.
    beta : float
        Angle between vectors :math:`\boldsymbol{a_1}` and :math:`\boldsymbol{a_3}`. In degrees.
    gamma : float
        Angle between vectors :math:`\boldsymbol{a_1}` and :math:`\boldsymbol{a_2}`. In degrees.

    Examples
    --------

    .. doctest::

        >>> import wulfric as wulf
        >>> cell = [[1,0,0],[0,2,0],[0,0,3]]
        >>> wulf.cell.get_params(cell)
        (1.0, 2.0, 3.0, 90.0, 90.0, 90.0)
    """

    return (
        float(np.linalg.norm(cell[0])),
        float(np.linalg.norm(cell[1])),
        float(np.linalg.norm(cell[2])),
        get_angle(cell[1], cell[2]),
        get_angle(cell[0], cell[2]),
        get_angle(cell[0], cell[1]),
    )


def get_scalar_products(cell):
    r"""
    Returns pairwise scalar products of the lattice vectors:

    * :math:`\boldsymbol{a}_2\cdot\boldsymbol{a}_3`
    * :math:`\boldsymbol{a}_1\cdot\boldsymbol{a}_3`
    * :math:`\boldsymbol{a}_1\cdot\boldsymbol{a}_2`

    Parameters
    ----------
    cell : (3, 3) |array-like|_
        Cell matrix, rows are interpreted as vectors.

    Returns
    -------
    sp_23 : float
        Scalar product of the vectors :math:`\boldsymbol{a}_2` and
        :math:`\boldsymbol{a}_3`.
    sp_13 : float
        Scalar product of the vectors :math:`\boldsymbol{a}_1` and
        :math:`\boldsymbol{a}_3`.
    sp_12 : float
        Scalar product of the vectors :math:`\boldsymbol{a}_1` and
        :math:`\boldsymbol{a}_2`.
    """

    return (
        float(np.dot(cell[1], cell[2])),
        float(np.dot(cell[0], cell[2])),
        float(np.dot(cell[0], cell[1])),
    )


def is_reasonable(cell, eps_lengths=1e-10, eps_volume=1e-5):
    r"""
    Check if the cell is *reasonable* (not *degenerate*) in the sense of [1]_.
    Routines of wulfric are tested for reasonable cells and should work as expected if the
    cell is reasonable. Below we recall the definition of *reasonable* cell from [1]_:

    The sell is *degenerate* if

    (i)   The minimum of the cell lengths divided by the maximum of the cell lengths is
          smaller than a certain factor :math:`\varepsilon_{lengths}`.
    (ii)  The unit-cell volume divided by the minimum of the cell
          lengths is smaller than a certain factor :math:`\varepsilon_{volume}`.

    The cell is *reasonable* if it is *not degenerate*.

    Wulfric is tested for reasonable cells with default values of ``eps_lengths`` and
    ``eps_volume``.


    Parameters
    ----------
    cell : (3,3) |array-like|_
        Rows are vectors.
    eps_lengths : float, default 1e-10
        Default value of :math:`\varepsilon_{lengths}`. We leave the option to change it,
        but do not recommend to do it unless you know exactly what you are doing and what
        the result would mean for the functionalities of the whole package.
    eps_volume : float, default 1e-5
        Default value of :math:`\varepsilon_{volume}`. We leave the option to change it,
        but do not recommend to do it unless you know exactly what you are doing and what
        the result would mean for the functionalities of the whole package.

    Returns
    -------
    reasonable : bool
        ``True`` if the cell is *reasonable*, ``False`` if cell is *degenerate*.

    References
    ----------
    .. [1] Grosse-Kunstleve, R.W., Sauter, N.K. and Adams, P.D., 2004.
        Numerically stable algorithms for the computation of reduced unit cells.
        Acta Crystallographica Section A: Foundations of Crystallography,
        60(1), pp.1-6.
    """

    cell_volume = get_volume(cell)

    # To guarantee finite max and min lengths
    if cell_volume == 0.0:
        return False

    min_length = np.linalg.norm(cell, axis=1).min()
    max_length = np.linalg.norm(cell, axis=1).max()

    if max_length == 0.0 or min_length / max_length < eps_lengths:
        return False

    if min_length == 0.0 or cell_volume / min_length < eps_volume:
        return False

    return True


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
