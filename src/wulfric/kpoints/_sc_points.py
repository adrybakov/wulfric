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


from math import cos, sin, tan

import numpy as np

from wulfric.constants._numerical import TORADIANS
from wulfric.constants._sc_convention import SC_BRAVAIS_LATTICE_SHORT_NAMES
from wulfric._exceptions import PotentialBugError
from wulfric.cell import get_params

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def _get_points_table_2():
    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "M": np.array([1 / 2, 1 / 2, 0]),
        "R": np.array([1 / 2, 1 / 2, 1 / 2]),
        "X": np.array([0, 1 / 2, 0]),
    }


def _get_points_table_3():
    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "K": np.array([3 / 8, 3 / 8, 3 / 4]),
        "L": np.array([1 / 2, 1 / 2, 1 / 2]),
        "U": np.array([5 / 8, 1 / 4, 5 / 8]),
        "W": np.array([1 / 2, 1 / 4, 3 / 4]),
        "X": np.array([1 / 2, 0, 1 / 2]),
    }


def _get_points_table_4():
    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "H": np.array([1 / 2, -1 / 2, 1 / 2]),
        "P": np.array([1 / 4, 1 / 4, 1 / 4]),
        "N": np.array([0, 0, 1 / 2]),
    }


def _get_points_table_5():
    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "A": np.array([1 / 2, 1 / 2, 1 / 2]),
        "M": np.array([1 / 2, 1 / 2, 0]),
        "R": np.array([0, 1 / 2, 1 / 2]),
        "X": np.array([0, 1 / 2, 0]),
        "Z": np.array([0, 0, 1 / 2]),
    }


def _get_points_table_6(a, c):
    eta = (1 + c**2 / a**2) / 4
    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "M": np.array([-1 / 2, 1 / 2, 1 / 2]),
        "N": np.array([0, 1 / 2, 0]),
        "P": np.array([1 / 4, 1 / 4, 1 / 4]),
        "X": np.array([0, 0, 1 / 2]),
        "Z": np.array([eta, eta, -eta]),
        "Z1": np.array([-eta, 1 - eta, eta]),
    }


def _get_points_table_7(a, c):
    eta = (1 + a**2 / c**2) / 4
    zeta = a**2 / (2 * c**2)
    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "N": np.array([0, 1 / 2, 0]),
        "P": np.array([1 / 4, 1 / 4, 1 / 4]),
        "SIGMA": np.array([-eta, eta, eta]),
        "SIGMA1": np.array([eta, 1 - eta, -eta]),
        "X": np.array([0, 0, 1 / 2]),
        "Y": np.array([-zeta, zeta, 1 / 2]),
        "Y1": np.array([1 / 2, 1 / 2, -zeta]),
        "Z": np.array([1 / 2, 1 / 2, -1 / 2]),
    }


def _get_points_table_8():
    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "R": np.array([1 / 2, 1 / 2, 1 / 2]),
        "S": np.array([1 / 2, 1 / 2, 0]),
        "T": np.array([0, 1 / 2, 1 / 2]),
        "U": np.array([1 / 2, 0, 1 / 2]),
        "X": np.array([1 / 2, 0, 0]),
        "Y": np.array([0, 1 / 2, 0]),
        "Z": np.array([0, 0, 1 / 2]),
    }


def _get_points_table_9(a, b, c):
    eta = (1 + a**2 / b**2 + a**2 / c**2) / 4
    zeta = (1 + a**2 / b**2 - a**2 / c**2) / 4

    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "A": np.array([1 / 2, 1 / 2 + zeta, zeta]),
        "A1": np.array([1 / 2, 1 / 2 - zeta, 1 - zeta]),
        "L": np.array([1 / 2, 1 / 2, 1 / 2]),
        "T": np.array([1, 1 / 2, 1 / 2]),
        "X": np.array([0, eta, eta]),
        "X1": np.array([1, 1 - eta, 1 - eta]),
        "Y": np.array([1 / 2, 0, 1 / 2]),
        "Z": np.array([1 / 2, 1 / 2, 0]),
    }


