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


from math import pi as PI

import numpy as np

from wulfric._exceptions import StandardizationTypeMismatch
from wulfric._numerical import compare_numerically
from wulfric.cell._basic_manipulation import (
    get_params,
    get_reciprocal,
    get_scalar_products,
)
from wulfric.cell._lepage import lepage
from wulfric.constants._sc_notation import C_MATRICES

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def _CUB_get_S_matrix(cell, length_tolerance=1e-8, angle_tolerance=1e-4):
    r"""
    For arbitrary cubic cell returns matrix S that transforms it to the standardized form.

    .. versionchanged:: 0.4.0  Renamed from ``CUB_standardize_cell``

    See :ref:`guide_cub` and :ref:`user-guide_conventions_cell_standardization` for the
    details.

    Parameters
    ----------
    cell : (3,3) |array-like|_
        Primitive unit cell.
    length_tolerance : float, default :math:`10^{-8}`
        Tolerance for length variables (lengths of the lattice vectors). Completely
        ignored by this function, the arguments are defined only for the homogeneity of
        the input for all 14 Bravais lattice types.
    angle_tolerance : float, default :math:`10^{-4}`
        Tolerance for angle variables (angles of the lattice). Completely ignored by this
        function, the arguments are defined only for the homogeneity of the input for all
        14 Bravais lattice types.

    Returns
    -------
    S : (3,3) :numpy:`ndarray`
        Transformation matrix :math:`S`.

    Notes
    -----
    It is assumed that the ``cell`` has the symmetries of the cubic lattice.
    If the cell is not cubic, the function will not work correctly.
    """

    return np.eye(3, dtype=float)


def _FCC_get_S_matrix(cell, length_tolerance=1e-8, angle_tolerance=1e-4):
    r"""
    For arbitrary face-centered cubic cell returns matrix S that transforms it to the
    standardized form.

    .. versionchanged:: 0.4.0  Renamed from ``FCC_standardize_cell``

    See :ref:`guide_fcc` and :ref:`user-guide_conventions_cell_standardization` for the
    details.

    Parameters
    ----------
    cell : (3,3) |array-like|_
        Primitive unit cell.
    length_tolerance : float, default :math:`10^{-8}`
        Tolerance for length variables (lengths of the lattice vectors). Completely
        ignored by this function, the arguments are defined only for the homogeneity of
        the input for all 14 Bravais lattice types.
    angle_tolerance : float, default :math:`10^{-4}`
        Tolerance for angle variables (angles of the lattice). Completely ignored by this
        function, the arguments are defined only for the homogeneity of the input for all
        14 Bravais lattice types.

    Returns
    -------
    S : (3,3) :numpy:`ndarray`
        Transformation matrix :math:`S`.

    Notes
    -----
    It is assumed that the ``cell`` has the symmetries of the face-centered cubic lattice.
    If the cell is not face-centered cubic, the function will not work correctly.
    """

    return np.eye(3, dtype=float)


def _BCC_get_S_matrix(cell, length_tolerance=1e-8, angle_tolerance=1e-4):
    r"""
    For arbitrary body-centered cubic cell returns matrix S that transforms it to the
    standardized form.

    .. versionchanged:: 0.4.0  Renamed from ``BCC_standardize_cell``

    See :ref:`guide_fcc` and :ref:`user-guide_conventions_cell_standardization` for the
    details.

    Parameters
    ----------
    cell : (3,3) |array-like|_
        Primitive unit cell.
    length_tolerance : float, default :math:`10^{-8}`
        Tolerance for length variables (lengths of the lattice vectors). Completely
        ignored by this function, the arguments are defined only for the homogeneity of
        the input for all 14 Bravais lattice types.
    angle_tolerance : float, default :math:`10^{-4}`
        Tolerance for angle variables (angles of the lattice). Completely ignored by this
        function, the arguments are defined only for the homogeneity of the input for all
        14 Bravais lattice types.

    Returns
    -------
    S : (3,3) :numpy:`ndarray`
        Transformation matrix :math:`S`.

    Notes
    -----
    It is assumed that the ``cell`` has the symmetries of the body-centered cubic lattice.
    If the cell is not body-centered cubic, the function will not work correctly.
    """

    return np.eye(3, dtype=float)


def _TET_get_S_matrix(cell, length_tolerance=1e-8, angle_tolerance=1e-4):
    r"""
    For arbitrary tetragonal cell returns matrix S that transforms it to the
    standardized form.

    .. versionchanged:: 0.4.0  Renamed from ``TET_standardize_cell``

    See :ref:`guide_tet` and :ref:`user-guide_conventions_cell_standardization` for the
    details.

    Parameters
    ----------
    cell : (3,3) |array-like|_
        Primitive unit cell.
    length_tolerance : float, default :math:`10^{-8}`
        Tolerance for length variables (lengths of the lattice vectors).
    angle_tolerance : float, default :math:`10^{-4}`
        Tolerance for angle variables (angles of the lattice). Completely ignored by this
        function, the arguments are defined only for the homogeneity of the input for all
        14 Bravais lattice types.

    Returns
    -------
    S : (3,3) :numpy:`ndarray`
        Transformation matrix :math:`S`

    Notes
    -----
    It is assumed that the ``cell`` has the symmetries of the tetragonal lattice. If the
    cell is not tetragonal, the function will not work correctly.

    Raises
    ------
    :py:class:`.StandardizationTypeMismatch`
        If none of the tetragonal conditions are satisfied.
    """

    a, b, c, _, _, _ = get_params(cell)

    if compare_numerically(a, "==", b, eps=length_tolerance) and compare_numerically(
        b, "!=", c, eps=length_tolerance
    ):
        S = np.eye(3, dtype=float)
    elif compare_numerically(b, "==", c, eps=length_tolerance) and compare_numerically(
        c, "!=", a, eps=length_tolerance
    ):
        S = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=float)
    elif compare_numerically(a, "==", c, eps=length_tolerance) and compare_numerically(
        c, "!=", b, eps=length_tolerance
    ):
        S = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=float)
    else:
        raise StandardizationTypeMismatch("tetragonal")

    return S


