# Wulfric - Crystal, Lattice, Atoms, K-path.
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


from math import cos, pi, sin

from wulfric.bravais_lattice.constructor import (
    BCC,
    BCT,
    CUB,
    FCC,
    HEX,
    MCL,
    MCLC,
    ORC,
    ORCC,
    ORCF,
    ORCI,
    RHL,
    TET,
    TRI,
)
from wulfric.constants import BRAVAIS_LATTICE_VARIATIONS, TORADIANS

__all__ = [
    "lattice_example",
]


def lattice_example(
    lattice_name: str = None,
    convention: str = None,
):
    r"""
    Return an example of the lattice.

    Parameters
    ----------
    lattice_name : str, optional
        Name of the lattice to be returned.
        For available names see documentation of each Bravais lattice class.
        Lowercased before usage.
    convention : str, optional
        Name of the convention that is used for cell standardization.
        Supported conventions are:
        * "sc" - for Setyawan and Curtarolo standardization.

        By default the lattice is not standardized.

        .. versionadded:: 0.3.1

    Returns
    -------
    lattice : Lattice or list
        :py:class:`.Lattice` class is returned.
        If no math found a list with available examples is returned.
    """

    correct_inputs = set(map(lambda x: x.lower(), BRAVAIS_LATTICE_VARIATIONS)).union(
        set(
            map(
                lambda x: x.translate(str.maketrans("", "", "12345ab")).lower(),
                BRAVAIS_LATTICE_VARIATIONS,
            )
        )
    )

    if not isinstance(lattice_name, str) or lattice_name.lower() not in correct_inputs:
        message = (
            f"There is no {lattice_name} Bravais lattice. Available examples are:\n"
        )
        for name in BRAVAIS_LATTICE_VARIATIONS:
            message += f"  * {name}\n"
        raise ValueError(message)

    lattice_name = lattice_name.lower()

    if lattice_name == "cub":
        lattice = CUB(pi)
    elif lattice_name == "fcc":
        lattice = FCC(pi)
    elif lattice_name == "bcc":
        lattice = BCC(pi)
    elif lattice_name == "tet":
        lattice = TET(pi, 1.5 * pi)
    elif lattice_name in ["bct1", "bct"]:
        lattice = BCT(1.5 * pi, pi)
    elif lattice_name == "bct2":
        lattice = BCT(pi, 1.5 * pi)
    elif lattice_name == "orc":
        lattice = ORC(pi, 1.5 * pi, 2 * pi)
    elif lattice_name in ["orcf1", "orcf"]:
        lattice = ORCF(0.7 * pi, 5 / 4 * pi, 5 / 3 * pi)
    elif lattice_name == "orcf2":
        lattice = ORCF(1.2 * pi, 5 / 4 * pi, 5 / 3 * pi)
    elif lattice_name == "orcf3":
        lattice = ORCF(pi, 5 / 4 * pi, 5 / 3 * pi)
    elif lattice_name == "orci":
        return ORCI(pi, 1.3 * pi, 1.7 * pi)
    elif lattice_name == "orcc":
        lattice = ORCC(pi, 1.3 * pi, 1.7 * pi)
    elif lattice_name == "hex":
        lattice = HEX(pi, 2 * pi)
    elif lattice_name in ["rhl1", "rhl"]:
        # If alpha = 60 it is effectively FCC!
        lattice = RHL(pi, 70)
    elif lattice_name == "rhl2":
        lattice = RHL(pi, 110)
    elif lattice_name == "mcl":
        lattice = MCL(pi, 1.3 * pi, 1.6 * pi, alpha=75)
    elif lattice_name in ["mclc1", "mclc"]:
        lattice = MCLC(pi, 1.4 * pi, 1.7 * pi, 80)
    elif lattice_name == "mclc2":
        lattice = MCLC(1.4 * pi * sin(75 * TORADIANS), 1.4 * pi, 1.7 * pi, 75)
    elif lattice_name == "mclc3":
        b = pi
        x = 1.1
        alpha = 78
        ralpha = alpha * TORADIANS
        c = b * (x**2) / (x**2 - 1) * cos(ralpha) * 1.8
        a = x * b * sin(ralpha)
        lattice = MCLC(a, b, c, alpha)
    elif lattice_name == "mclc4":
        b = pi
        x = 1.2
        alpha = 65
        ralpha = alpha * TORADIANS
        c = b * (x**2) / (x**2 - 1) * cos(ralpha)
        a = x * b * sin(ralpha)
        lattice = MCLC(a, b, c, alpha)
    elif lattice_name == "mclc5":
        b = pi
        x = 1.4
        alpha = 53
        ralpha = alpha * TORADIANS
        c = b * (x**2) / (x**2 - 1) * cos(ralpha) * 0.9
        a = x * b * sin(ralpha)
        lattice = MCLC(a, b, c, alpha)
    elif lattice_name in ["tri1a", "tri1", "tri", "tria"]:
        lattice = TRI(1, 1.5, 2, 120, 110, 100, reciprocal=True)
    elif lattice_name in ["tri2a", "tri2"]:
        lattice = TRI(1, 1.5, 2, 120, 110, 90, reciprocal=True)
    elif lattice_name in ["tri1b", "trib"]:
        lattice = TRI(1, 1.5, 2, 60, 70, 80, reciprocal=True)
    elif lattice_name == "tri2b":
        lattice = TRI(1, 1.5, 2, 60, 70, 90, reciprocal=True)

    if convention is not None:
        lattice.convention = convention

    return lattice
