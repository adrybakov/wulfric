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


old_dir = set(dir())
old_dir.add("old_dir")


class StandardizationTypeMismatch(Exception):
    r"""
    Raised if standardization functions is called on the cell that does not match the
    expected lattice type (i.e. :py:func:`.TET_get_S_matrix` is called on the cubic cell).

    .. versionadded:: 0.4.0
    """

    def __init__(self, expected_lattice_type, step=None):
        if step is not None:
            self.message = f"{step} step of the standardization process fails. "
        else:
            self.message = ""
        self.message += f"Are you sure that the cell is {expected_lattice_type}?"

    def __str__(self):
        return self.message


class FailedToDeduceAtomSpecies(Exception):
    r"""
    Raise when the automatic deduction of the atom species from its name fails.
    """

    def __init__(self, name: str):
        self.message = f"Tried to deduce name from '{name}'. Failed."

    def __str__(self):
        return self.message


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
