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


from math import cos, sin

import numpy as np

from wulfric._numerical import compare_numerically
from wulfric.cell._basic_manipulation import get_params, get_reciprocal
from wulfric.cell._lepage import lepage
from wulfric.cell._sc_standardize import get_conventional
from wulfric.constants._numerical import TORADIANS
from wulfric.geometry._geometry import get_volume

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def _BCT_variation(conv_a: float, conv_c: float):
    r"""
    Two variations of the BCT lattice.

    Condition :math:`a \ne c` is assumed.

    :math:`\text{BCT}_1: c < a` and :math:`\text{BCT}_2: c > a`

    Parameters
    ----------
    conv_a : float
        Length of the :math:`a_1 == a_2` vector of the conventional cell.
    conv_c : float
        Length of the :math:`a_3` vector of the conventional cell.

    Returns
    -------
    variation : str
        Variation of the lattice. "BCT1" or "BCT2".

    Raises
    ------
    ValueError
        If :math:`a == c`.
    """
    if conv_a > conv_c:
        return "BCT1"
    elif conv_a < conv_c:
        return "BCT2"
    else:
        raise ValueError("a == c")


def _ORCF_variation(conv_a: float, conv_b: float, conv_c: float, eps: float):
    r"""
    Three variations of the ORCF lattice.

    Ordering :math:`a < b < c` is assumed.

    :math:`\text{ORCF}_1: \dfrac{1}{a^2} > \dfrac{1}{b^2} + \dfrac{1}{c^2}`,
    :math:`\text{ORCF}_2: \dfrac{1}{a^2} < \dfrac{1}{b^2} + \dfrac{1}{c^2}`,
    :math:`\text{ORCF}_3: \dfrac{1}{a^2} = \dfrac{1}{b^2} + \dfrac{1}{c^2}`,

    Parameters
    ----------
    conv_a : float
        Length of the :math:`a_1` vector of the conventional cell.
    conv_b : float
        Length of the :math:`a_2` vector of the conventional cell.
    conv_c : float
        Length of the :math:`a_3` vector of the conventional cell.
    eps : float
        Tolerance for numerical comparison.

    Returns
    -------
    variation : str
        Variation of the lattice. "ORCF1", "ORCF2" or "ORCF3".

    Raises
    ------
    ValueError
        If :math:`a < b < c` is not satisfied.
    """
    if compare_numerically(conv_a, ">=", conv_b, eps) or compare_numerically(
        conv_b, ">=", conv_c, eps
    ):
        raise ValueError(f"a < b < c is not satisfied with {eps} tolerance.")

    expression = 1 / conv_a**2 - 1 / conv_b**2 - 1 / conv_c**2
    if compare_numerically(expression, "==", 0, eps):
        return "ORCF3"
    elif compare_numerically(expression, ">", 0, eps):
        return "ORCF1"
    elif compare_numerically(expression, "<", 0, eps):
        return "ORCF2"


def _RHL_variation(conv_alpha: float, eps: float):
    r"""
    Two variations of the RHL lattice.

    Condition :math:`\alpha \ne 90^{\circ}` is assumed.

    :math:`\text{RHL}_1 \alpha < 90^{\circ}`,
    :math:`\text{RHL}_2 \alpha > 90^{\circ}`

    Parameters
    ----------
    conv_alpha : float
        Angle between vectors :math:`a_1` and :math:`a_2` of the conventional cell. In degrees.
    eps : float
        Tolerance for numerical comparison.

    Returns
    -------
    variation : str
        Variation of the lattice. Either "RHL1" or "RHL2".

    Raises
    ------
    ValueError
        If :math:`\alpha == 90^{\circ}` with given tolerance ``eps``.
    """
    if compare_numerically(conv_alpha, "<", 90, eps):
        return "RHL1"
    elif compare_numerically(conv_alpha, ">", 90, eps):
        return "RHL2"
    else:
        raise ValueError(f"alpha == 90 with {eps} tolerance.")


