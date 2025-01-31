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
from hypothesis import given
from hypothesis import strategies as st
from scipy.spatial.transform import Rotation

from wulfric.cell._basic_manipulation import get_params
from wulfric.cell._lepage import lepage
from wulfric.cell._sc_examples import get_cell_example
from wulfric.cell._sc_standardize import get_standardized
from wulfric.cell._sc_variation import get_variation
from wulfric.constants._sc_notation import BRAVAIS_LATTICE_VARIATIONS


@pytest.mark.parametrize(
    "lattice_variation", BRAVAIS_LATTICE_VARIATIONS, ids=BRAVAIS_LATTICE_VARIATIONS
)
def test_lattice_example(lattice_variation: str):
    lattice_type = lattice_variation.translate(str.maketrans("", "", "12345ab"))
    cell = get_cell_example(lattice_variation)
    cell = get_standardized(cell)
    assert lepage(*get_params(cell)) == lattice_type
    assert get_variation(cell) == lattice_variation


@given(st.text())
def test_lattice_example_error(wrong_name: str):
    if wrong_name.lower() not in list(
        map(lambda x: x.lower(), BRAVAIS_LATTICE_VARIATIONS)
    ):
        with pytest.raises(ValueError):
            get_cell_example(wrong_name)
