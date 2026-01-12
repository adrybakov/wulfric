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
from wulfric.constants import (
    BRAVAIS_LATTICES,
    INVERSION_SYMMETRY,
    CRYSTAL_FAMILY,
    CENTRING_TYPE,
)


def test_inversion_symmetry():
    assert [_ for _ in range(1, 231)] == list(INVERSION_SYMMETRY)


def test_crystal_family():
    assert [_ for _ in range(1, 231)] == list(CRYSTAL_FAMILY)


def test_centring_type():
    assert [_ for _ in range(1, 231)] == list(CENTRING_TYPE)


def test_bravais_lattice_type():
    assert sorted(list(BRAVAIS_LATTICES)) == sorted(
        list(set([CRYSTAL_FAMILY[_] + CENTRING_TYPE[_] for _ in range(1, 231)]))
    )
