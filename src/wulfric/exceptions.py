# Wulfric - Crystal, Lattice, Atoms, K-path.
# Copyright (C) 2023-2024 Andrey Rybakov
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

__all__ = ["StandardizationTypeMismatch"]


class StandardizationTypeMismatch(Exception):
    r"""
    Raised if standardization functions is called on the cell that does not match the
    expected lattice type (i.e. :py:func:`.TET_get_S_matrix` is called on the cubic cell).
    """

    def __init__(self, expected_lattice_type, step=None):
        if step is None:
            message = f"{step} step of the standardization process fails. "
        else:
            message = ""
        message += f"Are you sure that the cell is {expected_lattice_type}?"

    def __str__(self):
        return self.message
