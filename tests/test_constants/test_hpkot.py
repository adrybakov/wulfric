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
from wulfric.constants import (
    HPKOT_CONVENTIONAL_TO_PRIMITIVE,
    HPKOT_DEFAULT_K_PATHS,
    HPKOT_EXTENDED_BL_SYMBOLS,
    BRAVAIS_LATTICES,
)


def test_hpkot_conventional_to_primitive():
    assert list(BRAVAIS_LATTICES) == list(HPKOT_CONVENTIONAL_TO_PRIMITIVE)


def test_hpkot_default_k_paths():
    assert list(HPKOT_EXTENDED_BL_SYMBOLS) == list(HPKOT_DEFAULT_K_PATHS)


def test_hpkot_extended_bl_symbols():
    assert len(HPKOT_EXTENDED_BL_SYMBOLS) == 29
