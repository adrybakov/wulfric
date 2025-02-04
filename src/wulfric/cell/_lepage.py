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


from math import acos, floor, log10

import numpy as np

from wulfric._decorate_array import print_2d_array
from wulfric._exceptions import NiggliReductionFailed
from wulfric.cell._basic_manipulation import from_params, get_reciprocal
from wulfric.constants._numerical import TODEGREES
from wulfric.geometry._geometry import get_volume, parallelepiped_check

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


################################################################################
#                                  LePage CUB                                  #
################################################################################
def _check_cub(angles: np.ndarray, axes: np.ndarray, eps_angle):
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
            < eps_angle
        ).all():
            xyz = []
            for i in range(9):
                if (
                    np.abs(np.sort(sub_angles[i]) - conventional_axis) < eps_angle
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
def _check_hex(angles: np.ndarray, eps_angle):
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
            < eps_angle
        ).all():
            return "HEX", False
        return None, True
    return None, True


################################################################################
#                                  LePage TET                                  #
################################################################################
def _check_tet(angles: np.ndarray, axes: np.ndarray, eps_angle, cell):
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
            < eps_angle
        ).all():
            xy = []
            for i in range(5):
                if (
                    np.abs(np.sort(sub_angles[i]) - conventional_axis) < eps_angle
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
def _check_rhl(angles: np.ndarray, eps_angle):
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
            < eps_angle
        ).all():
            return "RHL", False
        return None, True
    return None, True


################################################################################
#                                  LePage ORC                                  #
################################################################################
def _check_orc(angles: np.ndarray, axes: np.ndarray, eps_angle):
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
            < eps_angle
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
def _get_perpendicular_shortest(v, cell, eps):
    perp_axes = []

    miller_indices = (np.indices((3, 3, 3)) - 1).transpose((1, 2, 3, 0)).reshape(27, 3)

    for index in miller_indices:
        if (index != [0, 0, 0]).any():
            if abs((index @ cell) @ (v @ cell)) < eps:
                perp_axes.append(index)

    perp_axes.sort(key=lambda x: np.linalg.norm(x @ cell))

    # indices 0 and 2 (not 0 and 1), since v and -v are present in miller_indices
    return perp_axes[0], perp_axes[2]