def _get_points_table_10(a, b, c):
    eta = (1 + a**2 / b**2 - a**2 / c**2) / 4
    delta = (1 + b**2 / a**2 - b**2 / c**2) / 4
    phi = (1 + c**2 / b**2 - c**2 / a**2) / 4

    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "C": np.array([1 / 2, 1 / 2 - eta, 1 - eta]),
        "C1": np.array([1 / 2, 1 / 2 + eta, eta]),
        "D": np.array([1 / 2 - delta, 1 / 2, 1 - delta]),
        "D1": np.array([1 / 2 + delta, 1 / 2, delta]),
        "L": np.array([1 / 2, 1 / 2, 1 / 2]),
        "H": np.array([1 - phi, 1 / 2 - phi, 1 / 2]),
        "H1": np.array([phi, 1 / 2 + phi, 1 / 2]),
        "X": np.array([0, 1 / 2, 1 / 2]),
        "Y": np.array([1 / 2, 0, 1 / 2]),
        "Z": np.array([1 / 2, 1 / 2, 0]),
    }


def _get_points_table_11(a, b, c):
    zeta = (1 + a**2 / c**2) / 4
    eta = (1 + b**2 / c**2) / 4
    delta = (b**2 - a**2) / (4 * c**2)
    mu = (a**2 + b**2) / (4 * c**2)

    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "L": np.array([-mu, mu, 1 / 2 - delta]),
        "L1": np.array([mu, -mu, 1 / 2 + delta]),
        "L2": np.array([1 / 2 - delta, 1 / 2 + delta, -mu]),
        "R": np.array([0, 1 / 2, 0]),
        "S": np.array([1 / 2, 0, 0]),
        "T": np.array([0, 0, 1 / 2]),
        "W": np.array([1 / 4, 1 / 4, 1 / 4]),
        "X": np.array([-zeta, zeta, zeta]),
        "X1": np.array([zeta, 1 - zeta, -zeta]),
        "Y": np.array([eta, -eta, eta]),
        "Y1": np.array([1 - eta, eta, -eta]),
        "Z": np.array([1 / 2, 1 / 2, -1 / 2]),
    }


def _get_points_table_12(a, b):
    zeta = (1 + a**2 / b**2) / 4

    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "A": np.array([zeta, zeta, 1 / 2]),
        "A1": np.array([-zeta, 1 - zeta, 1 / 2]),
        "R": np.array([0, 1 / 2, 1 / 2]),
        "S": np.array([0, 1 / 2, 0]),
        "T": np.array([-1 / 2, 1 / 2, 1 / 2]),
        "X": np.array([zeta, zeta, 0]),
        "X1": np.array([-zeta, 1 - zeta, 0]),
        "Y": np.array([-1 / 2, 1 / 2, 0]),
        "Z": np.array([0, 0, 1 / 2]),
    }


def _get_points_table_13():
    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "A": np.array([0, 0, 1 / 2]),
        "H": np.array([1 / 3, 1 / 3, 1 / 2]),
        "K": np.array([1 / 3, 1 / 3, 0]),
        "L": np.array([1 / 2, 0, 1 / 2]),
        "M": np.array([1 / 2, 0, 0]),
    }


def _get_points_table_14(alpha):
    alpha *= TORADIANS

    eta = (1 + 4 * cos(alpha)) / (2 + 4 * cos(alpha))
    nu = 3 / 4 - eta / 2

    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "B": np.array([eta, 1 / 2, 1 - eta]),
        "B1": np.array([1 / 2, 1 - eta, eta - 1]),
        "F": np.array([1 / 2, 1 / 2, 0]),
        "L": np.array([1 / 2, 0, 0]),
        "L1": np.array([0, 0, -1 / 2]),
        "P": np.array([eta, nu, nu]),
        "P1": np.array([1 - nu, 1 - nu, 1 - eta]),
        "P2": np.array([nu, nu, eta - 1]),
        "Q": np.array([1 - nu, nu, 0]),
        "X": np.array([nu, 0, -nu]),
        "Z": np.array([1 / 2, 1 / 2, 1 / 2]),
    }