def _BCT_get_S_matrix(cell, length_tolerance=1e-8, angle_tolerance=1e-4):
    r"""
    For arbitrary body-centered tetragonal cell returns matrix S that transforms it to the
    standardized form.

    .. versionchanged:: 0.4.0  Renamed from ``BCT_standardize_cell``

    See :ref:`guide_bct` and :ref:`user-guide_conventions_cell_standardization` for the
    details.

    Parameters
    ----------
    cell : (3,3) :numpy:`ndarray`
        Primitive unit cell.
    length_tolerance : float, default :math:`10^{-8}`
        Tolerance for length variables (lengths of the lattice vectors). Completely
        ignored by this function, the arguments are defined only for the homogeneity of
        the input for all 14 Bravais lattice types.
    angle_tolerance : float, default :math:`10^{-4}`
        Tolerance for angle variables (angles of the lattice).

    Returns
    -------
    S : (3,3) :numpy:`ndarray`
        Transformation matrix :math:`S`

    Notes
    -----
    It is assumed that the ``cell`` has the symmetries of the body-centered tetragonal
    lattice. If the cell is not body-centered tetragonal, the function will not work correctly.

    Raises
    ------
    :py:class:`.StandardizationTypeMismatch`
        If none of the body-centered tetragonal conditions are satisfied.
    """
    cell = np.array(cell)

    _, _, _, alpha, beta, gamma = get_params(cell)

    if compare_numerically(
        alpha, "==", beta, eps=angle_tolerance
    ) and compare_numerically(beta, "!=", gamma, eps=angle_tolerance):
        S = np.eye(3, dtype=float)
    elif compare_numerically(
        beta, "==", gamma, eps=angle_tolerance
    ) and compare_numerically(gamma, "!=", alpha, eps=angle_tolerance):
        S = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=float)
    elif compare_numerically(
        alpha, "==", gamma, eps=angle_tolerance
    ) and compare_numerically(gamma, "!=", beta, eps=angle_tolerance):
        S = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=float)
    else:
        raise StandardizationTypeMismatch("body-centered tetragonal")

    return S


def _ORC_get_S_matrix(cell, length_tolerance=1e-8, angle_tolerance=1e-4):
    r"""
    For arbitrary orthorhombic cell returns matrix S that transforms it to the
    standardized form.

    .. versionchanged:: 0.4.0  Renamed from ``ORC_standardize_cell``

    See :ref:`guide_orc` and :ref:`user-guide_conventions_cell_standardization` for the
    details.

    Parameters
    ----------
    cell : (3,3) |array-like|_
        Primitive unit cell.
    length_tolerance : float, default :math:`10^{-8}`
        Tolerance for length variables (lengths of the lattice vectors).
    angle_tolerance : float, default :math:`10^{-4}`
        Tolerance for angle variables (angles of the lattice). Completely ignored by this
        function, the arguments are defined only for the homogeneity of the input for all
        14 Bravais lattice types.

    Returns
    -------
    S : (3,3) :numpy:`ndarray`
        Transformation matrix :math:`S`

    Notes
    -----
    It is assumed that the ``cell`` has the symmetries of the orthorhombic lattice. If
    the cell is not orthorhombic, the function will not work correctly.

    Raises
    ------
    :py:class:`.StandardizationTypeMismatch`
        If none of the orthorhombic conditions are satisfied.
    """

    a, b, c, _, _, _ = get_params(cell)

    if compare_numerically(c, ">", b, eps=length_tolerance) and compare_numerically(
        b, ">", a, eps=length_tolerance
    ):
        S = np.eye(3, dtype=float)
    elif compare_numerically(c, ">", a, eps=length_tolerance) and compare_numerically(
        a, ">", b, eps=length_tolerance
    ):
        S = np.array([[0, -1, 0], [-1, 0, 0], [0, 0, -1]], dtype=float)
    elif compare_numerically(b, ">", c, eps=length_tolerance) and compare_numerically(
        c, ">", a, eps=length_tolerance
    ):
        S = np.array([[-1, 0, 0], [0, 0, -1], [0, -1, 0]], dtype=float)
    elif compare_numerically(b, ">", a, eps=length_tolerance) and compare_numerically(
        a, ">", c, eps=length_tolerance
    ):
        S = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=float)
    elif compare_numerically(a, ">", c, eps=length_tolerance) and compare_numerically(
        c, ">", b, eps=length_tolerance
    ):
        S = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=float)
    elif compare_numerically(a, ">", b, eps=length_tolerance) and compare_numerically(
        b, ">", c, eps=length_tolerance
    ):
        S = np.array([[0, 0, -1], [0, -1, 0], [-1, 0, 0]], dtype=float)
    else:
        raise StandardizationTypeMismatch("orthorhombic")

    return S