def _check_mcl(angles: np.ndarray, axes: np.ndarray, eps, cell):
    axes = np.array([i[0] for i in axes])
    angles = angles[:1]
    if 1 <= angles.shape[0]:
        b = axes[0]

        # If we are here by mistake it can fail
        try:
            a, c = _get_perpendicular_shortest(b, cell, eps)
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
    a=1,
    b=1,
    c=1,
    alpha=90,
    beta=90,
    gamma=90,
    eps_relative=1e-4,
    verbose=False,
    very_verbose=False,
    give_all_results=False,
    eps_angle=1e-14,
):
    r"""
    Le Page algorithm [1]_.

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
    eps_relative : float, default TODO
        Relative epsilon.
    verbose : bool, default False
        Whether to print the steps of an algorithm.
    very_verbose : bool, default False
        Whether to print the detailed steps of an algorithm.
    give_all_results : bool, default False
        Whether to give the whole list of consecutive results.
    eps_angle : float, default TODO
        Maximum angle tolerance, in degrees.

    Returns
    -------
    result : str
        Bravais lattice type. If give_all_results == True, then return list of all
        consecutive results.

    References
    ----------
    .. [1] Le Page, Y., 1982.
        The derivation of the axes of the conventional unit cell from
        the dimensions of the Buerger-reduced cell.
        Journal of Applied Crystallography, 15(3), pp.255-259.
    """

    if very_verbose:
        verbose = True

    # Check if provided parameters can form a parallelepiped
    parallelepiped_check(a, b, c, alpha, beta, gamma, raise_error=True)

    eps_volume = eps_relative * get_volume(a, b, c, alpha, beta, gamma) ** (1 / 3.0)

    # Limit value for the condition on keeping the axis
    limit = max(1.5, eps_angle * 1.1)

    decimals = abs(floor(log10(abs(eps_volume))))

    # Niggli reduction
    try:
        a, b, c, alpha, beta, gamma = niggli(
            a=a,
            b=b,
            c=c,
            alpha=alpha,
            beta=beta,
            gamma=gamma,
            eps_relative=eps_relative,
            return_cell=True,
        )
    except NiggliReductionFailed:
        import warnings

        warnings.warn(
            "LePage algorithm: Niggli reduction failed, using input parameters",
            RuntimeWarning,
        )

    cell = from_params(a, b, c, alpha, beta, gamma)
    rcell = get_reciprocal(cell)
    if very_verbose:
        print("Cell:")
        print_2d_array(cell, fmt=f"{4+decimals}.{1+decimals}f")
        print("Reciprocal cell:")
        print_2d_array(rcell, fmt=f"{4+decimals}.{1+decimals}f")

    # Find all axes with twins
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
                if delta < limit:
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

    if very_verbose:
        print(f"Axes with delta < {limit}:")
        print(f"       U     {'delta':>{4+decimals}}")
        for ax in axes:
            print(
                f"  ({ax[0][0]:2.0f} "
                + f"{ax[0][1]:2.0f} "
                + f"{ax[0][2]:2.0f}) "
                + f"{ax[-1]:{4+decimals}.{1+decimals}f}"
            )

    # Compute angles matrix
    n = len(axes)
    angles = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(i, n):
            angles[i][j] = (
                acos(abs(np.clip(np.array(axes[i][1]) @ np.array(axes[j][1]), -1, 1)))
                * TODEGREES
            )
    angles += angles.T

    # Main check cycle
    delta = None
    separator = lambda x: "=" * 20 + f" Cycle {x} " + "=" * 20
    cycle = 0
    if give_all_results:
        results = []
    while delta is None or delta > eps_angle:
        if verbose:
            cycle += 1
            print(separator(cycle))

        try:
            delta = max(axes, key=lambda x: x[-1])[-1]
        except ValueError:
            delta = 0
        eps = max(eps_volume, delta)
        decimals = abs(floor(log10(abs(eps))))
        if very_verbose:
            decimals = abs(floor(log10(abs(eps))))
            print(
                f"Epsilon = {eps:{4+decimals}.{1+decimals}f}\n"
                + f"delta   = {delta:{4+decimals}.{1+decimals}f}"
            )
            print("Axes:")
            print(f"       U     {'delta':>{4+decimals}}")
            for ax in axes:
                print(
                    f"  ({ax[0][0]:2.0f} "
                    + f"{ax[0][1]:2.0f} "
                    + f"{ax[0][2]:2.0f}) "
                    + f"{ax[-1]:{4+decimals}.{1+decimals}f}"
                )
            print("Angles:")
            print_2d_array(angles, fmt=f"{4+decimals}.{1+decimals}f")

        continue_search = True
        n = len(axes)
        result = None

        # CUB
        result, continue_search = _check_cub(angles, axes, eps)

        # HEX
        if continue_search:
            result, continue_search = _check_hex(angles, eps)

        # TET
        if continue_search:
            result, continue_search = _check_tet(angles, axes, eps, cell)

        # RHL
        if continue_search:
            result, continue_search = _check_rhl(angles, eps)

        # ORC
        if continue_search:
            result, continue_search = _check_orc(angles, axes, eps)

        # MCL
        if continue_search:
            result, continue_search = _check_mcl(angles, axes, eps, cell)

        # TRI
        if continue_search:
            result = "TRI"

        if verbose:
            print(
                f"System {result} with the worst delta = {delta:{4+decimals}.{1+decimals}f}"
            )

        if len(axes) > 0:
            # remove worst axes
            while len(axes) >= 2 and axes[-1][-1] == axes[-2][-1]:
                axes = axes[:-1]
                angles = np.delete(angles, -1, -1)[:-1]
            axes = axes[:-1]
            angles = np.delete(angles, -1, -1)[:-1]

        if give_all_results:
            results.append((result, delta))

    if give_all_results:
        return results

    return result


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
