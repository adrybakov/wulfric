# WULFRIC - Crystal, Lattice, Atoms, K-path.
# Copyright (C) 2023 Andrey Rybakov
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

from math import cos, sqrt

import numpy as np

from wulfric.constants import TODEGREES, TORADIANS
from wulfric.numerical import ABS_TOL, ABS_TOL_ANGLE, compare_numerically

__all__ = ["volume", "angle", "parallelepiped_check", "absolute_to_relative"]


def volume(*args):
    r"""
    Computes volume.

    Three type of arguments are expected:

    * One argument.
        Matrix ``cell``.
        Volume is computed as:

        .. math::
            V = v_1 \cdot (v_2 \times v_3)
    * Three arguments.
        Vectors ``v1``, ``v2``, ``v3``.
        Volume is computed as:

        .. math::
            V = v_1 \cdot (v_2 \times v_3)
    * Six arguments.
        Parameters ``a``, ``b``, ``c``, ``alpha``, ``beta``, ``gamma``.
        Volume is computed as:

        .. math::
            V = abc\sqrt{1+2\cos(\alpha)\cos(\beta)\cos(\gamma)-\cos^2(\alpha)-\cos^2(\beta)-\cos^2(\gamma)}


    Parameters
    ----------
    v1 : (3,) |array-like|_
        First vector.
    v2 : (3,) |array-like|_
        Second vector.
    v3 : (3,) |array-like|_
        Third vector.
    cell : (3,3) |array-like|_
        Cell matrix, rows are interpreted as vectors.
    a : float, default 1
        Length of the :math:`v_1` vector.
    b : float, default 1
        Length of the :math:`v_2` vector.
    c : float, default 1
        Length of the :math:`v_3` vector.
    alpha : float, default 90
        Angle between vectors :math:`v_2` and :math:`v_3`. In degrees.
    beta : float, default 90
        Angle between vectors :math:`v_1` and :math:`v_3`. In degrees.
    gamma : float, default 90
        Angle between vectors :math:`v_1` and :math:`v_2`. In degrees.

    Returns
    -------
    volume : float
        Volume of corresponding region in space.
    """

    if len(args) == 1:
        cell = np.array(args[0])
    elif len(args) == 3:
        cell = np.array(args)
    elif len(args) == 6:
        a, b, c, alpha, beta, gamma = args
        alpha = alpha * TORADIANS
        beta = beta * TORADIANS
        gamma = gamma * TORADIANS
        sq_root = (
            1
            + 2 * cos(alpha) * cos(beta) * cos(gamma)
            - cos(alpha) ** 2
            - cos(beta) ** 2
            - cos(gamma) ** 2
        )
        return a * b * c * sqrt(sq_root)
    else:
        raise ValueError(
            "Unable to identify input. "
            + "Supported: one (3,3) array-like, or three (3,) array-like, or 6 floats."
        )

    return abs(np.linalg.det(cell))


def angle(v1, v2, radians=False):
    r"""
    Angle between two vectors.

    .. math::

        \alpha = \dfrac{(\vec{v_1} \cdot \vec{v_2})}{\vert\vec{v_1}\vert\cdot\vert\vec{v_2}\vert}

    Parameters
    ----------
    v1 : (3,) |array-like|_
        First vector.
    v2 : (3,) |array-like|_
        Second vector.
    radians : bool, default False
        Whether to return value in radians.

    Returns
    -------
    angle: float
        Angle in degrees or radians (see ``radians``).

    Raises
    ------
    ValueError
        If one of the vectors is zero vector (or both). Norm is compared against
        :numpy:`finfo`\ (float).eps.
    """

    # Normalize vectors
    v1_norm = np.linalg.norm(v1)
    v2_norm = np.linalg.norm(v2)
    if abs(v1_norm) <= np.finfo(float).eps or abs(v2_norm) <= np.finfo(float).eps:
        raise ValueError("Angle is ill defined (zero vector).")

    v1 = np.array(v1) / v1_norm
    v2 = np.array(v2) / v2_norm

    alpha = np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0))
    if radians:
        return alpha
    return alpha * TODEGREES


