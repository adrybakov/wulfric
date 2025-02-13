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


from math import cos, sin, sqrt

import numpy as np

from wulfric.cell._basic_manipulation import from_params, get_reciprocal
from wulfric.constants import TORADIANS

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


# Primitive cell`s construction
def CUB(a: float):
    r"""
    Constructs primitive cubic cell as defined in [1]_.

    See :ref:`guide_cub` for the definition of primitive and conventional cells.

    Parameters
    ----------
    a : float or int
        Length of the three lattice vectors of the conventional cell.

    Returns
    -------
    cell : (3, 3) :numpy:`ndarray`
        Matrix of a primitive cell, rows are interpreted as vectors.

        .. code-block:: python

            cell = [[a1_x, a1_y, a1_z],
                    [a2_x, a2_y, a2_z],
                    [a3_x, a3_y, a3_z]]

    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp. 299-312.

    Examples
    --------

    .. doctest::

        >>> import wulfric as wulf
        >>> wulf.cell.CUB(a=2)
        array([[2, 0, 0],
               [0, 2, 0],
               [0, 0, 2]])
    """

    return np.array([[a, 0, 0], [0, a, 0], [0, 0, a]])


def FCC(a: float):
    r"""
    Constructs primitive face-centred cubic cell as defined in [1]_.

    See :ref:`guide_fcc` for the definition of primitive and conventional cells.

    Parameters
    ----------
    a : float
        Length of the three lattice vectors of the conventional cell.

    Returns
    -------
    cell : (3, 3) :numpy:`ndarray`
        Matrix of a primitive cell, rows are interpreted as vectors.

        .. code-block:: python

            cell = [[a1_x, a1_y, a1_z],
                    [a2_x, a2_y, a2_z],
                    [a3_x, a3_y, a3_z]]

    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp. 299-312.

    Examples
    --------

    .. doctest::

        >>> import wulfric as wulf
        >>> wulf.cell.FCC(a=2)
        array([[0., 1., 1.],
               [1., 0., 1.],
               [1., 1., 0.]])
    """

    return np.array([[0, a / 2, a / 2], [a / 2, 0, a / 2], [a / 2, a / 2, 0]])


def BCC(a: float):
    r"""
    Constructs primitive body-centred cubic cell as defined in [1]_.

    See :ref:`guide_bcc` for the definition of primitive and conventional cells.

    Parameters
    ----------
    a : float
        Length of the three lattice vectors of the conventional cell.

    Returns
    -------
    cell : (3, 3) :numpy:`ndarray`
        Matrix of a primitive cell, rows are interpreted as vectors.

        .. code-block:: python

            cell = [[a1_x, a1_y, a1_z],
                    [a2_x, a2_y, a2_z],
                    [a3_x, a3_y, a3_z]]

    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp. 299-312.

    Examples
    --------

    .. doctest::

        >>> import wulfric as wulf
        >>> wulf.cell.BCC(a=2)
        array([[-1.,  1.,  1.],
               [ 1., -1.,  1.],
               [ 1.,  1., -1.]])
    """

    return np.array(
        [[-a / 2, a / 2, a / 2], [a / 2, -a / 2, a / 2], [a / 2, a / 2, -a / 2]]
    )


def TET(a: float, c: float):
    r"""
    Constructs primitive tetragonal cell as defined in [1]_.

    See :ref:`guide_tet` for the definition of primitive and conventional cells.

    Parameters
    ----------
    a : float
        Length of the first two lattice vectors of the conventional cell.
    c : float
        Length of the third lattice vector of the conventional cell.

    Returns
    -------
    cell : (3, 3) :numpy:`ndarray`
        Matrix of a primitive cell, rows are interpreted as vectors.

        .. code-block:: python

            cell = [[a1_x, a1_y, a1_z],
                    [a2_x, a2_y, a2_z],
                    [a3_x, a3_y, a3_z]]

    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp. 299-312.

    Examples
    --------

    .. doctest::

        >>> import wulfric as wulf
        >>> wulf.cell.TET(a=2, c=5)
        array([[2, 0, 0],
               [0, 2, 0],
               [0, 0, 5]])
    """

    return np.array([[a, 0, 0], [0, a, 0], [0, 0, c]])