def _get_points_table_15(alpha):
    alpha *= TORADIANS

    eta = 1 / (2 * tan(alpha / 2) ** 2)
    nu = 3 / 4 - eta / 2

    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "F": np.array([1 / 2, -1 / 2, 0]),
        "L": np.array([1 / 2, 0, 0]),
        "P": np.array([1 - nu, -nu, 1 - nu]),
        "P1": np.array([nu, nu - 1, nu - 1]),
        "Q": np.array([eta, eta, eta]),
        "Q1": np.array([1 - eta, -eta, -eta]),
        "Z": np.array([1 / 2, -1 / 2, 1 / 2]),
    }


def _get_points_table_16(b, c, alpha):
    alpha *= TORADIANS

    eta = (1 - b * cos(alpha) / c) / (2 * sin(alpha) ** 2)
    nu = 1 / 2 - eta * c * cos(alpha) / b

    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "A": np.array([1 / 2, 1 / 2, 0]),
        "C": np.array([0, 1 / 2, 1 / 2]),
        "D": np.array([1 / 2, 0, 1 / 2]),
        "D1": np.array([1 / 2, 0, -1 / 2]),
        "E": np.array([1 / 2, 1 / 2, 1 / 2]),
        "H": np.array([0, eta, 1 - nu]),
        "H1": np.array([0, 1 - eta, nu]),
        "H2": np.array([0, eta, -nu]),
        "M": np.array([1 / 2, eta, 1 - nu]),
        "M1": np.array([1 / 2, 1 - eta, nu]),
        "M2": np.array([1 / 2, eta, -nu]),
        "X": np.array([0, 1 / 2, 0]),
        "Y": np.array([0, 0, 1 / 2]),
        "Y1": np.array([0, 0, -1 / 2]),
        "Z": np.array([1 / 2, 0, 0]),
    }


def _get_points_table_17(a, b, c, alpha):
    alpha *= TORADIANS

    zeta = (2 - b * cos(alpha) / c) / (4 * sin(alpha) ** 2)
    eta = 1 / 2 + 2 * zeta * c * cos(alpha) / b
    psi = 3 / 4 - a**2 / (4 * b**2 * sin(alpha) ** 2)
    phi = psi + (3 / 4 - psi) * b * cos(alpha) / c

    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "N": np.array([1 / 2, 0, 0]),
        "N1": np.array([0, -1 / 2, 0]),
        "F": np.array([1 - zeta, 1 - zeta, 1 - eta]),
        "F1": np.array([zeta, zeta, eta]),
        "F2": np.array([-zeta, -zeta, 1 - eta]),
        "F3": np.array([1 - zeta, -zeta, 1 - eta]),
        "I": np.array([phi, 1 - phi, 1 / 2]),
        "I1": np.array([1 - phi, phi - 1, 1 / 2]),
        "L": np.array([1 / 2, 1 / 2, 1 / 2]),
        "M": np.array([1 / 2, 0, 1 / 2]),
        "X": np.array([1 - psi, psi - 1, 0]),
        "X1": np.array([psi, 1 - psi, 0]),
        "X2": np.array([psi - 1, -psi, 0]),
        "Y": np.array([1 / 2, 1 / 2, 0]),
        "Y1": np.array([-1 / 2, -1 / 2, 0]),
        "Z": np.array([0, 0, 1 / 2]),
    }


