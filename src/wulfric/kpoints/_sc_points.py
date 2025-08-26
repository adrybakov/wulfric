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


from math import cos, sin, tan

import numpy as np

from wulfric.cell._basic_manipulation import get_params, get_reciprocal
from wulfric._spglib_interface import get_spglib_data, validate_spglib_data
from wulfric._syntactic_sugar import SyntacticSugar
from wulfric.constants._numerical import TORADIANS
from wulfric.constants._sc_convention import SC_BRAVAIS_LATTICE_SHORT_NAMES
from wulfric.constants._kpoints import HS_PLOT_NAMES
from wulfric.crystal._crystal_validation import validate_atoms
from wulfric.crystal._conventional import get_conventional
from wulfric.crystal._primitive import get_primitive
from wulfric.crystal._sc_variation import sc_get_variation

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def _SC_CUB_hs_points():
    r"""
    Get high-symmetry points for the CUB lattice.

    See :ref:`guide_cub` for the details.

    Returns
    -------
    kpoints : dict
        High-symmetry points.
    """

    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "M": np.array([1 / 2, 1 / 2, 0]),
        "R": np.array([1 / 2, 1 / 2, 1 / 2]),
        "X": np.array([0, 1 / 2, 0]),
    }


def _SC_FCC_hs_points():
    r"""
    Get high-symmetry points for the FCC lattice.

    See :ref:`guide_fcc` for the details.

    Returns
    -------
    kpoints : dict
        High-symmetry points.
    """

    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "K": np.array([3 / 8, 3 / 8, 3 / 4]),
        "L": np.array([1 / 2, 1 / 2, 1 / 2]),
        "U": np.array([5 / 8, 1 / 4, 5 / 8]),
        "W": np.array([1 / 2, 1 / 4, 3 / 4]),
        "X": np.array([1 / 2, 0, 1 / 2]),
    }


def _SC_BCC_hs_points():
    r"""
    Get high-symmetry points for the CUB lattice.

    See :ref:`guide_bcc` for the details.

    Returns
    -------
    kpoints : dict
        High-symmetry points.
    """

    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "H": np.array([1 / 2, -1 / 2, 1 / 2]),
        "P": np.array([1 / 4, 1 / 4, 1 / 4]),
        "N": np.array([0, 0, 1 / 2]),
    }


def _SC_TET_hs_points():
    r"""
    Get high-symmetry points for the TET lattice.

    See :ref:`guide_tet` for the details.

    Returns
    -------
    kpoints : dict
        High-symmetry points.
    """
    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "A": np.array([1 / 2, 1 / 2, 1 / 2]),
        "M": np.array([1 / 2, 1 / 2, 0]),
        "R": np.array([0, 1 / 2, 1 / 2]),
        "X": np.array([0, 1 / 2, 0]),
        "Z": np.array([0, 0, 1 / 2]),
    }


