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

from wulfric.cell._basic_manipulation import get_params
from wulfric.constants._numerical import TORADIANS
from wulfric._exceptions import PotentialBugError

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def _get_points_table_69():
    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "R": np.array([1 / 2, 1 / 2, 1 / 2]),
        "M": np.array([1 / 2, 1 / 2, 0.0]),
        "X": np.array([0.0, 1 / 2, 0.0]),
        "X1": np.array([1 / 2, 0.0, 0.0]),
    }


def _get_points_table_70():
    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "X": np.array([1 / 2, 0.0, 1 / 2]),
        "L": np.array([1 / 2, 1 / 2, 1 / 2]),
        "W": np.array([1 / 2, 1 / 4, 3 / 4]),
        "W2": np.array([3 / 4, 1 / 4, 1 / 2]),
        "K": np.array([3 / 8, 3 / 8, 3 / 4]),
        "U": np.array([5 / 8, 1 / 4, 5 / 8]),
    }


def _get_points_table_71():
    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "H": np.array([1 / 2, -1 / 2, 1 / 2]),
        "P": np.array([1 / 4, 1 / 4, 1 / 4]),
        "N": np.array([0.0, 0.0, 1 / 2]),
    }


def _get_points_table_72():
    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "Z": np.array([0.0, 0.0, 1 / 2]),
        "M": np.array([1 / 2, 1 / 2, 0.0]),
        "A": np.array([1 / 2, 1 / 2, 1 / 2]),
        "R": np.array([0.0, 1 / 2, 1 / 2]),
        "X": np.array([0.0, 1 / 2, 0.0]),
    }


def _get_points_table_73(a, c):
    eta = (1 + (c / a) ** 2) / 4
    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "M": np.array([-1 / 2, 1 / 2, 1 / 2]),
        "X": np.array([0.0, 0.0, 1 / 2]),
        "P": np.array([1 / 4, 1 / 4, 1 / 4]),
        "Z": np.array([eta, eta, -eta]),
        "Z0": np.array([-eta, 1 - eta, eta]),
        "N": np.array([0.0, 1 / 2, 0.0]),
    }


def _get_points_table_74(a, c):
    eta = (1 + (a / c) ** 2) / 4
    zeta = ((a / c) ** 2) / 2
    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "M": np.array([1 / 2, 1 / 2, -1 / 2]),
        "X": np.array([0.0, 0.0, 1 / 2]),
        "P": np.array([1 / 4, 1 / 4, 1 / 4]),
        "N": np.array([0.0, 1 / 2, 0.0]),
        "S0": np.array([-eta, eta, eta]),
        "S": np.array([eta, 1 - eta, -eta]),
        "R": np.array([-zeta, zeta, 1 / 2]),
        "G": np.array([1 / 2, 1 / 2, -zeta]),
    }


def _get_points_table_75():
    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "X": np.array([1 / 2, 0.0, 0.0]),
        "Z": np.array([0.0, 0.0, 1 / 2]),
        "U": np.array([1 / 2, 0.0, 1 / 2]),
        "Y": np.array([0.0, 1 / 2, 0.0]),
        "S": np.array([1 / 2, 1 / 2, 0.0]),
        "T": np.array([0.0, 1 / 2, 1 / 2]),
        "R": np.array([1 / 2, 1 / 2, 1 / 2]),
    }


def _get_points_table_76(a, b, c):
    zeta = (1 + (a / b) ** 2 - (a / c) ** 2) / 4
    eta = (1 + (a / b) ** 2 + (a / c) ** 2) / 4
    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "T": np.array([1.0, 1 / 2, 1 / 2]),
        "Z": np.array([1 / 2, 1 / 2, 0.0]),
        "Y": np.array([1 / 2, 0.0, 1 / 2]),
        "SIGMA0": np.array([0.0, eta, eta]),
        "U0": np.array([1.0, 1 - eta, 1 - eta]),
        "A0": np.array([1 / 2, 1 / 2 + zeta, zeta]),
        "C0": np.array([1 / 2, 1 / 2 - zeta, 1 - zeta]),
        "L": np.array([1 / 2, 1 / 2, 1 / 2]),
    }


