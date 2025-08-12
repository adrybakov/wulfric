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
import numpy as np
from wulfric._exceptions import _raise_with_message
from wulfric.constants._atoms import ATOM_SPECIES

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def validate_atoms(atoms, required_keys=None, raise_errors=True):
    r"""
    Validate keys and values of the atoms dictionary.

    Checks that all values in the atom's dictionary have the same amount of elements.
    Checks that atoms have required keys with expected shape of their values.

    If one of the following keys is in ``atoms``, then an extra check is performed on its
    value

    *   "names"

        Checks that the value is a list of N ``str``.

    *   "species"

        Checks that the value is a list of N ``str``.

        Checks that each element is a valid species of an atom (i.e. Cr, H, Br, Fe, ...) or "X".
        Note that "CR" is not a valid species, but "Cr" is.

    *   "positions"

        Checks that the ``atoms["positions"]`` has the shape (N, 3)

    For all other keys the only check on their values is that they all have the same length.

    Parameters
    ==========
    atoms : dict
        Dictionary of atoms.
    required_keys : list of str, optional
        List of required keys.
    raise_errors : bool, default True
        If ``False``, then no errors are raised.


    Returns
    =======
    check_passed : bool
        ``True`` if all checks passed. ``False`` otherwise.

    Raises
    ======
    TypeError
        If ``atoms[key]`` is not iterable for any ``key`` and ``raise_errors=False``.
    ValueError
        If any check is not passed and ``raise_errors=False``.
    """

    if required_keys is None:
        required_keys = []

    # Check that for every key value has N elements
    lengths = []
    for key in atoms:
        try:
            lengths.append(len(atoms[key]))
        except TypeError as e:
            if raise_errors:
                _raise_with_message(
                    e,
                    f'Failed to count elements of atoms["{key}"]. Are you sure that it is an iterable?\n'
                    + f'  atoms["{key}"] -> {atoms[key]}',
                )
            else:
                return False

    # Allow for an empty atoms dictionary
    if len(set(lengths)) not in [0, 1]:
        if raise_errors:
            raise ValueError(
                "Inconsistent amount of atoms:\n  * "
                + "\n  * ".join(
                    [
                        f'len(atoms["{key}"]) -> {N}'
                        for key, N in list(zip(list(atoms), lengths))
                    ]
                )
            )
        else:
            return False

    # Check that all required keys are present in atoms.
    for key in required_keys:
        if key not in atoms:
            if raise_errors:
                raise ValueError(
                    f'Expected to have the key "{key}" in atoms. Did not find one. Keys found in atoms:\n  * '
                    + "\n  * ".join(list(atoms))
                )
            else:
                return False

    # At this moment it is guaranteed that len(atoms[key]) is the same for all keys

    # Check values of positions
    if "positions" in atoms:
        try:
            shape = np.array(atoms["positions"]).shape
        except ValueError as e:
            if raise_errors:
                _raise_with_message(
                    e,
                    'atoms["positions"] is not array-like\n'
                    + f'  atoms["positions"] -> {atoms["positions"]}',
                )
            else:
                return False

        if len(shape) != 2 or shape[1] != 3:
            if raise_errors:
                raise ValueError(
                    f'Expected atoms["positions"] to have the shape (N, 3), got {shape}.\n'
                    + f'  atoms["positions"] -> {atoms["positions"]}'
                )
            else:
                return False

    # Check values of names
    if "names" in atoms:
        for index, element in enumerate(atoms["names"]):
            if not isinstance(element, str):
                if raise_errors:
                    raise ValueError(
                        f'Element #{index} of atoms["names"] is not a string:\n  '
                        f'atoms["names"][{index}] -> {element}'
                    )
                else:
                    return False

    # Check values of species
    if "species" in atoms:
        for index, element in enumerate(atoms["species"]):
            if not isinstance(element, str):
                if raise_errors:
                    raise ValueError(
                        f'Element #{index} of atoms["species"] is not a string:\n  '
                        f'atoms["species"][{index}] -> {element}'
                    )
                else:
                    return False

            if element != "X" and element not in ATOM_SPECIES:
                if raise_errors:
                    raise ValueError(
                        f'Element #{index} of atoms["species"] is not a valid species nor "X":\n  '
                        f'atoms["species"][{index}] -> {element}'
                    )
                else:
                    return False

    return True


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
