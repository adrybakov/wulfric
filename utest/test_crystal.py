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
from hypothesis import example, given, settings
from hypothesis import strategies as st
from hypothesis.extra.numpy import arrays as harrays

from wulfric.atom import Atom
from wulfric.crystal import Crystal
from wulfric.numerical import MAX_LENGTH, compare_numerically

VECTOR_3 = harrays(
    np.float64,
    (3,),
    elements=st.floats(
        allow_nan=False,
        allow_infinity=False,
        max_value=MAX_LENGTH,
        min_value=-MAX_LENGTH,
    ),
)
REL_VECTOR_3 = harrays(
    np.float64,
    (3,),
    elements=st.floats(
        allow_nan=False,
        allow_infinity=False,
        max_value=2,
        min_value=-2,
    ),
)


def test_deepcopy():
    from copy import deepcopy

    c = Crystal()
    a = deepcopy(c)


@example("Cr__e3", (0, 0, 0))
@given(
    st.text(min_size=1, max_size=10),
    st.lists(st.floats(min_value=0, max_value=1), min_size=3, max_size=3),
)
def test_add_atom(name, position):
    if not name.startswith("__") and not name.endswith("__"):
        c = Crystal(cell=[[1, 0, 0], [0, 2, 0], [0, 0, 3]], standardize=False)
        c.add_atom(name=name, position=position)
        assert c.atoms[0].name == name
        assert np.allclose(c.atoms[0].position, position)
        c.add_atom(Atom(name, position))
        assert c.atoms[1].name == name
        assert np.allclose(c.atoms[1].position, position)
        c.add_atom(name, position=position)
        assert c.atoms[2].name == name
        assert np.allclose(c.atoms[2].position, position)
        c.add_atom(name, position=position, relative=False)
        assert c.atoms[3].name == name
        assert np.allclose(
            c.atoms[3].position, [position[0], position[1] / 2.0, position[2] / 3.0]
        )


def test_add_atom_raises():
    c = Crystal()

    with pytest.raises(TypeError):
        c.add_atom(nam=4)

    with pytest.raises(TypeError):
        c.add_atom(1)


@example("Cr__e3", (0, 0, 0))
@given(
    st.text(min_size=1, max_size=10),
    st.lists(st.floats(min_value=0, max_value=1), min_size=3, max_size=3),
)
def test_get_atom(name, position):
    if not name.startswith("__") and not name.endswith("__"):
        position = np.array(position)
        c = Crystal(cell=[[1, 0, 0], [0, 2, 0], [0, 0, 3]], standardize=False)
        c.add_atom(name=name, position=position)
        c.add_atom(name, position=position * 2.0)
        if "__" in name:
            data = name.split("__")
            if len(data) > 2:
                with pytest.raises(ValueError):
                    atom = c.get_atom(name)
            else:
                try:
                    int(data[1])
                except ValueError:
                    with pytest.raises(ValueError):
                        atom = c.get_atom(name)
        else:
            atom = c.get_atom(name, 2)
            assert np.allclose(atom.position, position * 2.0)
            with pytest.raises(ValueError):
                c.get_atom(name)
            atoms = c.get_atom(name, return_all=True)
            assert len(atoms) == 2


def test_remove_atom():
    c = Crystal()
    c.add_atom(Atom("H", (0, 0, 0)))
    c.add_atom(Atom("H", (1, 0, 0)))
    c.add_atom(Atom("O", (2, 0, 0)))
    c.remove_atom("H", index=1)
    assert c.atoms[0].name == "H"
    assert c.atoms[0].index == 2
    assert np.allclose(c.atoms[0].position, (1, 0, 0))
    c = Crystal()
    c.add_atom(Atom("H", (0, 0, 0)))
    c.add_atom(Atom("H", (1, 0, 0)))
    c.add_atom(Atom("O", (2, 0, 0)))
    O = Atom("O", (0, 4, 0))
    c.add_atom(O)
    c.remove_atom("H")
    assert c.atoms[0].name == "O"
    assert c.atoms[0].index == 3
    assert np.allclose(c.atoms[0].position, (2, 0, 0))
    c.remove_atom(O)
    assert len(c.atoms) == 1

    with pytest.raises(ValueError):
        c.remove_atom("H", index=1)


