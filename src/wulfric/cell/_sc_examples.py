# ================================== LICENSE ===================================
# Wulfric - Cell, Atoms, K-path, visualization.
# Copyright (C) 2023-2026 Andrey Rybakov
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
from math import cos
from math import pi as PI
from math import sin, sqrt

import numpy as np

from wulfric.cell._basic_manipulation import from_params, get_reciprocal
from wulfric.constants._numerical import TORADIANS
from wulfric.constants._sc_convention import SC_BRAVAIS_LATTICE_VARIATIONS

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


# Primitive cell`s construction
def SC_CUB(a: float):
    r"""
    Constructs primitive cubic cell as defined in [1]_.

    .. math::

        \begin{matrix}
            \boldsymbol{a}_1 &=& (a, &0, &0)\\
            \boldsymbol{a}_2 &=& (0, &a, &0)\\
            \boldsymbol{a}_3 &=& (0, &0, &a)
        \end{matrix}

    Parameters
    ----------
    a : float or int
        Length of the three lattice vectors of the conventional cell.

    Returns
    -------
    cell : (3, 3) :numpy:`ndarray`
        Matrix of a primitive cell, rows are interpreted as vectors.

        .. code-block:: python

            cell = [
                [a1_x, a1_y, a1_z],
                [a2_x, a2_y, a2_z],
                [a3_x, a3_y, a3_z],
            ]

    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp. 299-312.

    Examples
    --------

    .. doctest::

        >>> import wulfric
        >>> wulfric.cell.SC_CUB(a=2)
        array([[2, 0, 0],
               [0, 2, 0],
               [0, 0, 2]])
    """

    return np.array([[a, 0, 0], [0, a, 0], [0, 0, a]])


def SC_FCC(a: float):
    r"""
    Constructs primitive face-centred cubic cell as defined in [1]_.

    .. math::

        \begin{matrix}
        \boldsymbol{a}_1 &=& (0, &a/2, &a/2)\\
        \boldsymbol{a}_2 &=& (a/2, &0, &a/2)\\
        \boldsymbol{a}_3 &=& (a/2, &a/2, &0)
        \end{matrix}

    Parameters
    ----------
    a : float
        Length of the three lattice vectors of the conventional cell.

    Returns
    -------
    cell : (3, 3) :numpy:`ndarray`
        Matrix of a primitive cell, rows are interpreted as vectors.

        .. code-block:: python

            cell = [
                [a1_x, a1_y, a1_z],
                [a2_x, a2_y, a2_z],
                [a3_x, a3_y, a3_z],
            ]

    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp. 299-312.

    Examples
    --------

    .. doctest::

        >>> import wulfric
        >>> wulfric.cell.SC_FCC(a=2)
        array([[0., 1., 1.],
               [1., 0., 1.],
               [1., 1., 0.]])
    """

    return np.array([[0, a / 2, a / 2], [a / 2, 0, a / 2], [a / 2, a / 2, 0]])


def SC_BCC(a: float):
    r"""
    Constructs primitive body-centred cubic cell as defined in [1]_.

    .. math::

        \begin{matrix}
        \boldsymbol{a}_1 &=& (-a/2,& a/2,& a/2)\\
        \boldsymbol{a}_2 &=& (a/2, &-a/2,& a/2)\\
        \boldsymbol{a}_3 &=& (a/2, &a/2, &-a/2)
        \end{matrix}

    Parameters
    ----------
    a : float
        Length of the three lattice vectors of the conventional cell.

    Returns
    -------
    cell : (3, 3) :numpy:`ndarray`
        Matrix of a primitive cell, rows are interpreted as vectors.

        .. code-block:: python

            cell = [
                [a1_x, a1_y, a1_z],
                [a2_x, a2_y, a2_z],
                [a3_x, a3_y, a3_z],
            ]

    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp. 299-312.

    Examples
    --------

    .. doctest::

        >>> import wulfric
        >>> wulfric.cell.SC_BCC(a=2)
        array([[-1.,  1.,  1.],
               [ 1., -1.,  1.],
               [ 1.,  1., -1.]])
    """

    return np.array(
        [[-a / 2, a / 2, a / 2], [a / 2, -a / 2, a / 2], [a / 2, a / 2, -a / 2]]
    )


