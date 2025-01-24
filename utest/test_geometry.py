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

from math import cos, pi, sin

import numpy as np
import pytest
from hypothesis import example, given
from hypothesis import strategies as st
from hypothesis.extra.numpy import arrays as harrays
from scipy.spatial.transform import Rotation

from wulfric._numerical import compare_numerically
from wulfric.cell._basic_manipulation import is_reasonable
from wulfric.constants._numerical import (
    ABS_TOL,
    ABS_TOL_ANGLE,
    MAX_LENGTH,
    MIN_ANGLE,
    MIN_LENGTH,
    TORADIANS,
)
from wulfric.geometry import absolute_to_relative, angle, parallelepiped_check, volume

################################################################################
#                               Service functions                              #
################################################################################

n_order = 5


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
#                             Absolute to relative                             #
################################################################################
@pytest.mark.parametrize(
    "cell, absolute, relative",
    [
        ([[1, 0, 0], [0, 1, 0], [0, 0, 1]], [0, 0, 0], [0, 0, 0]),
        ([[1, 0, 0], [0, 1, 0], [0, 0, 1]], [0, 0, 1], [0, 0, 1]),
        ([[1, 0, 0], [0, 1, 0], [0, 0, 1]], [0, 1, 0], [0, 1, 0]),
        ([[1, 0, 0], [0, 1, 0], [0, 0, 1]], [1, 0, 0], [1, 0, 0]),
        ([[1, 0, 0], [0, 1, 0], [0, 0, 1]], [0.5, 0.5, 0], [0.5, 0.5, 0]),
        ([[1, 1, 0], [0, 1, 0], [0, 0, 1]], [0.5, 1, 0], [0.5, 0.5, 0]),
        ([[2, 1, 0], [1, 1, 0], [0, 0, 1]], [0.9, 0.7, 0.4], [0.2, 0.5, 0.4]),
    ],
)
def test_absolute_to_relative(cell, absolute, relative):
    new_relative = absolute_to_relative(absolute, cell)
    assert (new_relative == relative).all()


################################################################################
#                                     Angle                                    #
################################################################################
@given(
    harrays(float, 3, elements=st.floats(allow_infinity=False, allow_nan=False)),
    harrays(float, 3, elements=st.floats(allow_infinity=False, allow_nan=False)),
)
def test_angle(v1, v2):
    if (
        abs(np.linalg.norm(v1)) > np.finfo(float).eps
        and abs(np.linalg.norm(v2)) > np.finfo(float).eps
    ):
        result_degrees = angle(v1, v2)
        result_radians = angle(v1, v2, radians=True)
        assert 0.0 <= result_degrees <= 180.0
        assert 0.0 <= result_radians <= pi
    else:
        with pytest.raises(ValueError):
            result_degrees = angle(v1, v2)


@example(0)
@example(0.0000000001)
@given(st.floats(min_value=-360, max_value=360))
def test_angle_values(alpha):
    v1 = np.array([1.0, 0.0, 0.0])
    v2 = np.array([cos(alpha * TORADIANS), sin(alpha * TORADIANS), 0.0])

    if alpha < 0:
        alpha = 360 + alpha

    if alpha > 180:
        alpha = 360 - alpha

    assert abs(angle(v1, v2) - alpha) < ABS_TOL_ANGLE


def test_angle_raises():
    with pytest.raises(ValueError):
        angle([0, 0, 0], [0, 0, 0])
    with pytest.raises(ValueError):
        angle([0, 0, 0], [1.0, 0, 0])


################################################################################
#                                    Volume                                    #
################################################################################
@pytest.mark.parametrize(
    "args, result, eps", [((4, 4.472, 4.583, 79.03, 64.13, 64.15), 66.3840797, ABS_TOL)]
)
def test_volume_example(args, result, eps):
    assert volume(*args) - result < eps


# No need to test the vectors - they take the same route as the cell
# if the vectors will move from rows to columns it is not a problem as well
# since the volume of the cell is its determinant
@example(np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]))
@example(np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 1]]))
@given(
    harrays(
        float, (3, 3), elements=st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH)
    )
)
def test_volume_with_cell(cell):
    # Its an "or" condition
    assert volume(cell) >= 0


@given(
    st.floats(
        min_value=MIN_LENGTH,
        max_value=MAX_LENGTH,
    ),
    st.floats(
        min_value=MIN_LENGTH,
        max_value=MAX_LENGTH,
    ),
    st.floats(
        min_value=MIN_LENGTH,
        max_value=MAX_LENGTH,
    ),
    st.floats(min_value=0, max_value=360),
    st.floats(min_value=0, max_value=360),
    st.floats(min_value=0, max_value=360),
)
def test_volume_parameters(a, b, c, alpha, beta, gamma):
    if parallelepiped_check(a, b, c, alpha, beta, gamma):
        assert volume(a, b, c, alpha, beta, gamma) > 0


################################################################################
#                             Parallelepiped check                             #
################################################################################
@given(
    st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
    st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
    st.floats(min_value=MIN_LENGTH, max_value=MAX_LENGTH),
    st.floats(min_value=0, max_value=360),
    st.floats(min_value=0, max_value=360),
    st.floats(min_value=0, max_value=360),
)
def test_parallelepiped_check(a, b, c, alpha, beta, gamma):
    assert parallelepiped_check(a, b, c, alpha, beta, gamma) == (
        compare_numerically(a, ">", 0.0, eps=ABS_TOL)
        and compare_numerically(b, ">", 0.0, eps=ABS_TOL)
        and compare_numerically(c, ">", 0.0, eps=ABS_TOL)
        and compare_numerically(alpha, "<", 180.0, eps=ABS_TOL_ANGLE)
        and compare_numerically(beta, "<", 180.0, eps=ABS_TOL_ANGLE)
        and compare_numerically(gamma, "<", 180.0, eps=ABS_TOL_ANGLE)
        and compare_numerically(alpha, ">", 0.0, eps=ABS_TOL_ANGLE)
        and compare_numerically(beta, ">", 0.0, eps=ABS_TOL_ANGLE)
        and compare_numerically(gamma, ">", 0.0, eps=ABS_TOL_ANGLE)
        and compare_numerically(gamma, "<", alpha + beta, eps=ABS_TOL_ANGLE)
        and compare_numerically(alpha + beta, "<", 360.0 - gamma, eps=ABS_TOL_ANGLE)
        and compare_numerically(beta, "<", alpha + gamma, eps=ABS_TOL_ANGLE)
        and compare_numerically(alpha + gamma, "<", 360.0 - beta, eps=ABS_TOL_ANGLE)
        and compare_numerically(alpha, "<", beta + gamma, eps=ABS_TOL_ANGLE)
        and compare_numerically(beta + gamma, "<", 360.0 - alpha, eps=ABS_TOL_ANGLE)
    )
