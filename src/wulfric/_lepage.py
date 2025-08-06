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
from math import acos

import numpy as np

from wulfric._exceptions import NiggliReductionFailed
from wulfric.cell._basic_manipulation import get_reciprocal
from wulfric.cell._niggli import get_niggli
from wulfric.constants._numerical import TODEGREES

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


################################################################################
#                                  LePage CUB                                  #
################################################################################
def _check_cub(angles, axes, angle_tolerance):
    target_angles = np.array(
        [
            [0, 45, 45, 45, 45, 90, 90, 90, 90],
            [0, 45, 45, 45, 45, 90, 90, 90, 90],
            [0, 45, 45, 45, 45, 90, 90, 90, 90],
            [0, 45, 45, 60, 60, 60, 60, 90, 90],
            [0, 45, 45, 60, 60, 60, 60, 90, 90],
            [0, 45, 45, 60, 60, 60, 60, 90, 90],
            [0, 45, 45, 60, 60, 60, 60, 90, 90],
            [0, 45, 45, 60, 60, 60, 60, 90, 90],
            [0, 45, 45, 60, 60, 60, 60, 90, 90],
        ]
    )

    conventional_axis = np.array([0, 45, 45, 45, 45, 90, 90, 90, 90])

    axes = np.array([i[0] for i in axes])

    if 9 <= angles.shape[0]:
        sub_angles = angles[:9, :9]
        sub_axes = axes[:9]
        if (
            np.abs(np.sort(sub_angles.flatten()) - np.sort(target_angles.flatten()))
            < angle_tolerance
        ).all():
            xyz = []
            for i in range(9):
                if (
                    np.abs(np.sort(sub_angles[i]) - conventional_axis) < angle_tolerance
                ).all():
                    xyz.append(sub_axes[i])
            det = np.abs(np.linalg.det(xyz))
            if det == 1:
                result = "CUB"
            elif det == 4:
                result = "FCC"
            elif det == 2:
                result = "BCC"
            return result, False
        return None, True
    return None, True


################################################################################
#                                  LePage HEX                                  #
################################################################################
def _check_hex(angles, angle_tolerance):
    target_angles = np.array(
        [
            [0, 90, 90, 90, 90, 90, 90],
            [0, 30, 30, 60, 60, 90, 90],
            [0, 30, 30, 60, 60, 90, 90],
            [0, 30, 30, 60, 60, 90, 90],
            [0, 30, 30, 60, 60, 90, 90],
            [0, 30, 30, 60, 60, 90, 90],
            [0, 30, 30, 60, 60, 90, 90],
        ]
    )
    if 7 <= angles.shape[0]:
        sub_angles = angles[:7, :7]
        if (
            np.abs(np.sort(sub_angles.flatten()) - np.sort(target_angles.flatten()))
            < angle_tolerance
        ).all():
            return "HEX", False
        return None, True
    return None, True


################################################################################
#                                  LePage TET                                  #
################################################################################
def _check_tet(angles, axes, angle_tolerance, cell):
    target_angles = np.array(
        [
            [0, 90, 90, 90, 90],
            [0, 45, 45, 90, 90],
            [0, 45, 45, 90, 90],
            [0, 45, 45, 90, 90],
            [0, 45, 45, 90, 90],
        ]
    )

    conventional_axis = np.array([0, 90, 90, 90, 90])

    axes = np.array([i[0] for i in axes])

    if 5 <= angles.shape[0]:
        sub_angles = angles[:5, :5]
        sub_axes = axes[:5]
        if (
            np.abs(np.sort(sub_angles.flatten()) - np.sort(target_angles.flatten()))
            < angle_tolerance
        ).all():
            xy = []
            for i in range(5):
                if (
                    np.abs(np.sort(sub_angles[i]) - conventional_axis) < angle_tolerance
                ).all():
                    z = sub_axes[i]
                else:
                    xy.append(sub_axes[i])
            xy.sort(key=lambda x: np.linalg.norm(x @ cell))

            xyz = [xy[0], xy[1], z]

            det = np.abs(np.linalg.det(xyz))
            if det == 1:
                result = "TET"
            elif det == 2:
                result = "BCT"
            return result, False
        return None, True
    return None, True


