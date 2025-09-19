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


import pytest

from wulfric.crystal import hpkot_get_example, hpkot_get_extended_bl_symbol
from wulfric.constants import HPKOT_EXTENDED_BL_SYMBOLS


@pytest.mark.parametrize(
    "extended_bl_symbol",
    HPKOT_EXTENDED_BL_SYMBOLS,
    ids=HPKOT_EXTENDED_BL_SYMBOLS,
)
def test_with_inversion(extended_bl_symbol):
    # TODO:REMOVE when those are added
    if extended_bl_symbol in ["oF2", "oI2", "oA1", "oA2"]:
        with pytest.raises(ValueError):
            cell, atoms = hpkot_get_example(
                extended_bl_symbol=extended_bl_symbol, with_inversion=True
            )
    else:
        cell, atoms = hpkot_get_example(
            extended_bl_symbol=extended_bl_symbol, with_inversion=True
        )
        assert extended_bl_symbol == hpkot_get_extended_bl_symbol(
            cell=cell, atoms=atoms
        )


@pytest.mark.parametrize(
    "extended_bl_symbol",
    HPKOT_EXTENDED_BL_SYMBOLS,
    ids=HPKOT_EXTENDED_BL_SYMBOLS,
)
def test_without_inversion(extended_bl_symbol):
    cell, atoms = hpkot_get_example(
        extended_bl_symbol=extended_bl_symbol, with_inversion=False
    )
    assert extended_bl_symbol == hpkot_get_extended_bl_symbol(cell=cell, atoms=atoms)