def parallelepiped_check(a, b, c, alpha, beta, gamma, raise_error=False):
    r"""
    Check if parallelepiped is valid.

    The following checks are performed:

    * :math:`a > 0`
    * :math:`b > 0`
    * :math:`c > 0`
    * :math:`0 < \alpha < 180`
    * :math:`0 < \beta < 180`
    * :math:`0 < \gamma < 180`
    * :math:`\gamma < \alpha + \beta < 360 - \gamma`
    * :math:`\beta < \alpha + \gamma < 360 - \beta`
    * :math:`\alpha < \beta + \gamma < 360 - \alpha`

    Parameters
    ----------
    a : float
        Length of the :math:`v_1` vector.
    b : float
        Length of the :math:`v_2` vector.
    c : float
        Length of the :math:`v_3` vector.
    alpha : float
        Angle between vectors :math:`v_2` and :math:`v_3`. In degrees.
    beta : float
        Angle between vectors :math:`v_1` and :math:`v_3`. In degrees.
    gamma : float
        Angle between vectors :math:`v_1` and :math:`v_2`. In degrees.
    raise_error : bool, default False
        Whether to raise error if parameters can not form a parallelepiped.

    Returns
    -------
    result: bool
        Whether the parameters could from a parallelepiped.

    Raises
    ------
    ValueError
        If parameters could not form a parallelepiped.
        Only raised if ``raise_error`` is ``True`` (it is ``False`` by default).
    """

    result = (
        compare_numerically(a, ">", 0.0, ABS_TOL)
        and compare_numerically(b, ">", 0.0, ABS_TOL)
        and compare_numerically(c, ">", 0.0, ABS_TOL)
        and compare_numerically(alpha, "<", 180.0, ABS_TOL_ANGLE)
        and compare_numerically(beta, "<", 180.0, ABS_TOL_ANGLE)
        and compare_numerically(gamma, "<", 180.0, ABS_TOL_ANGLE)
        and compare_numerically(alpha, ">", 0.0, ABS_TOL_ANGLE)
        and compare_numerically(beta, ">", 0.0, ABS_TOL_ANGLE)
        and compare_numerically(gamma, ">", 0.0, ABS_TOL_ANGLE)
        and compare_numerically(gamma, "<", alpha + beta, ABS_TOL_ANGLE)
        and compare_numerically(alpha + beta, "<", 360.0 - gamma, ABS_TOL_ANGLE)
        and compare_numerically(beta, "<", alpha + gamma, ABS_TOL_ANGLE)
        and compare_numerically(alpha + gamma, "<", 360.0 - beta, ABS_TOL_ANGLE)
        and compare_numerically(alpha, "<", beta + gamma, ABS_TOL_ANGLE)
        and compare_numerically(beta + gamma, "<", 360.0 - alpha, ABS_TOL_ANGLE)
    )

    if not result and raise_error:
        message = "Parameters could not form a parallelepiped:\n"
        message += f"a = {a}"
        if not compare_numerically(a, ">", 0.0, ABS_TOL):
            message += f" (a <= 0 with numerical tolerance: {ABS_TOL})"
        message += "\n"
        message += f"b = {b}"
        if not compare_numerically(b, ">", 0.0, ABS_TOL):
            message += f" (b <= 0 with numerical tolerance: {ABS_TOL})"
        message += "\n"
        message += f"c = {c}"
        if not compare_numerically(c, ">", 0.0, ABS_TOL):
            message += f" (c <= 0 with numerical tolerance: {ABS_TOL})"
        message += "\n"
        message += f"alpha = {alpha}\n"
        if not compare_numerically(alpha, "<", 180.0, ABS_TOL_ANGLE):
            message += f"  (alpha >= 180 with numerical tolerance: {ABS_TOL_ANGLE})\n"
        if not compare_numerically(alpha, ">", 0.0, ABS_TOL_ANGLE):
            message += f"  (alpha <= 0 with numerical tolerance: {ABS_TOL_ANGLE})\n"
        message += f"beta = {beta}\n"
        if not compare_numerically(beta, "<", 180.0, ABS_TOL_ANGLE):
            message += f"  (beta >= 180 with numerical tolerance: {ABS_TOL_ANGLE})\n"
        if not compare_numerically(beta, ">", 0.0, ABS_TOL_ANGLE):
            message += f"  (beta <= 0 with numerical tolerance: {ABS_TOL_ANGLE})\n"
        message += f"gamma = {gamma}\n"
        if not compare_numerically(gamma, "<", 180.0, ABS_TOL_ANGLE):
            message += f"  (gamma >= 180 with numerical tolerance: {ABS_TOL_ANGLE})\n"
        if not compare_numerically(gamma, ">", 0.0, ABS_TOL_ANGLE):
            message += f"  (gamma <= 0 with numerical tolerance: {ABS_TOL_ANGLE})\n"
        if not compare_numerically(gamma, "<", alpha + beta, ABS_TOL_ANGLE):
            message += f"Inequality gamma < alpha + beta is not satisfied with numerical tolerance: {ABS_TOL_ANGLE}\n"
        if not compare_numerically(alpha + beta, "<", 360.0 - gamma, ABS_TOL_ANGLE):
            message += f"Inequality alpha + beta < 360 - gamma is not satisfied with numerical tolerance: {ABS_TOL_ANGLE}\n"
        if not compare_numerically(beta, "<", alpha + gamma, ABS_TOL_ANGLE):
            message += f"Inequality beta < alpha + gamma is not satisfied with numerical tolerance: {ABS_TOL_ANGLE}\n"
        if not compare_numerically(alpha + gamma, "<", 360.0 - beta, ABS_TOL_ANGLE):
            message += f"Inequality alpha + gamma < 360 - beta is not satisfied with numerical tolerance: {ABS_TOL_ANGLE}\n"
        if not compare_numerically(alpha, "<", beta + gamma, ABS_TOL_ANGLE):
            message += f"Inequality alpha < beta + gamma is not satisfied with numerical tolerance: {ABS_TOL_ANGLE}\n"
        if not compare_numerically(beta + gamma, "<", 360.0 - alpha, ABS_TOL_ANGLE):
            message += f"Inequality beta + gamma < 360 - alpha is not satisfied with numerical tolerance: {ABS_TOL_ANGLE}\n"
        raise ValueError(message)

    return result


