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
old_dir = set(dir())
old_dir.add("old_dir")


class StandardizationTypeMismatch(Exception):
    r"""
    Raised if standardization functions is called on the cell that does not match the
    expected lattice type. It is not guaranteed to be raised if the lattice type is
    incorrect.
    """

    def __init__(self, expected_lattice_type, step=None):
        if step is not None:
            self.message = f"{step} step of the standardization process fails. "
        else:
            self.message = ""
        self.message += f"Are you sure that the cell is {expected_lattice_type}?"

    def __str__(self):
        return self.message


class ConventionNotSupported(Exception):
    """
    Raised when the convention for the cell/crystall is not one of the supported ones.
    """

    def __init__(self, convention: str, with_spglib=False):
        self.conventions = ["hpkot", "sc"]
        if with_spglib:
            self.conventions += ["spglib"]
        self.message = (
            f'Convention "{convention}" is not supported. Supported conventions are\n  * '
            + "\n  * ".join(self.conventions)
        )

    def __str__(self):
        return self.message


class FailedToDeduceAtomSpecies(Exception):
    r"""
    Raised when the automatic deduction of the atom species from its name fails.
    """

    def __init__(self, name: str):
        self.message = f"Tried to deduce name from '{name}'. Failed."

    def __str__(self):
        return self.message


class NiggliReductionFailed(Exception):
    r"""
    Raised when niggli reduction reaches ``max_iterations``.
    """

    def __init__(self, max_iterations: int):
        self.message = f"Niggli reduction algorithm reached maximum amount of iterations: {max_iterations}"

    def __str__(self):
        return self.message


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
