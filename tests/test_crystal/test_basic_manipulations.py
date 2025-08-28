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
import numpy as np
from hypothesis import given
from hypothesis import strategies as st
from hypothesis.extra.numpy import arrays as harrays

from wulfric.crystal._basic_manipulation import (
    cure_negative,
    get_distance,
    get_vector,
    shift_atoms,
)

VECTOR_3 = harrays(
    np.float64,
    (3,),
    elements=st.floats(
        allow_nan=False,
        allow_infinity=False,
    ),
)
REL_VECTOR_3 = harrays(
    np.float64,
    (3,),
    elements=st.floats(
        allow_nan=False,
        allow_infinity=False,
        max_value=1,
        min_value=-1,
    ),
)


@given(
    st.lists(st.floats(min_value=0, max_value=1), min_size=3, max_size=3),
    st.lists(st.floats(min_value=0, max_value=1), min_size=3, max_size=3),
    st.lists(st.integers(min_value=-1e9, max_value=1e9), min_size=3, max_size=3),
)
def test_get_vector(position1, position2, R):
    atoms = {"positions": [position1, position2]}
    cell = np.eye(3, dtype=float)

    assert np.allclose(
        get_vector(cell=cell, atoms=atoms, atom1=0, atom2=1, R=R),
        (np.array(R) + position2 - position1) @ cell,
    )
    assert np.allclose(
        get_vector(cell=cell, atoms=atoms, atom1=0, atom2=1, R=R, return_relative=True),
        np.array(R) + position2 - position1,
    )


@given(
    st.lists(st.floats(min_value=0, max_value=1), min_size=3, max_size=3),
    st.lists(st.floats(min_value=0, max_value=1), min_size=3, max_size=3),
    st.lists(st.integers(min_value=-1e9, max_value=1e9), min_size=3, max_size=3),
)
def test_get_distance(position1, position2, R):
    atoms = {"positions": [position1, position2]}
    cell = np.eye(3, dtype=float)

    assert np.allclose(
        get_distance(cell=cell, atoms=atoms, atom1=0, atom2=1, R=R),
        np.linalg.norm((np.array(R) + position2 - position1) @ cell),
    )


@given(REL_VECTOR_3, REL_VECTOR_3, REL_VECTOR_3)
def test_cure_negative(pos1, pos2, pos3):
    atoms = {"positions": [pos1, pos2, pos3]}

    cure_negative(atoms)
    for position in atoms["positions"]:
        assert (position >= 0).all()


@given(REL_VECTOR_3, REL_VECTOR_3, REL_VECTOR_3, REL_VECTOR_3)
def test_shift_atoms(pos1, pos2, pos3, gravity_point):
    atoms = {"positions": [pos1, pos2, pos3]}

    shift_atoms(atoms, gravity_point=gravity_point)

    min_coord = np.min(atoms["positions"], axis=0)
    max_coord = np.max(atoms["positions"], axis=0)
    shifted_gravity_point = (max_coord + min_coord) / 2
    assert np.allclose(shifted_gravity_point, gravity_point)