def _ORCF_get_S_matrix(cell, length_tolerance=1e-8, angle_tolerance=1e-4):
    r"""
    For arbitrary face-centered orthorhombic cell returns matrix S that transforms it to
    the standardized form.

    .. versionchanged:: 0.4.0  Renamed from ``ORCF_standardize_cell``

    See :ref:`guide_orcf` and :ref:`user-guide_conventions_cell_standardization` for the
    details.

    Parameters
    ----------
    cell : (3,3) |array-like|_
        Primitive unit cell.
    length_tolerance : float, default :math:`10^{-8}`
        Tolerance for length variables (lengths of the lattice vectors).
    angle_tolerance : float, default :math:`10^{-4}`
        Tolerance for angle variables (angles of the lattice). Completely ignored by this
        function, the arguments are defined only for the homogeneity of the input for all
        14 Bravais lattice types.

    Returns
    -------
    S : (3,3) :numpy:`ndarray`
        Transformation matrix :math:`S`

    Notes
    -----
    It is assumed that the ``cell`` has the symmetries of the face-centered orthorhombic
    lattice. If the cell is not face-centered orthorhombic, the function will not work
    correctly.

    Raises
    ------
    :py:class:`.StandardizationTypeMismatch`
        If none of the face-centered orthorhombic conditions are satisfied.
    """

    a, b, c, _, _, _ = get_params(cell)

    if compare_numerically(c, "<", b, eps=length_tolerance) and compare_numerically(
        b, "<", a, eps=length_tolerance
    ):
        S = np.eye(3, dtype=float)
    elif compare_numerically(c, "<", a, eps=length_tolerance) and compare_numerically(
        a, "<", b, eps=length_tolerance
    ):
        S = np.array([[0, -1, 0], [-1, 0, 0], [0, 0, -1]], dtype=float)
    elif compare_numerically(b, "<", c, eps=length_tolerance) and compare_numerically(
        c, "<", a, eps=length_tolerance
    ):
        S = np.array([[-1, 0, 0], [0, 0, -1], [0, -1, 0]], dtype=float)
    elif compare_numerically(b, "<", a, eps=length_tolerance) and compare_numerically(
        a, "<", c, eps=length_tolerance
    ):
        S = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=float)
    elif compare_numerically(a, "<", c, eps=length_tolerance) and compare_numerically(
        c, "<", b, eps=length_tolerance
    ):
        S = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=float)
    elif compare_numerically(a, "<", b, eps=length_tolerance) and compare_numerically(
        b, "<", c, eps=length_tolerance
    ):
        S = np.array([[0, 0, -1], [0, -1, 0], [-1, 0, 0]], dtype=float)
    else:
        raise StandardizationTypeMismatch("face-centered orthorhombic")

    return S


def _ORCI_get_S_matrix(cell, length_tolerance=1e-8, angle_tolerance=1e-4):
    r"""
    For arbitrary body-centered orthorhombic cell returns matrix S that transforms it to
    the standardized form.

    .. versionchanged:: 0.4.0  Renamed from ``ORCI_standardize_cell``

    See :ref:`guide_orci` and :ref:`user-guide_conventions_cell_standardization` for the
    details.

    Parameters
    ----------
    cell : (3,3) |array-like|_
        Primitive unit cell.
    length_tolerance : float, default :math:`10^{-8}`
        Tolerance for length variables (lengths of the lattice vectors). Completely
        ignored by this function, the arguments are defined only for the homogeneity of
        the input for all 14 Bravais lattice types.
    angle_tolerance : float, default :math:`10^{-4}`
        Tolerance for angle variables (angles of the lattice).

    Returns
    -------
    S : (3,3) :numpy:`ndarray`
        Transformation matrix :math:`S`

    Notes
    -----
    It is assumed that the ``cell`` has the symmetries of the body-centered orthorhombic
    lattice. If the cell is not body-centered orthorhombic, the function will not work
    correctly.

    Raises
    ------
    :py:class:`.StandardizationTypeMismatch`
        If none of the body-centered orthorhombic conditions are satisfied.
    """

    _, _, _, alpha, beta, gamma = get_params(cell)

    if compare_numerically(
        gamma, "<", beta, eps=length_tolerance
    ) and compare_numerically(beta, "<", alpha, eps=length_tolerance):
        S = np.eye(3, dtype=float)
    elif compare_numerically(
        gamma, "<", alpha, eps=length_tolerance
    ) and compare_numerically(alpha, "<", beta, eps=length_tolerance):
        S = np.array([[0, -1, 0], [-1, 0, 0], [0, 0, -1]], dtype=float)
    elif compare_numerically(
        beta, "<", gamma, eps=length_tolerance
    ) and compare_numerically(gamma, "<", alpha, eps=length_tolerance):
        S = np.array([[-1, 0, 0], [0, 0, -1], [0, -1, 0]], dtype=float)
    elif compare_numerically(
        beta, "<", alpha, eps=length_tolerance
    ) and compare_numerically(alpha, "<", gamma, eps=length_tolerance):
        S = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=float)
    elif compare_numerically(
        alpha, "<", gamma, eps=length_tolerance
    ) and compare_numerically(gamma, "<", beta, eps=length_tolerance):
        S = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=float)
    elif compare_numerically(
        alpha, "<", beta, eps=length_tolerance
    ) and compare_numerically(beta, "<", gamma, eps=length_tolerance):
        S = np.array([[0, 0, -1], [0, -1, 0], [-1, 0, 0]], dtype=float)
    else:
        raise StandardizationTypeMismatch("body-centered orthorhombic")

    return S