################################################################################
#                                  LePage RHL                                  #
################################################################################
def _check_rhl(angles, angle_tolerance):
    target_angles = np.array(
        [
            [0, 60, 60],
            [0, 60, 60],
            [0, 60, 60],
        ]
    )

    if 3 <= angles.shape[0]:
        sub_angles = angles[:3, :3]
        if (
            np.abs(np.sort(sub_angles.flatten()) - np.sort(target_angles.flatten()))
            < angle_tolerance
        ).all():
            return "RHL", False
        return None, True
    return None, True


################################################################################
#                                  LePage ORC                                  #
################################################################################
def _check_orc(angles, axes, angle_tolerance):
    target_angles = np.array(
        [
            [0, 90, 90],
            [0, 90, 90],
            [0, 90, 90],
        ]
    )

    axes = np.array([i[0] for i in axes])
    if 3 <= angles.shape[0]:
        sub_angles = angles[:3, :3]
        sub_axes = axes[:3]
        if (
            np.abs(np.sort(sub_angles.flatten()) - np.sort(target_angles.flatten()))
            < angle_tolerance
        ).all():
            C = np.array(sub_axes, dtype=float).T
            det = np.abs(np.linalg.det(C))
            if det == 1:
                result = "ORC"
            if det == 4:
                result = "ORCF"
            if det == 2:
                v = C @ [1, 1, 1]

                def gcd(p, q):
                    while q != 0:
                        p, q = q, p % q
                    return p

                if (
                    gcd(abs(v[0]), abs(v[1])) > 1
                    and gcd(abs(v[0]), abs(v[2])) > 1
                    and gcd(abs(v[1]), abs(v[2])) > 1
                ):
                    result = "ORCI"
                else:
                    result = "ORCC"
            return result, False
        return None, True
    return None, True


################################################################################
#                                  LePage MCL                                  #
################################################################################
def _get_perpendicular_shortest(v, cell, angle_tolerance):
    perp_axes = []

    miller_indices = (np.indices((3, 3, 3)) - 1).transpose((1, 2, 3, 0)).reshape(27, 3)

    for index in miller_indices:
        if (index != [0, 0, 0]).any():
            if abs((index @ cell) @ (v @ cell)) < angle_tolerance:
                perp_axes.append(index)

    perp_axes.sort(key=lambda x: np.linalg.norm(x @ cell))

    # indices 0 and 2 (not 0 and 1), since v and -v are present in miller_indices
    return perp_axes[0], perp_axes[2]


def _check_mcl(angles, axes, angle_tolerance, cell):
    axes = np.array([i[0] for i in axes])
    angles = angles[:1]
    if 1 <= angles.shape[0]:
        b = axes[0]

        # If we are here by mistake it can fail
        try:
            a, c = _get_perpendicular_shortest(b, cell, angle_tolerance)
        except IndexError:
            return None, True
        C = np.array([a, b, c], dtype=float).T
        det = np.abs(np.linalg.det(C))
        if det == 1:
            return "MCL", False
        if det == 2:
            return "MCLC", False
        return None, True
    return None, True


