# ================================== LICENSE ===================================
# Wulfric - Cell, Atoms, K-path, visualization.
# Copyright (C) 2023-2026 Andrey Rybakov
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
from wulfric.crystal._crystal_validation import validate_atoms

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def get_atom_species(name: str, raise_on_fail=False) -> str:
    r"""
    Attempts to identify atom's species based on its name (i.e. Cr1 -> Cr, ...).

    If no species is identified, then return "X".

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

    See Also
    --------
    get_atoms_species


    Notes
    -----
    If ``name`` contains several possible atom species of length 2
    as substrings, then the species is equal to the first one found.

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

    """

    atom_species = "X"
    for trial_species in ATOM_SPECIES:
        if trial_species.lower() in name.lower():
            atom_species = trial_species
            # Maximum amount of characters in the atom species
            # Some 1-character species are parts of some 2-character species (i.e. "Se" and "S")
            # If species of two characters is found then it is unique,
            # If species of one character is found, then the search must continue
            if len(atom_species) == 2:
                break

    if atom_species == "X":
        if raise_on_fail:
            raise FailedToDeduceAtomSpecies(name=name)
        else:
            import warnings

            warnings.warn(
                f"Atom species deduction failed for '{name}'. Set species to 'X'",
                RuntimeWarning,
            )

    return atom_species


def get_atoms_species(atoms, raise_on_fail=False) -> str:
    r"""
    Attempts to identify atoms species based on their names (i.e. Cr1 -> Cr, ...).

    If no species is identified, then return "X".

    Parameters
    ----------
    atoms : dict
        Dictionary with N atoms. Expected keys:

        *   "names" : (N, ) list of str
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

    See Also
    --------
    get_atom_species

    Notes
    -----
    If ``atoms["names"][i]`` contains several possible atom species of length 2
    as substrings, then the species is equal to the first one found.

    Examples
    --------

    .. doctest::

        >>> import wulfric
        >>> atoms = dict(names=["Fe1", "Fe2", "Cr", "Br3"])
        >>> wulfric.crystal.get_atoms_species(atoms)
        ['Fe', 'Fe', 'Cr', 'Br']
        >>> atoms = {"names": ["Cr1", "cr2", "Br3", "S4", "fe5", "Fe6"]}
        >>> wulfric.crystal.get_atoms_species(atoms)
        ['Cr', 'Cr', 'Br', 'S', 'Fe', 'Fe']

    """

    validate_atoms(atoms=atoms, required_keys=["names"], raise_errors=True)

    return [
        get_atom_species(name=name, raise_on_fail=raise_on_fail)
        for name in atoms["names"]
    ]


def get_unique_names(atoms, strategy: str = "all") -> list:
    r"""
    Ensures that atoms have unique ``"names"``.

    If atom names are already unique, then returns ``atoms["names"]``.

    Parameters
    ----------
    atoms : dict
        Dictionary with N atoms. Expected keys:

        *   "names" : (N, ) list of str

    strategy : str, default "all"
        Strategy for the modification of atom names. Supported strategies are

        * "all"

          Add an index to the end of every atom, starting from 1.
        * "repeated-only"

          Add an index only to the repeated names, index starts with 1, independently for
          each repeated group. (See examples)

        Case-insensitive.

    Returns
    -------
    unique_names : list of str
        Unique names of atoms.

    Raises
    ------
    ValueError
        If ``strategy`` is not supported.

    Examples
    --------

    .. doctest::

        >>> import wulfric
        >>> atoms = {"names": ["Cr1", "Cr2", "Br", "Br", "S", "S"]}
        >>> # Default strategy is "all"
        >>> wulfric.crystal.get_unique_names(atoms)
        ['Cr11', 'Cr22', 'Br3', 'Br4', 'S5', 'S6']
        >>> atoms = {"names": ["Cr1", "Cr2", "Br", "Br", "S", "S"]}
        >>> wulfric.crystal.get_unique_names(atoms, strategy="repeated-only")
        ['Cr1', 'Cr2', 'Br1', 'Br2', 'S1', 'S2']
        >>> # Nothing happens if atom names are already unique
        >>> wulfric.crystal.get_unique_names(atoms)
        ['Cr1', 'Cr2', 'Br1', 'Br2', 'S1', 'S2']
        >>> wulfric.crystal.get_unique_names(atoms, strategy="repeated-only")
        ['Cr1', 'Cr2', 'Br1', 'Br2', 'S1', 'S2']

    """

    validate_atoms(atoms=atoms, required_keys=["names"], raise_errors=True)

    SUPPORTED_STRATEGIES = ["all", "repeated-only"]
    strategy = strategy.lower()

    if strategy not in SUPPORTED_STRATEGIES:
        raise ValueError(
            f"{strategy} strategy is not supported. Supported are:\n"
            + ("\n").join([f"  * {i}" for i in SUPPORTED_STRATEGIES])
        )

    unique_names = atoms["names"]

    names_are_not_unique = not len(unique_names) == len(set(unique_names))

    if names_are_not_unique and strategy == "all":
        unique_names = [f"{name}{i + 1}" for i, name in enumerate(atoms["names"])]

    if names_are_not_unique and strategy == "repeated-only":
        counter = {}
        for name in unique_names:
            if name not in counter:
                counter[name] = [1, 1]
            else:
                counter[name][1] += 1

        for i in range(len(unique_names)):
            name = unique_names[i]
            total = counter[name][1]
            if total > 1:
                unique_names[i] += str(counter[name][0])
                counter[name][0] += 1

    return unique_names


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
