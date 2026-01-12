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
    SC_BRAVAIS_LATTICE_SHORT_NAMES,
    SC_BRAVAIS_LATTICE_LONG_NAMES,
    SC_CONVENTIONAL_TO_PRIMITIVE,
    SC_BRAVAIS_LATTICE_VARIATIONS,
    SC_DEFAULT_K_PATHS,
    BRAVAIS_LATTICES,
)


def test_sc_bravais_lattice_short_names():
    assert list(BRAVAIS_LATTICES) == list(SC_BRAVAIS_LATTICE_SHORT_NAMES)


def test_sc_bravais_lattice_long_names():
    assert list(BRAVAIS_LATTICES) == list(SC_BRAVAIS_LATTICE_LONG_NAMES)


def test_sc_conventional_to_primitive():
    assert list(BRAVAIS_LATTICES) == list(SC_CONVENTIONAL_TO_PRIMITIVE)


def test_sc_bravais_lattice_variations():
    assert len(SC_BRAVAIS_LATTICE_VARIATIONS) == 25


def test_sc_default_k_paths():
    assert list(SC_BRAVAIS_LATTICE_VARIATIONS) == list(SC_DEFAULT_K_PATHS)