################################################################################
#                                    LePage                                    #
################################################################################
def lepage(
    cell, angle_tolerance=1e-4, give_all_results=False, no_niggli=False, _limit=2.0
):
    r"""
    Detect Bravais lattice type with the Le Page algorithm [1]_.

    .. warning:: This function is left in the package as a legacy function.
        It is not used in any of the internal routines, it is not used to identify the
        Bravais lattice type. Use with caution. There is no guarantee of the correct
        behavior for this function.


    Parameters
    ----------
    cell : (3, 3) |array-like|_
        Matrix of a cell, rows are interpreted as vectors.
    angle_tolerance : float, default 1e-4
        Angle tolerance for the search of the actual symmetry axes. It is recommended to
        reduce ``angle_tolerance`` to account for the finite precision of the angles of
        the ``cell``. Default value is chosen in the contexts of condense matter physics,
        assuming that angles are in degrees. Please choose appropriate tolerance for your
        problem.
    give_all_results : bool, default False
        Whether to return the list of Bravais lattice types identified during the
        process of exclusion of the pseudosymmetry axes. Last element is the computed
        Bravais lattice type.
    no_niggli : bool, default False
        Whether to skip niggli reduction.
    _limit : float, default 2.0
        Tolerance parameter for the construction of the list of potential symmetry axes.
        Given in degrees. Change with caution and only if you understand what this
        parameter means and read [1]_.

    Returns
    -------
    lattice_type : str
        Bravais lattice type.
    intermediate_types : list of str
        Returned if ``give_all_results`` is ``True``.

    References
    ----------
    .. [1] Le Page, Y., 1982.
        The derivation of the axes of the conventional unit cell from
        the dimensions of the Buerger-reduced cell.
        Journal of Applied Crystallography, 15(3), pp.255-259.

    Examples
    --------

    .. doctest::

        >>> import wulfric as wulf
        >>> wulf.lepage([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        'CUB'
        >>> wulf.lepage([[1, 0, 0], [0, 1, 0], [0, 0, 2]])
        'TET'
        >>> wulf.lepage([[1, 0, 0], [0, 2, 0], [0, 0, 3]])
        'ORC'
    """

    # Safeguard to avoid infinite loops
    angle_tolerance = abs(angle_tolerance)

    if not no_niggli:
        # Niggli reduction
        try:
            cell = get_niggli(cell=cell)
        except NiggliReductionFailed:
            import warnings

            warnings.warn(
                "LePage algorithm: Niggli reduction failed, using input cell",
                RuntimeWarning,
            )

    rcell = get_reciprocal(cell)

    # Find all potential axes, including twins
    miller_indices = (np.indices((5, 5, 5)) - 2).transpose((1, 2, 3, 0)).reshape(125, 3)
    axes = []
    for U in miller_indices:
        for h in miller_indices:
            if abs(U @ h) == 2:
                t = U @ cell
                tau = h @ rcell
                delta = (
                    np.arctan(np.linalg.norm(np.cross(t, tau)) / abs(t @ tau))
                    * TODEGREES
                )
                if delta < _limit:
                    axes.append([U, t / np.linalg.norm(t), abs(U @ h), delta])

    # Sort and filter
    axes.sort(key=lambda x: x[-1])
    keep_index = np.ones(len(axes))
    for i in range(len(axes)):
        if keep_index[i]:
            for j in range(i + 1, len(axes)):
                if (
                    (axes[i][0] == axes[j][0]).all()
                    or (axes[i][0] == -axes[j][0]).all()
                    or (axes[i][0] == 2 * axes[j][0]).all()
                    or (axes[i][0] == 0.5 * axes[j][0]).all()
                ):
                    keep_index[i] = 0
                    break
    new_axes = []
    for i in range(len(axes)):
        if keep_index[i]:
            if set(axes[i][0]) == {0, 2}:
                axes[i][0] = axes[i][0] / 2
            new_axes.append(axes[i])
    axes = new_axes

    # Compute matrix of pair-wise angles
    n = len(axes)
    angles = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(i, n):
            angles[i][j] = (
                acos(abs(np.clip(np.array(axes[i][1]) @ np.array(axes[j][1]), -1, 1)))
                * TODEGREES
            )
    angles += angles.T

    # Main cycle
    delta = None

    if give_all_results:
        results = []

    while delta is None or delta > angle_tolerance:
        if len(axes) == 0:
            delta = 0
        else:
            delta = max(axes, key=lambda x: x[-1])[-1]

        continue_search = True
        n = len(axes)
        result = None

        # CUB
        result, continue_search = _check_cub(angles, axes, angle_tolerance)

        # HEX
        if continue_search:
            result, continue_search = _check_hex(angles, angle_tolerance)

        # TET
        if continue_search:
            result, continue_search = _check_tet(angles, axes, angle_tolerance, cell)

        # RHL
        if continue_search:
            result, continue_search = _check_rhl(angles, angle_tolerance)

        # ORC
        if continue_search:
            result, continue_search = _check_orc(angles, axes, angle_tolerance)

        # MCL
        if continue_search:
            result, continue_search = _check_mcl(angles, axes, angle_tolerance, cell)

        # TRI
        if continue_search:
            result = "TRI"

        if len(axes) > 0:
            # remove worst axes
            while len(axes) >= 2 and axes[-1][-1] == axes[-2][-1]:
                axes = axes[:-1]
                angles = angles[:-1, :-1]
            axes = axes[:-1]
            angles = angles[:-1, :-1]

        if give_all_results:
            results.append(result)

    if give_all_results:
        return results

    return result


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