def _MCLC_variation(
    conv_a: float,
    conv_b: float,
    conv_c: float,
    conv_alpha: float,
    k_gamma: float,
    eps: float,
):
    r"""
    Five variation of the MCLC lattice.

    Ordering :math:`a \le c` and :math:`b \le c` and :math:`\alpha < 90^{\circ}` is assumed.

    :math:`\text{MCLC}_1: k_{\gamma} > 90^{\circ}`,
    :math:`\text{MCLC}_2: k_{\gamma} = 90^{\circ}`,
    :math:`\text{MCLC}_3: k_{\gamma} < 90^{\circ}, \dfrac{b\cos(\alpha)}{c} + \dfrac{b^2\sin(\alpha)^2}{a^2} < 1`
    :math:`\text{MCLC}_4: k_{\gamma} < 90^{\circ}, \dfrac{b\cos(\alpha)}{c} + \dfrac{b^2\sin(\alpha)^2}{a^2} = 1`
    :math:`\text{MCLC}_5: k_{\gamma} < 90^{\circ}, \dfrac{b\cos(\alpha)}{c} + \dfrac{b^2\sin(\alpha)^2}{a^2} > 1`

    Parameters
    ----------
    conv_a : float
        Length of the :math:`a_1` vector of the conventional cell.
    conv_b : float
        Length of the :math:`a_2` vector of the conventional cell.
    conv_c : float
        Length of the :math:`a_3` vector of the conventional cell.
    conv_alpha : float
        Angle between vectors :math:`a_2` and :math:`a_3` of the conventional cell. In degrees.
    k_gamma : float
        Angle between reciprocal vectors :math:`b_1` and :math:`b_2`. In degrees.
    eps : float
        Tolerance for numerical comparison.

    Returns
    -------
    variation : str
        Variation of the lattice.
        Either "MCLC1", "MCLC2", "MCLC3", "MCLC4" or "MCLC5".

    Raises
    ------
    ValueError
        If :math:`\alpha > 90^{\circ}` or :math:`a > c` or :math:`b > c` with given tolerance ``eps``.
    """

    if compare_numerically(conv_alpha, ">", 90, eps) or compare_numerically(
        conv_b, ">", conv_c, eps
    ):
        raise ValueError(
            f"alpha > 90 or  or b > c with {eps} tolerance:\n"
            + f"  alpha = {conv_alpha}\n"
            + f"  b = {conv_b}\n"
            + f"  c = {conv_c}\n"
        )

    conv_alpha *= TORADIANS

    if compare_numerically(k_gamma, "==", 90, eps):
        return "MCLC2"
    elif compare_numerically(k_gamma, ">", 90, eps):
        return "MCLC1"
    elif compare_numerically(k_gamma, "<", 90, eps):
        expression = (
            conv_b * cos(conv_alpha) / conv_c
            + conv_b**2 * sin(conv_alpha) ** 2 / conv_a**2
        )
        if compare_numerically(expression, "==", 1, eps):
            return "MCLC4"
        elif compare_numerically(expression, "<", 1, eps):
            return "MCLC3"
        elif compare_numerically(expression, ">", 1, eps):
            return "MCLC5"