def BCT(a: float, c: float):
    r"""
    Constructs primitive body-centred tetragonal cell as defined in [1]_.

    See :ref:`guide_bct` for the definition of primitive and conventional cells.

    Parameters
    ----------
    a : float
        Length of the first two lattice vectors of the conventional cell.
    c : float
        Length of the third lattice vector of the conventional cell.

    Returns
    -------
    cell : (3, 3) :numpy:`ndarray`
        Matrix of a primitive cell, rows are interpreted as vectors.

        .. code-block:: python

            cell = [[a1_x, a1_y, a1_z],
                    [a2_x, a2_y, a2_z],
                    [a3_x, a3_y, a3_z]]

    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp. 299-312.

    Examples
    --------

    .. doctest::

        >>> import wulfric as wulf
        >>> wulf.cell.BCT(a=2, c=5)
        array([[-1. ,  1. ,  2.5],
               [ 1. , -1. ,  2.5],
               [ 1. ,  1. , -2.5]])
    """

    return np.array(
        [[-a / 2, a / 2, c / 2], [a / 2, -a / 2, c / 2], [a / 2, a / 2, -c / 2]]
    )


def ORC(a: float, b: float, c: float):
    r"""
    Constructs primitive orthorhombic cell as defined in [1]_.

    See :ref:`guide_orc` for the definition of primitive and conventional cells.

    Input values are used as they are, therefore, the cell might not be a standard
    primitive one.

    Parameters
    ----------
    a : float
        Length of the first lattice vector of the conventional cell.
    b : float
        Length of the second lattice vector of the conventional cell.
    c : float
        Length of the third lattice vector of the conventional cell.

    Returns
    -------
    cell : (3, 3) :numpy:`ndarray`
        Matrix of a primitive cell, rows are interpreted as vectors.

        .. code-block:: python

            cell = [[a1_x, a1_y, a1_z],
                    [a2_x, a2_y, a2_z],
                    [a3_x, a3_y, a3_z]]

    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp. 299-312.

    Examples
    --------

    .. doctest::

        >>> import wulfric as wulf
        >>> wulf.cell.ORC(a=3, b=5, c=7)
        array([[3, 0, 0],
               [0, 5, 0],
               [0, 0, 7]])
    """

    return np.array([[a, 0, 0], [0, b, 0], [0, 0, c]])


def ORCF(a: float, b: float, c: float):
    r"""
    Constructs primitive face-centred orthorhombic cell as defined in [1]_.

    See :ref:`guide_orcf` for the definition of primitive and conventional cells.

    Input values are used as they are, therefore, the cell might not be a standard
    primitive one.

    Parameters
    ----------
    a : float
        Length of the first lattice vector of the conventional cell.
    b : float
        Length of the second lattice vector of the conventional cell.
    c : float
        Length of the third lattice vector of the conventional cell.

    Returns
    -------
    cell : (3, 3) :numpy:`ndarray`
        Matrix of a primitive cell, rows are interpreted as vectors.

        .. code-block:: python

            cell = [[a1_x, a1_y, a1_z],
                    [a2_x, a2_y, a2_z],
                    [a3_x, a3_y, a3_z]]

    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp. 299-312.

    Examples
    --------

    .. doctest::

        >>> import wulfric as wulf
        >>> wulf.cell.ORCF(a=3, b=5, c=7)
        array([[0. , 2.5, 3.5],
               [1.5, 0. , 3.5],
               [1.5, 2.5, 0. ]])
    """

    return np.array([[0, b / 2, c / 2], [a / 2, 0, c / 2], [a / 2, b / 2, 0]])


def ORCI(a: float, b: float, c: float):
    r"""
    Constructs primitive body-centred orthorhombic cell as defined in [1]_.

    See :ref:`guide_orci` for the definition of primitive and conventional cells.

    Input values are used as they are, therefore, the cell might not be a standard
    primitive one.

    Parameters
    ----------
    a : float
        Length of the first lattice vector of the conventional cell.
    b : float
        Length of the second lattice vector of the conventional cell.
    c : float
        Length of the third lattice vector of the conventional cell.

    Returns
    -------
    cell : (3, 3) :numpy:`ndarray`
        Matrix of a primitive cell, rows are interpreted as vectors.

        .. code-block:: python

            cell = [[a1_x, a1_y, a1_z],
                    [a2_x, a2_y, a2_z],
                    [a3_x, a3_y, a3_z]]

    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp. 299-312.

    Examples
    --------

    .. doctest::

        >>> import wulfric as wulf
        >>> wulf.cell.ORCI(a=3, b=5, c=7)
        array([[-1.5,  2.5,  3.5],
               [ 1.5, -2.5,  3.5],
               [ 1.5,  2.5, -3.5]])
    """

    return np.array(
        [[-a / 2, b / 2, c / 2], [a / 2, -b / 2, c / 2], [a / 2, b / 2, -c / 2]]
    )