def _SC_BCT_hs_points(variation, conv_a, conv_c):
    r"""
    Get high-symmetry points for the BCT lattice.

    See :ref:`guide_bct` for the details.

    Parameters
    ----------
    variation : str
        BCT variation. Case-insensitive.
    conv_a : float
        Length of the first two lattice vectors of the conventional cell.
    conv_c : float
        Length of the third lattice vector of the conventional cell.

    Returns
    -------
    kpoints : dict
        High-symmetry points.
    """

    variation = variation.upper()

    if variation == "BCT1":
        eta = (1 + conv_c**2 / conv_a**2) / 4
        kpoints = {
            "GAMMA": np.array([0.0, 0.0, 0.0]),
            "M": np.array([-1 / 2, 1 / 2, 1 / 2]),
            "N": np.array([0, 1 / 2, 0]),
            "P": np.array([1 / 4, 1 / 4, 1 / 4]),
            "X": np.array([0, 0, 1 / 2]),
            "Z": np.array([eta, eta, -eta]),
            "Z1": np.array([-eta, 1 - eta, eta]),
        }

    elif variation == "BCT2":
        eta = (1 + conv_a**2 / conv_c**2) / 4
        zeta = conv_a**2 / (2 * conv_c**2)
        kpoints = {
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
    return kpoints


def _SC_ORC_hs_points():
    r"""
    Get high-symmetry points for the ORC lattice.

    See :ref:`guide_orc` for the details.

    Returns
    -------
    kpoints : dict
        High-symmetry points.
    """
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


def _SC_ORCF_hs_points(variation, conv_a, conv_b, conv_c):
    r"""
    Get high-symmetry points for the ORCF lattice.

    See :ref:`guide_orcf` for the details.

    Parameters
    ----------
    variation : str
        ORCF variation. Case-insensitive.
    conv_a : float
        Length of the first lattice vector of the conventional cell.
    conv_b : float
        Length of the second lattice vector of the conventional cell.
    conv_c : float
        Length of the third lattice vector of the conventional cell.

    Returns
    -------
    kpoints : dict
        High-symmetry points.
    """

    variation = variation.upper()

    if variation == "ORCF1":
        eta = (1 + conv_a**2 / conv_b**2 + conv_a**2 / conv_c**2) / 4
        zeta = (1 + conv_a**2 / conv_b**2 - conv_a**2 / conv_c**2) / 4

        kpoints = {
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
    elif variation == "ORCF2":
        eta = (1 + conv_a**2 / conv_b**2 - conv_a**2 / conv_c**2) / 4
        delta = (1 + conv_b**2 / conv_a**2 - conv_b**2 / conv_c**2) / 4
        phi = (1 + conv_c**2 / conv_b**2 - conv_c**2 / conv_a**2) / 4

        kpoints = {
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

    elif variation == "ORCF3":
        eta = (1 + conv_a**2 / conv_b**2 + conv_a**2 / conv_c**2) / 4
        zeta = (1 + conv_a**2 / conv_b**2 - conv_a**2 / conv_c**2) / 4

        kpoints = {
            "GAMMA": np.array([0.0, 0.0, 0.0]),
            "A": np.array([1 / 2, 1 / 2 + zeta, zeta]),
            "A1": np.array([1 / 2, 1 / 2 - zeta, 1 - zeta]),
            "L": np.array([1 / 2, 1 / 2, 1 / 2]),
            "T": np.array([1, 1 / 2, 1 / 2]),
            "X": np.array([0, eta, eta]),
            "Y": np.array([1 / 2, 0, 1 / 2]),
            "Z": np.array([1 / 2, 1 / 2, 0]),
        }
    return kpoints


def _SC_ORCI_hs_points(conv_a, conv_b, conv_c):
    r"""
    Get high-symmetry points for the ORCI lattice.

    See :ref:`guide_orci` for the details.

    Parameters
    ----------
    conv_a : float
        Length of the first lattice vector of the conventional cell.
    conv_b : float
        Length of the second lattice vector of the conventional cell.
    conv_c : float
        Length of the third lattice vector of the conventional cell.

    Returns
    -------
    kpoints : dict
        High-symmetry points.
    """

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


def _SC_ORCC_hs_points(conv_a, conv_b):
    r"""
    Get high-symmetry points for the ORCC lattice.

    See :ref:`guide_orcc` for the details.

    Parameters
    ----------
    conv_a : float
        Length of the first lattice vector of the conventional cell.
    conv_b : float
        Length of the second lattice vector of the conventional cell.

    Returns
    -------
    kpoints : dict
        High-symmetry points.
    """

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


def _SC_HEX_hs_points():
    r"""
    Get high-symmetry points for the HEX lattice.

    See :ref:`guide_hex` for the details.

    Returns
    -------
    kpoints : dict
        High-symmetry points.
    """

    return {
        "GAMMA": np.array([0.0, 0.0, 0.0]),
        "A": np.array([0, 0, 1 / 2]),
        "H": np.array([1 / 3, 1 / 3, 1 / 2]),
        "K": np.array([1 / 3, 1 / 3, 0]),
        "L": np.array([1 / 2, 0, 1 / 2]),
        "M": np.array([1 / 2, 0, 0]),
    }


def _SC_RHL_hs_points(variation, conv_alpha):
    r"""
    Get high-symmetry points for the RHL lattice.

    See :ref:`guide_rhl` for the details.

    Parameters
    ----------
    variation : str
        RHL variation. Case-insensitive.
    alpha : float
        Angle between the lattice vectors.

    Returns
    -------
    kpoints : dict
        High-symmetry points.
    """

    variation = variation.upper()

    conv_alpha *= TORADIANS

    if variation == "RHL1":
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

    elif variation == "RHL2":
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


def _SC_MCL_hs_points(conv_b, conv_c, conv_alpha):
    r"""
    Get high-symmetry points for the MCL lattice.

    See :ref:`guide_mcl` for the details.

    Parameters
    ----------
    conv_b : float
        Length of the second lattice vector of the conventional cell.
    conv_c : float
        Length of the third lattice vector of the conventional cell.
    conv_alpha : float
        Angle between the lattice vectors.

    Returns
    -------
    kpoints : dict
        High-symmetry points.
    """
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


def _SC_MCLC_hs_points(variation, conv_a, conv_b, conv_c, conv_alpha):
    r"""
    Get high-symmetry points for the MCLC lattice.

    See :ref:`guide_mclc` for the details.

    Parameters
    ----------
    variation : str
        MCLC variation.  Case-insensitive.
    conv_a : float
        Length of the first lattice vector of the conventional cell.
    conv_b : float
        Length of the second lattice vector of the conventional cell.
    conv_c : float
        Length of the third lattice vector of the conventional cell.
    conv_alpha : float
        Angle between the lattice vectors.

    Returns
    -------
    kpoints : dict
        High-symmetry points.
    """
    variation = variation.upper()

    conv_alpha *= TORADIANS
    # Parameters
    if variation in ["MCLC1", "MCLC2"]:
        zeta = (2 - conv_b * cos(conv_alpha) / conv_c) / (4 * sin(conv_alpha) ** 2)
        eta = 1 / 2 + 2 * zeta * conv_c * cos(conv_alpha) / conv_b
        psi = 3 / 4 - conv_a**2 / (4 * conv_b**2 * sin(conv_alpha) ** 2)
        phi = psi + (3 / 4 - psi) * conv_b * cos(conv_alpha) / conv_c
    elif variation in ["MCLC3", "MCLC4"]:
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
    elif variation == "MCLC5":
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

    # Path
    if variation == "MCLC1":
        return {
            "GAMMA": np.array([0.0, 0.0, 0.0]),
            "N": np.array([1 / 2, 0, 0]),
            "N1": np.array([0, -1 / 2, 0]),
            "F": np.array([1 - zeta, 1 - zeta, 1 - eta]),
            "F1": np.array([zeta, zeta, eta]),
            "F2": np.array([-zeta, -zeta, 1 - eta]),
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
    elif variation == "MCLC2":
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
            "Y": np.array([1 / 2, 1 / 2, 0]),
            "Y1": np.array([-1 / 2, -1 / 2, 0]),
            "Z": np.array([0, 0, 1 / 2]),
        }
    elif variation == "MCLC3":
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
    elif variation == "MCLC4":
        return {
            "GAMMA": np.array([0.0, 0.0, 0.0]),
            "F": np.array([1 - phi, 1 - phi, 1 - psi]),
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
    elif variation == "MCLC5":
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


def _SC_TRI_hs_points(variation):
    r"""
    Get high-symmetry points for the TRI lattice.

    See :ref:`guide_tri` for the details.

    Parameters
    ----------
    variation : str
        TRI variation. Case-insensitive.

    Returns
    -------
    kpoints : dict
        High-symmetry points.
    """

    variation = variation.upper()

    if variation in ["TRI1A", "TRI2A"]:
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

    elif variation in ["TRI1B", "TRI2B"]:
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


def sc_get_hs_points(
    cell,
    atoms,
    spglib_data=None,
    relative=True,
    length_tolerance=1e-8,
    angle_tolerance=1e-4,
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
    length_tolerance : float, default :math:`10^{-8}`
        Tolerance for length variables (lengths of the lattice vectors).  Default value is
        chosen in the contexts of condense matter physics, assuming that length is given
        in Angstroms. Please choose appropriate tolerance for your problem.
    angle_tolerance : float, default :math:`10^{-4}`
        Tolerance for angle variables (angles of the lattice). Default value is chosen in
        the contexts of condense matter physics, assuming that angles are in degrees.
        Please choose appropriate tolerance for your problem.

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
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp. 299-312.

    See Also
    --------
    wulfric.Kpoints : Class with a convenient interface for the same information.

    Examples
    --------

    .. doctest::

        >>> import wulfric
        >>> cell = wulfric.cell.sc_get_example_cell("hex")
        >>> atoms = dict(spglib_types=[1], positions=[[0, 0, 0]])
        >>> coordinates, names, labels = wulfric.kpoints.sc_get_hs_points(cell, atoms)
        >>> labels
        ['$\\Gamma$', 'A', 'H', 'K', 'L', 'M']
        >>> names
        ['G', 'A', 'H', 'K', 'L', 'M']
        >>> coordinates
        [array([0., 0., 0.]), array([0. , 0. , 0.5]), array([0.33333333, 0.33333333, 0.5       ]), array([0.33333333, 0.33333333, 0.        ]), array([0.5, 0. , 0.5]), array([0.5, 0. , 0. ])]

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

    lattice_type = SC_BRAVAIS_LATTICE_SHORT_NAMES[
        spglib_data.crystal_family + spglib_data.centring_type
    ]

    lattice_variation = sc_get_variation(
        cell=cell,
        atoms=atoms,
        spglib_data=spglib_data,
        length_tolerance=length_tolerance,
        angle_tolerance=angle_tolerance,
    )

    if lattice_type in [
        "BCT",
        "ORCF",
        "ORCI",
        "ORCC",
        "RHL",
        "MCL",
        "MCLC",
    ]:
        conv_cell, _ = get_conventional(
            cell=cell, atoms=atoms, spglib_data=spglib_data, convention="SC"
        )
        conv_a, conv_b, conv_c, conv_alpha, _, _ = get_params(cell=conv_cell)

    if lattice_type == "CUB":
        hs_points = _SC_CUB_hs_points()
    elif lattice_type == "FCC":
        hs_points = _SC_FCC_hs_points()
    elif lattice_type == "BCC":
        hs_points = _SC_BCC_hs_points()
    elif lattice_type == "TET":
        hs_points = _SC_TET_hs_points()
    elif lattice_type == "BCT":
        hs_points = _SC_BCT_hs_points(lattice_variation, conv_a, conv_c)
    elif lattice_type == "ORC":
        hs_points = _SC_ORC_hs_points()
    elif lattice_type == "ORCF":
        hs_points = _SC_ORCF_hs_points(lattice_variation, conv_a, conv_b, conv_c)
    elif lattice_type == "ORCI":
        hs_points = _SC_ORCI_hs_points(conv_a, conv_b, conv_c)
    elif lattice_type == "ORCC":
        hs_points = _SC_ORCC_hs_points(conv_a, conv_b)
    elif lattice_type == "HEX":
        hs_points = _SC_HEX_hs_points()
    elif lattice_type == "RHL":
        hs_points = _SC_RHL_hs_points(lattice_variation, conv_alpha)
    elif lattice_type == "MCL":
        hs_points = _SC_MCL_hs_points(conv_b, conv_c, conv_alpha)
    elif lattice_type == "MCLC":
        hs_points = _SC_MCLC_hs_points(
            lattice_variation, conv_a, conv_b, conv_c, conv_alpha
        )
    elif lattice_type == "TRI":
        hs_points = _SC_TRI_hs_points(lattice_variation)

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


if __name__ == "__main__":
    import wulfric

    cell = wulfric.cell.sc_get_example_cell("hex")
    atoms = dict(spglib_types=[1], positions=[[0, 0, 0]])
    coordinates, names, labels = sc_get_hs_points(cell, atoms)

    print(coordinates, names, labels, sep="\n\n")

    prim_cell, _ = get_primitive(cell=cell, atoms=atoms, convention="SC")
    old_coord = (
        coordinates
        @ get_reciprocal(cell=cell)
        @ np.linalg.inv(get_reciprocal(cell=prim_cell))
    )

    print(old_coord @ get_reciprocal(cell=prim_cell))
    print(coordinates @ get_reciprocal(cell=cell))
