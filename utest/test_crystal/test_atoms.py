# Wulfric - Crystal, Lattice, Atoms, K-path.
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

import numpy as np
import pytest
from hypothesis import given
from hypothesis import strategies as st
from hypothesis.extra.numpy import arrays as harrays

from wulfric.constants._atoms import ATOM_TYPES
from wulfric.crystal._atoms import deduce_atom_type


@given(
    st.text(
        min_size=1,
        max_size=3,
        alphabet=[i for i in "0123456789_-#$%!"],
    ),
    st.text(
        min_size=1,
        max_size=3,
        alphabet=[i for i in "0123456789_-#$%!"],
    ),
)
def test_Atom_type(prefix, suffix):
    for atom_type in ATOM_TYPES:
        name = prefix + atom_type + suffix
        assert deduce_atom_type(name) == atom_type
