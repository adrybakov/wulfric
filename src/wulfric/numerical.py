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

__all__ = [
    "compare_numerically",
    "ABS_TOL",
    "REL_TOL",
    "MIN_LENGTH",
    "MAX_LENGTH",
    "ABS_TOL_ANGLE",
    "REL_TOL_ANGLE",
    "MIN_ANGLE",
]

# Length variables
ABS_TOL = 1e-8  # For the linear spatial variables
REL_TOL = 1e-4  # For the linear spatial variables
# MIN_LENGTH is a direct consequence of the REL_TOL and ABS_TOL:
# for l = MIN_LENGTH => ABS_TOL = l * REL_TOL
MIN_LENGTH = ABS_TOL / REL_TOL
# MAX_LENGTH is a direct consequence of the ABS_TOL:
# Inverse of the MAX_LENGTH in the real space has to be meaningful
# in the reciprocal space (< ABS_TOL).
MAX_LENGTH = 1 / ABS_TOL

# TODO Think how to connect angle tolerance with spatial tolerance.

ABS_TOL_ANGLE = 1e-4  # For the angular variables, in degrees.
REL_TOL_ANGLE = 1e-2  # For the angular variables.
# MIN_ANGLE is a direct consequence of the REL_TOL_ANGLE and ABS_TOL_ANGLE:
# for a = MIN_ANGLE => ABS_TOL_ANGLE = a * REL_TOL_ANGLE
MIN_ANGLE = ABS_TOL_ANGLE / REL_TOL_ANGLE  # In degrees


def compare_numerically(x, condition, y, eps=None, rtol=REL_TOL, atol=ABS_TOL):
    r"""
    Compare two numbers numerically.

    The approach is taken from [1]_:

    .. math::

        \begin{matrix}
            x < y  & x < y - \varepsilon \\
            x > y  & y < x - \varepsilon \\
            x \le y & \text{ not } (y < x - \varepsilon) \\
            x \ge y & \text{ not } (x < y - \varepsilon) \\
            x = y  & \text{ not } (x < y - \varepsilon \text{ or } y < x - \varepsilon) \\
            x \ne y & x < y - \varepsilon \text{ or } y < x - \varepsilon
        \end{matrix}

    Parameters
    ----------
    x : float
        First number.
    condition : str
        Condition to compare with. One of "<", ">", "<=", ">=", "==", "!=".
    y : float
        Second number.
    eps : float, optional
        Tolerance. Used for the comparison if provided. If ``None``, then computed as:

        .. code-block:: python

            eps = atol + rtol * abs(y)

    rtol : float, default 1e-04
        Relative tolerance.
    atol : float, default 1e-08
        Absolute tolerance.

    Returns
    -------
    result: bool
        Whether the condition is satisfied.

    Raises
    ------
    ValueError
        If ``condition`` is not one of "<", ">", "<=", ">=", "==", "!=".

    References
    ----------
    .. [1] Grosse-Kunstleve, R.W., Sauter, N.K. and Adams, P.D., 2004.
        Numerically stable algorithms for the computation of reduced unit cells.
        Acta Crystallographica Section A: Foundations of Crystallography,
        60(1), pp.1-6.
    """

    if eps is None:
        eps = atol + rtol * abs(y)

    if condition == "<":
        return x < y - eps
    if condition == ">":
        return y < x - eps
    if condition == "<=":
        return not y < x - eps
    if condition == ">=":
        return not x < y - eps
    if condition == "==":
        return not (x < y - eps or y < x - eps)
    if condition == "!=":
        return x < y - eps or y < x - eps

    raise ValueError(f'Condition must be one of "<", ">", "<=", ">=", "==", "!=".')