def _TRI_variation(k_alpha: float, k_beta: float, k_gamma: float, eps: float):
    r"""
    Four variations of the TRI lattice.

    Conditions :math:`k_{\alpha} \ne 90^{\circ}` and :math:`k_{\beta} \ne 90^{\circ}` are assumed.

    :math:`\text{TRI}_{1a} k_{\alpha} > 90^{\circ}, k_{\beta} > 90^{\circ}, k_{\gamma} > 90^{\circ}, k_{\gamma} = \min(k_{\alpha}, k_{\beta}, k_{\gamma})`

    :math:`\text{TRI}_{1b} k_{\alpha} < 90^{\circ}, k_{\beta} < 90^{\circ}, k_{\gamma} < 90^{\circ}, k_{\gamma} = \max(k_{\alpha}, k_{\beta}, k_{\gamma})`

    :math:`\text{TRI}_{2a} k_{\alpha} > 90^{\circ}, k_{\beta} > 90^{\circ}, k_{\gamma} = 90^{\circ}`

    :math:`\text{TRI}_{2b} k_{\alpha} < 90^{\circ}, k_{\beta} < 90^{\circ}, k_{\gamma} = 90^{\circ}`

    Parameters
    ----------
    k_alpha : float
        Angle between reciprocal vectors :math:`b_2` and :math:`b_3`. In degrees.
    k_beta : float
        Angle between reciprocal vectors :math:`b_1` and :math:`b_3`. In degrees.
    k_gamma : float
        Angle between reciprocal vectors :math:`b_1` and :math:`b_2`. In degrees.
    eps : float
        Tolerance for numerical comparison.

    Returns
    -------
    variation : str
        Variation of the lattice.
        Either "TRI1a", "TRI1b", "TRI2a" or "TRI2b".

    Raises
    ------
    ValueError
        If :math:`k_{\alpha} == 90^{\circ}` or :math:`k_{\beta} == 90^{\circ}` with given tolerance ``eps``.
    """

    if compare_numerically(k_alpha, "==", 90, eps) or compare_numerically(
        k_beta, "==", 90, eps
    ):
        raise ValueError(f"k_alpha == 90 or k_beta == 90 with {eps} tolerance.")

    if compare_numerically(k_gamma, "==", 90, eps):
        if compare_numerically(k_alpha, ">", 90, eps) and compare_numerically(
            k_beta, ">", 90, eps
        ):
            return "TRI2a"
        elif compare_numerically(k_alpha, "<", 90, eps) and compare_numerically(
            k_beta, "<", 90, eps
        ):
            return "TRI2b"
    elif compare_numerically(min(k_gamma, k_beta, k_alpha), ">", 90, eps):
        return "TRI1a"
    elif compare_numerically(max(k_gamma, k_beta, k_alpha), "<", 90, eps):
        return "TRI1b"
    else:
        return "TRI"


def get_variation(cell, lattice_type=None, eps_rel=1e-8, angle_tol=1e-4):
    r"""
    Return variation of the lattice as define in the paper by Setyawan and Curtarolo [1]_.

    Parameters
    ----------
    cell : (3,3) |array-like|_
        Unit cell of the lattice. Rows define lattice vectors.
    lattice_type : str, optional
        One of the 14 lattice types that correspond to the provided ``cell``.
        If not provided, then computed automatically. Case-insensitive.
    eps_rel : float, default TODO
        Relative tolerance for distance.
    angle_tol : float, default TODO
        Absolute tolerance for angles, in degrees.

    Returns
    -------
    variation : str
        Variation of the lattice defined by the ``cell``.


    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp.299-312.
    """

    cell = np.array(cell, dtype=float)

    if lattice_type is None:
        lattice_type = lepage(
            *get_params(cell),
            eps_relative=eps_rel,
            eps_angle=angle_tol,
        )

    lattice_type = lattice_type.upper()

    if lattice_type in ["BCT", "ORCF", "RHL", "MCLC", "TRI"]:
        eps = eps_rel * abs(get_volume(cell)) ** (1 / 3.0)

    if lattice_type in ["BCT", "ORCF", "RHL", "MCLC"]:
        conv_a, conv_b, conv_c, conv_alpha, conv_beta, conv_gamma = get_params(
            get_conventional(cell)
        )

    if lattice_type == "BCT":
        result = _BCT_variation(conv_a, conv_c)
    elif lattice_type == "ORCF":
        result = _ORCF_variation(conv_a, conv_b, conv_c, eps)
    elif lattice_type == "RHL":
        result = _RHL_variation(conv_alpha, eps)
    elif lattice_type == "MCLC":
        _, _, _, _, _, k_gamma = get_params(get_reciprocal(cell))
        result = _MCLC_variation(
            conv_a,
            conv_b,
            conv_c,
            conv_alpha,
            k_gamma,
            eps,
        )
    elif lattice_type == "TRI":
        _, _, _, k_alpha, k_beta, k_gamma = get_params(get_reciprocal(cell))
        result = _TRI_variation(k_alpha, k_beta, k_gamma, eps)
    else:
        result = lattice_type

    return result


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