def _ORCC_get_S_matrix(cell, length_tolerance=1e-8, angle_tolerance=1e-4):
    r"""
    For arbitrary base-centered orthorhombic cell returns matrix S that transforms it to
    the standardized form.

    .. versionchanged:: 0.4.0  Renamed from ``ORCC_standardize_cell``

    See :ref:`guide_orcc` and :ref:`user-guide_conventions_cell_standardization` for the
    details.

    Parameters
    ----------
    cell : (3,3) |array-like|_
        Primitive unit cell.
    length_tolerance : float, default :math:`10^{-8}`
        Tolerance for length variables (lengths of the lattice vectors). Completely
        ignored by this function, the arguments are defined only for the homogeneity of
        the input for all 14 Bravais lattice types.
    angle_tolerance : float, default :math:`10^{-4}`
        Tolerance for angle variables (angles of the lattice).

    Returns
    -------
    S : (3,3) :numpy:`ndarray`
        Transformation matrix :math:`S`

    Notes
    -----
    It is assumed that the ``cell`` has the symmetries of the base-centered orthorhombic
    lattice. If the cell is not base-centered orthorhombic, the function will not work
    correctly.

    Raises
    ------
    :py:class:`.StandardizationTypeMismatch`
        If none of the base-centered orthorhombic conditions are satisfied.
    """

    _, _, _, alpha, beta, gamma = get_params(cell)

    if (
        compare_numerically(alpha, "==", PI / 2, eps=angle_tolerance)
        and compare_numerically(beta, "==", PI / 2, eps=angle_tolerance)
        and compare_numerically(gamma, ">", PI / 2, eps=angle_tolerance)
    ):
        S = np.eye(3, dtype=float)
    elif (
        compare_numerically(alpha, "==", PI / 2, eps=angle_tolerance)
        and compare_numerically(beta, "==", PI / 2, eps=angle_tolerance)
        and compare_numerically(gamma, "<", PI / 2, eps=angle_tolerance)
    ):
        S = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]], dtype=float)
    elif (
        compare_numerically(beta, "==", PI / 2, eps=angle_tolerance)
        and compare_numerically(gamma, "==", PI / 2, eps=angle_tolerance)
        and compare_numerically(alpha, ">", PI / 2, eps=angle_tolerance)
    ):
        S = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=float)
    elif (
        compare_numerically(beta, "==", PI / 2, eps=angle_tolerance)
        and compare_numerically(gamma, "==", PI / 2, eps=angle_tolerance)
        and compare_numerically(alpha, "<", PI / 2, eps=angle_tolerance)
    ):
        S = np.array([[0, 0, 1], [0, -1, 0], [1, 0, 0]], dtype=float)

    elif (
        compare_numerically(alpha, "==", PI / 2, eps=angle_tolerance)
        and compare_numerically(gamma, "==", PI / 2, eps=angle_tolerance)
        and compare_numerically(beta, ">", PI / 2, eps=angle_tolerance)
    ):
        S = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=float)
    elif (
        compare_numerically(alpha, "==", PI / 2, eps=angle_tolerance)
        and compare_numerically(gamma, "==", PI / 2, eps=angle_tolerance)
        and compare_numerically(beta, "<", PI / 2, eps=angle_tolerance)
    ):
        S = np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]], dtype=float)
    else:
        raise StandardizationTypeMismatch("base-centered orthorhombic")

    return S