def _get_points_table_18(a, b, c, alpha):
    alpha *= TORADIANS

    mu = (1 + b**2 / a**2) / 4
    delta = b * c * cos(alpha) / (2 * a**2)
    zeta = mu - 1 / 4 + (1 - b * cos(alpha) / c) / (4 * sin(alpha) ** 2)
    eta = 1 / 2 + 2 * zeta * c * cos(alpha) / b
    phi = 1 + zeta - 2 * mu
    psi = eta - 2 * delta

    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "F": np.array([1 - phi, 1 - phi, 1 - psi]),
        "F1": np.array([phi, phi - 1, psi]),
        "F2": np.array([1 - phi, -phi, 1 - psi]),
        "H": np.array([zeta, zeta, eta]),
        "H1": np.array([1 - zeta, -zeta, 1 - eta]),
        "H2": np.array([-zeta, -zeta, 1 - eta]),
        "I": np.array([1 / 2, -1 / 2, 1 / 2]),
        "M": np.array([1 / 2, 0, 1 / 2]),
        "N": np.array([1 / 2, 0, 0]),
        "N1": np.array([0, -1 / 2, 0]),
        "X": np.array([1 / 2, -1 / 2, 0]),
        "Y": np.array([mu, mu, delta]),
        "Y1": np.array([1 - mu, -mu, -delta]),
        "Y2": np.array([-mu, -mu, -delta]),
        "Y3": np.array([mu, mu - 1, delta]),
        "Z": np.array([0, 0, 1 / 2]),
    }


def _get_points_table_19(a, b, c, alpha):
    alpha *= TORADIANS

    zeta = (b**2 / a**2 + (1 - b * cos(alpha) / c) / sin(alpha) ** 2) / 4
    eta = 1 / 2 + 2 * zeta * c * cos(alpha) / b
    mu = eta / 2 + b**2 / (4 * a**2) - b * c * cos(alpha) / (2 * a**2)
    nu = 2 * mu - zeta
    rho = 1 - zeta * a**2 / b**2
    omega = (4 * nu - 1 - b**2 * sin(alpha) ** 2 / a**2) * c / (2 * b * cos(alpha))
    delta = zeta * c * cos(alpha) / b + omega / 2 - 1 / 4

    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "F": np.array([nu, nu, omega]),
        "F1": np.array([1 - nu, 1 - nu, 1 - omega]),
        "F2": np.array([nu, nu - 1, omega]),
        "H": np.array([zeta, zeta, eta]),
        "H1": np.array([1 - zeta, -zeta, 1 - eta]),
        "H2": np.array([-zeta, -zeta, 1 - eta]),
        "I": np.array([rho, 1 - rho, 1 / 2]),
        "I1": np.array([1 - rho, rho - 1, 1 / 2]),
        "L": np.array([1 / 2, 1 / 2, 1 / 2]),
        "M": np.array([1 / 2, 0, 1 / 2]),
        "N": np.array([1 / 2, 0, 0]),
        "N1": np.array([0, -1 / 2, 0]),
        "X": np.array([1 / 2, -1 / 2, 0]),
        "Y": np.array([mu, mu, delta]),
        "Y1": np.array([1 - mu, -mu, -delta]),
        "Y2": np.array([-mu, -mu, -delta]),
        "Y3": np.array([mu, mu - 1, delta]),
        "Z": np.array([0, 0, 1 / 2]),
    }


def _get_points_table_20():
    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "L": np.array([1 / 2, 1 / 2, 0]),
        "M": np.array([0, 1 / 2, 1 / 2]),
        "N": np.array([1 / 2, 0, 1 / 2]),
        "R": np.array([1 / 2, 1 / 2, 1 / 2]),
        "X": np.array([1 / 2, 0, 0]),
        "Y": np.array([0, 1 / 2, 0]),
        "Z": np.array([0, 0, 1 / 2]),
    }