def ORCC(a: float, b: float, c: float):
    r"""
    Constructs primitive base-centred orthorhombic cell as defined in [1]_.

    See :ref:`guide_orcc` for the definition of primitive and conventional cells.

    Input values are used as they are, therefore, the cell might not be a standard
    primitive one.

    Parameters
    ----------
    a : float
        Length of the first lattice vector of the conventional cell.
    b : float
        Length of the second lattice vector of the conventional cell.
    c : float
        Length of the third lattice vector of the conventional cell.

    Returns
    -------
    cell : (3, 3) :numpy:`ndarray`
        Matrix of a primitive cell, rows are interpreted as vectors.

        .. code-block:: python

            cell = [[a1_x, a1_y, a1_z],
                    [a2_x, a2_y, a2_z],
                    [a3_x, a3_y, a3_z]]

    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp. 299-312.

    Examples
    --------

    .. doctest::

        >>> import wulfric as wulf
        >>> wulf.cell.ORCC(a=3, b=5, c=7)
        array([[ 1.5, -2.5,  0. ],
               [ 1.5,  2.5,  0. ],
               [ 0. ,  0. ,  7. ]])
    """

    return np.array([[a / 2, -b / 2, 0], [a / 2, b / 2, 0], [0, 0, c]])


def HEX(a: float, c: float):
    r"""
    Constructs primitive hexagonal cell as defined in [1]_.

    See :ref:`guide_hex` for the definition of primitive and conventional cells.

    Parameters
    ----------
    a : float
        Length of the first two lattice vectors of the conventional cell.
    c : float
        Length of the third lattice vector of the conventional cell.

    Returns
    -------
    cell : (3, 3) :numpy:`ndarray`
        Matrix of a primitive cell, rows are interpreted as vectors.

        .. code-block:: python

            cell = [[a1_x, a1_y, a1_z],
                    [a2_x, a2_y, a2_z],
                    [a3_x, a3_y, a3_z]]

    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp. 299-312.

    Examples
    --------

    .. doctest::

        >>> import wulfric as wulf
        >>> wulf.cell.HEX(a=3, c=5)
        array([[ 1.5       , -2.59807621,  0.        ],
               [ 1.5       ,  2.59807621,  0.        ],
               [ 0.        ,  0.        ,  5.        ]])
    """

    return np.array(
        [[a / 2, -a * sqrt(3) / 2, 0], [a / 2, a * sqrt(3) / 2, 0], [0, 0, c]]
    )


def RHL(a: float, alpha: float):
    r"""
    Constructs primitive rhombohedral cell as defined in [1]_.

    See :ref:`guide_rhl` for the definition of primitive and conventional cells.

    Input values are used as they are, therefore, the cell might not be a standard
    primitive one.

    Parameters
    ----------
    a : float
        Length of the lattice vectors of the conventional cell.
    alpha : float
        Angle between vectors :math:`a_2` and :math:`a_3` of the conventional cell in
        degrees.

    Returns
    -------
    cell : (3, 3) :numpy:`ndarray`
        Matrix of a primitive cell, rows are interpreted as vectors.

        .. code-block:: python

            cell = [[a1_x, a1_y, a1_z],
                    [a2_x, a2_y, a2_z],
                    [a3_x, a3_y, a3_z]]

    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp. 299-312.

    Examples
    --------

    .. doctest::

        >>> import wulfric as wulf
        >>> wulf.cell.RHL(a=3, alpha=40)
        array([[ 2.81907786, -1.02606043,  0.        ],
               [ 2.81907786,  1.02606043,  0.        ],
               [ 2.44562241,  0.        ,  1.73750713]])
    """

    alpha *= TORADIANS
    return np.array(
        [
            [a * cos(alpha / 2), -a * sin(alpha / 2), 0],
            [a * cos(alpha / 2), a * sin(alpha / 2), 0],
            [
                a * cos(alpha) / cos(alpha / 2),
                0,
                a * sqrt(1 - cos(alpha) ** 2 / cos(alpha / 2) ** 2),
            ],
        ]
    )


