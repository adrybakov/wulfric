# Wulfric - Crystal, Lattice, Atoms, K-path.
# Copyright (C) 2023-2024 Andrey Rybakov
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

from wulfric.atom import Atom
from wulfric.constants import ATOM_TYPES, TORADIANS

VECTOR_3 = harrays(
    np.float64,
    (3,),
    elements=st.floats(
        allow_nan=False, allow_infinity=False, max_value=1e9, min_value=-1e9
    ),
)


@given(VECTOR_3)
def test_Atom_spin(v):
    atom = Atom()

    assert np.allclose(atom.spin_direction, [0, 0, 0])
    assert np.allclose(atom.spin_vector, [0, 0, 0])
    assert np.allclose(atom.spin, 0)

    atom.spin = np.linalg.norm(v)
    assert np.allclose(atom.spin, np.linalg.norm(v))
    if np.linalg.norm(v) != 0:
        assert np.allclose(atom.spin_direction, [0, 0, 1])
    else:
        assert np.allclose(atom.spin_direction, [0, 0, 0])
    assert np.allclose(atom.spin_vector, [0, 0, np.linalg.norm(v)])

    atom.spin_vector = v
    assert np.allclose(atom.spin, np.linalg.norm(v))
    assert np.allclose(
        atom.spin_direction,
        np.divide(
            v, np.linalg.norm(v), out=np.zeros_like(v), where=np.linalg.norm(v) != 0
        ),
    )
    assert np.allclose(atom.spin_vector, v)

    atom.spin_direction = v
    assert np.allclose(atom.spin, np.linalg.norm(v))
    assert np.allclose(
        atom.spin_direction,
        np.divide(
            v, np.linalg.norm(v), out=np.zeros_like(v), where=np.linalg.norm(v) != 0
        ),
    )
    assert np.allclose(atom.spin_vector, v)


@given(
    st.floats(allow_nan=False, allow_infinity=False, max_value=180, min_value=0),
    st.floats(allow_nan=False, allow_infinity=False, max_value=360, min_value=0),
)
def test_Atom_phi_theta(theta, phi):
    atom = Atom(spin=1)
    atom.spin_angles = theta, phi

    phi *= TORADIANS
    theta *= TORADIANS

    assert np.allclose(
        atom.spin_vector,
        (np.cos(phi) * np.sin(theta), np.sin(phi) * np.sin(theta), np.cos(theta)),
    )


@given(VECTOR_3)
def test_Atom_magmom(v):
    atom = Atom()

    assert np.allclose(atom.spin_direction, [0, 0, 0])
    assert np.allclose(atom.spin_vector, [0, 0, 0])
    assert np.allclose(atom.spin, 0)

    atom.magmom = v
    spin = v / -atom.g_factor
    assert np.allclose(atom.spin, np.linalg.norm(spin))
    if np.linalg.norm(v) != 0:
        assert np.allclose(atom.spin_direction, spin / np.linalg.norm(spin))
    else:
        assert np.allclose(atom.spin_direction, [0, 0, 0])
    assert np.allclose(atom.spin_vector, spin)

    atom.spin_vector = v
    magmom = v * -atom.g_factor
    assert np.allclose(atom.spin, np.linalg.norm(v))
    assert np.allclose(
        atom.spin_direction,
        np.divide(
            v,
            np.linalg.norm(v),
            out=np.zeros_like(v),
            where=np.linalg.norm(v) != 0,
        ),
    )
    assert np.allclose(atom.spin_vector, v)
    assert np.allclose(atom.magmom, magmom)

    atom.spin = 1.5
    atom.spin_direction = v
    spin_direction = np.divide(
        v,
        np.linalg.norm(v),
        out=np.zeros_like(v),
        where=np.linalg.norm(v) != 0,
    )
    magmom = spin_direction * -atom.g_factor * 1.5
    assert np.allclose(
        atom.spin, 1.5 if not np.allclose(atom.spin_direction, [0, 0, 0]) else 0
    )
    assert np.allclose(atom.spin_direction, spin_direction)
    assert np.allclose(atom.spin_vector, spin_direction * 1.5)
    assert np.allclose(atom.magmom, magmom)


@given(st.floats(max_value=1e9, min_value=-1e9))
def test_Atom_g_factor(factor):
    atom = Atom()

    atom.spin = (1, 1, 1)
    assert np.allclose(atom.spin_vector, (1, 1, 1))
    assert np.allclose(atom.magmom, (-2, -2, -2))
    atom.g_factor = factor
    assert np.allclose(atom.spin_vector, (1, 1, 1))
    assert np.allclose(atom.magmom, (-factor, -factor, -factor))


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
    if not prefix.startswith("__") and not suffix.endswith("__"):
        for atom_type in ATOM_TYPES:
            atom = Atom(prefix + atom_type + suffix)
            assert atom.type == atom_type
    else:
        with pytest.raises(ValueError):
            for atom_type in ATOM_TYPES:
                atom = Atom(prefix + atom_type + suffix)


# TODO test spin_phi and spin_theta


def test_atom():
    atom = Atom()
    assert (atom.position == np.zeros(3)).all()
    assert atom.name == "X"
    atom.name = "Cr1"
    assert atom.type == "Cr"
    atom.name = "CR1"
    assert atom.type == "Cr"
    atom.name = "cr1"
    assert atom.type == "Cr"
    with pytest.raises(ValueError):
        atom.spin_vector = "adsfasdfs"
    with pytest.raises(ValueError):
        atom.spin_vector = (4, 5)
    with pytest.raises(ValueError):
        atom.spin_vector = (4, 5, 4, 5)
    atom.spin_vector = (0, 0, 1 / 2)
    assert atom.spin - 0.5 < 1e-10
    assert (atom.spin_vector - np.array([0, 0, 0.5]) < 1e-10).all()
    assert (atom.spin_direction - np.array([0, 0, 1]) < 1e-10).all()
    atom.spin = 2
    assert (atom.spin_vector - np.array([0, 0, 2]) < 1e-10).all()
    assert (atom.spin_direction - np.array([0, 0, 1]) < 1e-10).all()
    assert atom.spin - 2 < 1e-10