def SC_TET(a: float, c: float):
    r"""
    Constructs primitive tetragonal cell as defined in [1]_.

    .. math::

        \begin{matrix}
        \boldsymbol{a}_1 &=& (a, &0, &0)\\
        \boldsymbol{a}_2 &=& (0, &a, &0)\\
        \boldsymbol{a}_3 &=& (0, &0, &c)
        \end{matrix}

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

            cell = [
                [a1_x, a1_y, a1_z],
                [a2_x, a2_y, a2_z],
                [a3_x, a3_y, a3_z],
            ]

    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp. 299-312.

    Examples
    --------

    .. doctest::

        >>> import wulfric
        >>> wulfric.cell.SC_TET(a=2, c=5)
        array([[2, 0, 0],
               [0, 2, 0],
               [0, 0, 5]])
    """

    return np.array([[a, 0, 0], [0, a, 0], [0, 0, c]])


def SC_BCT(a: float, c: float):
    r"""
    Constructs primitive body-centred tetragonal cell as defined in [1]_.

    .. math::

        \begin{matrix}
        \boldsymbol{a}_1 &=& (-a/2, &a/2, &c/2)\\
        \boldsymbol{a}_2 &=& (a/2, &-a/2, &c/2)\\
        \boldsymbol{a}_3 &=& (a/2, &a/2, &-c/2)
        \end{matrix}

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

            cell = [
                [a1_x, a1_y, a1_z],
                [a2_x, a2_y, a2_z],
                [a3_x, a3_y, a3_z],
            ]

    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp. 299-312.

    Examples
    --------

    .. doctest::

        >>> import wulfric
        >>> wulfric.cell.SC_BCT(a=2, c=5)
        array([[-1. ,  1. ,  2.5],
               [ 1. , -1. ,  2.5],
               [ 1. ,  1. , -2.5]])
    """

    return np.array(
        [[-a / 2, a / 2, c / 2], [a / 2, -a / 2, c / 2], [a / 2, a / 2, -c / 2]]
    )


def SC_ORC(a: float, b: float, c: float):
    r"""
    Constructs primitive orthorhombic cell as defined in [1]_.

    .. math::

        \begin{matrix}
            \boldsymbol{a}_1 &=& (a, &0, &0)\\
            \boldsymbol{a}_2 &=& (0, &b, &0)\\
            \boldsymbol{a}_3 &=& (0, &0, &c)
        \end{matrix}

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

            cell = [
                [a1_x, a1_y, a1_z],
                [a2_x, a2_y, a2_z],
                [a3_x, a3_y, a3_z],
            ]

    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp. 299-312.

    Examples
    --------

    .. doctest::

        >>> import wulfric
        >>> wulfric.cell.SC_ORC(a=3, b=5, c=7)
        array([[3, 0, 0],
               [0, 5, 0],
               [0, 0, 7]])
    """

    return np.array([[a, 0, 0], [0, b, 0], [0, 0, c]])


def SC_ORCF(a: float, b: float, c: float):
    r"""
    Constructs primitive face-centred orthorhombic cell as defined in [1]_.

    .. math::

        \begin{matrix}
            \boldsymbol{a}_1 &=& (0, &b/2, &c/2)\\
            \boldsymbol{a}_2 &=& (a/2, &0, &c/2)\\
            \boldsymbol{a}_3 &=& (a/2, &b/2, &0)
        \end{matrix}

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

            cell = [
                [a1_x, a1_y, a1_z],
                [a2_x, a2_y, a2_z],
                [a3_x, a3_y, a3_z],
            ]

    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp. 299-312.

    Examples
    --------

    .. doctest::

        >>> import wulfric
        >>> wulfric.cell.SC_ORCF(a=3, b=5, c=7)
        array([[0. , 2.5, 3.5],
               [1.5, 0. , 3.5],
               [1.5, 2.5, 0. ]])
    """

    return np.array([[0, b / 2, c / 2], [a / 2, 0, c / 2], [a / 2, b / 2, 0]])


def SC_ORCI(a: float, b: float, c: float):
    r"""
    Constructs primitive body-centred orthorhombic cell as defined in [1]_.

    .. math::

        \begin{matrix}
            \boldsymbol{a}_1 &=& (-a/2, &b/2, &c/2)\\
            \boldsymbol{a}_2 &=& (a/2, &-b/2, &c/2)\\
            \boldsymbol{a}_3 &=& (a/2, &b/2, &-c/2)
        \end{matrix}

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

            cell = [
                [a1_x, a1_y, a1_z],
                [a2_x, a2_y, a2_z],
                [a3_x, a3_y, a3_z],
            ]

    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp. 299-312.

    Examples
    --------

    .. doctest::

        >>> import wulfric
        >>> wulfric.cell.SC_ORCI(a=3, b=5, c=7)
        array([[-1.5,  2.5,  3.5],
               [ 1.5, -2.5,  3.5],
               [ 1.5,  2.5, -3.5]])
    """

    return np.array(
        [[-a / 2, b / 2, c / 2], [a / 2, -b / 2, c / 2], [a / 2, b / 2, -c / 2]]
    )