def _get_points_table_77(a, b, c):
    zeta = (1 + (c / a) ** 2 - (c / b) ** 2) / 4
    eta = (1 + (c / a) ** 2 + (c / b) ** 2) / 4
    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "T": np.array([0.0, 1 / 2, 1 / 2]),
        "Z": np.array([1 / 2, 1 / 2, 1.0]),
        "Y": np.array([1 / 2, 0.0, 1 / 2]),
        "LAMBDA0": np.array([eta, eta, 0.0]),
        "Q0": np.array([1 - eta, 1 - eta, 1.0]),
        "G0": np.array([1 / 2 - zeta, 1 - zeta, 1 / 2]),
        "H0": np.array([1 / 2 + zeta, zeta, 1 / 2]),
        "L": np.array([1 / 2, 1 / 2, 1 / 2]),
    }


def _get_points_table_78(a, b, c):
    eta = (1 + (a / b) ** 2 - (a / c) ** 2) / 4
    delta = (1 + (b / a) ** 2 - (b / c) ** 2) / 4
    phi = (1 + (c / b) ** 2 - (c / a) ** 2) / 4
    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "T": np.array([0.0, 1 / 2, 1 / 2]),
        "Z": np.array([1 / 2, 1 / 2, 0.0]),
        "Y": np.array([1 / 2, 0.0, 1 / 2]),
        "A0": np.array([1 / 2, 1 / 2 + eta, eta]),
        "C0": np.array([1 / 2, 1 / 2 - eta, 1 - eta]),
        "B0": np.array([1 / 2 + delta, 1 / 2, delta]),
        "D0": np.array([1 / 2 - delta, 1 / 2, 1 - delta]),
        "G0": np.array([phi, 1 / 2 + phi, 1 / 2]),
        "H0": np.array([1 - phi, 1 / 2 - phi, 1 / 2]),
        "L": np.array([1 / 2, 1 / 2, 1 / 2]),
    }


def _get_points_table_79(a, b, c):
    zeta = (1 + (a / c) ** 2) / 4
    eta = (1 + (b / c) ** 2) / 4
    delta = (b**2 - a**2) / 4 / c**2
    mu = (a**2 + b**2) / 4 / c**2
    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "X": np.array([1 / 2, 1 / 2, -1 / 2]),
        "S": np.array([1 / 2, 0.0, 0.0]),
        "R": np.array([0.0, 1 / 2, 0.0]),
        "T": np.array([0.0, 0.0, 1 / 2]),
        "W": np.array([1 / 4, 1 / 4, 1 / 4]),
        "SIGMA0": np.array([-zeta, zeta, zeta]),
        "F2": np.array([zeta, 1 - zeta, -zeta]),
        "Y0": np.array([eta, -eta, eta]),
        "U0": np.array([1 - eta, eta, -eta]),
        "L0": np.array([-mu, mu, 1 / 2 - delta]),
        "M0": np.array([mu, -mu, 1 / 2 + delta]),
        "J0": np.array([1 / 2 - delta, 1 / 2 + delta, -mu]),
    }


def _get_points_table_80(a, b, c):
    zeta = (1 + (b / a) ** 2) / 4
    eta = (1 + (c / a) ** 2) / 4
    delta = (c**2 - b**2) / 4 / a**2
    mu = (b**2 + c**2) / 4 / a**2
    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "X": np.array([-1 / 2, 1 / 2, 1 / 2]),
        "S": np.array([1 / 2, 0.0, 0.0]),
        "R": np.array([0.0, 1 / 2, 0.0]),
        "T": np.array([0.0, 0.0, 1 / 2]),
        "W": np.array([1 / 4, 1 / 4, 1 / 4]),
        "Y0": np.array([zeta, -zeta, zeta]),
        "U2": np.array([-zeta, zeta, 1 - zeta]),
        "LAMBDA0": np.array([eta, eta, -eta]),
        "G2": np.array([-eta, 1 - eta, eta]),
        "K": np.array([1 / 2 - delta, -mu, mu]),
        "K2": np.array([1 / 2 + delta, mu, -mu]),
        "K4": np.array([-mu, 1 / 2 - delta, 1 / 2 + delta]),
    }


