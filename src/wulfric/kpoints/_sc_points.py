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


def _get_points_table_6(conv_a, conv_c):
    eta = (1 + conv_c**2 / conv_a**2) / 4
    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "M": np.array([-1 / 2, 1 / 2, 1 / 2]),
        "N": np.array([0, 1 / 2, 0]),
        "P": np.array([1 / 4, 1 / 4, 1 / 4]),
        "X": np.array([0, 0, 1 / 2]),
        "Z": np.array([eta, eta, -eta]),
        "Z1": np.array([-eta, 1 - eta, eta]),
    }


def _get_points_table_7(conv_a, conv_c):
    eta = (1 + conv_a**2 / conv_c**2) / 4
    zeta = conv_a**2 / (2 * conv_c**2)
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


def _get_points_table_9(conv_a, conv_b, conv_c):
    eta = (1 + conv_a**2 / conv_b**2 + conv_a**2 / conv_c**2) / 4
    zeta = (1 + conv_a**2 / conv_b**2 - conv_a**2 / conv_c**2) / 4

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


def _get_points_table_10(conv_a, conv_b, conv_c):
    eta = (1 + conv_a**2 / conv_b**2 - conv_a**2 / conv_c**2) / 4
    delta = (1 + conv_b**2 / conv_a**2 - conv_b**2 / conv_c**2) / 4
    phi = (1 + conv_c**2 / conv_b**2 - conv_c**2 / conv_a**2) / 4

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


def _get_points_table_11(conv_a, conv_b, conv_c):
    zeta = (1 + conv_a**2 / conv_c**2) / 4
    eta = (1 + conv_b**2 / conv_c**2) / 4
    delta = (conv_b**2 - conv_a**2) / (4 * conv_c**2)
    mu = (conv_a**2 + conv_b**2) / (4 * conv_c**2)

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


def _get_points_table_12(conv_a, conv_b):
    zeta = (1 + conv_a**2 / conv_b**2) / 4

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


def _get_points_table_14(conv_alpha):
    conv_alpha *= TORADIANS

    eta = (1 + 4 * cos(conv_alpha)) / (2 + 4 * cos(conv_alpha))
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


def _get_points_table_15(conv_alpha):
    conv_alpha *= TORADIANS

    eta = 1 / (2 * tan(conv_alpha / 2) ** 2)
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


def _get_points_table_16(conv_b, conv_c, conv_alpha):
    conv_alpha *= TORADIANS

    eta = (1 - conv_b * cos(conv_alpha) / conv_c) / (2 * sin(conv_alpha) ** 2)
    nu = 1 / 2 - eta * conv_c * cos(conv_alpha) / conv_b

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


def _get_points_table_17(conv_a, conv_b, conv_c, conv_alpha):
    conv_alpha *= TORADIANS

    zeta = (2 - conv_b * cos(conv_alpha) / conv_c) / (4 * sin(conv_alpha) ** 2)
    eta = 1 / 2 + 2 * zeta * conv_c * cos(conv_alpha) / conv_b
    psi = 3 / 4 - conv_a**2 / (4 * conv_b**2 * sin(conv_alpha) ** 2)
    phi = psi + (3 / 4 - psi) * conv_b * cos(conv_alpha) / conv_c

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


def _get_points_table_18(conv_a, conv_b, conv_c, conv_alpha):
    conv_alpha *= TORADIANS

    mu = (1 + conv_b**2 / conv_a**2) / 4
    delta = conv_b * conv_c * cos(conv_alpha) / (2 * conv_a**2)
    zeta = (
        mu
        - 1 / 4
        + (1 - conv_b * cos(conv_alpha) / conv_c) / (4 * sin(conv_alpha) ** 2)
    )
    eta = 1 / 2 + 2 * zeta * conv_c * cos(conv_alpha) / conv_b
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


def _get_points_table_19(conv_a, conv_b, conv_c, conv_alpha):
    conv_alpha *= TORADIANS

    zeta = (
        conv_b**2 / conv_a**2
        + (1 - conv_b * cos(conv_alpha) / conv_c) / sin(conv_alpha) ** 2
    ) / 4
    eta = 1 / 2 + 2 * zeta * conv_c * cos(conv_alpha) / conv_b
    mu = (
        eta / 2
        + conv_b**2 / (4 * conv_a**2)
        - conv_b * conv_c * cos(conv_alpha) / (2 * conv_a**2)
    )
    nu = 2 * mu - zeta
    rho = 1 - zeta * conv_a**2 / conv_b**2
    omega = (
        (4 * nu - 1 - conv_b**2 * sin(conv_alpha) ** 2 / conv_a**2)
        * conv_c
        / (2 * conv_b * cos(conv_alpha))
    )
    delta = zeta * conv_c * cos(conv_alpha) / conv_b + omega / 2 - 1 / 4

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


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