def SC_ORCC(a: float, b: float, c: float):
    r"""
    Constructs primitive base-centred orthorhombic cell as defined in [1]_.

    .. math::

        \begin{matrix}
            \boldsymbol{a}_1 &=& (a/2, &-b/2, &0)\\
            \boldsymbol{a}_2 &=& (a/2, &b/2, &0)\\
            \boldsymbol{a}_3 &=& (0, &0, &c)
        \end{matrix}

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

            cell = [
                [a1_x, a1_y, a1_z],
                [a2_x, a2_y, a2_z],
                [a3_x, a3_y, a3_z],
            ]

    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp. 299-312.

    Examples
    --------

    .. doctest::

        >>> import wulfric
        >>> wulfric.cell.SC_ORCC(a=3, b=5, c=7)
        array([[ 1.5, -2.5,  0. ],
               [ 1.5,  2.5,  0. ],
               [ 0. ,  0. ,  7. ]])
    """

    return np.array([[a / 2, -b / 2, 0], [a / 2, b / 2, 0], [0, 0, c]])


def SC_HEX(a: float, c: float):
    r"""
    Constructs primitive hexagonal cell as defined in [1]_.

    .. math::

        \begin{matrix}
            \boldsymbol{a}_1 &=& (\frac{a}{2}, &\frac{-a\sqrt{3}}{2}, &0)\\
            \boldsymbol{a}_2 &=& (\frac{a}{2}, &\frac{a\sqrt{3}}{2}, &0)\\
            \boldsymbol{a}_3 &=& (0, &0, &c)
        \end{matrix}

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

            cell = [
                [a1_x, a1_y, a1_z],
                [a2_x, a2_y, a2_z],
                [a3_x, a3_y, a3_z],
            ]

    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp. 299-312.

    Examples
    --------

    .. doctest::

        >>> import wulfric
        >>> wulfric.cell.SC_HEX(a=3, c=5)
        array([[ 1.5       , -2.59807621,  0.        ],
               [ 1.5       ,  2.59807621,  0.        ],
               [ 0.        ,  0.        ,  5.        ]])
    """

    return np.array(
        [[a / 2, -a * sqrt(3) / 2, 0], [a / 2, a * sqrt(3) / 2, 0], [0, 0, c]]
    )


def SC_RHL(a: float, alpha: float):
    r"""
    Constructs primitive rhombohedral cell as defined in [1]_.

    .. math::

        \begin{matrix}
            \boldsymbol{a}_1 &=& (a\cos(\alpha / 2), &-a\sin(\alpha/2), &0)\\
            \boldsymbol{a}_2 &=& (a\cos(\alpha / 2), &a\sin(\alpha/2), &0)\\
            \boldsymbol{a}_3 &=& \left(\dfrac{\cos\alpha}{\cos(\alpha/2)}\right.,
            &0, &\left.a\sqrt{1 - \dfrac{\cos^2\alpha}{\cos^2(\alpha/2)}}\right)
        \end{matrix}

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

            cell = [
                [a1_x, a1_y, a1_z],
                [a2_x, a2_y, a2_z],
                [a3_x, a3_y, a3_z],
            ]

    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp. 299-312.

    Examples
    --------

    .. doctest::

        >>> import wulfric
        >>> wulfric.cell.SC_RHL(a=3, alpha=40)
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


def SC_MCL(a: float, b: float, c: float, alpha: float):
    r"""
    Constructs primitive monoclinic cell as defined in [1]_.

    .. math::

        \begin{matrix}
            \boldsymbol{a}_1 &=& (a, &0, &0)\\
            \boldsymbol{a}_2 &=& (0, &b, &0)\\
            \boldsymbol{a}_3 &=& (0, &c\cos\alpha, &c\sin\alpha)
        \end{matrix}

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

            cell = [
                [a1_x, a1_y, a1_z],
                [a2_x, a2_y, a2_z],
                [a3_x, a3_y, a3_z],
            ]

    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp. 299-312.

    Examples
    --------

    .. doctest::

        >>> import wulfric
        >>> wulfric.cell.SC_MCL(a=3, b=5, c=7, alpha=45)
        array([[3.        , 0.        , 0.        ],
               [0.        , 5.        , 0.        ],
               [0.        , 4.94974747, 4.94974747]])
    """

    alpha *= TORADIANS
    return np.array([[a, 0, 0], [0, b, 0], [0, c * cos(alpha), c * sin(alpha)]])


def SC_MCLC(a: float, b: float, c: float, alpha: float):
    r"""
    Constructs primitive base-centred monoclinic cell as defined in [1]_.

    .. math::

        \begin{matrix}
            \boldsymbol{a}_1 &=& (a/2, &b/2, &0)\\
            \boldsymbol{a}_2 &=& (-a/2, &b/2, &0)\\
            \boldsymbol{a}_3 &=& (0, &c\cos\alpha, &c\sin\alpha)
        \end{matrix}

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

            cell = [
                [a1_x, a1_y, a1_z],
                [a2_x, a2_y, a2_z],
                [a3_x, a3_y, a3_z],
            ]

    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp. 299-312.

    Examples
    --------

    .. doctest::

        >>> import wulfric
        >>> wulfric.cell.SC_MCLC(a=3, b=5, c=7, alpha=45)
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