@given(
    st.text(min_size=1, max_size=10),
    st.lists(st.floats(min_value=0, max_value=1), min_size=3, max_size=3),
    st.lists(st.integers(min_value=-1e9, max_value=1e9), min_size=3, max_size=3),
)
def test_get_atom_coordinates(name, position, R):
    if not name.startswith("__") and not name.endswith("__"):
        position = np.array(position)
        c = Crystal(cell=[[1, 0, 0], [0, 2, 0], [0, 0, 3]], standardize=False)
        c.add_atom(name=name, position=position)
        assert np.allclose(c.get_atom_coordinates(name, R=R), position + np.array(R))
        assert np.allclose(
            c.get_atom_coordinates(name, R=R, relative=False),
            (position + np.array(R)) @ c.cell,
        )


@given(
    st.text(min_size=1, max_size=10),
    st.lists(st.floats(min_value=0, max_value=1), min_size=3, max_size=3),
    st.text(min_size=1, max_size=10),
    st.lists(st.floats(min_value=0, max_value=1), min_size=3, max_size=3),
    st.lists(st.integers(min_value=-1e9, max_value=1e9), min_size=3, max_size=3),
)
def test_get_vector(name1, position1, name2, position2, R):
    if (
        not name1.startswith("__")
        and not name1.endswith("__")
        and not name2.startswith("__")
        and not name2.endswith("__")
    ):
        position1 = np.array(position1)
        position2 = np.array(position2)
        c = Crystal(cell=[[1, 0, 0], [0, 2, 0], [0, 0, 3]], standardize=False)
        c.add_atom(name=name1, position=position1)
        c.add_atom(name=name2, position=position2)
        assert np.allclose(
            c.get_vector(name1, name2, R=R, index1=1, index2=2),
            (position2 - position1 + np.array(R)) @ c.cell,
        )
        assert np.allclose(
            c.get_vector(name1, name2, R=R, index1=1, index2=2, relative=True),
            position2 - position1 + np.array(R),
        )


@given(
    st.text(min_size=1, max_size=10),
    st.lists(st.floats(min_value=0, max_value=1), min_size=3, max_size=3),
    st.text(min_size=1, max_size=10),
    st.lists(st.floats(min_value=0, max_value=1), min_size=3, max_size=3),
    st.lists(st.integers(min_value=-1e9, max_value=1e9), min_size=3, max_size=3),
)
def test_get_distance(name1, position1, name2, position2, R):
    if (
        not name1.startswith("__")
        and not name1.endswith("__")
        and not name2.startswith("__")
        and not name2.endswith("__")
    ):
        position1 = np.array(position1)
        position2 = np.array(position2)
        c = Crystal(cell=[[1, 0, 0], [0, 2, 0], [0, 0, 3]], standardize=False)
        c.add_atom(name=name1, position=position1)
        c.add_atom(name=name2, position=position2)
        assert np.allclose(
            c.get_distance(name1, name2, R=R, index1=1, index2=2),
            np.linalg.norm((position2 - position1 + np.array(R)) @ c.cell),
        )
        assert np.allclose(
            c.get_distance(name1, name2, R=R, index1=1, index2=2, relative=True),
            np.linalg.norm(position2 - position1 + np.array(R)),
        )