def absolute_to_relative(vector, basis):
    r"""
    Compute relative coordinates of the vector with respect to the basis.

    .. math::
        \vec{v} = v_1 \vec{e_1} + v_2 \vec{e_2} + v_3 \vec{e_3}

    We compute scalar products of the vector with the basis vectors:

    .. math::
        \begin{matrix}
        \vec{v} \cdot \vec{e_1} = v_1 \vec{e_1} \cdot \vec{e_1} + v_2 \vec{e_2} \cdot \vec{e_1} + v_3 \vec{e_3} \cdot \vec{e_1} \\
        \vec{v} \cdot \vec{e_2} = v_1 \vec{e_1} \cdot \vec{e_2} + v_2 \vec{e_2} \cdot \vec{e_2} + v_3 \vec{e_3} \cdot \vec{e_2} \\
        \vec{v} \cdot \vec{e_3} = v_1 \vec{e_1} \cdot \vec{e_3} + v_2 \vec{e_2} \cdot \vec{e_3} + v_3 \vec{e_3} \cdot \vec{e_3}
        \end{matrix}

    Which leads to the system of linear equations for :math:`v_1`, :math:`v_2`, :math:`v_3`.

    Parameters
    ----------
    vector : (3,) |array-like|_
        Absolute coordinates of a vector.
    basis : (3, 3) |array-like|_
        Basis vectors. Rows are interpreted as vectors.
        Columns are interpreted as coordinates.

    Returns
    -------
    relative : (3,) :numpy:`ndarray`
        Relative coordinates of the ``vector`` with respect to the ``basis``.
    """

    # Three vectors of the basis
    e1 = np.array(basis[0], dtype=float)
    e2 = np.array(basis[1], dtype=float)
    e3 = np.array(basis[2], dtype=float)

    v = np.array(vector, dtype=float)
    if (v == np.zeros(3)).all():
        return np.zeros(3)

    # Compose system of linear equations
    B = np.array([np.dot(e1, v), np.dot(e2, v), np.dot(e3, v)])
    A = np.array(
        [
            [np.dot(e1, e1), np.dot(e1, e2), np.dot(e1, e3)],
            [np.dot(e2, e1), np.dot(e2, e2), np.dot(e2, e3)],
            [np.dot(e3, e1), np.dot(e3, e2), np.dot(e3, e3)],
        ]
    )

    # Solve and return
    return np.linalg.solve(A, B)