def _get_points_table_81(a, b, c):
    zeta = (1 + (c / b) ** 2) / 4
    eta = (1 + (a / b) ** 2) / 4
    delta = (a**2 - c**2) / 4 / b**2
    mu = (c**2 + a**2) / 4 / b**2
    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "X": np.array([1 / 2, -1 / 2, 1 / 2]),
        "S": np.array([1 / 2, 0.0, 0.0]),
        "R": np.array([0.0, 1 / 2, 0.0]),
        "T": np.array([0.0, 0.0, 1 / 2]),
        "W": np.array([1 / 4, 1 / 4, 1 / 4]),
        "SIGMA0": np.array([-eta, eta, eta]),
        "F0": np.array([eta, -eta, 1 - eta]),
        "LAMBDA0": np.array([zeta, zeta, -zeta]),
        "G0": np.array([1 - zeta, -zeta, zeta]),
        "V0": np.array([mu, 1 / 2 - delta, -mu]),
        "H0": np.array([-mu, 1 / 2 + delta, mu]),
        "H2": np.array([1 / 2 + delta, -mu, 1 / 2 - delta]),
    }


def _get_points_table_82(a, b, c, lattice_type):
    if lattice_type == "oA":
        zeta = (1 + (b / c) ** 2) / 4
    elif lattice_type == "oC":
        zeta = (1 + (a / b) ** 2) / 4
    else:
        raise PotentialBugError(
            error_summary=f'(convention="HPKOT"), table 82. Wrong lattice type, got "{lattice_type}", expected "oA" or "oC".'
        )
    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "Y": np.array([-1 / 2, 1 / 2, 0.0]),
        "T": np.array([-1 / 2, 1 / 2, 1 / 2]),
        "Z": np.array([0.0, 0.0, 1 / 2]),
        "S": np.array([0.0, 1 / 2, 0.0]),
        "R": np.array([0.0, 1 / 2, 1 / 2]),
        "SIGMA0": np.array([zeta, zeta, 0.0]),
        "C0": np.array([-zeta, 1 - zeta, 0.0]),
        "A0": np.array([zeta, zeta, 1 / 2]),
        "E0": np.array([-zeta, 1 - zeta, 1 / 2]),
    }


def _get_points_table_83(a, b, c, lattice_type):
    if lattice_type == "oA":
        zeta = (1 + (c / b) ** 2) / 4
    elif lattice_type == "oC":
        zeta = (1 + (b / a) ** 2) / 4
    else:
        raise PotentialBugError(
            error_summary=f'(convention="HPKOT"), table 83. Wrong lattice type, got "{lattice_type}", expected "oA" or "oC".'
        )
    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "Y": np.array([1 / 2, 1 / 2, 0.0]),
        "T": np.array([1 / 2, 1 / 2, 1 / 2]),
        "T2": np.array([1 / 2, 1 / 2, -1 / 2]),
        "Z": np.array([0.0, 0.0, 1 / 2]),
        "Z2": np.array([0.0, 0.0, -1 / 2]),
        "S": np.array([0.0, 1 / 2, 0.0]),
        "R": np.array([0.0, 1 / 2, 1 / 2]),
        "R2": np.array([0.0, 1 / 2, -1 / 2]),
        "DELTA0": np.array([-zeta, zeta, 0.0]),
        "F0": np.array([zeta, 1 - zeta, 0.0]),
        "B0": np.array([-zeta, zeta, 1 / 2]),
        "B2": np.array([-zeta, zeta, -1 / 2]),
        "G0": np.array([zeta, 1 - zeta, 1 / 2]),
        "G2": np.array([zeta, 1 - zeta, -1 / 2]),
    }


def _get_points_table_84():
    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "A": np.array([0.0, 0.0, 1 / 2]),
        "K": np.array([1 / 3, 1 / 3, 0.0]),
        "H": np.array([1 / 3, 1 / 3, 1 / 2]),
        "H2": np.array([1 / 3, 1 / 3, -1 / 2]),
        "M": np.array([1 / 2, 0.0, 0.0]),
        "L": np.array([1 / 2, 0.0, 1 / 2]),
    }


