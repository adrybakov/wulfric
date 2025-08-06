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
from math import cos, sin, sqrt

import numpy as np
import pytest
from hypothesis import given
from hypothesis import strategies as st

from wulfric.cell._sc_examples import (
    BCC_SC,
    BCT_SC,
    CUB_SC,
    FCC_SC,
    HEX_SC,
    MCL_SC,
    MCLC_SC,
    ORC_SC,
    ORCC_SC,
    ORCF_SC,
    ORCI_SC,
    RHL_SC,
    TET_SC,
    # TRI_SC,
    get_example_cell_SC,
)
from wulfric.constants._numerical import TORADIANS
from wulfric.constants._sc_notation import BRAVAIS_LATTICE_VARIATIONS

ANGLE_TOLERANCE = 1e-4


@given(st.floats(min_value=0, allow_infinity=False, allow_nan=False))
def test_CUB_SC(a):
    cell = CUB_SC(a)
    assert np.allclose(cell, np.eye(3) * a)


@given(st.floats(min_value=0, allow_infinity=False, allow_nan=False))
def test_FCC_SC(a):
    cell = FCC_SC(a)
    assert np.allclose(cell, (np.ones((3, 3)) - np.eye(3)) * a / 2)


@given(st.floats(min_value=0, allow_infinity=False, allow_nan=False))
def test_BCC_SC(a):
    cell = BCC_SC(a)
    assert np.allclose(cell, (np.ones((3, 3)) - 2 * np.eye(3)) * a / 2)


@given(
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
)
def test_TET_SC(a, c):
    cell = TET_SC(a, c)
    assert np.allclose(cell, np.diag([a, a, c]))


@given(
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
)
def test_BCT_SC(a, c):
    cell = BCT_SC(a, c)
    correct_cell = (np.ones((3, 3)) - 2 * np.eye(3)) / 2
    correct_cell[:, :2] *= a
    correct_cell[:, 2] *= c
    assert np.allclose(cell, correct_cell)


@given(
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
)
def test_ORC_SC(a, b, c):
    cell = ORC_SC(a, b, c)
    assert np.allclose(cell, np.diag([a, b, c]))


@given(
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
)
def test_ORCF_SC(a, b, c):
    cell = ORCF_SC(a, b, c)
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
def test_ORCI_SC(a, b, c):
    cell = ORCI_SC(a, b, c)
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
def test_ORCC_SC(a, b, c):
    cell = ORCC_SC(a, b, c)
    correct_cell = np.array([[1, -1, 0], [1, 1, 0], [0, 0, 2]]) / 2
    correct_cell[:, 0] *= a
    correct_cell[:, 1] *= b
    correct_cell[:, 2] *= c
    assert np.allclose(cell, correct_cell)


@given(
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
)
def test_HEX_SC(a, c):
    cell = HEX_SC(a, c)
    correct_cell = np.array(
        [[a / 2, -a * sqrt(3) / 2, 0], [a / 2, a * sqrt(3) / 2, 0], [0, 0, c]]
    )
    assert np.allclose(cell, correct_cell)


@given(
    st.floats(min_value=0, allow_infinity=False, allow_nan=False),
    st.floats(min_value=ANGLE_TOLERANCE, max_value=120.0 - ANGLE_TOLERANCE),
)
def test_RHL_SC(a, alpha):
    cell = RHL_SC(a, alpha)
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
def test_MCL_SC(a, b, c, alpha):
    cell = MCL_SC(a, b, c, alpha)

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
def test_MCLC_SC(a, b, c, alpha):
    cell = MCLC_SC(a, b, c, alpha)

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


@given(st.text())
def test_lattice_example_error(wrong_name: str):
    if wrong_name.lower() not in list(
        map(lambda x: x.lower(), BRAVAIS_LATTICE_VARIATIONS)
    ):
        with pytest.raises(ValueError):
            get_example_cell_SC(wrong_name)
