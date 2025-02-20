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


from math import cos, sin, sqrt

import numpy as np
import pytest
from hypothesis import given
from hypothesis import strategies as st

from wulfric.cell._sc_constructors import (
    BCC,
    BCT,
    CUB,
    FCC,
    HEX,
    MCL,
    MCLC,
    ORC,
    ORCC,
    ORCF,
    ORCI,
    RHL,
    TET,
    TRI,
)
from wulfric.constants._numerical import TORADIANS

ANGLE_TOLERANCE = 1e-4


@given(st.floats(min_value=0, allow_infinity=False, allow_nan=False))
def test_CUB(a):
    cell = CUB(a)
    assert np.allclose(cell, np.eye(3) * a)


@given(st.floats(min_value=0, allow_infinity=False, allow_nan=False))
def test_FCC(a):
    cell = FCC(a)
    assert np.allclose(cell, (np.ones((3, 3)) - np.eye(3)) * a / 2)


@given(st.floats(min_value=0, allow_infinity=False, allow_nan=False))
def test_BCC(a):
    cell = BCC(a)
    assert np.allclose(cell, (np.ones((3, 3)) - 2 * np.eye(3)) * a / 2)


@given(
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
)
def test_TET(a, c):
    cell = TET(a, c)
    assert np.allclose(cell, np.diag([a, a, c]))


@given(
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
)
def test_BCT(a, c):
    cell = BCT(a, c)
    correct_cell = (np.ones((3, 3)) - 2 * np.eye(3)) / 2
    correct_cell[:, :2] *= a
    correct_cell[:, 2] *= c
    assert np.allclose(cell, correct_cell)


@given(
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
)
def test_ORC(a, b, c):
    cell = ORC(a, b, c)
    assert np.allclose(cell, np.diag([a, b, c]))


@given(
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
)
def test_ORCF(a, b, c):
    cell = ORCF(a, b, c)
    correct_cell = (np.ones((3, 3)) - np.eye(3)) / 2
    correct_cell[:, 0] *= a
    correct_cell[:, 1] *= b
    correct_cell[:, 2] *= c
    assert np.allclose(cell, correct_cell)


@given(
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
)
def test_ORCI(a, b, c):
    cell = ORCI(a, b, c)
    correct_cell = (np.ones((3, 3)) - 2 * np.eye(3)) / 2
    correct_cell[:, 0] *= a
    correct_cell[:, 1] *= b
    correct_cell[:, 2] *= c
    assert np.allclose(cell, correct_cell)


@given(
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
)
def test_ORCC(a, b, c):
    cell = ORCC(a, b, c)
    correct_cell = np.array([[1, -1, 0], [1, 1, 0], [0, 0, 2]]) / 2
    correct_cell[:, 0] *= a
    correct_cell[:, 1] *= b
    correct_cell[:, 2] *= c
    assert np.allclose(cell, correct_cell)


@given(
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
)
def test_HEX(a, c):
    cell = HEX(a, c)
    correct_cell = np.array(
        [[a / 2, -a * sqrt(3) / 2, 0], [a / 2, a * sqrt(3) / 2, 0], [0, 0, c]]
    )
    assert np.allclose(cell, correct_cell)


@given(
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=ANGLE_TOLERANCE, max_value=120.0 - ANGLE_TOLERANCE),
)
def test_RHL(a, alpha):
    cell = RHL(a, alpha)
    alpha *= TORADIANS
    correct_cell = np.array(
        [
            [a * cos(alpha / 2), -a * sin(alpha / 2), 0],
            [a * cos(alpha / 2), a * sin(alpha / 2), 0],
            [
                a * cos(alpha) / cos(alpha / 2),
                0,
                a * sqrt(1 - cos(alpha) ** 2 / cos(alpha / 2) ** 2),
            ],
        ]
    )
    assert np.allclose(cell, correct_cell)


@given(
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=ANGLE_TOLERANCE, max_value=180.0),
)
def test_MCL(a, b, c, alpha):
    cell = MCL(a, b, c, alpha)

    alpha *= TORADIANS
    correct_cell = np.array(
        [
            [a, 0, 0],
            [0, b, 0],
            [0, c * cos(alpha), c * sin(alpha)],
        ]
    )
    assert np.allclose(cell, correct_cell)


@given(
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=ANGLE_TOLERANCE, max_value=180.0),
)
def test_MCLC(a, b, c, alpha):
    cell = MCLC(a, b, c, alpha)

    alpha *= TORADIANS

    correct_cell = np.array(
        [
            [a / 2, b / 2, 0],
            [-a / 2, b / 2, 0],
            [0, c * cos(alpha), c * sin(alpha)],
        ]
    )
    assert np.allclose(cell, correct_cell)


# # TODO Test trigonal
# full_set = []


# @pytest.mark.parametrize("a, b, c, alpha, beta, gamma, reciprocal", full_set)
# def test_TRI(a, b, c, alpha, beta, gamma, reciprocal):
#     cell = TRI(a, b, c, alpha, beta, gamma, reciprocal, return_cell = True)
#     pass