def _get_points_table_85(a, c):
    delta = ((a / c) ** 2) / 4
    eta = 5 / 6 - 2 * delta
    nu = 1 / 3 + delta

    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "T": np.array([1 / 2, 1 / 2, 1 / 2]),
        "L": np.array([1 / 2, 0.0, 0.0]),
        "L2": np.array([0.0, -1 / 2, 0.0]),
        "L4": np.array([0.0, 0.0, -1 / 2]),
        "F": np.array([1 / 2, 0.0, 1 / 2]),
        "F2": np.array([1 / 2, 1 / 2, 0.0]),
        "S0": np.array([nu, -nu, 0.0]),
        "S2": np.array([1 - nu, 0.0, nu]),
        "S4": np.array([nu, 0.0, -nu]),
        "S6": np.array([1 - nu, nu, 0.0]),
        "H0": np.array([1 / 2, -1 + eta, 1 - eta]),
        "H2": np.array([eta, 1 - eta, 1 / 2]),
        "H4": np.array([eta, 1 / 2, 1 - eta]),
        "H6": np.array([1 / 2, 1 - eta, -1 + eta]),
        "M0": np.array([nu, -1 + eta, nu]),
        "M2": np.array([1 - nu, 1 - eta, 1 - nu]),
        "M4": np.array([eta, nu, nu]),
        "M6": np.array([1 - nu, 1 - nu, 1 - eta]),
        "M8": np.array([nu, nu, -1 + eta]),
    }


def _get_points_table_86(a, c):
    zeta = 1 / 6 - ((c / a) ** 2) / 9
    eta = 1 / 2 - 2 * zeta
    nu = 1 / 2 + zeta
    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "T": np.array([1 / 2, -1 / 2, 1 / 2]),
        "P0": np.array([eta, -1 + eta, eta]),
        "P2": np.array([eta, eta, eta]),
        "R0": np.array([1 - eta, -eta, -eta]),
        "M": np.array([1 - nu, -nu, 1 - nu]),
        "M2": np.array([nu, -1 + nu, -1 + nu]),
        "L": np.array([1 / 2, 0.0, 0.0]),
        "F": np.array([1 / 2, -1 / 2, 0.0]),
    }


def _get_points_table_87(a, c, beta):
    beta = beta * TORADIANS
    eta = (1 + (a / c) * cos(beta)) / 2 / sin(beta) ** 2
    nu = 1 / 2 + eta * c * cos(beta) / a
    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "Z": np.array([0.0, 1 / 2, 0.0]),
        "B": np.array([0.0, 0.0, 1 / 2]),
        "B2": np.array([0.0, 0.0, -1 / 2]),
        "Y": np.array([1 / 2, 0.0, 0.0]),
        "Y2": np.array([-1 / 2, 0.0, 0.0]),
        "C": np.array([1 / 2, 1 / 2, 0.0]),
        "C2": np.array([-1 / 2, 1 / 2, 0.0]),
        "D": np.array([0.0, 1 / 2, 1 / 2]),
        "D2": np.array([0.0, 1 / 2, -1 / 2]),
        "A": np.array([-1 / 2, 0.0, 1 / 2]),
        "E": np.array([-1 / 2, 1 / 2, 1 / 2]),
        "H": np.array([-eta, 0.0, 1 - nu]),
        "H2": np.array([-1 + eta, 0.0, nu]),
        "H4": np.array([-eta, 0.0, -nu]),
        "M": np.array([-eta, 1 / 2, 1 - nu]),
        "M2": np.array([-1 + eta, 1 / 2, nu]),
        "M4": np.array([-eta, 1 / 2, -nu]),
    }


