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

from wulfric._exceptions import NiggliReductionFailed
from wulfric._numerical import compare_numerically
from wulfric.geometry._geometry import get_volume

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def _niggli_step_1(A, B, C, xi, eta, zeta, trans_matrix, eps):
    condition = compare_numerically(A, ">", B, eps=eps) or (
        compare_numerically(A, "==", B, eps=eps)
        and compare_numerically(abs(xi), ">", abs(eta), eps=eps)
    )
    if condition:
        trans_matrix = trans_matrix @ np.array(
            [
                [0, -1, 0],
                [-1, 0, 0],
                [0, 0, -1],
            ],
            dtype=int,
        )

        A, xi, B, eta = B, eta, A, xi

    return condition, (A, B, C, xi, eta, zeta), trans_matrix


def _niggli_step_2(A, B, C, xi, eta, zeta, trans_matrix, eps):
    condition = compare_numerically(B, ">", C, eps=eps) or (
        compare_numerically(B, "==", C, eps=eps)
        and compare_numerically(abs(eta), ">", abs(zeta), eps=eps)
    )
    if condition:
        trans_matrix = trans_matrix @ np.array(
            [
                [-1, 0, 0],
                [0, 0, -1],
                [0, -1, 0],
            ],
            dtype=int,
        )

        B, eta, C, zeta = C, zeta, B, eta

    return condition, (A, B, C, xi, eta, zeta), trans_matrix


def _niggli_step_3(A, B, C, xi, eta, zeta, trans_matrix, eps):
    condition = compare_numerically(xi * eta * zeta, ">", 0, eps=eps)
    if condition:
        if compare_numerically(xi, ">", 0, eps=eps):
            i = 1
        else:
            i = -1

        if compare_numerically(eta, ">", 0, eps=eps):
            j = 1
        else:
            j = -1

        if compare_numerically(zeta, ">", 0, eps=eps):
            k = 1
        else:
            k = -1

        trans_matrix = trans_matrix @ np.array(
            [
                [i, 0, 0],
                [0, j, 0],
                [0, 0, k],
            ],
            dtype=int,
        )

        xi, eta, zeta = abs(xi), abs(eta), abs(zeta)

    return condition, (A, B, C, xi, eta, zeta), trans_matrix


def _niggli_step_4(A, B, C, xi, eta, zeta, trans_matrix, eps):
    condition = compare_numerically(xi * eta * zeta, "<=", 0, eps=eps)
    if condition:
        # Step 1
        i, j, k = 1, 1, 1
        p = None

        # Step 2
        if compare_numerically(xi, ">", 0):
            i = -1
        elif not compare_numerically(xi, "<", 0):
            p = "i"

        # Step 3
        if compare_numerically(eta, ">", 0):
            j = -1
        elif not compare_numerically(eta, "<", 0):
            p = "j"

        # Step 4
        if compare_numerically(zeta, ">", 0):
            k = -1
        elif not compare_numerically(zeta, "<", 0):
            p = "k"

        # Step 5
        if i * j * k < 0 and p is not None:
            if p == "i":
                i = -1
            elif p == "j":
                j = -1
            elif p == "k":
                k = -1

        trans_matrix = trans_matrix @ np.array(
            [
                [i, 0, 0],
                [0, j, 0],
                [0, 0, k],
            ],
            dtype=int,
        )

        xi, eta, zeta = -abs(xi), -abs(eta), -abs(zeta)

    return condition, (A, B, C, xi, eta, zeta), trans_matrix


def _niggli_step_5(A, B, C, xi, eta, zeta, trans_matrix, eps):
    condition = (
        compare_numerically(abs(xi), ">", B, eps=eps)
        or (
            compare_numerically(xi, "==", B, eps=eps)
            and compare_numerically(2 * eta, "<", zeta, eps=eps)
        )
        or (
            compare_numerically(xi, "==", -B, eps=eps)
            and compare_numerically(zeta, "<", 0, eps=eps)
        )
    )
    if condition:
        trans_matrix = trans_matrix @ np.array(
            [
                [1, 0, 0],
                [0, 1, -np.sign(xi)],
                [0, 0, 1],
            ],
            dtype=int,
        )

        C = B + C - xi * np.sign(xi)
        eta = eta - zeta * np.sign(xi)
        xi = xi - 2 * B * np.sign(xi)

    return condition, (A, B, C, xi, eta, zeta), trans_matrix