def _HEX_get_S_matrix(cell, length_tolerance=1e-8, angle_tolerance=1e-4):
    r"""
    For arbitrary hexagonal cell returns matrix S that transforms it to the standardized
    form.

    .. versionchanged:: 0.4.0  Renamed from ``HEX_standardize_cell``

    See :ref:`guide_hex` and :ref:`user-guide_conventions_cell_standardization` for the
    details.

    Parameters
    ----------
    cell : (3,3) |array-like|_
        Primitive unit cell.
    length_tolerance : float, default :math:`10^{-8}`
        Tolerance for length variables (lengths of the lattice vectors). Completely
        ignored by this function, the arguments are defined only for the homogeneity of
        the input for all 14 Bravais lattice types.
    angle_tolerance : float, default :math:`10^{-4}`
        Tolerance for angle variables (angles of the lattice).

    Returns
    -------
    S : (3,3) :numpy:`ndarray`
        Transformation matrix :math:`S`

    Notes
    -----
    It is assumed that the ``cell`` has the symmetries of the hexagonal lattice. If the
    cell is not hexagonal, the function will not work correctly.

    Raises
    ------
    :py:class:`.StandardizationTypeMismatch`
        If none of the hexagonal conditions are satisfied.
    """

    # Step 1
    _, _, _, alpha, beta, gamma = get_params(cell)

    if compare_numerically(
        alpha, "==", PI / 2, eps=angle_tolerance
    ) and compare_numerically(beta, "==", PI / 2, eps=angle_tolerance):
        S1 = np.eye(3, dtype=float)
    elif compare_numerically(
        beta, "==", PI / 2, eps=angle_tolerance
    ) and compare_numerically(gamma, "==", PI / 2, eps=angle_tolerance):
        S1 = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=float)
    elif compare_numerically(
        alpha, "==", PI / 2, eps=angle_tolerance
    ) and compare_numerically(gamma, "==", PI / 2, eps=angle_tolerance):
        S1 = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=float)
    else:
        raise StandardizationTypeMismatch("hexagonal", step="first")

    # Step 2
    cell1 = S1.T @ cell
    _, _, _, _, _, gamma = get_params(cell)

    if compare_numerically(gamma, "==", 2 * PI / 3, eps=angle_tolerance):
        S2 = np.eye(3, dtype=float)
    elif compare_numerically(gamma, "==", PI / 3, eps=angle_tolerance):
        S2 = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]], dtype=float)
    else:
        raise StandardizationTypeMismatch("hexagonal", step="second")

    return S1 @ S2


def _RHL_get_S_matrix(cell, length_tolerance=1e-8, angle_tolerance=1e-4):
    r"""
    For arbitrary rhombohedral cell returns matrix S that transforms it to the standardized
    form.

    .. versionchanged:: 0.4.0  Renamed from ``RHL_standardize_cell``

    See :ref:`guide_rhl` and :ref:`user-guide_conventions_cell_standardization` for the
    details.

    Parameters
    ----------
    cell : (3,3) |array-like|_
        Primitive unit cell.
    length_tolerance : float, default :math:`10^{-8}`
        Tolerance for length variables (lengths of the lattice vectors). Completely
        ignored by this function, the arguments are defined only for the homogeneity of
        the input for all 14 Bravais lattice types.
    angle_tolerance : float, default :math:`10^{-4}`
        Tolerance for angle variables (angles of the lattice). Completely ignored by this
        function, the arguments are defined only for the homogeneity of the input for all
        14 Bravais lattice types.

    Returns
    -------
    S : (3,3) :numpy:`ndarray`
        Transformation matrix :math:`S`

    Notes
    -----
    It is assumed that the ``cell`` has the symmetries of the rhombohedral lattice. If the
    cell is not rhombohedral, the function will not work correctly.
    """

    return np.eye(3, dtype=float)


def _MCL_get_S_matrix(cell, length_tolerance=1e-8, angle_tolerance=1e-4):
    r"""
    For arbitrary monoclinic cell returns matrix S that transforms it to the standardized
    form.

    .. versionchanged:: 0.4.0  Renamed from ``MCL_standardize_cell``

    See :ref:`guide_mcl` and :ref:`user-guide_conventions_cell_standardization` for the
    details.

    Parameters
    ----------
    cell : (3,3) |array-like|_
        Primitive unit cell.
    length_tolerance : float, default :math:`10^{-8}`
        Tolerance for length variables (lengths of the lattice vectors). Completely
        ignored by this function, the arguments are defined only for the homogeneity of
        the input for all 14 Bravais lattice types.
    angle_tolerance : float, default :math:`10^{-4}`
        Tolerance for angle variables (angles of the lattice). Completely ignored by this
        function, the arguments are defined only for the homogeneity of the input for all
        14 Bravais lattice types.

    Returns
    -------
    S : (3,3) :numpy:`ndarray`
        Transformation matrix :math:`S`

    Notes
    -----
    It is assumed that the ``cell`` has the symmetries of the monoclinic lattice. If the
    cell is not monoclinic, the function will not work correctly.

    Raises
    ------
    :py:class:`.StandardizationTypeMismatch`
        If none of the monoclinic conditions are satisfied.
    """

    # Step 1

    sp23, sp13, sp12 = get_scalar_products(cell)

    if (
        compare_numerically(sp13, "==", 0.0, rtol=rtol, atol=atol)
        and compare_numerically(sp12, "==", 0.0, rtol=rtol, atol=atol)
        and compare_numerically(sp23, "!=", 0.0, rtol=rtol, atol=atol)
    ):
        S1 = np.eye(3, dtype=float)
    elif (
        compare_numerically(sp23, "==", 0.0, rtol=rtol, atol=atol)
        and compare_numerically(sp12, "==", 0.0, rtol=rtol, atol=atol)
        and compare_numerically(sp13, "!=", 0.0, rtol=rtol, atol=atol)
    ):
        S1 = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=float)
    elif (
        compare_numerically(sp23, "==", 0.0, rtol=rtol, atol=atol)
        and compare_numerically(sp13, "==", 0.0, rtol=rtol, atol=atol)
        and compare_numerically(sp12, "!=", 0.0, rtol=rtol, atol=atol)
    ):
        S1 = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=float)
    else:
        raise StandardizationTypeMismatch("monoclinic", step="First")

    # Step 2
    cell1 = np.linalg.inv(S1.T) @ cell
    a, b, c, alpha, beta, gamma = get_params(cell1)

    if b < c:
        S2 = np.eye(3, dtype=float)
    elif b > c:
        S2 = np.array([[-1, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=float)
    else:
        raise StandardizationTypeMismatch("monoclinic", step="Second")

    # Step 3
    cell2 = np.linalg.inv(S2.T) @ cell1
    sp23, sp13, sp12 = get_scalar_products(cell2)
    if compare_numerically(sp23, ">", 0, rtol=rtol, atol=atol):
        S3 = np.eye(3, dtype=float)
    elif compare_numerically(sp23, "<", 0, rtol=rtol, atol=atol):
        S3 = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]], dtype=float)
    else:
        raise StandardizationTypeMismatch("monoclinic", step="Third")

    return S3 @ S2 @ S1