def _get_points_table_88(a, b, c, beta):
    beta = beta * TORADIANS
    zeta = (2 + (a / c) * cos(beta)) / 4 / sin(beta) ** 2
    eta = 1 / 2 - 2 * zeta * c * cos(beta) / a
    psi = 3 / 4 - b**2 / 4 / a**2 / sin(beta) ** 2
    phi = psi - (3 / 4 - psi) * a * cos(beta) / c
    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "Y2": np.array([-1 / 2, 1 / 2, 0.0]),
        "Y4": np.array([1 / 2, -1 / 2, 0.0]),
        "A": np.array([0.0, 0.0, 1 / 2]),
        "M2": np.array([-1 / 2, 1 / 2, 1 / 2]),
        "V": np.array([1 / 2, 0.0, 0.0]),
        "V2": np.array([0.0, 1 / 2, 0.0]),
        "L2": np.array([0.0, 1 / 2, 1 / 2]),
        "C": np.array([1 - psi, 1 - psi, 0.0]),
        "C2": np.array([-1 + psi, psi, 0.0]),
        "C4": np.array([psi, -1 + psi, 0.0]),
        "D": np.array([-1 + phi, phi, 1 / 2]),
        "D2": np.array([1 - phi, 1 - phi, 1 / 2]),
        "E": np.array([-1 + zeta, 1 - zeta, 1 - eta]),
        "E2": np.array([-zeta, zeta, eta]),
        "E4": np.array([zeta, -zeta, 1 - eta]),
    }


def _get_points_table_89(a, b, c, beta):
    beta = beta * TORADIANS
    mu = (1 + (a / b) ** 2) / 4
    delta = -a * c * cos(beta) / 2 / b**2
    zeta = ((a / b) ** 2 + (1 + (a / c) * cos(beta)) / sin(beta) ** 2) / 4
    eta = 1 / 2 - 2 * zeta * c * cos(beta) / a
    phi = 1 + zeta - 2 * mu
    psi = eta - 2 * delta
    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "Y": np.array([1 / 2, 1 / 2, 0.0]),
        "A": np.array([0.0, 0.0, 1 / 2]),
        "M": np.array([1 / 2, 1 / 2, 1 / 2]),
        "V2": np.array([0.0, 1 / 2, 0.0]),
        "L2": np.array([0.0, 1 / 2, 1 / 2]),
        "F": np.array([-1 + phi, 1 - phi, 1 - psi]),
        "F2": np.array([1 - phi, phi, psi]),
        "F4": np.array([phi, 1 - phi, 1 - psi]),
        "H": np.array([-zeta, zeta, eta]),
        "H2": np.array([zeta, 1 - zeta, 1 - eta]),
        "H4": np.array([zeta, -zeta, 1 - eta]),
        "G": np.array([-mu, mu, delta]),
        "G2": np.array([mu, 1 - mu, -delta]),
        "G4": np.array([mu, -mu, -delta]),
        "G6": np.array([1 - mu, mu, delta]),
    }


def _get_points_table_90(a, b, c, beta):
    beta = beta * TORADIANS
    zeta = ((a / b) ** 2 + (1 + (a / c) * cos(beta)) / sin(beta) ** 2) / 4
    rho = 1 - zeta * (b / a) ** 2
    eta = 1 / 2 - 2 * zeta * c * cos(beta) / a
    mu = eta / 2 + ((a / b) ** 2) / 4 + a * c * cos(beta) / 2 / b**2
    nu = 2 * mu - zeta
    omega = c * (1 - 4 * nu + (a / b) ** 2 * sin(beta) ** 2) / 2 / a / cos(beta)
    delta = -1 / 4 + omega / 2 - zeta * (c / a) * cos(beta)
    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "Y": np.array([1 / 2, 1 / 2, 0.0]),
        "A": np.array([0.0, 0.0, 1 / 2]),
        "M2": np.array([-1 / 2, 1 / 2, 1 / 2]),
        "V": np.array([1 / 2, 0.0, 0.0]),
        "V2": np.array([0.0, 1 / 2, 0.0]),
        "L2": np.array([0.0, 1 / 2, 1 / 2]),
        "I": np.array([-1 + rho, rho, 1 / 2]),
        "I2": np.array([1 - rho, 1 - rho, 1 / 2]),
        "K": np.array([-nu, nu, omega]),
        "K2": np.array([-1 + nu, 1 - nu, 1 - omega]),
        "K4": np.array([1 - nu, nu, omega]),
        "H": np.array([-zeta, zeta, eta]),
        "H2": np.array([zeta, 1 - zeta, 1 - eta]),
        "H4": np.array([zeta, -zeta, 1 - eta]),
        "N": np.array([-mu, mu, delta]),
        "N2": np.array([mu, 1 - mu, -delta]),
        "N4": np.array([mu, -mu, -delta]),
        "N6": np.array([1 - mu, mu, delta]),
    }


