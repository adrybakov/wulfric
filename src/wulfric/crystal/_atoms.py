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


from wulfric._exceptions import FailedToDeduceAtomSpecies
from wulfric.constants._atoms import ATOM_SPECIES

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def get_atom_species(name: str, raise_on_fail=False) -> str:
    r"""
    Attempts to identify atom's type based on its name (i.e. Cr1 -> Cr, ...).

    If no type is identified, then return "X".

    Parameters
    ----------
    name : str
        Name of the atom.
    raise_on_fail : bool, default False
        Whether to raise an exception if automatic species deduction fails.

    Returns
    -------
    species : str
        Species of the atom.

    Raises
    ------
    FailedToDeduceAtomSpecies
        If ``raise_on_fail = True`` and automatic species deduction fails.

    Warnings
    --------
    If ``raise_on_fail = True`` and automatic species deduction fails, then
    ``RuntimeWarning`` is issued, and atom species is set to "X".

    Examples
    --------

    .. doctest::

        >>> from wulfric.crystal import get_atom_species
        >>> get_atom_species("@%^#$")
        'X'
        >>> get_atom_species("Cr")
        'Cr'
        >>> get_atom_species("Cr1")
        'Cr'
        >>> get_atom_species("_3341Cr")
        'Cr'
        >>> get_atom_species("cr")
        'Cr'
        >>> get_atom_species("S")
        'S'
        >>> get_atom_species("Se")
        'Se'
        >>> get_atom_species("Sp")
        'S'
        >>> get_atom_species("123a")
        'X'
        >>> get_atom_species("CrSBr")
        'Cr'

    Notes
    -----
    If ``name`` contains several possible atom types of length 2
    as substrings, then the type is equal to the first one found.
    """

    atom_type = "X"
    for trial_type in ATOM_SPECIES:
        if trial_type.lower() in name.lower():
            atom_type = trial_type
            # Maximum amount of characters in the atom type
            # Some 1-character types are parts of some 2-character types (i.e. "Se" and "S")
            # If type of two characters is found then it is unique,
            # If type of one character is found, then the search must continue
            if len(atom_type) == 2:
                break

    if atom_type == "X":
        if raise_on_fail:
            raise FailedToDeduceAtomSpecies(name=name)
        else:
            import warnings

            warnings.warn(
                f"Atom species deduction failed for '{name}'. Set species to 'X'",
                RuntimeWarning,
            )

    return atom_type


def populate_atom_species(atoms, raise_on_fail=False) -> None:
    r"""
    Populate atom species, based on their names.
    If atom species are already present in the ``atoms``, then they will be overwritten.

    Parameters
    ----------
    atoms : dict
        Dictionary with atoms. Must have a ``names`` with the value of ``list`` of N
        ``str``.
    raise_on_fail : bool, default False
        Whether to raise an error if the atom type can not be deduced based on its name.

    Raises
    ------
    FailedToDeduceAtomSpecies
        If ``raise_on_fail = True`` and automatic species deduction fails.

    Warnings
    --------
    If ``raise_on_fail = True`` and automatic species deduction fails, then
    ``RuntimeWarning`` is issued, and atom species is set to "X".

    Examples
    --------

    .. doctest::

        >>> import wulfric as wulf
        >>> atoms = {"names" : ["Cr1", "cr2", "Br3", "S4", "fe5", "Fe6"]}
        >>> atoms
        {'names': ['Cr1', 'cr2', 'Br3', 'S4', 'fe5', 'Fe6']}
        >>> wulf.crystal.populate_atom_species(atoms)
        >>> atoms
        {'names': ['Cr1', 'cr2', 'Br3', 'S4', 'fe5', 'Fe6'], 'species': ['Cr', 'Cr', 'Br', 'S', 'Fe', 'Fe']}

    """

    atoms["species"] = []

    for i in range(len(atoms["names"])):
        atoms["species"].append(
            get_atom_species(atoms["names"][i], raise_on_fail=raise_on_fail)
        )


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