def _niggli_step_6(A, B, C, xi, eta, zeta, trans_matrix, eps):
    condition = (
        compare_numerically(abs(eta), ">", A, eps=eps)
        or (
            compare_numerically(eta, "==", A, eps=eps)
            and compare_numerically(2 * xi, "<", zeta, eps=eps)
        )
        or (
            compare_numerically(eta, "==", -A, eps=eps)
            and compare_numerically(zeta, "<", 0, eps=eps)
        )
    )
    if condition:
        trans_matrix = trans_matrix @ np.array(
            [
                [1, 0, -np.sign(eta)],
                [0, 1, 0],
                [0, 0, 1],
            ],
            dtype=int,
        )

        C = A + C - eta * np.sign(eta)
        xi = xi - zeta * np.sign(eta)
        eta = eta - 2 * A * np.sign(eta)

    return condition, (A, B, C, xi, eta, zeta), trans_matrix


def _niggli_step_7(A, B, C, xi, eta, zeta, trans_matrix, eps):
    condition = (
        compare_numerically(abs(zeta), ">", A, eps=eps)
        or (
            compare_numerically(zeta, "==", A, eps=eps)
            and compare_numerically(2 * xi, "<", eta, eps=eps)
        )
        or (
            compare_numerically(zeta, "==", -A, eps=eps)
            and compare_numerically(eta, "<", 0, eps=eps)
        )
    )
    if condition:
        trans_matrix = trans_matrix @ np.array(
            [
                [1, -np.sign(zeta), 0],
                [0, 1, 0],
                [0, 0, 1],
            ],
            dtype=int,
        )

        B = A + B - zeta * np.sign(zeta)
        xi = xi - eta * np.sign(zeta)
        zeta = zeta - 2 * A * np.sign(zeta)

    return condition, (A, B, C, xi, eta, zeta), trans_matrix


def _niggli_step_8(A, B, C, xi, eta, zeta, trans_matrix, eps):
    condition = compare_numerically(xi + eta + zeta + A + B, "<", 0, eps=eps) or (
        compare_numerically(xi + eta + zeta + A + B, "==", 0, eps=eps)
        and compare_numerically(2 * (A + eta) + zeta, ">", 0, eps=eps)
    )
    if condition:
        trans_matrix = trans_matrix @ np.array(
            [
                [1, 0, 1],
                [0, 1, 1],
                [0, 0, 1],
            ],
            dtype=int,
        )

        C = A + B + C + xi + eta + zeta
        xi = 2 * B + xi + zeta
        eta = 2 * A + eta + zeta

    return condition, (A, B, C, xi, eta, zeta), trans_matrix


