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
from wulfric.crystal._crystal_validation import validate_atoms

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
        Dictionary with N atoms. Expected keys:

        *   "names" : (N, ) list of str
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

        >>> import wulfric
        >>> atoms = {"names": ["Cr1", "cr2", "Br3", "S4", "fe5", "Fe6"]}
        >>> atoms
        {'names': ['Cr1', 'cr2', 'Br3', 'S4', 'fe5', 'Fe6']}
        >>> wulfric.crystal.populate_atom_species(atoms)
        >>> atoms
        {'names': ['Cr1', 'cr2', 'Br3', 'S4', 'fe5', 'Fe6'], 'species': ['Cr', 'Cr', 'Br', 'S', 'Fe', 'Fe']}

    """

    atoms["species"] = []

    for i in range(len(atoms["names"])):
        atoms["species"].append(
            get_atom_species(atoms["names"][i], raise_on_fail=raise_on_fail)
        )


def get_spglib_types(atoms):
    r"""
    Construct spglib_types for the given atoms.

    First satisfied rule is applied

    1.  "spglib_types" in atoms

        Return ``atoms["spglib_types"]``.

    2.  "species" in atoms.

        ``spglib_types`` are deduced from ``atoms["species"]``. If two atoms have the same
        species, then they will have the same integer assigned to them in
        ``spglib_types``.

    3.  "names" in ``atoms``

        Species are automatically deduced based on atom's names (via
        :py:func:`wulfric.crystal.get_atom_species`), and then the second rule is
        applied.

    Parameters
    ==========
    atoms : dict
        Dictionary with N atoms. At least one of the following keys is expected

        *   "names" : (N, ) list of str, optional
            See Notes
        *   "species" : (N, ) list of str, optional
            See Notes
        *   "spglib_types" : (N, ) list of int, optional

    Returns
    =======
    spglib_types : (N, ) list of int
        List of integer indices ready to be passed to |spglib|_.
    """

    validate_atoms(atoms=atoms, raise_errors=True)

    if "spglib_types" in atoms:
        spglib_types = atoms["spglib_types"]
    else:
        if "species" not in atoms and "names" in atoms:
            species = [
                get_atom_species(name=name, raise_on_fail=False)
                for name in atoms["names"]
            ]
        elif "species" in atoms:
            species = atoms["species"]
        else:
            raise ValueError(
                'Expected at least one of "spglib_types", "species" or "names" keys in ""atoms, found none.'
            )

        mapping = {
            name: index + 1 for index, name in enumerate(sorted(list(set(species))))
        }
        spglib_types = [mapping[name] for name in species]

    return spglib_types


def ensure_unique_names(atoms, strategy: str = "all") -> None:
    r"""
    Ensures that atoms have unique ``"names"``.

    If atom names are already unique, then this function does nothing.

    .. versionadded:: 0.5.1

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
          each repeated grooup. (See examples)

        Case-insensitive.

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
        >>> wulfric.crystal.ensure_unique_names(atoms)
        >>> atoms
        {'names': ['Cr11', 'Cr22', 'Br3', 'Br4', 'S5', 'S6']}
        >>> atoms = {"names": ["Cr1", "Cr2", "Br", "Br", "S", "S"]}
        >>> wulfric.crystal.ensure_unique_names(atoms, strategy="repeated-only")
        >>> atoms
        {'names': ['Cr1', 'Cr2', 'Br1', 'Br2', 'S1', 'S2']}
        >>> # Nothing happens if atom names are already unique
        >>> wulfric.crystal.ensure_unique_names(atoms)
        >>> atoms
        {'names': ['Cr1', 'Cr2', 'Br1', 'Br2', 'S1', 'S2']}
        >>> wulfric.crystal.ensure_unique_names(atoms, strategy="repeated-only")
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
