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

import pytest
from wulfric.constants import ATOM_SPECIES, ATOMIC_MASS, ATOM_COLORS


def test_atomic_mass():
    assert list(ATOM_SPECIES) == list(ATOMIC_MASS)


def test_atom_colors():
    assert list(ATOM_SPECIES) + ["X"] == list(ATOM_COLORS)


@pytest.mark.parametrize("atom_species", list(ATOM_COLORS))
def test_atom_colors_values(atom_species):
    color = ATOM_COLORS[atom_species]

    assert color[0] == "#"

    allowed_letters = "0123456789ABCDEF"

    for letter in color[1:]:
        assert letter in allowed_letters