def _MCLC_get_S_matrix(cell, length_tolerance=1e-8, angle_tolerance=1e-4):
    r"""
    For arbitrary base-centered monoclinic cell returns matrix S that transforms it to the
    standardized form.

    .. versionchanged:: 0.4.0  Renamed from ``MCLC_standardize_cell``

    See :ref:`guide_mclc` and :ref:`user-guide_conventions_cell_standardization` for the
    details.

    Parameters
    ----------
    cell : (3,3) |array-like|_
        Primitive unit cell.
    length_tolerance : float, default :math:`10^{-8}`
        Tolerance for length variables (lengths of the lattice vectors). Completely
        ignored by this function, the arguments are defined only for the homogeneity of
        the input for all 14 Bravais lattice types.
    angle_tolerance : float, default :math:`10^{-4}`
        Tolerance for angle variables (angles of the lattice). Completely ignored by this
        function, the arguments are defined only for the homogeneity of the input for all
        14 Bravais lattice types.

    Returns
    -------
    S : (3,3) :numpy:`ndarray`
        Transformation matrix :math:`S`

    Notes
    -----
    It is assumed that the ``cell`` has the symmetries of the base-centered monoclinic
    lattice. If the cell is not base-centered monoclinic, the function will not work
    correctly.

    Raises
    ------
    :py:class:`.StandardizationTypeMismatch`
        If none of the base-centered monoclinic conditions are satisfied.
    """

    # Step 1

    a, b, c, alpha, beta, gamma = get_params(cell)

    if compare_numerically(a, "==", b, rtol=rtol, atol=atol) and compare_numerically(
        b, "!=", c, rtol=rtol, atol=atol
    ):
        S1 = np.eye(3, dtype=float)
    elif compare_numerically(b, "==", c, rtol=rtol, atol=atol) and compare_numerically(
        c, "!=", a, rtol=rtol, atol=atol
    ):
        S1 = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=float)
    elif compare_numerically(c, "==", a, rtol=rtol, atol=atol) and compare_numerically(
        a, "!=", b, rtol=rtol, atol=atol
    ):
        S1 = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=float)
    else:
        raise StandardizationTypeMismatch("base-centered monoclinic", step="First")

    # Step 2
    cell1 = np.linalg.inv(S1.T) @ cell
    a, b, c, alpha, beta, gamma = get_params(cell1)
    sp23, sp13, sp12 = get_scalar_products(cell1)

    if compare_numerically(
        2 * a**2 * (1 + sp12 / a / b), "<=", c**2, rtol=rtol, atol=atol
    ):
        S2 = np.eye(3, dtype=float)
    else:
        S2 = np.array([[-0.5, 0.5, 1], [0.5, -0.5, 1], [0.5, 0.5, 0]], dtype=float)

    # Step 3
    cell2 = np.linalg.inv(S2.T) @ cell1
    sp23, sp13, sp12 = get_scalar_products(cell2)
    if compare_numerically(sp23, ">", 0, rtol=rtol, atol=atol):
        S3 = np.eye(3, dtype=float)
    elif compare_numerically(sp23, "<", 0, rtol=rtol, atol=atol):
        S3 = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]], dtype=float)
    else:
        raise StandardizationTypeMismatch("base-centered monoclinic", step="Third")

    return S3 @ S2 @ S1


