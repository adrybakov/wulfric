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


from math import cos, sin, sqrt

import numpy as np

from wulfric.cell._basic_manipulation import get_params, get_reciprocal
from wulfric._spglib_interface import get_spglib_data, validate_spglib_data
from wulfric._syntactic_sugar import SyntacticSugar
from wulfric.constants._kpoints import HS_PLOT_NAMES
from wulfric.crystal._crystal_validation import validate_atoms
from wulfric.crystal._conventional import get_conventional
from wulfric.crystal._primitive import get_primitive
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


def _hpkot_get_extended_bl_symbol(lattice_type, space_group_number, conventional_cell):
    r"""
    Computes extended Bravais lattice symbol as in Table 94 of [1]_.

    Parameters
    ==========
    lattice_type : str
         Bravais lattice type.
    space_group_number : int
        Number of space group. ``1 <= space_group_number < 230``.
    conventional_cell : (3, 3) |arrray-like|_

    Returns
    =======
    extended_bl_symbol : str

    References
    ----------
    .. [1] Hinuma, Y., Pizzi, G., Kumagai, Y., Oba, F. and Tanaka, I., 2017.
           Band structure diagram paths based on crystallography.
           Computational Materials Science, 128, pp.140-184.
    """

    # Lattice types that do not require computation of lattice parameters
    if lattice_type in ["cI", "tP", "oP", "mP"]:
        return f"{lattice_type}1"

    if lattice_type == "cP":
        if 195 <= space_group_number <= 206:
            return "cP1"
        elif 207 <= space_group_number <= 230:
            return "cP2"
        else:
            raise PotentialBugError(
                error_summary=f'(convention="HPKOT"), lattice type cP, space group {space_group_number}. Failed to define extended Bravais lattice symbol.'
            )

    if lattice_type == "cF":
        if 195 <= space_group_number <= 206:
            return "cF1"
        elif 207 <= space_group_number <= 230:
            return "cF2"
        else:
            raise PotentialBugError(
                error_summary=f'(convention="HPKOT"), lattice type cF, space group {space_group_number}. Failed to define extended Bravais lattice symbol.'
            )

    if lattice_type == "hP":
        if (
            143 <= space_group_number <= 149
            or 159 <= space_group_number <= 163
            or space_group_number in [151, 153, 157]
        ):
            return "hP1"
        else:
            return "hP2"

    # Lattice types that require computation of lattice parameters
    a, b, c, alpha, beta, gamma = get_params(cell=conventional_cell)

    if lattice_type == "tI":
        if c <= a:
            return "tI1"
        else:
            return "tI2"

    if lattice_type == "oF":
        if 1 / a**2 > 1 / b**2 + 1 / c**2:
            return "oF1"
        elif 1 / c**2 > 1 / a**2 + 1 / b**2:
            return "oF2"
        else:
            return "oF3"

    if lattice_type == "oI":
        if c >= a and c >= b:
            return "oI1"
        if a >= b and a >= c:
            return "oI2"
        if b >= a and b >= c:
            return "oI3"

    if lattice_type == "oC":
        if a <= b:
            return "oC1"
        else:
            return "oC2"

    if lattice_type == "oA":
        if b <= c:
            return "oA1"
        else:
            return "oA2"

    if lattice_type == "hR":
        if sqrt(3) * a <= sqrt(2) * c:
            return "hR1"
        else:
            return "hR2"

    if lattice_type == "mC":
        if b <= a * sin(beta):
            return "mC1"
        else:
            if -a * cos(beta) / c + ((a * sin(beta)) / b) ** 2 <= 1:
                return "mC2"
            else:
                return "mC3"

    if lattice_type == "aP":
        _, _, _, r_alpha, r_beta, r_gamma = get_params(
            cell=get_reciprocal(cell=conventional_cell)
        )

        if r_alpha >= 90 and r_beta >= 90 and r_gamma >= 90:
            return "aP2"
        else:
            return "aP3"

    # If lattice type is not one of the expected ones
    raise PotentialBugError(
        f'(convention="HPKOT"), lattice type {lattice_type}, space group {space_group_number}.. Failed to identify lattice type (not one of supported).'
    )


def _hpkot_get_hs_points(lattice_type, extended_bl_type, conventional_cell):
    if lattice_type == "cP":
        pass


def hpkot_get_hs_points(
    cell,
    atoms,
    spglib_data=None,
    relative=True,
):
    r"""
    Returns set of high symmetry points as defined in [1]_.

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
    relative : bool, default True
        Whether to return coordinates as relative to the reciprocal cell or in absolute
        coordinates in the reciprocal Cartesian space.

    Returns
    -------
    coordinates : list of (3, 3) :numpy:`ndarray`
        Coordinates of the high symmetry points in reciprocal space. Relative to the
        reciprocal cell.
    names: list of str
        Names of the high symmetry points. Used for programming, not for plotting. Have
        the same length as ``coordinates``.
    labels : list of str
        List of the high symmetry points labels for plotting. Have the same length as
        ``coordinates``. Labels are not necessary equal to the names.

    Notes
    =====
    |spglib|_ uses ``types`` to distinguish the atoms. To see how wulfric deduces the
    ``types`` for given atoms see :py:func:`wulfric.crystal.get_spglib_types`.

    References
    ----------
    .. [1] Hinuma, Y., Pizzi, G., Kumagai, Y., Oba, F. and Tanaka, I., 2017.
           Band structure diagram paths based on crystallography.
           Computational Materials Science, 128, pp.140-184.

    See Also
    --------
    wulfric.Kpoints : Class with a convenient interface for the same information.

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

    conv_cell, _ = get_conventional(
        cell=cell, atoms=atoms, spglib_data=spglib_data, convention="SC"
    )

    extended_bl_type = _hpkot_get_extended_bl_symbol(
        lattice_type=lattice_type,
        space_group_number=spglib_data.space_group_number,
        conventional_cell=conv_cell,
    )

    hs_points = _hpkot_get_hs_points(
        lattice_type=lattice_type,
        extended_bl_type=extended_bl_type,
        conventional_cell=conv_cell,
    )

    names = []
    labels = []
    coordinates = []

    primitive_cell, _ = get_primitive(
        cell=cell, atoms=atoms, convention="SC", spglib_data=spglib_data
    )
    primitive_rcell = get_reciprocal(cell=primitive_cell)

    for point in hs_points:
        names.append(point)

        labels.append(HS_PLOT_NAMES[point])

        # Here coordinates are absolute
        coordinates.append(hs_points[point] @ primitive_rcell)

    if relative:
        # absolute -> relative
        coordinates = coordinates @ np.linalg.inv(get_reciprocal(cell=cell))

    return coordinates, names, labels


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