def get_N_matrix(cell, eps_relative=1e-5, max_iterations=100000):
    r"""
    Computes the transformation  matrix from the given cell to the corresponding
    reduced Niggli cell. Implements algorithm from [2]_.

    Details of the implementation are written in :ref:`library_niggli`.

    .. versionadded:: 0.6.0

    Parameters
    ----------
    cell : (3, 3) |array-like|_
        Matrix of a cell, rows are interpreted as vectors.
    eps_relative : float, default :math:`10^{-5}`
        Relative epsilon as defined in [2]_.
    max_iterations : int, default 100000
        Maximum number of iterations.

    Returns
    -------
    transformation_matrix : (3, 3) :numpy:`ndarray`
        Transformation matrix from the given ``cell`` to its corresponding niggli cell.

    Raises
    ------
    wulfric.exceptions.NiggliReductionFailed
        If the niggli cell is not found in ``max_iterations`` iterations.
    ValueError
        If the volume of ``cell`` is zero.

    See Also
    --------
    get_niggli
    :ref:`user-guide_conventions_basic-notation_transformation`

    References
    ----------
    .. [1] Křivý, I. and Gruber, B., 1976.
        A unified algorithm for determining the reduced (Niggli) cell.
        Acta Crystallographica Section A: Crystal Physics, Diffraction,
        Theoretical and General Crystallography,
        32(2), pp.297-298.
    .. [2] Grosse-Kunstleve, R.W., Sauter, N.K. and Adams, P.D., 2004.
        Numerically stable algorithms for the computation of reduced unit cells.
        Acta Crystallographica Section A: Foundations of Crystallography,
        60(1), pp.1-6.

    Examples
    --------

    .. doctest::

        >>> import wulfric
        >>> wulfric.cell.get_N_matrix([[1, -0.5, 0], [-0.5, 1, 0], [0, 0, 1]])
        array([[ 1,  0, -1],
               [ 1,  0,  0],
               [ 0, -1,  0]])

    Example from [1]_ (parameters are reproducing :math:`A=9`, :math:`B=27`, :math:`C=4`,
    :math:`\xi` = -5, :math:`\eta` = -4, :math:`\zeta = -22`):

    .. doctest::

        >>> import wulfric
        >>> from wulfric.constants import TODEGREES
        >>> from math import sqrt, acos
        >>> a = 3
        >>> b = sqrt(27)
        >>> c = 2
        >>> alpha = acos(-5 / 2 / b / c) * TODEGREES
        >>> beta = acos(-4 / 2 / a / c) * TODEGREES
        >>> gamma = acos(-22 / 2 / a / b) * TODEGREES
        >>> cell = wulfric.cell.from_params(a, b, c, alpha, beta, gamma)
        >>> wulfric.cell.get_N_matrix(cell)
        array([[0, 1, 2],
               [0, 0, 1],
               [1, 1, 2]])

    """

    volume = get_volume(cell)
    if volume == 0:
        raise ValueError("Cell volume is zero")

    eps = eps_relative * volume ** (1 / 3.0)

    # 0
    metric_tensor = np.matmul(cell, np.transpose(cell))

    params = (
        metric_tensor[0][0],
        metric_tensor[1][1],
        metric_tensor[2][2],
        2 * metric_tensor[1][2],
        2 * metric_tensor[0][2],
        2 * metric_tensor[0][1],
    )

    trans_matrix = np.eye(3, dtype=int)

    iter_count = 0
    while True:
        if iter_count > max_iterations:
            raise NiggliReductionFailed(max_iterations=max_iterations)

        # Note : each iteration changes the transformation matrix

        iter_count += 1
        # 1
        condition, params, trans_matrix = _niggli_step_1(*params, trans_matrix, eps=eps)

        # 2
        condition, params, trans_matrix = _niggli_step_2(*params, trans_matrix, eps=eps)
        if condition:
            continue

        # 3
        condition, params, trans_matrix = _niggli_step_3(*params, trans_matrix, eps=eps)

        # 4
        condition, params, trans_matrix = _niggli_step_4(*params, trans_matrix, eps=eps)

        # 5
        condition, params, trans_matrix = _niggli_step_5(*params, trans_matrix, eps=eps)
        if condition:
            continue

        # 6
        condition, params, trans_matrix = _niggli_step_6(*params, trans_matrix, eps=eps)
        if condition:
            continue

        # 7
        condition, params, trans_matrix = _niggli_step_7(*params, trans_matrix, eps=eps)
        if condition:
            continue

        # 8
        condition, params, trans_matrix = _niggli_step_8(*params, trans_matrix, eps=eps)
        if condition:
            continue

        break

    return trans_matrix


