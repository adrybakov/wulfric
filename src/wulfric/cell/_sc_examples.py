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


from math import cos, pi, sin

from wulfric.cell._sc_constructors import (
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
from wulfric.constants._numerical import TORADIANS
from wulfric.constants._sc_notation import BRAVAIS_LATTICE_VARIATIONS

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def get_cell_example(
    lattice_variation: str = None,
    convention: str = None,
):
    r"""
    Return an example of the lattice.

    Parameters
    ----------
    lattice_variation : str, optional
        Name of the lattice type or variation to be returned.
        For available names see documentation of each Bravais lattice class.
        Case-insensitive.
    convention : str, optional
        Name of the convention that is used for cell standardization.
        Supported conventions are:
        * "sc" - for Setyawan and Curtarolo standardization.

        By default the lattice is not standardized.

        .. versionadded:: 0.3.1

    Returns
    -------
    cell : (3, 3) :numpy:`ndarray`
        Rows are lattice vectors.
    """

    correct_inputs = set(map(lambda x: x.lower(), BRAVAIS_LATTICE_VARIATIONS)).union(
        set(
            map(
                lambda x: x.translate(str.maketrans("", "", "12345ab")).lower(),
                BRAVAIS_LATTICE_VARIATIONS,
            )
        )
    )

    if (
        not isinstance(lattice_variation, str)
        or lattice_variation.lower() not in correct_inputs
    ):
        message = f"There is no {lattice_variation} Bravais lattice. Available examples are:\n"
        for name in BRAVAIS_LATTICE_VARIATIONS:
            message += f"  * {name}\n"
        raise ValueError(message)

    lattice_variation = lattice_variation.lower()

    if lattice_variation == "cub":
        cell = CUB(pi)
    elif lattice_variation == "fcc":
        cell = FCC(pi)
    elif lattice_variation == "bcc":
        cell = BCC(pi)
    elif lattice_variation == "tet":
        cell = TET(pi, 1.5 * pi)
    elif lattice_variation in ["bct1", "bct"]:
        cell = BCT(1.5 * pi, pi)
    elif lattice_variation == "bct2":
        cell = BCT(pi, 1.5 * pi)
    elif lattice_variation == "orc":
        cell = ORC(pi, 1.5 * pi, 2 * pi)
    elif lattice_variation in ["orcf1", "orcf"]:
        cell = ORCF(0.7 * pi, 5 / 4 * pi, 5 / 3 * pi)
    elif lattice_variation == "orcf2":
        cell = ORCF(1.2 * pi, 5 / 4 * pi, 5 / 3 * pi)
    elif lattice_variation == "orcf3":
        cell = ORCF(pi, 5 / 4 * pi, 5 / 3 * pi)
    elif lattice_variation == "orci":
        return ORCI(pi, 1.3 * pi, 1.7 * pi)
    elif lattice_variation == "orcc":
        cell = ORCC(pi, 1.3 * pi, 1.7 * pi)
    elif lattice_variation == "hex":
        cell = HEX(pi, 2 * pi)
    elif lattice_variation in ["rhl1", "rhl"]:
        # If alpha = 60 it is effectively FCC!
        cell = RHL(pi, 70)
    elif lattice_variation == "rhl2":
        cell = RHL(pi, 110)
    elif lattice_variation == "mcl":
        cell = MCL(pi, 1.3 * pi, 1.6 * pi, alpha=75)
    elif lattice_variation in ["mclc1", "mclc"]:
        cell = MCLC(pi, 1.4 * pi, 1.7 * pi, 80)
    elif lattice_variation == "mclc2":
        cell = MCLC(1.4 * pi * sin(75 * TORADIANS), 1.4 * pi, 1.7 * pi, 75)
    elif lattice_variation == "mclc3":
        b = pi
        x = 1.1
        alpha = 78
        ralpha = alpha * TORADIANS
        c = b * (x**2) / (x**2 - 1) * cos(ralpha) * 1.8
        a = x * b * sin(ralpha)
        cell = MCLC(a, b, c, alpha)
    elif lattice_variation == "mclc4":
        b = pi
        x = 1.2
        alpha = 65
        ralpha = alpha * TORADIANS
        c = b * (x**2) / (x**2 - 1) * cos(ralpha)
        a = x * b * sin(ralpha)
        cell = MCLC(a, b, c, alpha)
    elif lattice_variation == "mclc5":
        b = pi
        x = 1.4
        alpha = 53
        ralpha = alpha * TORADIANS
        c = b * (x**2) / (x**2 - 1) * cos(ralpha) * 0.9
        a = x * b * sin(ralpha)
        cell = MCLC(a, b, c, alpha)
    elif lattice_variation in ["tri1a", "tri1", "tri", "tria"]:
        cell = TRI(1, 1.5, 2, 120, 110, 100, input_reciprocal=True)
    elif lattice_variation in ["tri2a", "tri2"]:
        cell = TRI(1, 1.5, 2, 120, 110, 90, input_reciprocal=True)
    elif lattice_variation in ["tri1b", "trib"]:
        cell = TRI(1, 1.5, 2, 60, 70, 80, input_reciprocal=True)
    elif lattice_variation == "tri2b":
        cell = TRI(1, 1.5, 2, 60, 70, 90, input_reciprocal=True)

    return cell


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
