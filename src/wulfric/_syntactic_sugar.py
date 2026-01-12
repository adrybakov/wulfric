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
R"""Syntactic sugar"""

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


class SyntacticSugar(dict):
    r"""
    Syntactic sugar for any dictionary.

    This class does only one thing. It allows to write
    ``atoms.names`` instead of ``atoms["names"]`` or
    ``spglib_data.number`` instead of ``spglib_data["number"]``.

    Examples
    --------

    Two code examples below give equivalent result

    .. doctest::

        >>> import wulfric
        >>> atoms = wulfric.SyntacticSugar()
        >>> atoms.names = ["Cr1", "Cr2"]
        >>> atoms.positions = [[0, 0, 0], [0.5, 0.5, 0.5]]
        >>> atoms
        {'names': ['Cr1', 'Cr2'], 'positions': [[0, 0, 0], [0.5, 0.5, 0.5]]}

    .. doctest::

        >>> import wulfric
        >>> atoms = {}
        >>> atoms["names"] = ["Cr1", "Cr2"]
        >>> atoms["positions"] = [[0, 0, 0], [0.5, 0.5, 0.5]]
        >>> atoms
        {'names': ['Cr1', 'Cr2'], 'positions': [[0, 0, 0], [0.5, 0.5, 0.5]]}
    """

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def add_sugar(dictionary: dict) -> SyntacticSugar:
    r"""
    Takes any dictionary and add attribute-like access to the key-values.

    Parameters
    ----------
    dictionary : dict
        Dictionary for the addition of the syntax sugar.

    Returns
    -------
    candy : :py:class:`.SyntacticSugar`
        Same dictionary with the easy access to the key-value pairs.

    Raises
    ------
    ValueError
        If ``not isinstance(dictionary, dict)``.

    See Also
    ========
    remove_sugar
    SyntacticSugar

    Examples
    --------

    .. doctest::

        >>> import wulfric
        >>> atoms = {"names": ["Cr1", "Cr2"]}
        >>> atoms.names
        Traceback (most recent call last):
        ...
        AttributeError: 'dict' object has no attribute 'names'
        >>> atoms = wulfric.add_sugar(atoms)
        >>> atoms.names
        ['Cr1', 'Cr2']
        >>> atoms.positions = [[0, 0, 0], [0.5, 0.5, 0.5]]
        >>> atoms.positions
        [[0, 0, 0], [0.5, 0.5, 0.5]]
        >>> # Note that it still behaves as a dictionary
        >>> atoms["positions"] = [[0.5, 0.5, 0.5], [0, 0, 0]]
        >>> atoms.positions
        [[0.5, 0.5, 0.5], [0, 0, 0]]
        >>> atoms["positions"]
        [[0.5, 0.5, 0.5], [0, 0, 0]]
        >>> atoms
        {'names': ['Cr1', 'Cr2'], 'positions': [[0.5, 0.5, 0.5], [0, 0, 0]]}

    """

    if not isinstance(dictionary, dict):
        raise ValueError(
            f"Failed to add sugar: Dictionary should be an instance of python dict, got {type(dictionary)}."
        )

    candy = SyntacticSugar()

    for key in dictionary:
        candy[key] = dictionary[key]

    return candy


def remove_sugar(candy: dict) -> dict:
    r"""
    Takes any dictionary and remove attribute-like access to the key-values to it.

    Parameters
    ----------
    candy : :py:class:`.SyntacticSugar`
        An object for the removal of the syntax sugar.

    Returns
    -------
    dictionary : dict
        Same dictionary without the easy access to the key-value pairs.

    Raises
    ------
    ValueError
        If ``not isinstance(candy, dict)``.

    See Also
    ========
    add_sugar
    SyntacticSugar

    Examples
    --------

    .. doctest::

        >>> import wulfric
        >>> atoms = {"names": ["Cr1", "Cr2"]}
        >>> atoms = wulfric.add_sugar(atoms)
        >>> atoms.names
        ['Cr1', 'Cr2']
        >>> atoms.positions = [[0, 0, 0], [0.5, 0.5, 0.5]]
        >>> atoms = wulfric.remove_sugar(atoms)
        >>> atoms.names
        Traceback (most recent call last):
        ...
        AttributeError: 'dict' object has no attribute 'names'
        >>> atoms
        {'names': ['Cr1', 'Cr2'], 'positions': [[0, 0, 0], [0.5, 0.5, 0.5]]}

    """

    if not isinstance(candy, dict):
        raise ValueError(
            f"Failed to remove sugar: candy should be an instance of python dict, got {type(candy)}."
        )

    dictionary = {}

    for key in candy:
        dictionary[key] = candy[key]

    return dictionary


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
