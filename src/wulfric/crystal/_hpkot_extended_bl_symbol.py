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
from math import cos, sin, sqrt

import numpy as np

from wulfric.cell._basic_manipulation import get_params, get_reciprocal
from wulfric.crystal._crystal_validation import validate_atoms
from wulfric._spglib_interface import get_spglib_data, validate_spglib_data
from wulfric._syntactic_sugar import SyntacticSugar
from wulfric.crystal._conventional import get_conventional
from wulfric._exceptions import PotentialBugError
from wulfric.constants import TORADIANS

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def hpkot_get_extended_bl_symbol(cell, atoms, spglib_data=None):
    r"""
    Returns extended bravais lattice symbol as defined in the paper by Hinuma, Pizzi,
    Kumagai, Oba, and Tanaka [1]_.

    .. versionadded:: 0.6.3

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

    Returns
    -------
    extended_bl_type : str
        Extended Bravais lattice symbol.

    Notes
    -----
    |spglib|_ uses ``types`` to distinguish the atoms. To see how wulfric deduces the
    ``types`` for given atoms see :py:func:`wulfric.get_spglib_types`.

    References
    ----------
    .. [1] Hinuma, Y., Pizzi, G., Kumagai, Y., Oba, F. and Tanaka, I., 2017.
           Band structure diagram paths based on crystallography.
           Computational Materials Science, 128, pp.140-184.

    Examples
    --------

    .. doctest::

        >>> import wulfric
        >>> wulfric.crystal.hpkot_get_extended_bl_symbol(
        ...     cell=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
        ...     atoms=dict(positions=[[0, 0, 0]], spglib_types=[1]),
        ... )
        'cP2'

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

    # Lattice types that do not require computation of lattice parameters
    if lattice_type in ["cI", "tP", "oP", "mP"]:
        return f"{lattice_type}1"

    if lattice_type == "cP":
        if 195 <= spglib_data.space_group_number <= 206:
            return "cP1"
        elif 207 <= spglib_data.space_group_number <= 230:
            return "cP2"
        else:
            raise PotentialBugError(
                error_summary=f'(convention="HPKOT"), lattice type cP, space group {spglib_data.space_group_number}. Failed to define extended Bravais lattice symbol.'
            )

    if lattice_type == "cF":
        if 195 <= spglib_data.space_group_number <= 206:
            return "cF1"
        elif 207 <= spglib_data.space_group_number <= 230:
            return "cF2"
        else:
            raise PotentialBugError(
                error_summary=f'(convention="HPKOT"), lattice type cF, space group {spglib_data.space_group_number}. Failed to define extended Bravais lattice symbol.'
            )

    if lattice_type == "hP":
        if (
            143 <= spglib_data.space_group_number <= 149
            or 159 <= spglib_data.space_group_number <= 163
            or spglib_data.space_group_number in [151, 153, 157]
        ):
            return "hP1"
        else:
            return "hP2"

    # Lattice types that require computation of lattice parameters
    conventional_cell, _ = get_conventional(
        cell=cell, atoms=atoms, convention="HPKOT", spglib_data=spglib_data
    )
    a, b, c, _, beta, _ = get_params(cell=conventional_cell)

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
        if b <= a * sin(beta * TORADIANS):
            return "mC1"
        else:
            if (
                -a * cos(beta * TORADIANS) / c + ((a * sin(beta * TORADIANS)) / b) ** 2
                <= 1
            ):
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
        f'(convention="HPKOT"), lattice type {lattice_type}, space group {spglib_data.space_group_number}.. Failed to identify lattice type (not one of supported).'
    )


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
