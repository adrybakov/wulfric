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
        >>> atoms = {"names": ["Cr1", "cr2", "Br3", "S4", "fe5", "Fe6"]}
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


def ensure_unique_names(atoms, strategy: str = "all") -> None:
    r"""
    Ensures that atoms have unique ``"names"``.

    If atom names are already unique, then this function does nothing.

    .. versionadded:: 0.5.1

    Parameters
    ----------
    atoms : dict
        Dictionary with atoms. Must have a ``"names"`` keyword with the value of
        ``list`` of N ``str``.
    strategy : str, default "all"
        Strategy for the modification of atom names. Supported strategies are

        * "all"

          Add an index to the end of every atom, starting from 1.
        * "repeated-only"

          Add an index only to the repeated names, index starts with 1, independently for
          each repeated grooup. (See examples)

        Case-insensitive.

    Raises
    ------
    ValueError
        If ``strategy`` is not supported.

    Examples
    --------

    .. doctest::

        >>> import wulfric as wulf
        >>> atoms = {"names": ["Cr1", "Cr2", "Br", "Br", "S", "S"]}
        >>> # Default strategy is "all"
        >>> wulf.crystal.ensure_unique_names(atoms)
        >>> atoms
        {'names': ['Cr11', 'Cr22', 'Br3', 'Br4', 'S5', 'S6']}
        >>> atoms = {"names": ["Cr1", "Cr2", "Br", "Br", "S", "S"]}
        >>> wulf.crystal.ensure_unique_names(atoms, strategy="repeated-only")
        >>> atoms
        {'names': ['Cr1', 'Cr2', 'Br1', 'Br2', 'S1', 'S2']}
        >>> # Nothing happens if atom names are already unique
        >>> wulf.crystal.ensure_unique_names(atoms)
        >>> atoms
        {'names': ['Cr1', 'Cr2', 'Br1', 'Br2', 'S1', 'S2']}
        >>> wulf.crystal.ensure_unique_names(atoms, strategy="repeated-only")
        >>> atoms
        {'names': ['Cr1', 'Cr2', 'Br1', 'Br2', 'S1', 'S2']}

    """

    SUPPORTED_STRATEGIES = ["all", "repeated-only"]
    strategy = strategy.lower()

    if strategy not in SUPPORTED_STRATEGIES:
        raise ValueError(
            f"{strategy} strategy is not supported. Supported are:\n"
            + ("\n").join([f"  * {i}" for i in SUPPORTED_STRATEGIES])
        )

    names_unique = len(atoms["names"]) == len(set(atoms["names"]))

    if not names_unique and strategy == "all":
        for i in range(len(atoms["names"])):
            atoms["names"][i] += f"{i + 1}"

    if not names_unique and strategy == "repeated-only":
        counter = {}
        for name in atoms["names"]:
            if name not in counter:
                counter[name] = [1, 1]
            else:
                counter[name][1] += 1

        for i in range(len(atoms["names"])):
            name = atoms["names"][i]
            total = counter[name][1]
            if total > 1:
                atoms["names"][i] += str(counter[name][0])
                counter[name][0] += 1


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
