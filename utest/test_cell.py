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


from math import pi

import numpy as np
import pytest
from hypothesis import example, given
from hypothesis import strategies as st
from hypothesis.extra.numpy import arrays as harrays
from scipy.spatial.transform import Rotation

import wulfric.cell as Cell
from wulfric.geometry import parallelepiped_check
from wulfric.numerical import (
    ABS_TOL,
    ABS_TOL_ANGLE,
    MAX_LENGTH,
    MIN_ANGLE,
    MIN_LENGTH,
    REL_TOL,
    REL_TOL_ANGLE,
)

N_ORDER = 5

ARRAYS_3x3 = harrays(
    float,
    (3, 3),
    elements=st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
)

################################################################################
#                               Service functions                              #
################################################################################


def shuffle(cell, order):
    if order == 0:
        return [cell[2], cell[0], cell[1]]
    if order == 1:
        return [cell[1], cell[2], cell[0]]
    if order == 2:
        return cell
    if order == 3:
        return [cell[1], cell[0], cell[2]]
    if order == 4:
        return [cell[2], cell[1], cell[0]]
    if order == 5:
        return [cell[0], cell[2], cell[1]]


def rotate(cell, r1, r2, r3):
    R = Rotation.from_rotvec([r1, r2, r3]).as_matrix()
    return R.T @ cell


################################################################################
#                                Reciprocal cell                               #
################################################################################


@example(
    r1=0.0,
    r2=0.0,
    r3=0.0,
    a=1.0,
    b=1.0,
    c=1.0,
    alpha=1.0,
    beta=1.0,
    gamma=1.0,
    order=3,
)
@given(
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=0, max_value=2 * pi),
    st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
    st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
    st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
    st.floats(min_value=MIN_ANGLE, max_value=180.0 - MIN_ANGLE),
    st.floats(min_value=MIN_ANGLE, max_value=180.0 - MIN_ANGLE),
    st.floats(min_value=MIN_ANGLE, max_value=180.0 - MIN_ANGLE),
    st.integers(min_value=0, max_value=N_ORDER),
)
def test_reciprocal(r1, r2, r3, a, b, c, alpha, beta, gamma, order):
    if (
        parallelepiped_check(a, b, c, alpha, beta, gamma)
        # TODO Relax this condition.
        # It passes only for the vectors, which are not too far away from each other.
        and min(a, b, c) / max(a, b, c) > REL_TOL
    ):
        cell = np.array(
            shuffle(
                rotate(Cell.from_params(a, b, c, alpha, beta, gamma), r1, r2, r3), order
            )
        )
        rcell = Cell.reciprocal(cell)
        # If the cell is left-handed, then the diagonal will be filled with -2pi,
        # The minus appears since the cross product is defined in the right-handed system.
        # If the cell is right-handed, then the diagonal will be filled with 2pi.
        # To check for both conditions we need to use np.abs().
        product = np.abs(np.diag(rcell @ cell.T))
        correct_product = np.ones(3) * 2 * pi
        # Non  diagonal terms are close to zero.
        assert np.allclose(product, correct_product, rtol=REL_TOL, atol=ABS_TOL)


@pytest.mark.parametrize(
    "cell, rec_cell",
    [
        (
            [[1, 0, 0], [0, 2, 0], [0, 0, 3]],
            [[2 * pi, 0, 0], [0, pi, 0], [0, 0, 2 / 3 * pi]],
        )
    ],
)
def test_reciprocal_cell_examples(cell, rec_cell):
    rcell = Cell.reciprocal(cell)
    assert np.allclose(rcell, np.array(rec_cell), rtol=REL_TOL, atol=ABS_TOL)


################################################################################
#                             Cell from parameters                             #
################################################################################
@given(
    st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
    st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
    st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
    st.floats(min_value=MIN_ANGLE, max_value=180.0 - MIN_ANGLE),
    st.floats(min_value=MIN_ANGLE, max_value=180.0 - MIN_ANGLE),
    st.floats(min_value=MIN_ANGLE, max_value=180.0 - MIN_ANGLE),
)
def test_cell_from_param(a, b, c, alpha, beta, gamma):
    if parallelepiped_check(a, b, c, alpha, beta, gamma):
        cell = Cell.from_params(a, b, c, alpha, beta, gamma)
        # TODO relax this condition. It does not allow to have 0 components.
        if (cell > MIN_LENGTH).all():
            ap, bp, cp, alphap, betap, gammap = Cell.params(cell)
            assert np.allclose([a, b, c], [ap, bp, cp], rtol=REL_TOL, atol=ABS_TOL)
            assert np.allclose(
                [alpha, beta, gamma],
                [alphap, betap, gammap],
                rtol=REL_TOL_ANGLE,
                atol=ABS_TOL_ANGLE,
            )
    else:
        with pytest.raises(ValueError):
            Cell.from_params(a, b, c, alpha, beta, gamma)


@pytest.mark.parametrize(
    "a, b, c, alpha, beta, gamma, cell",
    [(1, 1, 1, 90, 90, 90, [[1, 0, 0], [0, 1, 0], [0, 0, 1]])],
)
def test_cell_from_params_example(a, b, c, alpha, beta, gamma, cell):
    assert (
        Cell.from_params(a, b, c, alpha, beta, gamma) - np.array(cell) < ABS_TOL
    ).all()


################################################################################
#                           Parameters from the cell                           #
################################################################################


@given(ARRAYS_3x3)
def test_params_from_cell(cell):
    a, b, c, alpha, beta, gamma = Cell.params(cell)