def _TRI_get_S_matrix(cell, length_tolerance=1e-8, angle_tolerance=1e-4):
    r"""
    For arbitrary triclinic cell returns matrix S that transforms it to the
    standardized form.

    .. versionchanged:: 0.4.0  Renamed from ``TRI_standardize_cell``

    See :ref:`guide_tri` and :ref:`user-guide_conventions_cell_standardization` for the
    details.

    Parameters
    ----------
    cell : (3,3) |array-like|_
        Primitive unit cell.
    length_tolerance : float, default :math:`10^{-8}`
        Tolerance for length variables (lengths of the lattice vectors). Completely
        ignored by this function, the arguments are defined only for the homogeneity of
        the input for all 14 Bravais lattice types.
    angle_tolerance : float, default :math:`10^{-4}`
        Tolerance for angle variables (angles of the lattice). Completely ignored by this
        function, the arguments are defined only for the homogeneity of the input for all
        14 Bravais lattice types.

    Returns
    -------
    S : (3,3) :numpy:`ndarray`
        Transformation matrix :math:`S`

    Notes
    -----
    It is assumed that the ``cell`` has the symmetries of the triclinic lattice. If the
    cell is not triclinic, the function will not work correctly.

    Raises
    ------
    :py:class:`.StandardizationTypeMismatch`
        If none of the triclinic conditions are satisfied.
    """

    # Compute reciprocal cell
    rcell = get_reciprocal(cell)

    # Step 1
    sp23, sp13, sp12 = get_scalar_products(rcell)
    a, b, c, alpha, beta, gamma = get_params(rcell)

    if (
        compare_numerically(alpha, ">=", 90.0, rtol=rtol, atol=atol)
        and compare_numerically(beta, ">=", 90.0, rtol=rtol, atol=atol)
        and compare_numerically(gamma, ">=", 90.0, rtol=rtol, atol=atol)
    ) or (
        compare_numerically(alpha, "<=", 90.0, rtol=rtol, atol=atol)
        and compare_numerically(beta, "<=", 90.0, rtol=rtol, atol=atol)
        and compare_numerically(gamma, "<=", 90.0, rtol=rtol, atol=atol)
    ):
        S1 = np.eye(3, dtype=float)
    elif (
        compare_numerically(alpha, ">=", 90.0, rtol=rtol, atol=atol)
        and compare_numerically(beta, ">=", 90.0, rtol=rtol, atol=atol)
        and compare_numerically(gamma, "<=", 90.0, rtol=rtol, atol=atol)
    ) or (
        compare_numerically(alpha, "<=", 90.0, rtol=rtol, atol=atol)
        and compare_numerically(beta, "<=", 90.0, rtol=rtol, atol=atol)
        and compare_numerically(gamma, ">=", 90.0, rtol=rtol, atol=atol)
    ):
        S1 = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]], dtype=float)
    elif (
        compare_numerically(alpha, ">=", 90.0, rtol=rtol, atol=atol)
        and compare_numerically(beta, "<=", 90.0, rtol=rtol, atol=atol)
        and compare_numerically(gamma, ">=", 90.0, rtol=rtol, atol=atol)
    ) or (
        compare_numerically(alpha, "<=", 90.0, rtol=rtol, atol=atol)
        and compare_numerically(beta, ">=", 90.0, rtol=rtol, atol=atol)
        and compare_numerically(gamma, "<=", 90.0, rtol=rtol, atol=atol)
    ):
        S1 = np.array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]], dtype=float)
    elif (
        compare_numerically(alpha, "<=", 90.0, rtol=rtol, atol=atol)
        and compare_numerically(beta, ">=", 90.0, rtol=rtol, atol=atol)
        and compare_numerically(gamma, ">=", 90.0, rtol=rtol, atol=atol)
    ) or (
        compare_numerically(alpha, ">=", 90.0, rtol=rtol, atol=atol)
        and compare_numerically(beta, "<=", 90.0, rtol=rtol, atol=atol)
        and compare_numerically(gamma, "<=", 90.0, rtol=rtol, atol=atol)
    ):
        S1 = np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]], dtype=float)
    else:
        raise StandardizationTypeMismatch("triclinic", step="First")

    # Step 2
    rcell1 = np.linalg.inv(S1.T) @ rcell
    sp23, sp13, sp12 = get_scalar_products(rcell1)
    a, b, c, alpha, beta, gamma = get_params(rcell1)

    if (
        gamma == min(alpha, beta, gamma)
        and compare_numerically(gamma, ">=", 90.0)
        or (gamma == max(alpha, beta, gamma) and compare_numerically(gamma, "<=", 90.0))
    ):
        S2 = np.eye(3, dtype=float)
    elif (
        beta == min(alpha, beta, gamma)
        and compare_numerically(beta, ">=", 90.0)
        or (beta == max(alpha, beta, gamma) and compare_numerically(beta, "<=", 90.0))
    ):
        S2 = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=float)
    elif (
        alpha == min(alpha, beta, gamma)
        and compare_numerically(alpha, ">=", 90.0)
        or (alpha == max(alpha, beta, gamma) and compare_numerically(alpha, "<=", 90.0))
    ):
        S2 = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=float)
    else:
        raise StandardizationTypeMismatch("triclinic", step="Second")

    return S2 @ S1