def get_niggli(cell, eps_relative=1e-5, max_iterations=100000):
    r"""
    Computes reduced Niggli cell. Implements algorithm from [2]_.

    Details of the implementation are written in :ref:`library_niggli`.

    .. versionchanged:: 0.6.0 Renamed from ``niggli``

    Parameters
    ----------
    cell : (3, 3) |array-like|_
        Matrix of a cell, rows are interpreted as vectors.
    eps_relative : float, default :math:`10^{-5}`
        Relative epsilon as defined in [2]_.
    max_iterations : int, default 100000
        Maximum number of iterations.

    Returns
    -------
    niggli_cell : (3, 3) :numpy:`ndarray`
        Matrix of a niggli reduced cell, rows are interpreted as vectors.

        .. code-block:: python

            niggli_cell = [[a1_x, a1_y, a1_z], [a2_x, a2_y, a2_z], [a3_x, a3_y, a3_z]]

    Raises
    ------
    wulfric.exceptions.NiggliReductionFailed
        If the niggli cell is not found in ``max_iterations`` iterations.
    ValueError
        If the volume of ``cell`` is zero.

    See Also
    --------
    get_N_matrix

    References
    ----------
    .. [1] Křivý, I. and Gruber, B., 1976.
        A unified algorithm for determining the reduced (Niggli) cell.
        Acta Crystallographica Section A: Crystal Physics, Diffraction,
        Theoretical and General Crystallography,
        32(2), pp.297-298.
    .. [2] Grosse-Kunstleve, R.W., Sauter, N.K. and Adams, P.D., 2004.
        Numerically stable algorithms for the computation of reduced unit cells.
        Acta Crystallographica Section A: Foundations of Crystallography,
        60(1), pp.1-6.

    Examples
    --------

    .. doctest::

        >>> import wulfric
        >>> wulfric.cell.get_niggli([[1, -0.5, 0], [-0.5, 1, 0], [0, 0, 1]])
        array([[ 0.5,  0.5,  0. ],
               [ 0. ,  0. , -1. ],
               [-1. ,  0.5,  0. ]])

    Example from [1]_ (parameters are reproducing :math:`A=9`, :math:`B=27`, :math:`C=4`,
    :math:`\xi` = -5, :math:`\eta` = -4, :math:`\zeta = -22`):

    .. doctest::

        >>> import wulfric
        >>> from wulfric.constants import TODEGREES
        >>> from math import sqrt, acos
        >>> a = 3
        >>> b = sqrt(27)
        >>> c = 2
        >>> alpha = acos(-5 / 2 / b / c) * TODEGREES
        >>> beta = acos(-4 / 2 / a / c) * TODEGREES
        >>> gamma = acos(-22 / 2 / a / b) * TODEGREES
        >>> cell = wulfric.cell.from_params(a, b, c, alpha, beta, gamma)
        >>> niggli_cell = wulfric.cell.get_niggli(cell)
        >>> niggli_cell @ niggli_cell.T
        array([[4. , 2. , 1.5],
               [2. , 9. , 4.5],
               [1.5, 4.5, 9. ]])

    """

    volume = get_volume(cell)
    if volume == 0:
        raise ValueError("Cell volume is zero")

    eps = eps_relative * volume ** (1 / 3.0)

    # 0
    metric_tensor = np.matmul(cell, np.transpose(cell))

    params = (
        metric_tensor[0][0],
        metric_tensor[1][1],
        metric_tensor[2][2],
        2 * metric_tensor[1][2],
        2 * metric_tensor[0][2],
        2 * metric_tensor[0][1],
    )

    trans_matrix = np.eye(3, dtype=int)

    iter_count = 0
    while True:
        if iter_count > max_iterations:
            raise NiggliReductionFailed(max_iterations=max_iterations)

        # Note : each iteration changes the transformation matrix

        iter_count += 1
        # 1
        condition, params, trans_matrix = _niggli_step_1(*params, trans_matrix, eps=eps)

        # 2
        condition, params, trans_matrix = _niggli_step_2(*params, trans_matrix, eps=eps)
        if condition:
            continue

        # 3
        condition, params, trans_matrix = _niggli_step_3(*params, trans_matrix, eps=eps)

        # 4
        condition, params, trans_matrix = _niggli_step_4(*params, trans_matrix, eps=eps)

        # 5
        condition, params, trans_matrix = _niggli_step_5(*params, trans_matrix, eps=eps)
        if condition:
            continue

        # 6
        condition, params, trans_matrix = _niggli_step_6(*params, trans_matrix, eps=eps)
        if condition:
            continue

        # 7
        condition, params, trans_matrix = _niggli_step_7(*params, trans_matrix, eps=eps)
        if condition:
            continue

        # 8
        condition, params, trans_matrix = _niggli_step_8(*params, trans_matrix, eps=eps)
        if condition:
            continue

        break

    return trans_matrix.T @ cell


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
