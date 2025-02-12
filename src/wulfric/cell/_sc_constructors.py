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
    Construct cubic primitive cell.

    See :ref:`guide_cub` for the definition of primitive and conventional cells.

    Parameters
    ----------
    a : float or int
        Length of the all three lattice vectors of the conventional cell.

    Returns
    -------
    cell : (3, 3) :numpy:`ndarray`
        Rows are lattice vectors.
    """

    return np.array([[a, 0, 0], [0, a, 0], [0, 0, a]])


def FCC(a: float):
    r"""
    Construct face-centred cubic primitive cell.

    See :ref:`guide_fcc` for the definition of primitive and conventional cells.

    Parameters
    ----------
    a : float
        Length of the all three lattice vectors of the conventional cell.

    Returns
    -------
    cell : (3, 3) :numpy:`ndarray`
        Rows are lattice vectors.
    """

    return np.array([[0, a / 2, a / 2], [a / 2, 0, a / 2], [a / 2, a / 2, 0]])


def BCC(a: float):
    r"""
    Construct body-centred cubic primitive cell.

    See :ref:`guide_bcc` for the definition of primitive and conventional cells.

    Parameters
    ----------
    a : float
        Length of the all three lattice vectors of the conventional cell.

    Returns
    -------
    cell : (3, 3) :numpy:`ndarray`
        Rows are lattice vectors.
    """

    return np.array(
        [[-a / 2, a / 2, a / 2], [a / 2, -a / 2, a / 2], [a / 2, a / 2, -a / 2]]
    )


def TET(a: float, c: float):
    r"""
    Construct tetragonal primitive cell.

    See :ref:`guide_tet` for the definition of primitive and conventional cells.

    Parameters
    ----------
    a : float
        Length of the two equal lattice vectors of the conventional cell.
    c : float
        Length of the third lattice vector of the conventional cell.

    Returns
    -------
    cell : (3, 3) :numpy:`ndarray`
        Rows are lattice vectors.
    """

    return np.array([[a, 0, 0], [0, a, 0], [0, 0, c]])


def BCT(a: float, c: float):
    r"""
    Construct body-centred tetragonal primitive cell.

    See :ref:`guide_bct` for the definition of primitive and conventional cells.

    Parameters
    ----------
    a : float
        Length of the two equal lattice vectors of the conventional cell.
    c : float
        Length of the third lattice vector of the conventional cell.

    Returns
    -------
    cell : (3, 3) :numpy:`ndarray`
        Rows are lattice vectors.
    """

    return np.array(
        [[-a / 2, a / 2, c / 2], [a / 2, -a / 2, c / 2], [a / 2, a / 2, -c / 2]]
    )


def ORC(a: float, b: float, c: float):
    r"""
    Construct orthorhombic primitive cell.

    See :ref:`guide_orc` for the definition of primitive and conventional cells.

    Order: :math:`a < b < c`. Input is reordered if necessary.

    Parameters
    ----------
    a : float
        Length of the smallest lattice vector of the conventional cell.
    b : float
        Length of the medium lattice vector of the conventional cell.
    c : float
        Length of the largest lattice vector of the conventional cell.

    Returns
    -------
    cell : (3, 3) :numpy:`ndarray`
        Rows are lattice vectors.
    """

    a, b, c = tuple(sorted([a, b, c]))

    return np.array([[a, 0, 0], [0, b, 0], [0, 0, c]])


def ORCF(a: float, b: float, c: float):
    r"""
    Construct face-centred orthorhombic primitive cell.

    See :ref:`guide_orcf` for the definition of primitive and conventional cells.

    Order: :math:`a < b < c`. Input is reordered if necessary.

    Parameters
    ----------
    a : float
        Length of the smallest lattice vector of the conventional cell.
    b : float
        Length of the medium lattice vector of the conventional cell.
    c : float
        Length of the largest lattice vector of the conventional cell.

    Returns
    -------
    cell : (3, 3) :numpy:`ndarray`
        Rows are lattice vectors.
    """

    a, b, c = tuple(sorted([a, b, c]))

    return np.array([[0, b / 2, c / 2], [a / 2, 0, c / 2], [a / 2, b / 2, 0]])


def ORCI(a: float, b: float, c: float):
    r"""
    Construct body-centred orthorhombic primitive cell.

    See :ref:`guide_orci` for the definition of primitive and conventional cells.

    Order: :math:`a < b < c`. Input is reordered if necessary.

    Parameters
    ----------
    a : float
        Length of the smallest lattice vector of the conventional cell.
    b : float
        Length of the medium lattice vector of the conventional cell.
    c : float
        Length of the largest lattice vector of the conventional cell.

    Returns
    -------
    cell : (3, 3) :numpy:`ndarray`
        Rows are lattice vectors.
    """

    a, b, c = tuple(sorted([a, b, c]))

    return np.array(
        [[-a / 2, b / 2, c / 2], [a / 2, -b / 2, c / 2], [a / 2, b / 2, -c / 2]]
    )


def ORCC(a: float, b: float, c: float):
    r"""
    Construct base-centred orthorhombic primitive cell.

    See :ref:`guide_orcc` for the definition of primitive and conventional cells.

    Order: :math:`a < b < c`. Input is reordered if necessary.

    Parameters
    ----------
    a : float
        Length of the smallest lattice vector of the conventional cell.
    b : float
        Length of the medium lattice vector of the conventional cell.
    c : float
        Length of the largest lattice vector of the conventional cell.

    Returns
    -------
    cell : (3, 3) :numpy:`ndarray`
        Rows are lattice vectors.
    """

    a, b = tuple(sorted([a, b]))

    return np.array([[a / 2, -b / 2, 0], [a / 2, b / 2, 0], [0, 0, c]])


def HEX(a: float, c: float):
    r"""
    Construct hexagonal primitive cell.

    See :ref:`guide_hex` for the definition of primitive and conventional cells.

    Parameters
    ----------
    a : float
        Length of the lattice vector of the conventional cell.
    c : float
        Length of the lattice vector of the conventional cell.

    Returns
    -------
    cell : (3, 3) :numpy:`ndarray`
        Rows are lattice vectors.
    """

    return np.array(
        [[a / 2, -a * sqrt(3) / 2, 0], [a / 2, a * sqrt(3) / 2, 0], [0, 0, c]]
    )


def RHL(a: float, alpha: float):
    r"""
    Construct rhombohedral primitive cell.

    See :ref:`guide_rhl` for the definition of primitive and conventional cells.

    Condition :math:`\alpha < 120^{\circ}` is assumed.

    Parameters
    ----------
    a : float
        Length of the lattice vector of the conventional cell.
    alpha : float
        Angle between vectors :math:`a_2` and :math:`a_3` of the conventional cell. In degrees.

    Returns
    -------
    cell : (3, 3) :numpy:`ndarray`
        Rows are lattice vectors.
    """

    if alpha >= 120:
        raise ValueError("alpha has to be < 120 degrees.")

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
    Construct monoclinic primitive cell.

    See :ref:`guide_mcl` for the definition of primitive and conventional cells.

    Order: :math:`b \le c`, :math:`\alpha < 90^{\circ}`. Input is reordered if necessary.

    Parameters
    ----------
    a : float
        Length of the first lattice vector of the conventional cell. (The one oriented along x axis)
    b : float
        Length of the shorter of the two remaining lattice vectors of the conventional cell.
    c : float
        Length of the longer of the two remaining lattice vectors of the conventional cell.
    alpha : float
        Angle between vectors :math:`a_2` and :math:`a_3` of the conventional cell. In degrees.

    Returns
    -------
    cell : (3, 3) :numpy:`ndarray`
        Rows are lattice vectors.
    """

    b, c = tuple(sorted([b, c]))
    if alpha > 90:
        alpha = 180 - alpha

    alpha *= TORADIANS
    return np.array([[a, 0, 0], [0, b, 0], [0, c * cos(alpha), c * sin(alpha)]])