def _get_points_table_91():
    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "Z": np.array([0.0, 0.0, 0.0]),
        "Y": np.array([0, 1 / 2, 0.0]),
        "X": np.array([1 / 2, 0.0, 0.0]),
        "V": np.array([1 / 2, 1 / 2, 0.0]),
        "U": np.array([1 / 2, 0.0, 1 / 2]),
        "T": np.array([0.0, 1 / 2, 1 / 2]),
        "R": np.array([1 / 2, 1 / 2, 1 / 2]),
    }


def _get_points_table_92():
    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "Z": np.array([0.0, 0.0, 1 / 2]),
        "Y": np.array([0.0, 1 / 2, 0.0]),
        "Y2": np.array([0.0, -1 / 2, 0.0]),
        "X": np.array([1 / 2, 0.0, 0.0]),
        "V2": np.array([1 / 2, -1 / 2, 0.0]),
        "U2": np.array([-1 / 2, 0.0, 1 / 2]),
        "T2": np.array([0, -1 / 2, 1 / 2]),
        "R2": np.array([-1 / 2, -1 / 2, 1 / 2]),
    }


def _hpkot_get_points(conventional_cell, lattice_type, extended_bl_symbol):
    a, b, c, _, beta, _ = get_params(cell=conventional_cell)

    if extended_bl_symbol in ["cP1", "cP2"]:
        return _get_points_table_69()

    if extended_bl_symbol in ["cF1", "cF2"]:
        return _get_points_table_70()

    if extended_bl_symbol == "cI1":
        return _get_points_table_71()

    if extended_bl_symbol == "tP1":
        return _get_points_table_72()

    if extended_bl_symbol == "tI1":
        return _get_points_table_73(a=a, c=c)

    if extended_bl_symbol == "tI2":
        return _get_points_table_74(a=a, c=c)

    if extended_bl_symbol == "oP1":
        return _get_points_table_75()

    if extended_bl_symbol == "oF1":
        return _get_points_table_76(a=a, b=b, c=c)

    if extended_bl_symbol == "oF2":
        return _get_points_table_77(a=a, b=b, c=c)

    if extended_bl_symbol == "oF3":
        return _get_points_table_78(a=a, b=b, c=c)

    if extended_bl_symbol == "oI1":
        return _get_points_table_79(a=a, b=b, c=c)

    if extended_bl_symbol == "oI2":
        return _get_points_table_80(a=a, b=b, c=c)

    if extended_bl_symbol == "oI3":
        return _get_points_table_81(a=a, b=b, c=c)

    if extended_bl_symbol == "oC1":
        return _get_points_table_82(a=a, b=b, c=c, lattice_type=lattice_type)

    if extended_bl_symbol == "oC2":
        return _get_points_table_83(a=a, b=b, c=c, lattice_type=lattice_type)

    if extended_bl_symbol == "oA1":
        return _get_points_table_82(a=a, b=b, c=c, lattice_type=lattice_type)

    if extended_bl_symbol == "oA2":
        return _get_points_table_83(a=a, b=b, c=c, lattice_type=lattice_type)

    if extended_bl_symbol in ["hP1", "hP2"]:
        return _get_points_table_84()

    if extended_bl_symbol == "hR1":
        return _get_points_table_85(a=a, c=c)

    if extended_bl_symbol == "hR2":
        return _get_points_table_86(a=a, c=c)

    if extended_bl_symbol == "mP1":
        return _get_points_table_87(a=a, c=c, beta=beta)

    if extended_bl_symbol == "mC1":
        return _get_points_table_88(a=a, b=b, c=c, beta=beta)

    if extended_bl_symbol == "mC2":
        return _get_points_table_89(a=a, b=b, c=c, beta=beta)

    if extended_bl_symbol == "mC3":
        return _get_points_table_90(a=a, b=b, c=c, beta=beta)

    if extended_bl_symbol == "aP2":
        return _get_points_table_91()

    if extended_bl_symbol == "aP3":
        return _get_points_table_92()

    raise PotentialBugError(
        error_summary=f'(convention="HPKOT"). Unexpected extended Bravais lattice symbol, got "{extended_bl_symbol}".'
    )


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
