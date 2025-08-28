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
from math import cos, sin

import numpy as np

from wulfric._numerical import compare_with_tolerance as cwt
from wulfric.cell._basic_manipulation import get_params, get_reciprocal
from wulfric.constants._numerical import TORADIANS
from wulfric.crystal._crystal_validation import validate_atoms
from wulfric._spglib_interface import get_spglib_data, validate_spglib_data
from wulfric._syntactic_sugar import SyntacticSugar
from wulfric.constants._sc_convention import SC_BRAVAIS_LATTICE_SHORT_NAMES
from wulfric.crystal._conventional import get_conventional
from wulfric.crystal._primitive import get_primitive

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
        raise ValueError('(convention="SC"): BCT variation). a == c')


def _ORCF_variation(
    conv_a: float, conv_b: float, conv_c: float, distance_tolerance=1e-8
):
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
    distance_tolerance : float, default :math:`10^{-5}`
        Tolerance parameter for comparing two linear variables.

    Returns
    -------
    variation : str
        Variation of the lattice. "ORCF1", "ORCF2" or "ORCF3".

    Raises
    ------
    ValueError
        If :math:`a < b < c` is not satisfied.
    """
    if cwt(conv_a, ">=", conv_b, eps=distance_tolerance) or cwt(
        conv_b, ">=", conv_c, eps=distance_tolerance
    ):
        raise ValueError(
            f'(convention="SC"): ORCF variation. a < b < c is not satisfied with {distance_tolerance} tolerance.'
        )

    expression = 1 / conv_a**2 - 1 / conv_b**2 - 1 / conv_c**2
    if cwt(expression, "==", 0, eps=distance_tolerance):
        return "ORCF3"
    elif cwt(expression, ">", 0, eps=distance_tolerance):
        return "ORCF1"
    elif cwt(expression, "<", 0, eps=distance_tolerance):
        return "ORCF2"


def _RHL_variation(conv_alpha: float, angle_tolerance=1e-4):
    r"""
    Two variations of the RHL lattice.

    Condition :math:`\alpha \ne 90^{\circ}` is assumed.

    :math:`\text{RHL}_1 \alpha < 90^{\circ}`,
    :math:`\text{RHL}_2 \alpha > 90^{\circ}`

    Parameters
    ----------
    conv_alpha : float
        Angle between vectors :math:`a_1` and :math:`a_2` of the conventional cell in
        degrees.
    angle_tolerance : float, default :math:`10^{-4}`
        Tolerance parameter for comparing two angles, given in degrees.

    Returns
    -------
    variation : str
        Variation of the lattice. Either "RHL1" or "RHL2".

    Raises
    ------
    ValueError
        If :math:`\alpha == 90^{\circ}` with given tolerance ``eps``.
    """
    if cwt(conv_alpha, "<", 90, eps=angle_tolerance):
        return "RHL1"
    elif cwt(conv_alpha, ">", 90, eps=angle_tolerance):
        return "RHL2"
    else:
        raise ValueError(
            f'(convention="SC"): RHL variation. alpha == 90 with {angle_tolerance} tolerance.'
        )


def _MCLC_variation(
    conv_a: float,
    conv_b: float,
    conv_c: float,
    conv_alpha: float,
    prim_k_gamma: float,
    distance_tolerance=1e-8,
    angle_tolerance=1e-4,
):
    r"""
    Five variations of the MCLC lattice.

    :math:`\alpha < 90^{\circ}` is checked.

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
        Angle between vectors :math:`a_2` and :math:`a_3` of the conventional cell in
        degrees.
    k_gamma : float
        Angle between reciprocal vectors :math:`b_1` and :math:`b_2`. In degrees.
    distance_tolerance : float, default :math:`10^{-5}`
        Tolerance parameter for comparing two linear variables.
    angle_tolerance : float, default :math:`10^{-4}`
        Tolerance parameter for comparing two angles, given in degrees.

    Returns
    -------
    variation : str
        Variation of the lattice.
        Either "MCLC1", "MCLC2", "MCLC3", "MCLC4" or "MCLC5".

    Raises
    ------
    ValueError
        If :math:`\alpha > 90^{\circ}` with given tolerance ``angle_tolerance``.
    """

    if cwt(conv_alpha, ">", 90, eps=angle_tolerance):
        raise ValueError(
            f'(convention="SC"): MCLC variation. alpha > 90 with {angle_tolerance} tolerance:\n  alpha = {conv_alpha}\n'
        )

    conv_alpha *= TORADIANS

    if cwt(prim_k_gamma, "==", 90, eps=angle_tolerance):
        return "MCLC2"
    elif cwt(prim_k_gamma, ">", 90, eps=angle_tolerance):
        return "MCLC1"
    elif cwt(prim_k_gamma, "<", 90, eps=angle_tolerance):
        expression = (
            conv_b * cos(conv_alpha) / conv_c
            + conv_b**2 * sin(conv_alpha) ** 2 / conv_a**2
        )
        if cwt(expression, "==", 1, eps=distance_tolerance):
            return "MCLC4"
        elif cwt(expression, "<", 1, eps=distance_tolerance):
            return "MCLC3"
        elif cwt(expression, ">", 1, eps=distance_tolerance):
            return "MCLC5"


def _TRI_variation(k_alpha: float, k_beta: float, k_gamma: float, angle_tolerance=1e-4):
    r"""
    Four variations of the TRI lattice.

    Conditions :math:`k_{\alpha} \ne 90^{\circ}` and :math:`k_{\beta} \ne 90^{\circ}` are checked.

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
    angle_tolerance : float, default :math:`10^{-4}`
        Tolerance parameter for comparing two angles, given in degrees.

    Returns
    -------
    variation : str
        Variation of the lattice.
        Either "TRI1a", "TRI1b", "TRI2a" or "TRI2b".

    Raises
    ------
    ValueError
        If :math:`k_{\alpha} == 90^{\circ}` or :math:`k_{\beta} == 90^{\circ}` with given
        tolerance ``angle_tolerance``.
    """

    if cwt(k_alpha, "==", 90, eps=angle_tolerance) or cwt(
        k_beta, "==", 90, eps=angle_tolerance
    ):
        raise ValueError(
            f'(convention="SC"): TRI variation. k_alpha == 90 or k_beta == 90 with {angle_tolerance} tolerance.'
        )

    if cwt(k_gamma, "==", 90, eps=angle_tolerance):
        if cwt(k_alpha, ">", 90, eps=angle_tolerance) and cwt(
            k_beta, ">", 90, eps=angle_tolerance
        ):
            return "TRI2a"
        elif cwt(k_alpha, "<", 90, eps=angle_tolerance) and cwt(
            k_beta, "<", 90, eps=angle_tolerance
        ):
            return "TRI2b"
    elif cwt(min(k_gamma, k_beta, k_alpha), ">", 90, eps=angle_tolerance):
        return "TRI1a"
    elif cwt(max(k_gamma, k_beta, k_alpha), "<", 90, eps=angle_tolerance):
        return "TRI1b"
    else:
        return "TRI"


def sc_get_variation(cell, atoms, spglib_data=None):
    r"""
    Return variation of the lattice as defined in the paper by Setyawan and Curtarolo [1]_.

    Parameters
    ----------
    cell : (3, 3) |array-like|_
        Matrix of a cell, rows are interpreted as vectors.
    atoms : dict
        Dictionary with N atoms. Expected keys:

        *   "positions" : (N, 3) |array-like|_

            Positions of the atoms in the basis of lattice vectors (``cell``). In other
            words - relative coordinates of atoms.
        *   "names" : (N, ) list of str, optional

            See Notes
        *   "species" : (N, ) list of str, optional

            See Notes
        *   "spglib_types" : (N, ) list of int, optional

            See Notes

        .. hint::
            Pass ``atoms = dict(positions=[[0, 0, 0]], spglib_types=[1])`` if you would
            like to interpret the ``cell`` alone (effectively assuming that the ``cell``
            is a primitive one).

    spglib_data : :py:class:`.SyntacticSugar`, optional
        If you need more control on the parameters passed to the spglib, then
        you can get ``spglib_data`` manually and pass it to this function.
        Use wulfric's interface to |spglib|_ as

        .. code-block:: python

            spglib_data = wulfric.get_spglib_data(...)

        using the same ``cell`` and ``atoms["positions"]`` that you are passing to this
        function.

    Returns
    -------
    variation : str
        Variation of the lattice defined by the ``cell``.

    Notes
    =====
    |spglib|_ uses ``types`` to distinguish the atoms. To see how wulfric deduces the
    ``types`` for given atoms see :py:func:`wulfric.get_spglib_types`.

    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp. 299-312.

    Examples
    --------

    .. doctest::

        >>> import wulfric
        >>> # There is no variation of cubic lattice, therefore, just lattice type is
        >>> # returned
        >>> wulfric.crystal.sc_get_variation(
        ...     cell=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
        ...     atoms=dict(positions=[[0, 0, 0]], spglib_types=[1]),
        ... )
        'CUB'
        >>> cell = wulfric.cell.sc_get_example_cell("bct")
        >>> wulfric.crystal.sc_get_variation(
        ...     cell=cell,
        ...     atoms=dict(positions=[[0, 0, 0]], spglib_types=[1]),
        ... )
        'BCT1'

    """

    # Validate that the atoms dictionary is what expected of it
    validate_atoms(atoms=atoms, required_keys=["positions"], raise_errors=True)

    # Call spglib
    if spglib_data is None:
        spglib_data = get_spglib_data(cell=cell, atoms=atoms)
    # Or check that spglib_data were *most likely* produced via wulfric's interface
    elif not isinstance(spglib_data, SyntacticSugar):
        raise TypeError(
            f"Are you sure that spglib_data were produced via wulfric's interface? Expected SyntacticSugar, got {type(spglib_data)}."
        )
    # Validate that user-provided spglib_data match user-provided structure
    else:
        validate_spglib_data(cell=cell, atoms=atoms, spglib_data=spglib_data)

    cell = np.array(cell, dtype=float)

    lattice_type = spglib_data.crystal_family + spglib_data.centring_type

    angle_tolerance = (
        spglib_data.angle_tolerance if spglib_data.angle_tolerance != -1 else 1e-4
    )

    if lattice_type in ["tI", "oF", "hR", "mC", "aP"]:
        conv_cell, _ = get_conventional(
            cell=cell, atoms=atoms, convention="SC", spglib_data=spglib_data
        )
        conv_a, conv_b, conv_c, conv_alpha, _, _ = get_params(cell=conv_cell)

    if lattice_type == "tI":
        return _BCT_variation(conv_a, conv_c)

    if lattice_type == "oF":
        return _ORCF_variation(
            conv_a, conv_b, conv_c, distance_tolerance=spglib_data.symprec
        )

    if lattice_type == "hR":
        return _RHL_variation(conv_alpha, angle_tolerance=angle_tolerance)

    if lattice_type == "mC":
        prim_cell, _ = get_primitive(
            cell=cell, atoms=atoms, convention="SC", spglib_data=spglib_data
        )
        _, _, _, _, _, prim_k_gamma = get_params(get_reciprocal(cell=prim_cell))
        return _MCLC_variation(
            conv_a,
            conv_b,
            conv_c,
            conv_alpha,
            prim_k_gamma,
            distance_tolerance=spglib_data.symprec,
            angle_tolerance=angle_tolerance,
        )

    if lattice_type == "aP":
        _, _, _, k_alpha, k_beta, k_gamma = get_params(get_reciprocal(cell=conv_cell))
        return _TRI_variation(
            k_alpha,
            k_beta,
            k_gamma,
            angle_tolerance=angle_tolerance,
        )

    return SC_BRAVAIS_LATTICE_SHORT_NAMES[lattice_type]


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