def _get_points_table_21():
    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "L": np.array([1 / 2, -1 / 2, 0]),
        "M": np.array([0, 0, 1 / 2]),
        "N": np.array([-1 / 2, -1 / 2, 1 / 2]),
        "R": np.array([0, -1 / 2, 1 / 2]),
        "X": np.array([0, -1 / 2, 0]),
        "Y": np.array([1 / 2, 0, 0]),
        "Z": np.array([-1 / 2, 0, 1 / 2]),
    }


def _sc_get_points(conventional_cell, lattice_type, lattice_variation):
    a, b, c, alpha, _, _ = get_params(cell=conventional_cell)

    if lattice_type not in SC_BRAVAIS_LATTICE_SHORT_NAMES:
        raise PotentialBugError(
            error_summary=f'(convention="SC"). Unexpected lattice type, got "{lattice_type}".'
        )

    lattice_type = SC_BRAVAIS_LATTICE_SHORT_NAMES[lattice_type]

    if lattice_type == "CUB":
        return _get_points_table_2()

    if lattice_type == "FCC":
        return _get_points_table_3()

    if lattice_type == "BCC":
        return _get_points_table_4()

    if lattice_type == "TET":
        return _get_points_table_5()

    if lattice_type == "BCT":
        if lattice_variation == "BCT1":
            return _get_points_table_6(a=a, c=c)
        elif lattice_variation == "BCT2":
            return _get_points_table_7(a=a, c=c)
        else:
            raise PotentialBugError(
                error_summary=f'(convention="SC"), lattice type "BCT". Unexpected lattice variation, got "{lattice_variation}".'
            )

    if lattice_type == "ORC":
        return _get_points_table_8()

    if lattice_type == "ORCF":
        if lattice_variation in ["ORCF1", "ORCF3"]:
            return _get_points_table_9(a=a, b=b, c=c)
        elif lattice_variation == "ORCF2":
            return _get_points_table_10(a=a, b=b, c=c)
        else:
            raise PotentialBugError(
                error_summary=f'(convention="SC"), lattice type "ORCF". Unexpected lattice variation, got "{lattice_variation}".'
            )

    if lattice_type == "ORCI":
        return _get_points_table_11(a=a, b=b, c=c)

    if lattice_type == "ORCC":
        return _get_points_table_12(a=a, b=b)

    if lattice_type == "HEX":
        return _get_points_table_13()

    if lattice_type == "RHL":
        if lattice_variation == "RHL1":
            return _get_points_table_14(alpha=alpha)
        elif lattice_variation == "RHL2":
            return _get_points_table_15(alpha=alpha)
        else:
            raise PotentialBugError(
                error_summary=f'(convention="SC"), lattice type "RHL". Unexpected lattice variation, got "{lattice_variation}".'
            )

    if lattice_type == "MCL":
        return _get_points_table_16(b=b, c=c, alpha=alpha)

    if lattice_type == "MCLC":
        if lattice_variation in ["MCLC1", "MCLC2"]:
            return _get_points_table_17(a=a, b=b, c=c, alpha=alpha)
        elif lattice_variation in ["MCLC3", "MCLC4"]:
            return _get_points_table_18(a=a, b=b, c=c, alpha=alpha)
        elif lattice_variation == "MCLC5":
            return _get_points_table_19(a=a, b=b, c=c, alpha=alpha)
        else:
            raise PotentialBugError(
                error_summary=f'(convention="SC"), lattice type "MCLC". Unexpected lattice variation, got "{lattice_variation}".'
            )

    if lattice_type == "TRI":
        if lattice_variation in ["TRI1a", "TRI2a"]:
            return _get_points_table_20()
        elif lattice_variation in ["TRI1b", "TRI2b"]:
            return _get_points_table_21()
        else:
            raise PotentialBugError(
                error_summary=f'(convention="SC"), lattice type "TRI". Unexpected lattice variation, got "{lattice_variation}".'
            )

    raise PotentialBugError(
        error_summary=f'(convention="SC"). Unexpected lattice type, got "{lattice_type}".'
    )


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
