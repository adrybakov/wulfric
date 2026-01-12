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
from hypothesis import given
from hypothesis import strategies as st

from wulfric.constants._atoms import ATOM_SPECIES
from wulfric.crystal._atoms import get_unique_names, get_atom_species


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
def test_get_atom_species(prefix, suffix):
    for atom_type in ATOM_SPECIES:
        name = prefix + atom_type + suffix
        assert get_atom_species(name) == atom_type


@given(st.lists(elements=st.text()))
def test_get_unique_names(names):
    atoms = {"names": names}
    unique_names = get_unique_names(atoms)

    assert len(unique_names) == len(set(unique_names))
