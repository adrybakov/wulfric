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
R"""Syntax sugar"""

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


class _SyntacticSugar(dict):
    r"""
    Syntactic sugar for any dictionary.

    This class does only one thing. It allows to write
    ``atoms.names`` instead of ``atoms["names"]``.

    Examples
    --------

    Two code examples below give equivalent result

    .. doctest::

        >>> import wulfric as wulf
        >>> atoms = wulf.Atoms()
        >>> atoms.names = ["Cr1", "Cr2"]
        >>> atoms.positions = [[0, 0, 0], [0.5, 0.5, 0.5]]
        {'names': ['Cr1', 'Cr2'], 'positions': [[0, 0, 0], [0.5, 0.5, 0.5]]}

    .. doctest::

        >>> import wulfric as wulf
        >>> atoms = {}
        >>> atoms["names"] = ["Cr1", "Cr2"]
        >>> atoms["positions"] = [[0, 0, 0], [0.5, 0.5, 0.5]]
        {'names': ['Cr1', 'Cr2'], 'positions': [[0, 0, 0], [0.5, 0.5, 0.5]]}

    ``Atom`` class behaves as dictionary

    .. doctest::

        >>> import wulfric as wulf
        >>> atoms = wulf.Atoms()
        >>> atoms.names = ["Cr1", "Cr2"]
        >>> atoms.positions = [[0, 0, 0], [0.5, 0.5, 0.5]]
        {'names': ['Cr1', 'Cr2'], 'positions': [[0, 0, 0], [0.5, 0.5, 0.5]]}

    """

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def add_sugar(dictionary: dict) -> _SyntacticSugar:
    r"""
    Takes any dictionary and add attribute-like access to the key-values to it.

    Parameters
    ----------
    dictionary : dict
        Dictionary for the addition of the syntax sugar.

    Returns
    -------
    candy : :py:class:`._SyntacticSugar`
        Same dictionary with the easy access to the key-value pairs.

    Raises
    ------
    ValueError
        If ``not isinstance(dictionary, dict)``.

    Examples
    --------

    .. doctest::

        >>> import wulfric as wulf
        >>> atoms = {"names": ["Cr1", "Cr2"]}
        >>> atoms.names
        Traceback (most recent call last):
        ...
        AttributeError: 'dict' object has no attribute 'names'
        >>> atoms = wulf.add_sugar(atoms)
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
            f"dictionary should be an instance of python dict, got {type(dictionary)}."
        )

    candy = _SyntacticSugar()

    for key in dictionary:
        candy[key] = dictionary[key]

    return candy


def remove_sugar(candy: dict) -> dict:
    r"""
    Takes any dictionary and remove attribute-like access to the key-values to it.

    Parameters
    ----------
    candy : dict
        Dictionary for the addition of the syntax sugar.

    Returns
    -------
    dictionary : dict
        Same dictionary without the easy access to the key-value pairs.

    Raises
    ------
    ValueError
        If ``not isinstance(candy, dict)``.

    Examples
    --------

    .. doctest::

        >>> import wulfric as wulf
        >>> atoms = {"names": ["Cr1", "Cr2"]}
        >>> atoms = wulf.add_sugar(atoms)
        >>> atoms.names
        ['Cr1', 'Cr2']
        >>> atoms.positions = [[0, 0, 0], [0.5, 0.5, 0.5]]
        >>> atoms = wulf.remove_sugar(atoms)
        >>> atoms.names
        Traceback (most recent call last):
        ...
        AttributeError: 'dict' object has no attribute 'names'
        >>> atoms
        {'names': ['Cr1', 'Cr2'], 'positions': [[0, 0, 0], [0.5, 0.5, 0.5]]}

    """

    if not isinstance(candy, dict):
        raise ValueError(
            f"candy should be an instance of python dict, got {type(candy)}."
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