def SC_TRI(
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

    .. math::

        \begin{matrix}
            \boldsymbol{a}_1 &=& (a, &0, &0)\\
            \boldsymbol{a}_2 &=& (b\cos\gamma, &b\sin\gamma, &0)\\
            \boldsymbol{a}_3 &=& (c\cos\beta, &\dfrac{c(\cos\alpha - \cos\beta\cos\gamma)}{\sin\gamma}, &\dfrac{c}{\sin\gamma}\sqrt{\sin^2\gamma - \cos^2\alpha - \cos^2\beta + 2\cos\alpha\cos\beta\cos\gamma})
        \end{matrix}

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

            cell = [
                [a1_x, a1_y, a1_z],
                [a2_x, a2_y, a2_z],
                [a3_x, a3_y, a3_z],
            ]

    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp. 299-312.

    Examples
    --------

    .. doctest::

        >>> import wulfric
        >>> wulfric.cell.SC_TRI(a=3, b=5, c=7, alpha=45, beta=33, gamma=21)
        array([[ 3.        ,  0.        ,  0.        ],
               [ 4.66790213,  1.79183975,  0.        ],
               [ 5.87069398, -1.48176621,  3.51273699]])
    """

    cell = from_params(a, b, c, alpha, beta, gamma)
    if input_reciprocal:
        cell = get_reciprocal(cell)

    return cell


def sc_get_example(lattice_variation: str = None):
    r"""
    Examples of the Bravais lattices as defined in the paper by Setyawan and Curtarolo [1]_.

    .. versionchanged:: 0.6.3 renamed from ``sc_get_example_cell``.

    Parameters
    ----------
    lattice_variation : str, optional
        Name of the lattice type or variation to be returned. For available names see
        documentation of each :ref:`user-guide_conventions_bravais-lattices`.
        Case-insensitive.

    Returns
    -------
    cell : (3, 3) :numpy:`ndarray`
        Matrix of a direct cell, rows are interpreted as vectors.

        .. code-block:: python

            cell = [
                [a1_x, a1_y, a1_z],
                [a2_x, a2_y, a2_z],
                [a3_x, a3_y, a3_z],
            ]

    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp. 299-312.

    Examples
    --------

    .. doctest::

        >>> import wulfric
        >>> wulfric.cell.sc_get_example("cub")
        array([[3.14159265, 0.        , 0.        ],
               [0.        , 3.14159265, 0.        ],
               [0.        , 0.        , 3.14159265]])
        >>> wulfric.cell.sc_get_example("ORCF3")
        array([[0.        , 1.96349541, 2.61799388],
               [1.57079633, 0.        , 2.61799388],
               [1.57079633, 1.96349541, 0.        ]])
    """

    correct_inputs = set(map(lambda x: x.lower(), SC_BRAVAIS_LATTICE_VARIATIONS)).union(
        set(
            map(
                lambda x: x.translate(str.maketrans("", "", "12345ab")).lower(),
                SC_BRAVAIS_LATTICE_VARIATIONS,
            )
        )
    )

    if (
        not isinstance(lattice_variation, str)
        or lattice_variation.lower() not in correct_inputs
    ):
        message = (
            f'There is no example of "{lattice_variation}" Bravais lattice. '
            "Available examples are:\n"
        )
        for name in correct_inputs:
            message += f"  * {name}\n"
        raise ValueError(message)

    lattice_variation = lattice_variation.lower()

    if lattice_variation == "cub":
        cell = SC_CUB(PI)
    elif lattice_variation == "fcc":
        cell = SC_FCC(PI)
    elif lattice_variation == "bcc":
        cell = SC_BCC(PI)
    elif lattice_variation == "tet":
        cell = SC_TET(PI, 1.5 * PI)
    elif lattice_variation in ["bct1", "bct"]:
        cell = SC_BCT(1.5 * PI, PI)
    elif lattice_variation == "bct2":
        cell = SC_BCT(PI, 1.5 * PI)
    elif lattice_variation == "orc":
        cell = SC_ORC(PI, 1.5 * PI, 2 * PI)
    elif lattice_variation in ["orcf1", "orcf"]:
        cell = SC_ORCF(0.7 * PI, 5 / 4 * PI, 5 / 3 * PI)
    elif lattice_variation == "orcf2":
        cell = SC_ORCF(1.2 * PI, 5 / 4 * PI, 5 / 3 * PI)
    elif lattice_variation == "orcf3":
        cell = SC_ORCF(PI, 5 / 4 * PI, 5 / 3 * PI)
    elif lattice_variation == "orci":
        return SC_ORCI(PI, 1.3 * PI, 1.7 * PI)
    elif lattice_variation == "orcc":
        cell = SC_ORCC(PI, 1.3 * PI, 1.7 * PI)
    elif lattice_variation == "hex":
        cell = SC_HEX(PI, 2 * PI)
    elif lattice_variation in ["rhl1", "rhl"]:
        # If alpha = 60 it is effectively FCC!
        cell = SC_RHL(PI, 70)
    elif lattice_variation == "rhl2":
        cell = SC_RHL(PI, 110)
    elif lattice_variation == "mcl":
        cell = SC_MCL(PI, 1.3 * PI, 1.6 * PI, alpha=75)
    elif lattice_variation in ["mclc1", "mclc"]:
        cell = SC_MCLC(PI, 1.4 * PI, 1.7 * PI, 80)
    elif lattice_variation == "mclc2":
        cell = SC_MCLC(1.4 * PI * sin(75 * TORADIANS), 1.4 * PI, 1.7 * PI, 75)
    elif lattice_variation == "mclc3":
        b = PI
        x = 1.1
        alpha = 78
        ralpha = alpha * TORADIANS
        c = b * (x**2) / (x**2 - 1) * cos(ralpha) * 1.8
        a = x * b * sin(ralpha)
        cell = SC_MCLC(a, b, c, alpha)
    elif lattice_variation == "mclc4":
        b = PI
        x = 1.2
        alpha = 65
        ralpha = alpha * TORADIANS
        c = b * (x**2) / (x**2 - 1) * cos(ralpha)
        a = x * b * sin(ralpha)
        cell = SC_MCLC(a, b, c, alpha)
    elif lattice_variation == "mclc5":
        b = PI
        x = 1.4
        alpha = 53
        ralpha = alpha * TORADIANS
        c = b * (x**2) / (x**2 - 1) * cos(ralpha) * 0.9
        a = x * b * sin(ralpha)
        cell = SC_MCLC(a, b, c, alpha)
    elif lattice_variation in ["tri1a", "tri1", "tri", "tria"]:
        cell = SC_TRI(0.5, 0.5, 0.5, 50.0, 60.0, 80.0)
    elif lattice_variation in ["tri2a", "tri2"]:
        cell = SC_TRI(0.5, 1.0, 1.0, 100.0, 100.0, 140.0)
    elif lattice_variation in ["tri1b", "trib"]:
        cell = SC_TRI(0.5, 1.0, 1.0, 100.0, 110.0, 60.0)
    elif lattice_variation == "tri2b":
        cell = SC_TRI(0.5, 1.0, 2.0, 80.0, 100.0, 40.0)

    return cell


# Deprecated in 0.6.3
# TODO:REMOVE in April of 2025
def sc_get_example_cell(lattice_variation: str = None):
    import warnings

    warnings.warn(
        "wulfric.cell.sc_get_example_cell has been renamed to wulfric.cell.sc_get_example in v0.6.3 release. This function with an old name will be removed in April of 2026.",
        DeprecationWarning,
    )

    return sc_get_example(lattice_variation=lattice_variation)


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
