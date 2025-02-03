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


from math import acos, cos, floor, log10, sqrt

import numpy as np
from termcolor import cprint

from wulfric._numerical import compare_numerically
from wulfric.constants._numerical import TODEGREES, TORADIANS
from wulfric.geometry._geometry import get_volume

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def niggli(
    a=1,
    b=1,
    c=1,
    alpha=90,
    beta=90,
    gamma=90,
    eps_relative=1e-5,
    verbose=False,
    return_cell=False,
    max_iter=10000,
):
    r"""
    Computes Niggli matrix form.

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
    eps_relative : float, default :math:`10^{-5}`
        Relative epsilon as defined in [2]_.
    verbose : bool, default False
        Whether to print the steps of an algorithm.
    return_cell : bool, default False
        Whether to return cell parameters instead of Niggli matrix form.
    max_iter : int, default 100000
        Maximum number of iterations.

    Returns
    -------
    result : (3,2) :numpy:`ndarray` or (6,) tuple of floats
        Niggli matrix form as defined in [1]_:

        .. math::

            \begin{pmatrix}
                A & B & C \\
                \xi/2 & \eta/2 & \zeta/2
            \end{pmatrix}

        If return_cell == True, then returns Niggli cell parameters: (a, b, c, alpha, beta, gamma).

    Raises
    ------
    ValueError
        If the niggli cell is not found in ``max_iter`` iterations.
    ValueError
        If the provided cell`s volume is zero.

    Notes
    -----

    The parameters are defined as follows:

    .. math::
        A & = a^2 \\
        B & = b^2 \\
        C & = c^2 \\
        \xi & = 2bc \cos(\alpha) \\
        \eta & = 2ac \cos(\beta) \\
        \zeta & = 2ab \cos(\gamma)


    Steps of an algorithm from the paper [1]_:

    1.  :math:`A > B` or (:math:`A = B` and :math:`|\xi| > |\eta|`),
        then swap :math:`(A, \xi) \leftrightarrow (B,\eta)`.

    2.  :math:`B > C` or (:math:`B = C` and :math:`|\eta| > |\zeta|`),
        then swap :math:`(B, \eta) \leftrightarrow (C,\zeta)` and go to 1.

    3.  If :math:`\xi \eta \zeta > 0`,
        then put :math:`(|\xi|, |\eta|, |\zeta|) \rightarrow (\xi, \eta, \zeta)`.

    4.  If :math:`\xi \eta \zeta \leq 0`,
        then put :math:`(-|\xi|, -|\eta|, -|\zeta|) \rightarrow (\xi, \eta, \zeta)`.

    5.  If :math:`|\xi| > B` or (:math:`\xi = B` and :math:`2\eta < \zeta`) or (:math:`\xi = -B` and :math:`\zeta < 0`),
        then apply the following transformation:

        .. math::
            C & = B + C - \xi \,\text{sign}(\xi) \\
            \eta & = \eta - \zeta \,\text{sign}(\xi) \\
            \xi & = \xi - 2B \,\text{sign}(\xi)

        and go to 1.

    6.  If :math:`|\eta| > A` or (:math:`\eta = A` and :math:`2\xi < \zeta`) or (:math:`\eta = -A` and :math:`\zeta < 0`),
        then apply the following transformation:

        .. math::
            C & = A + C - \eta \,\text{sign}(\eta) \\
            \xi & = \xi - \zeta \,\text{sign}(\eta) \\
            \eta & = \eta - 2A \,\text{sign}(\eta)

        and go to 1.

    7.  If :math:`|\zeta| > A` or (:math:`\zeta = A` and :math:`2\xi < \eta`) or (:math:`\zeta = -A` and :math:`\eta < 0`),
        then apply the following transformation:

        .. math::
            B & = A + B - \zeta \,\text{sign}(\zeta) \\
            \xi & = \xi - \eta \,\text{sign}(\zeta) \\
            \zeta & = \zeta - 2A \,\text{sign}(\zeta)

        and go to 1.

    8.  If :math:`\xi + \eta + \zeta + A + B < 0` or (:math:`\xi + \eta + \zeta + A + B = 0` and :math:`2(A + \eta) + \zeta > 0`),
        then apply the following transformation:

        .. math::
            C & = A + B + C + \xi + \eta + \zeta \\
            \xi & = 2B + \xi + \zeta \\
            \eta & = 2A + \eta + \zeta

        and go to 1.

    Examples
    --------
    Example from [1]_
    (parameters are reproducing :math:`A=9`, :math:`B=27`, :math:`C=4`,
    :math:`\xi` = -5, :math:`\eta` = -4, :math:`\zeta = -22`):

    .. doctest::

        >>> import wulfric as wulf
        >>> from wulfric.constants import TODEGREES
        >>> from math import acos, sqrt
        >>> a = 3
        >>> b = sqrt(27)
        >>> c = 2
        >>> print(f"{a} {b:.3f} {c}")
        3 5.196 2
        >>> alpha = acos(-5 / 2 / b / c) * TODEGREES
        >>> beta = acos(-4 / 2 / a / c) * TODEGREES
        >>> gamma = acos(-22 / 2 / a / b) * TODEGREES
        >>> print(f"{alpha:.2f} {beta:.2f} {gamma:.2f}")
        103.92 109.47 134.88
        >>> niggli_matrix_form = wulf.cell.niggli(a, b, c, alpha, beta, gamma, verbose=True, eps_relative=1e-4) # doctest: +NORMALIZE_WHITESPACE
                       A         B         C        xi        eta      zeta
        start:       9.0000  27.0000   4.0000  -5.0000  -4.0000 -22.0000
        2 appl. to   9.0000  27.0000   4.0000  -5.0000  -4.0000 -22.0000
        1 appl. to   9.0000   4.0000  27.0000  -5.0000 -22.0000  -4.0000
        4 appl. to   4.0000   9.0000  27.0000 -22.0000  -5.0000  -4.0000
        5 appl. to   4.0000   9.0000  27.0000 -22.0000  -5.0000  -4.0000
        4 appl. to   4.0000   9.0000  14.0000  -4.0000  -9.0000  -4.0000
        6 appl. to   4.0000   9.0000  14.0000  -4.0000  -9.0000  -4.0000
        4 appl. to   4.0000   9.0000   9.0000  -8.0000  -1.0000  -4.0000
        7 appl. to   4.0000   9.0000   9.0000  -8.0000  -1.0000  -4.0000
        3 appl. to   4.0000   9.0000   9.0000  -9.0000  -1.0000   4.0000
        5 appl. to   4.0000   9.0000   9.0000   9.0000   1.0000   4.0000
        3 appl. to   4.0000   9.0000   9.0000  -9.0000  -3.0000   4.0000
        result:      4.0000   9.0000   9.0000   9.0000   3.0000   4.0000
        >>> niggli_matrix_form
        array([[4. , 9. , 9. ],
               [4.5, 1.5, 2. ]])

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

    """

    volume = get_volume(a, b, c, alpha, beta, gamma)
    if volume == 0:
        raise ValueError("Cell volume is zero")

    eps = eps_relative * volume ** (1 / 3.0)
    n = abs(floor(log10(abs(eps))))

    # 0
    A = a**2
    B = b**2
    C = c**2
    xi = 2 * b * c * cos(alpha * TORADIANS)
    eta = 2 * a * c * cos(beta * TORADIANS)
    zeta = 2 * a * b * cos(gamma * TORADIANS)
    N = (
        max(
            len(str(A).split(".")[0]),
            len(str(B).split(".")[0]),
            len(str(C).split(".")[0]),
            len(str(xi).split(".")[0]),
            len(str(eta).split(".")[0]),
            len(str(zeta).split(".")[0]),
        )
        + 1
        + n
    )

    def summary_line():
        return (
            f"{A:{N}.{n}f} {B:{N}.{n}f} {C:{N}.{n}f} "
            + f"{xi:{N}.{n}f} {eta:{N}.{n}f} {zeta:{N}.{n}f}"
        )

    if verbose:
        print(
            f"           {'A':^{N}} {'B':^{N}} {'C':^{N}} "
            + f"{'xi':^{N}} {'eta':^{N}} {'zeta':^{N}}"
        )
        cprint(
            f"start:     {summary_line()}",
            color="yellow",
        )
        phrase = "appl. to"
    iter_count = 0
    while True:
        if iter_count > max_iter:
            raise ValueError(f"Niggli cell not found in {max_iter} iterations")
        iter_count += 1
        # 1
        if compare_numerically(A, ">", B, eps) or (
            compare_numerically(A, "==", B, eps)
            and compare_numerically(abs(xi), ">", abs(eta), eps)
        ):
            if verbose:
                print(f"1 {phrase} {summary_line()}")
            A, xi, B, eta = B, eta, A, xi
        # 2
        if compare_numerically(B, ">", C, eps) or (
            compare_numerically(B, "==", C, eps)
            and compare_numerically(abs(eta), ">", abs(zeta), eps)
        ):
            if verbose:
                print(f"2 {phrase} {summary_line()}")
            B, eta, C, zeta = C, zeta, B, eta
            # go to 1
            continue
        # 3
        if compare_numerically(xi * eta * zeta, ">", 0, eps):
            if verbose:
                print(f"3 {phrase} {summary_line()}")
            xi, eta, zeta = abs(xi), abs(eta), abs(zeta)
        # 4
        if compare_numerically(xi * eta * zeta, "<=", 0, eps):
            if verbose:
                print(f"4 {phrase} {summary_line()}")
            xi, eta, zeta = -abs(xi), -abs(eta), -abs(zeta)
        # 5
        if (
            compare_numerically(abs(xi), ">", B, eps)
            or (
                compare_numerically(xi, "==", B, eps)
                and compare_numerically(2 * eta, "<", zeta, eps)
            )
            or (
                compare_numerically(xi, "==", -B, eps)
                and compare_numerically(zeta, "<", 0, eps)
            )
        ):
            if verbose:
                print(f"5 {phrase} {summary_line()}")
            C = B + C - xi * np.sign(xi)
            eta = eta - zeta * np.sign(xi)
            xi = xi - 2 * B * np.sign(xi)
            # go to 1
            continue
        # 6
        if (
            compare_numerically(abs(eta), ">", A, eps)
            or (
                compare_numerically(eta, "==", A, eps)
                and compare_numerically(2 * xi, "<", zeta, eps)
            )
            or (
                compare_numerically(eta, "==", -A, eps)
                and compare_numerically(zeta, "<", 0, eps)
            )
        ):
            if verbose:
                print(f"6 {phrase} {summary_line()}")
            C = A + C - eta * np.sign(eta)
            xi = xi - zeta * np.sign(eta)
            eta = eta - 2 * A * np.sign(eta)
            # go to 1
            continue
        # 7
        if (
            compare_numerically(abs(zeta), ">", A, eps)
            or (
                compare_numerically(zeta, "==", A, eps)
                and compare_numerically(2 * xi, "<", eta, eps)
            )
            or (
                compare_numerically(zeta, "==", -A, eps)
                and compare_numerically(eta, "<", 0, eps)
            )
        ):
            if verbose:
                print(f"7 {phrase} {summary_line()}")
            B = A + B - zeta * np.sign(zeta)
            xi = xi - eta * np.sign(zeta)
            zeta = zeta - 2 * A * np.sign(zeta)
            # go to 1
            continue
        # 8
        if compare_numerically(xi + eta + zeta + A + B, "<", 0, eps) or (
            compare_numerically(xi + eta + zeta + A + B, "==", 0, eps)
            and compare_numerically(2 * (A + eta) + zeta, ">", 0, eps)
        ):
            if verbose:
                print(f"8 {phrase} {summary_line()}")
            C = A + B + C + xi + eta + zeta
            xi = 2 * B + xi + zeta
            eta = 2 * A + eta + zeta
            # go to 1
            continue
        break
    if verbose:
        cprint(
            f"result:    {summary_line()}",
            color="green",
        )
    if return_cell:
        a = sqrt(A)
        b = sqrt(B)
        c = sqrt(C)
        alpha = acos(xi / 2 / b / c) * TODEGREES
        beta = acos(eta / 2 / a / c) * TODEGREES
        gamma = acos(zeta / 2 / a / b) * TODEGREES
        return a, b, c, alpha, beta, gamma
    return np.array([[A, B, C], [xi / 2, eta / 2, zeta / 2]], dtype=float)


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
