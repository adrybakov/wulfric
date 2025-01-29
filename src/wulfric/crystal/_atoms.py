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

from wulfric.constants._atoms import ATOM_TYPES

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def get_atom_type(name: str) -> str:
    r"""
    Attempts to identify atom's type based on its name (i.e. Cr1 -> Cr, ...).

    If no type is identified, then return "X".

    Parameters
    ----------
    name : str
        Name of the atom.

    Returns
    -------
    type : str
        Type of the atom.

    Examples
    --------

    .. doctest::

        >>> from wulfric.crystal import get_atom_type
        >>> get_atom_type("@%^#$")
        'X'
        >>> deduc_atom_type("Cr")
        'Cr'
        >>> deduc_atom_type("Cr1")
        'Cr'
        >>> deduc_atom_type("_3341Cr")
        'Cr'
        >>> deduc_atom_type("cr")
        'Cr'
        >>> deduc_atom_type("S")
        'S'
        >>> deduc_atom_type("Se")
        'Se'
        >>> deduc_atom_type("Sp")
        'S'
        >>> deduc_atom_type("123a")
        'X'
        >>> deduc_atom_type("CrSBr")
        'Cr'

    Notes
    -----
    If ``name`` contains several possible atom types of length 2
    as substrings, then the type is equal to the first one found.
    """

    atom_type = "X"
    for trial_type in ATOM_TYPES:
        if trial_type.lower() in name.lower():
            atom_type = trial_type
            # Maximum amount of characters in the atom type
            # Some 1-character types are parts of some 2-character types (i.e. "Se" and "S")
            # If type of two characters is found then it is unique,
            # If type of one character is found, then the search must continue
            if len(atom_type) == 2:
                break
    return atom_type


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