def MCLC(a: float, b: float, c: float, alpha: float):
    r"""
    Construct base-centred monoclinic primitive cell.

    See :ref:`guide_mclc` for the definition of primitive and conventional cells.

    Order: :math:`b \le c`, :math:`\alpha < 90^{\circ}`. Input is reordered if necessary.

    Parameters
    ----------
    a : float
        Length of the first lattice vector of the conventional cell. (The one oriented along x axis)
    b : float
        Length of the shorter of the two remaining lattice vectors of the conventional cell.
    c : float
        Length of the longer of the two remaining lattice vectors of the conventional cell.
    alpha : float
        Angle between vectors :math:`a_2` and :math:`a_3` of the conventional cell. In degrees.

    Returns
    -------
    cell : (3, 3) :numpy:`ndarray`
        Rows are lattice vectors.
    """

    b, c = tuple(sorted([b, c]))
    if alpha > 90:
        alpha = 180.0 - alpha

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
    Construct triclinic primitive cell.

    See :ref:`guide_tri` for the definition of primitive and conventional cells.

    Parameters
    ----------
    a : float
        Length of the lattice vector of the conventional cell.
    b : float
        Length of the lattice vector of the conventional cell.
    c : float
        Length of the lattice vector of the conventional cell.
    alpha : float
        Angle between vectors :math:`a_2` and :math:`a_3` of the conventional cell. In degrees.
    beta : float
        Angle between vectors :math:`a_1` and :math:`a_3` of the conventional cell. In degrees.
    gamma : float
        Angle between vectors :math:`a_1` and :math:`a_2` of the conventional cell. In degrees.
    input_reciprocal : bool, default False
        Whether to interpret input as reciprocal parameters.

    Returns
    -------
    cell : (3, 3) :numpy:`ndarray`
        Rows are lattice vectors.
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