def MCL(a: float, b: float, c: float, alpha: float):
    r"""
    Constructs primitive monoclinic cell as defined in [1]_.

    See :ref:`guide_mcl` for the definition of primitive and conventional cells.

    Input values are used as they are, therefore, the cell might not be a standard
    primitive one.

    Parameters
    ----------
    a : float
        Length of the first lattice vector of the conventional cell.
    b : float
        Length of the second of the two remaining lattice vectors of the conventional
        cell.
    c : float
        Length of the third of the two remaining lattice vectors of the conventional cell.
    alpha : float
        Angle between vectors :math:`a_2` and :math:`a_3` of the conventional cell in
        degrees.

    Returns
    -------
    cell : (3, 3) :numpy:`ndarray`
        Matrix of a primitive cell, rows are interpreted as vectors.

        .. code-block:: python

            cell = [[a1_x, a1_y, a1_z],
                    [a2_x, a2_y, a2_z],
                    [a3_x, a3_y, a3_z]]

    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp. 299-312.

    Examples
    --------

    .. doctest::

        >>> import wulfric as wulf
        >>> wulf.cell.MCL(a=3, b=5, c=7, alpha = 45)
        array([[3.        , 0.        , 0.        ],
               [0.        , 5.        , 0.        ],
               [0.        , 4.94974747, 4.94974747]])
    """

    alpha *= TORADIANS
    return np.array([[a, 0, 0], [0, b, 0], [0, c * cos(alpha), c * sin(alpha)]])


def MCLC(a: float, b: float, c: float, alpha: float):
    r"""
    Constructs primitive base-centred monoclinic cell as defined in [1]_.

    See :ref:`guide_mclc` for the definition of primitive and conventional cells.

    Input values are used as they are, therefore, the cell might not be a standard
    primitive one.

    Parameters
    ----------
    a : float
        Length of the first lattice vector of the conventional cell.
    b : float
        Length of the second of the two remaining lattice vectors of the conventional
        cell.
    c : float
        Length of the third of the two remaining lattice vectors of the conventional
        cell.
    alpha : float
        Angle between vectors :math:`a_2` and :math:`a_3` of the conventional cell in
        degrees.

    Returns
    -------
    cell : (3, 3) :numpy:`ndarray`
        Matrix of a primitive cell, rows are interpreted as vectors.

        .. code-block:: python

            cell = [[a1_x, a1_y, a1_z],
                    [a2_x, a2_y, a2_z],
                    [a3_x, a3_y, a3_z]]

    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp. 299-312.

    Examples
    --------

    .. doctest::

        >>> import wulfric as wulf
        >>> wulf.cell.MCLC(a=3, b=5, c=7, alpha = 45)
        array([[ 1.5       ,  2.5       ,  0.        ],
               [-1.5       ,  2.5       ,  0.        ],
               [ 0.        ,  4.94974747,  4.94974747]])
    """

    alpha *= TORADIANS
    return np.array(
        [
            [a / 2, b / 2, 0],
            [-a / 2, b / 2, 0],
            [0, c * cos(alpha), c * sin(alpha)],
        ]
    )


def TRI(
    a: float,
    b: float,
    c: float,
    alpha: float,
    beta: float,
    gamma: float,
    input_reciprocal=False,
):
    r"""
    Constructs primitive triclinic cell as defined in [1]_.

    See :ref:`guide_tri` for the definition of primitive and conventional cells.

    Parameters
    ----------
    a : float
        Length of the first lattice vector of the conventional cell.
    b : float
        Length of the second lattice vector of the conventional cell.
    c : float
        Length of the third lattice vector of the conventional cell.
    alpha : float
        Angle between vectors :math:`a_2` and :math:`a_3` of the conventional cell in
        degrees.
    beta : float
        Angle between vectors :math:`a_1` and :math:`a_3` of the conventional cell in
        degrees.
    gamma : float
        Angle between vectors :math:`a_1` and :math:`a_2` of the conventional cell in
        degrees.
    input_reciprocal : bool, default False
        Whether to interpret input as reciprocal parameters.

    Returns
    -------
    cell : (3, 3) :numpy:`ndarray`
        Matrix of a primitive cell, rows are interpreted as vectors.

        .. code-block:: python

            cell = [[a1_x, a1_y, a1_z],
                    [a2_x, a2_y, a2_z],
                    [a3_x, a3_y, a3_z]]

    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp. 299-312.

    Examples
    --------

    .. doctest::

        >>> import wulfric as wulf
        >>> wulf.cell.TRI(a=3, b=5, c=7, alpha = 45, beta = 33, gamma = 21)
        array([[ 3.        ,  0.        ,  0.        ],
               [ 4.66790213,  1.79183975,  0.        ],
               [ 5.87069398, -1.48176621,  3.51273699]])
    """

    cell = from_params(a, b, c, alpha, beta, gamma)
    if input_reciprocal:
        cell = get_reciprocal(cell)

    return cell


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
