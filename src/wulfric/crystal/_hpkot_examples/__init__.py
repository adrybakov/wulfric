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
import os
from wulfric.io._vasp import load_poscar
from wulfric.constants._hpkot_convention import HPKOT_EXTENDED_BL_SYMBOLS

__all__ = ["hpkot_get_example"]


def hpkot_get_example(extended_bl_symbol, with_inversion=False):
    r"""
    Returns an example of the crystal structure for each of the
    given extended Bravais lattice symbol as defined in [1]_.

    .. versionadded:: 0.6.3

    Crystal structures are taken from the |seekpath|_ repository
    with the permission of its authors.

    See :ref:`api_constants_HPKOT_EXTENDED_BL_SYMBOLS` for the full list of supported
    symbols.

    .. warning::
        "oF2", "oI2", "oA1", "oA2" with ``with_inversion=True`` are not supported fo now.


    Parameters
    ----------
    extended_bl_symbol : str
        Extended Bravais lattice symbol. Case-sensitive.
    with_inversion : bool, default False
        Whether give an example that has inversion symmetry.

    Returns
    -------
    cell : (3, 3) :numpy:`ndarray`
        Unit cell of the crystal structure.
    atoms : dict
        Atoms of the crystal structure.

    Raises
    ------
    ValueError
        If ``extended_bl_symbol`` is not supported.


    References
    ----------
    .. [1] Hinuma, Y., Pizzi, G., Kumagai, Y., Oba, F. and Tanaka, I., 2017.
           Band structure diagram paths based on crystallography.
           Computational Materials Science, 128, pp.140-184.
    """

    if extended_bl_symbol in ["oF2", "oI2", "oA1", "oA2"] and with_inversion:
        raise ValueError(
            '"oF2", "oI2", "oA1", "oA2" with with_inversion=True currently are not supported.'
        )

    supported_symbols = list(HPKOT_EXTENDED_BL_SYMBOLS)

    supported_symbols += list(set([_[:2] for _ in supported_symbols]))

    if extended_bl_symbol not in supported_symbols:
        raise ValueError(
            f'Extended Bravais lattice symbol "{extended_bl_symbol}" is not supported. Supported are:\n  * '
            + "\n  * ".join(supported_symbols)
        )

    if len(extended_bl_symbol) == 2:
        if extended_bl_symbol == "aP":
            extended_bl_symbol = "aP2"
        else:
            extended_bl_symbol += "1"

    POSCAR_filename = os.path.join(
        os.path.split(os.path.abspath(__file__))[0], "POSCAR-files", extended_bl_symbol
    )

    if with_inversion:
        POSCAR_filename = os.path.join(POSCAR_filename, "POSCAR_inversion")
    else:
        POSCAR_filename = os.path.join(POSCAR_filename, "POSCAR_noinversion")

    cell, atoms, _ = load_poscar(file_object=POSCAR_filename)

    return cell, atoms