def test_get_atom_coordinates():
    model = Crystal()
    model.cell = [[10, 0, 0], [0, 10, 0], [0, 0, 10]]
    Cr1 = Atom("Cr1", (0.1, 0.6, 0.2))
    model.add_atom(Cr1)
    x, y, z = model.get_atom_coordinates(Cr1, relative=False)
    assert compare_numerically(x, "==", 1)
    assert compare_numerically(y, "==", 6)
    assert compare_numerically(z, "==", 2)
    x, y, z = model.get_atom_coordinates(Cr1, R=[1, 0, 0], relative=False)
    assert compare_numerically(x, "==", 11)
    assert compare_numerically(y, "==", 6)
    assert compare_numerically(z, "==", 2)
    x, y, z = model.get_atom_coordinates(Cr1, R=[0, -1, 0], relative=False)
    assert compare_numerically(x, "==", 1)
    assert compare_numerically(y, "==", -4)
    assert compare_numerically(z, "==", 2)
    x, y, z = model.get_atom_coordinates(Cr1, R=[0, 0, 2], relative=False)
    assert compare_numerically(x, "==", 1)
    assert compare_numerically(y, "==", 6)
    assert compare_numerically(z, "==", 22)
    x, y, z = model.get_atom_coordinates(Cr1, R=[0, -3, 2], relative=False)
    assert compare_numerically(x, "==", 1)
    assert compare_numerically(y, "==", -24)
    assert compare_numerically(z, "==", 22)
    x, y, z = model.get_atom_coordinates(Cr1, R=[3, -3, 2], relative=False)
    assert compare_numerically(x, "==", 31)
    assert compare_numerically(y, "==", -24)
    assert compare_numerically(z, "==", 22)
    model.cell = [[10, 10, 0], [0, 10, 10], [0, 0, 10]]
    x, y, z = model.get_atom_coordinates(Cr1, relative=False)
    assert compare_numerically(x, "==", 1)
    assert compare_numerically(y, "==", 7)
    assert compare_numerically(z, "==", 8)
    x, y, z = model.get_atom_coordinates(Cr1, R=[1, 0, 0], relative=False)
    assert compare_numerically(x, "==", 11)
    assert compare_numerically(y, "==", 17)
    assert compare_numerically(z, "==", 8)
    x, y, z = model.get_atom_coordinates(Cr1, R=[0, -1, 0], relative=False)
    assert compare_numerically(x, "==", 1)
    assert compare_numerically(y, "==", -3)
    assert compare_numerically(z, "==", -2)
    x, y, z = model.get_atom_coordinates(Cr1, R=[0, 0, 2], relative=False)
    assert compare_numerically(x, "==", 1)
    assert compare_numerically(y, "==", 7)
    assert compare_numerically(z, "==", 28)
    x, y, z = model.get_atom_coordinates(Cr1, R=[0, -3, 2], relative=False)
    assert compare_numerically(x, "==", 1)
    assert compare_numerically(y, "==", -23)
    assert compare_numerically(z, "==", -2)
    x, y, z = model.get_atom_coordinates(Cr1, R=[3, -3, 2], relative=False)
    assert compare_numerically(x, "==", 31)
    assert compare_numerically(y, "==", 7)
    assert compare_numerically(z, "==", -2)


@given(REL_VECTOR_3, REL_VECTOR_3, REL_VECTOR_3)
def test_cure_negative(pos1, pos2, pos3):
    a1 = Atom(position=pos1)
    a2 = Atom(position=pos2)
    a3 = Atom(position=pos3)
    c = Crystal(atoms=[a1, a2, a3])
    c.cure_negative()
    for atom in c.atoms:
        assert (atom.position >= 0).all()


@given(REL_VECTOR_3, REL_VECTOR_3, REL_VECTOR_3, REL_VECTOR_3)
def test_shift_atoms(pos1, pos2, pos3, gravity_point):
    a1 = Atom(position=pos1)
    a2 = Atom(position=pos2)
    a3 = Atom(position=pos3)
    c = Crystal(atoms=[a1, a2, a3])
    c.shift_atoms(gravity_point=gravity_point)
    coordinates = np.array([atom.position for atom in c.atoms])
    min_coord = np.min(coordinates, axis=0)
    max_coord = np.max(coordinates, axis=0)
    shifted_gravity_point = (max_coord + min_coord) / 2
    assert np.allclose(shifted_gravity_point, gravity_point)