def get_S_matrix(cell, lattice_type=None, length_tolerance=1e-8, angle_tolerance=1e-4):
    r"""
    Analyse arbitrary cell and redefine it
    if required to ensure the unique choice of lattice vectors.

    .. versionchanged:: 0.4.0  Renamed from ``standardize_cell``

    See :ref:`docs for each Bravais lattice <user-guide_conventions_bravais-lattices>` for the details.

    Parameters
    ----------
    cell : (3,3) |array-like|_
        Primitive unit cell.
    lattice_type : str, optional
        One of the 14 lattice types that correspond to the provided ``cell``.
        If not provided, then computed automatically. Case-insensitive.
    length_tolerance : float, default :math:`10^{-8}`
        Tolerance for length variables (lengths of the lattice vectors). Default values
        are chosen for the contexts of condense matter physics, where Angstroms are used.
        Please choose appropriate tolerance for your problem.
    angle_tolerance : float, default :math:`10^{-4}`
        Tolerance for angle variables (angles of the lattice). Default values are chosen
        for the contexts of condense matter physics, where Angstroms are used. Please
        choose appropriate tolerance for your problem.

    Returns
    -------
    S : (3,3) :numpy:`ndarray`
        Transformation matrix :math:`S`
    """
    cell = np.array(cell, dtype=float)

    if lattice_type is None:
        lattice_type = lepage(cell, eps_relative=rtol, eps_angle=atol)

    lattice_type = lattice_type.upper()

    functions = {
        "CUB": _CUB_get_S_matrix,
        "FCC": _FCC_get_S_matrix,
        "BCC": _BCC_get_S_matrix,
        "TET": _TET_get_S_matrix,
        "BCT": _BCT_get_S_matrix,
        "ORC": _ORC_get_S_matrix,
        "ORCF": _ORCF_get_S_matrix,
        "ORCI": _ORCI_get_S_matrix,
        "ORCC": _ORCC_get_S_matrix,
        "HEX": _HEX_get_S_matrix,
        "RHL": _RHL_get_S_matrix,
        "MCL": _MCL_get_S_matrix,
        "MCLC": _MCLC_get_S_matrix,
        "TRI": _TRI_get_S_matrix,
    }

    return functions[lattice_type](cell, rtol=rtol, atol=atol)


def get_C_matrix(lattice_type):
    r"""
    Transformation matrix that transforms primitive cell
    to the **conventional standardized** cell.

    See :ref:`user-guide_conventions_cell_standardization` for details.

    Parameters
    ----------
    lattice_type : str
        One of the 14 lattice types that correspond to the provided ``cell``.
        If not provided, then computed automatically. Case-insensitive.

    Returns
    -------
    C_matrix : (3,3) :numpy:`ndarray`
    """

    return C_MATRICES[lattice_type.upper()]


def get_standardized(cell, S_matrix=None, rtol=1e-8, atol=1e-8):
    R"""
    Standardize cell with respect to the Bravais lattice type as defined in [1]_.

    .. versionadded:: 0.3.0

    Parameters
    ----------
    cell : (3,3) |array-like|_
        Primitive unit cell.
    S_matrix : (3,3) |array-like|_, optional
        Transformation matrix S.
    rtol : float, default TODO
        Relative tolerance for numerical comparison. Ignored if ``S_matrix`` is provided.
    atol : float, default TODO
        Absolute tolerance for numerical comparison. Ignored if ``S_matrix`` is provided.

    Returns
    -------
    cell : (3,3) :numpy:`ndarray`
        Standardized cell. Rows are lattice vectors. Independent from the initial cell,
        safe to modify.

    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp.299-312.
    """

    cell = np.array(cell, dtype=float)

    if S_matrix is None:
        lattice_type = lepage(cell, eps_relative=rtol, eps_angle=atol)

        S_matrix = get_S_matrix(cell, lattice_type, rtol=rtol, atol=atol)
    else:
        S_matrix = np.array(S_matrix, dtype=float)

    return np.linalg.inv(S_matrix.T) @ cell


def get_conventional(cell, S_matrix=None, C_matrix=None, rtol=1e-8, atol=1e-8):
    r"""
    Conventional cell.

    .. math::

        (\boldsymbol{a_1}, \boldsymbol{a_2}, \boldsymbol{a_3})
        =
        (\boldsymbol{a^{cs}}_1, \boldsymbol{a^{cs}}_2, \boldsymbol{a^{cs}}_3)
        (\boldsymbol{C}\boldsymbol{S})

    .. code-block:: python

        conv_cell = np.linalg.inv(C @ S).T @ cell

    Parameters
    ----------
    cell : (3,3) |array-like|_
        Primitive unit cell.
    S_matrix : (3,3) |array-like|_, optional
        Transformation matrix S.
    C_matrix : (3,3) |array-like|_, optional
        Transformation matrix C.
    rtol : float, default TODO
        Relative tolerance for numerical comparison. Ignored if ``S_matrix`` is provided.
    atol : float, default TODO
        Absolute tolerance for numerical comparison. Ignored if ``S_matrix`` is provided.

    Returns
    -------
    conv_cell : (3, 3) :numpy:`ndarray`
        Conventional cell, rows are vectors, columns are coordinates.
    """
    cell = np.array(cell, dtype=float)

    if S_matrix is None or C_matrix is None:
        lattice_type = lepage(cell, eps_relative=rtol, eps_angle=atol)

    if C_matrix is None:
        C_matrix = get_C_matrix(lattice_type)
    else:
        C_matrix = np.array(C_matrix, dtype=float)

    if S_matrix is None:
        S_matrix = get_S_matrix(cell, lattice_type, rtol=rtol, atol=atol)
    else:
        S_matrix = np.array(S_matrix, dtype=float)

    return C_matrix.T @ S_matrix.T @ cell


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
